from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField, TimeField, SelectField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    start = DateTimeField('Start Date/Time', validators=[DataRequired()])
    end = DateTimeField('End Date/Time', validators=[DataRequired()])
    price = IntegerField('Price')
    location = StringField('Location')
    submit = SubmitField('Add Event')

class EventsPageForm(FlaskForm):
    submit = SubmitField('Attend Event')

#class PreferenceForm(FlaskForm):

class TimeSlotForm(FlaskForm):
    day = SelectField('[Day]', choices=[('Monday', 'Monday'),
                                        ('Tuesday', 'Tuesday'),
                                        ('Wednesday', 'Wednesday'),
                                        ('Thursday', 'Thursday'),
                                        ('Friday', 'Friday'),
                                        ('Saturday', 'Saturday'),
                                        ('Sunday', 'Sunday')], validators=[DataRequired()])
    startTime = TimeField('Start Time:', validators=[DataRequired()], format="%H:%M")
    endTime = TimeField('End Time:', validators=[DataRequired()], format="%H:%M")
    submit = SubmitField('Add Time Slot')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


'''
timeslot_id = IntegerField('timeslot_id')


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

class EventsPageForm(FlaskForm):
    submit = SubmitField('Attend Event')


'''
