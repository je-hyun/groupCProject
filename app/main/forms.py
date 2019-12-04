from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField, FloatField
from wtforms import RadioField
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    start = DateTimeField('Start Date/Time', validators=[DataRequired()])
    end = DateTimeField('End Date/Time', validators=[DataRequired()])
    price = FloatField('Price')
    location = StringField('Location')
    submit = SubmitField('Add Event')


class EventsPageForm(FlaskForm):
    event_id = IntegerField('Event ID')
    submit = SubmitField('Attend')



class PreferenceForm(FlaskForm):
    Price = FloatField('Price', validators=[DataRequired()])
    Distance = IntegerField('Distance', validators=[DataRequired()])
    Size = RadioField('size', validators=[DataRequired()])
