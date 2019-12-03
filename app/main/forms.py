from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField, TimeField, SelectField
from wtforms.validators import DataRequired, InputRequired, Email, Length, ValidationError, EqualTo
from app.models import User

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    start = DateTimeField('Start Date/Time', validators=[DataRequired()])
    end = DateTimeField('End Date/Time', validators=[DataRequired()])
    price = IntegerField('Price')
    location = StringField('Location')
    submit = SubmitField('Add Event')

class EventsPageForm(FlaskForm):
    submit = SubmitField('Attend')

#class PreferenceForm(FlaskForm):

class TimeSlotForm(FlaskForm):

    day = SelectField('[Day]', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                                      ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'),
                                      ('Sunday', 'Sunday')], validators=[DataRequired()])
    startTime = TimeField('Start Time:', validators=[DataRequired()], format="%H:%M")
    endTime = TimeField('End Time:', validators=[DataRequired()], format="%H:%M")
    submit = SubmitField('Add Time Slot')

#Kamil Peza Login and Register Forms:
#https://github.com/PrettyPrinted/building_user_login_system/blob/master/finish/app.py

#https://hackersandslackers.com/authenticating-users-with-flask-login/
class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8, max=20)])
    #remember = BooleanField('remember me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email:', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8, max=20)])
    password2 = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


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
