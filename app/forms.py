from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    basketball = BooleanField('Basketball')
    football = BooleanField('Football')
    soccer = BooleanField('Soccer')
    badminton = BooleanField('Badminton')  # New Badminton field
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class CreateEventForm(FlaskForm):
    sport_type = StringField('Sport Type', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    max_participants = IntegerField('Max Participants', validators=[DataRequired()])
    submit = SubmitField('Create Event')
    
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    sports = SelectMultipleField('Sports Interested', choices=[('basketball', 'Basketball'), ('football', 'Football'), ('soccer', 'Soccer'), ('badminton', 'Badminton')])
    submit = SubmitField('Update Profile')