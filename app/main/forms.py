from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import *

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    start = DateTimeField('Start Date/Time', validators=[DataRequired()])
    end = DateTimeField('End Date/Time', validators=[DataRequired()])
    price = IntegerField('Price')
    location = StringField('Location')
    submit = SubmitField('Add Event')

class EventsPageForm(FlaskForm):
    submit = SubmitField('Attend Event')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired, EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()    
        if user is not None:
            raise ValidationError('Username is taken, please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email address is taken, please use a different email address.')
#class PreferenceForm(FlaskForm):
    