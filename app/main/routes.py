from app.main import bp, auth
from flask import Flask, render_template, request, flash, redirect, url_for
import calendar
from app.main.forms import EventForm, EventsPageForm, TimeSlotForm, LoginForm, RegistrationForm
from app.main.forms import EventForm, EventsPageForm, PreferenceForm, TimeSlotForm
from app.models import *
from app import db
from app import db, models
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from flask_login import LoginManager, logout_user, login_required, current_user, login_user, current_user, login_manager

'''
@bp.route('/testroute', methods=['GET','POST'])
def testroute():
    users = db.session.query(User).all()
    my_user = db.session.query(User).get(0)

     event = Event(
        id = 0,
        start = datetime.datetime(2018, 8, 1),
        end = datetime.datetime(2018, 8, 2),
        name = "Rock climbing event",
        price = "10",
        location = "NYC"
    )

    #succesfullyAdded = db.session.query(User).get(0).attend_event(event)
    #succesfullyAdded = db.session.query(User).get(1).attend_event(event)
    #succesfullyAdded = db.session.query(User).get(2).attend_event(event)
    #print(succesfullyAdded)
    return render_template("test.html", map_lat=0.0, map_lon=0.0)

'''

'''
now = datetime.datetime.now()
    return redirect(url_for('main.calendar_page_monthly', year=now.year, month=now.month))
'''

@bp.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    form = LoginForm()
    if current_user.is_authenticated:
        now = datetime.datetime.now()
        return redirect(url_for('main.calendar_page_monthly', year=now.year, month=now.month))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            #login_user(user)  # , remember=form.remember_me.data
            flash('Invalid Username or Password')
            return redirect(url_for('main.index'))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            now = datetime.datetime.now()
            next_page = url_for('main.calendar_page_monthly', year=now.year, month=now.month)
        return redirect(next_page)
        # return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/calendar_page/monthly/<int:year>/<int:month>/')
def calendar_page_monthly(year, month):
    now = datetime.datetime.now()
    if (month > 12 or month < 1):
        return ("Oops, the month is out of range!")
    # Initialize some useful variables:
    current_user_id = 0
    current_user = User.query.get(current_user_id)
    c = calendar.TextCalendar(calendar.SUNDAY) # Calendar object starting on Sunday
    now = datetime.datetime.now()
    event_list = Event.query.all()
    month_name = calendar.month_name[month]
    daylist = list(c.itermonthdays(year, month))
    day_delta = datetime.timedelta(days=1)
    # daylist is the list of numbers to put in each box of the calendar,
    # where 0 is an empty box, and 1 is the 1st of the month, etc.
    # example: [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 0, 0]

    event_list = [None] * len(daylist)
    # The following loop creates an event_list with event objects inside
    # The indices correspond with the indices in daylist

    # for day_index in range(len(daylist)):
    #     if daylist[day_index] != 0:
    #         day = datetime.datetime(year, month, daylist[day_index])
    #         event_list[day_index] = Event.query.filter(Event.start >= day, Event.start < day+day_delta, Event.attending_user.any(User.id==current_user_id)).all()


    #
    recommended_events = [None] * len(daylist)
    user_preferences = Preference.query.filter(Preference.user_id == current_user_id).all()
    if len(user_preferences) == 1 :
        user_preferences = user_preferences[0]
    for day_index in range(len(daylist)):
        if daylist[day_index] != 0:
            day = datetime.datetime(year, month, daylist[day_index])
            event_list[day_index] = Event.query.filter(Event.start >= day, Event.start < day+day_delta, Event.attending_user.any(User.id==current_user_id)).all()
            # Recommending Events Below:

            recommended_events[day_index] = Event.query.filter(Event.start >= day, Event.start < day+day_delta)

            #Find if the current user has any preference categories that match any event categories.
            user_categories = [u.id for u in user_preferences.categories]
            recommended_events[day_index] = recommended_events[day_index].filter(Event.categories.any(Category.id.in_(user_categories)))

            if user_preferences.price != None:
                recommended_events[day_index] = recommended_events[day_index].filter(Event.price<=user_preferences.price).all()
            if user_preferences.distance != None or user_preferences.distance != 0:
                for event in reversed(recommended_events[day_index]):
                    if user_preferences.distance_preference_conflicts_with_event(event):
                        recommended_events[day_index].remove(event)
            for event in reversed(recommended_events[day_index]):
                if current_user.is_Attending(event):
                    recommended_events[day_index].remove(event)
    return render_template("calender.html", now=now, month_name=month_name, month=month, year=year, daylist=daylist, event_list=event_list, recommended_events=recommended_events)

@bp.route('/calendar_page/weekly/<int:year>/<int:month>/<int:week>')
def calendar_page_weekly(year, month, week):
    if (month > 12 or month < 1):
        return ("Oops, the month is out of range!")
    # Initialize some useful variables:
    current_user_id = 0
    c = calendar.TextCalendar(calendar.SUNDAY) # Calendar object starting on Sunday
    now = datetime.datetime.now()
    event_list = Event.query.all()
    month_name = calendar.month_name[month]
    daylist = list(c.itermonthdays(year, month))
    day_delta = datetime.timedelta(days=1)
    current_user = User.query.get(current_user_id)
    # daylist is the list of numbers to put in each box of the calendar,
    # where 0 is an empty box, and 1 is the 1st of the month, etc.
    # example: [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 0, 0]

    if len(daylist) <= (week-1) * 7 or week < 1:
        return ("Oops, the week is out of range!")

    if (month == 1):
        days_in_previous_month = len(list(c.itermonthdays(year-1,12)))
    else:
        days_in_previous_month = len(list(c.itermonthdays(year,month-1)))

    event_list = [None] * len(daylist)


    week_of_today = (daylist.index(now.day) // 7) + 1
    # The following loop creates an event_list with event objects inside
    # The indices correspond with the indices in daylist
    recommended_events = [None] * len(daylist)
    user_preferences = Preference.query.filter(Preference.user_id == current_user_id).all()
    if len(user_preferences) == 1 :
        user_preferences = user_preferences[0]
    for day_index in range(len(daylist)):
        if daylist[day_index] != 0:
            day = datetime.datetime(year, month, daylist[day_index])
            event_list[day_index] = Event.query.filter(Event.start >= day, Event.start < day+day_delta, Event.attending_user.any(User.id==current_user_id)).all()
            # Recommending Events Below:
            recommended_events[day_index] = Event.query.filter(Event.start >= day, Event.start < day+day_delta)

            #Find if the current user has any preference categories that match any event categories.
            user_categories = [u.id for u in user_preferences.categories]
            recommended_events[day_index] = recommended_events[day_index].filter(Event.categories.any(Category.id.in_(user_categories)))
            if user_preferences.price != None:
                recommended_events[day_index] = recommended_events[day_index].filter(Event.price<=user_preferences.price).all()
            if user_preferences.distance != None or user_preferences.distance != 0:
                for event in reversed(recommended_events[day_index]):
                    if user_preferences.distance_preference_conflicts_with_event(event):
                        recommended_events[day_index].remove(event)
            for event in reversed(recommended_events[day_index]):
                if current_user.is_Attending(event):
                    recommended_events[day_index].remove(event)


    return render_template("calender_week.html", now=now, month_name=month_name, month=month, year=year, daylist=daylist, event_list=event_list, week=week, days_in_previous_month=days_in_previous_month, week_of_today=week_of_today,recommended_events=recommended_events)


@bp.route('/calendar_page/daily/<int:year>/<int:month>/<int:currentDay>')
def calendar_page_daily(year, month, currentDay):
    if (month > 12 or month < 1):
        return ("Oops, the month is out of range!")
    # Initialize some useful variables:
    current_user_id = 0
    c = calendar.TextCalendar(calendar.SUNDAY) # Calendar object starting on Sunday
    now = datetime.datetime.now()
    event_list = Event.query.all()
    month_name = calendar.month_name[month]
    daylist = list(c.itermonthdays(year, month))
    day_delta = datetime.timedelta(days=1)
    # daylist is the list of numbers to put in each box of the calendar,
    # where 0 is an empty box, and 1 is the 1st of the month, etc.
    # example: [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 0, 0]

    if (month == 1):
        days_in_previous_month = calendar.monthrange(year-1, 12)[1]
    else:
        days_in_previous_month = calendar.monthrange(year, month-1)[1]

    days_in_current_month = calendar.monthrange(year, month)[1]

    event_list = [None]


    # The following loop creates an event_list with event objects inside
    # The indices correspond with the indices in daylist for attending_events
    day = datetime.datetime(year, month, currentDay)
    event_list[0] = Event.query.filter(Event.start >= day, Event.start < day+day_delta, Event.attending_user.any(User.id==current_user_id)).all()
    return render_template("calender_day.html", now=now, month_name=month_name, month=month, year=year, daylist=daylist, event_list=event_list, currentDay=currentDay, days_in_previous_month=days_in_previous_month, days_in_current_month=days_in_current_month)



    # List of Recommended Events
    recommended_events = [None]
    user_preferences = Preference.query.filter(Preference.user_id == current_user_id).all()
    if len(user_preferences) == 1 :
        user_preferences = user_preferences[0]
        # The indices correspond with the indices in daylist for recommended_events
        recommended_events[0] = Event.query.filter(Event.start >= day, Event.start < day+day_delta)

        #Find if the current user has any preference categories that match any event categories.
        user_categories = [u.id for u in user_preferences.categories]
        recommended_events[0] = recommended_events[0].filter(Event.categories.any(Category.id.in_(user_categories)))



        current_user = User.query.get(current_user_id)
        if user_preferences.price != None:
            recommended_events[0] = recommended_events[0].filter(Event.price<=user_preferences.price).all()
        if user_preferences.distance != None or user_preferences.distance != 0:
            for event in reversed(recommended_events[0]):
                if user_preferences.distance_preference_conflicts_with_event(event):
                    recommended_events[0].remove(event)
        for event in reversed(recommended_events[0]):
            if current_user.is_Attending(event):
                recommended_events[0].remove(event)

    return render_template("calender_day.html", now=now, month_name=month_name, month=month, year=year, daylist=daylist, event_list=event_list, currentDay=currentDay, days_in_previous_month=days_in_previous_month, days_in_current_month=days_in_current_month, recommended_events=recommended_events)





@bp.route('/events_page/<int:sortby>/', methods=['GET', 'POST'])
def events_page(sortby):
    #sortby can be [0,1,2,3,4], representing sorting by:
    #ID/Start Time/Name/Price/Location Respectively
    current_user_id = 0
    current_user = User.query.get(current_user_id)
    events_user_attend = current_user.events
    attend_form = EventsPageForm()
    if attend_form.is_submitted():
        selected_event_to_attend = Event.query.get(attend_form.event_id.data)
        if not current_user.is_Attending(selected_event_to_attend):
            current_user.attend_event(selected_event_to_attend)
        else:
            current_user.unattend_event(selected_event_to_attend)

        flash('Successfully Added')



    if sortby==0:
        events = Event.query.order_by(Event.id)
    elif sortby==1:
        events = Event.query.order_by(Event.start)
    elif sortby==2:
        events = Event.query.order_by(Event.name)
    elif sortby==3:
        events = Event.query.order_by(Event.price)
    elif sortby==4:
        events = Event.query.order_by(Event.location)
    else:
        events = Event.query.order_by(Event.id)

    list_is_attending = [None] * len(events.all())
    for i in range(len(events.all())):
        if events[i] in events_user_attend:
            list_is_attending[i] = True
        else:
            list_is_attending[i] = False
    return render_template('events_page.html', events=events, attend_form=attend_form, list_is_attending=list_is_attending)

@bp.route('/add_events', methods=['GET', 'POST'])
def add_events():
    event_form = EventForm()
    if event_form.validate_on_submit():
        event = Event(start=event_form.start.data, end=event_form.end.data, name=event_form.name.data, price=event_form.price.data, latitude=event_form.locationLatitude.data, longitude=event_form.locationLongitude.data)
        db.session.add(event)
        db.session.commit()
        event.save_list_of_categories(event_form.Categories.data.split(','))
        flash('Event Added.')
    return render_template('add_events.html', event_form=event_form)

@bp.route('/pref')
def preferences():
    pref_form = PreferenceForm()
    userid = 0
    pref = db.session.query(Preference).filter(Preference.user_id == userid).first()
    if pref is None:
        pref = Preference()
        pref.price = 0
        pref.distance = 10
        pref.size = "large"
        pref.latitude = 0
        pref.longitude = 0
    return render_template("Preference.html", preference=pref, pref_form=pref_form)

@bp.route('/save_preference', methods=['GET', 'POST'])
def save_preference():
    pref_form = PreferenceForm()
    userid = 0
    pref = db.session.query(Preference).filter(Preference.user_id == userid).first()
    if pref is None:
        prefer = Preference()
        prefer.user_id = userid
        prefer.price = pref_form.Price.data
        prefer.distance = pref_form.Distance.data
        prefer.size = request.form['size']
        prefer.latitude = request.form['locationLatitude']
        prefer.longitude = request.form['locationLongitude']
        db.session.add(prefer)
        db.session.commit()

    else:
        pref.price = pref_form.Price.data
        pref.distance = pref_form.Distance.data
        pref.size = request.form['size']
        pref.latitude = request.form['locationLatitude']
        pref.longitude = request.form['locationLongitude']
        db.session.commit()
        pref.save_list_of_categories(pref_form.Categories.data.split(','))

    return redirect(url_for('main.preferences', preference=pref))

@bp.route('/event/<int:id>', methods=['GET', 'POST'])
def event(id):
    current_user_id = 0
    current_user = User.query.get(current_user_id)

    events_user_attend = current_user.events

    attend_form = EventsPageForm()
    if attend_form.is_submitted():
        print(attend_form.event_id.data)
        selected_event_to_attend = Event.query.get(attend_form.event_id.data)
        if not current_user.is_Attending(selected_event_to_attend):
            current_user.attend_event(selected_event_to_attend)
        else:
            current_user.unattend_event(selected_event_to_attend)
        flash('Successfully Added')


    event = Event.query.get(id)


    is_attending = event in events_user_attend
    return render_template('single_event_page.html', event=event, attend_form=attend_form, is_attending=is_attending)

@bp.route('/add_time_slot', methods=['GET', 'POST'])
def add_time_slot():
    form = TimeSlotForm()
    if form.validate_on_submit():
        timeslot = TimeSlot(day=form.day.data, start_time=form.start_time.data, end_time=form.end_time.data)
        db.session.add(timeslot)
        db.session.commit()
        flash('Time Slot Added. Thank you.')
        return redirect(url_for('main.add_time_slot'))

    added_timeslots = db.session.query(TimeSlot).all()
    return render_template('workingtime_form.html', added_timeslots=added_timeslots, form=form)


#######################################################################
'''
@bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))# trying to redirect to intro page
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            #login_user(user)  # , remember=form.remember_me.data
            flash('Invalid Username or Password')
            return redirect(url_for('main.login'))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
        #return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
'''

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


'''
@auth.route('/signup', methods=['POST'])
def signup_post():
    form = RegisteredForm()
    user = User.query.filter_by(email=form).first()

    if user:
        flash('Email address already exists.')
        return(redirect(url_for('auth.login')))

    new_user = User(email=email. username=username, password=generate_password_hash(password, method='sha256')

    return render_template('signup.html', form=form)



@auth
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route

@bp.after_request
def sendsms(response):
    return response
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
'''



'''
    timeslot_id = request.form.get("timeslot_id")
    day = request.form.get("day")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    
     unused code/testing

if__name__ == '__main__':
    bp.run(debug=True)
def add_course():
    id = request.form.get("id")
    course_number = request.form.get("course_number")
    course_title = request.form.get("course_title")
    
    course = Course(id = id ,course_number=course_number, course_title = course_title)
    db.session.add(course)
    db.session.commit()
    course = Course.query.all()
    return render_template('index.html', course = course)
    
   
    
    
 @bp.route('/add_TimeSlot/', methods=['GET', 'POST'])
def add_TimeSlot():
    timeslot_id = request.form.get("timeslot_id")
    day = request.form.get("day")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    timeslot = TimeSlot(timeslot_id=timeslot_id, day=day, start_time=start_time, end_time=end_time)
    db.session.add(timeslot)
    db.session.commit()
    timeslots = TimeSlot.query.all()
    return render_template("workingtime_form.html", timeslots=timeslots)   
    
    
    
timeslot_id=timeslot_form.timeslot_id.data, 
'''