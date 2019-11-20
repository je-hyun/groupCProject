from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired

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
