
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, IntegerField, FileField, SelectField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp 
from flask_wtf.file import FileAllowed
from datetime import datetime
from wtforms.fields import DateField, TimeField
from wtforms import ValidationError
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    first_name = StringField(
        'First Name', validators=[DataRequired()]
    )
    last_name = StringField(
        'Last Name', validators=[DataRequired()]
    )
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match.')]
    )
    
    # Sports Interest as Boolean Fields
    basketball = BooleanField('Basketball')
    football = BooleanField('Football')
    soccer = BooleanField('Soccer')
    badminton = BooleanField('Badminton')  # Newly added sport field

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password', validators=[DataRequired()]
    )
    submit = SubmitField('Login')

from wtforms.validators import NumberRange
class CreateEventForm(FlaskForm):
    """Form for creating a new event."""
    sport_type = StringField(
        'Sport Type', validators=[DataRequired()]
    )
    date = DateField(
        'Date', format='%Y-%m-%d', validators=[DataRequired()]
    )
    time = TimeField(
        'Time', validators=[DataRequired()]
    )
    location = StringField(
        'Location', validators=[DataRequired()]
    )
    max_participants = IntegerField(
        'Max Participants', validators=[DataRequired()]
    )
    background_image = SelectField(
        'Background Image', 
        choices=[
            ('background.png', 'Default'), 
            ('badminton_court.png', 'Badminton Court'),
            ('football_court.png', 'Football Court'),
            ('soccer_court.png', 'Soccer Court')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Create Event')

    def validate_date(form, field):
        """Ensure the selected date is in the future."""
        if field.data < datetime.today().date():
            raise ValidationError("Date must be in the future.")

    def validate_time(form, field):
        """Optional: Custom validation for time."""
        if field.data and (field.data.hour < 8 or field.data.hour > 22):
            raise ValidationError("Time must be between 08:00 and 22:00.")




class EditProfileForm(FlaskForm):
    """Form for editing user profile."""
    username = StringField(
        'Username', validators=[DataRequired()]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
    )
    telephone = StringField(
        'Telephone Number',
        validators=[
            DataRequired(),
            Regexp(r'^\+?[1-9]\d{1,14}$', message="Please enter a valid phone number."),
        ],
    )

    avatar = FileField('Upload Avatar', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    # Sports Interests as Boolean Fields
    basketball = BooleanField('Basketball')
    football = BooleanField('Football')
    soccer = BooleanField('Soccer')
    badminton = BooleanField('Badminton')

    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    """Form for changing user password."""
    current_password = PasswordField(
        'Current Password', validators=[DataRequired()]
    )
    new_password = PasswordField(
        'New Password', validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        'Confirm New Password',
        validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')]
    )
    submit = SubmitField('Change Password')
