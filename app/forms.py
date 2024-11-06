from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, IntegerField, FileField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileAllowed

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


class CreateEventForm(FlaskForm):
    """Form for creating a new event."""
    sport_type = StringField(
        'Sport Type', validators=[DataRequired()]
    )
    date = StringField(
        'Date', validators=[DataRequired()]
    )
    time = StringField(
        'Time', validators=[DataRequired()]
    )
    location = StringField(
        'Location', validators=[DataRequired()]
    )
    max_participants = IntegerField(
        'Max Participants', validators=[DataRequired()]
    )
    submit = SubmitField('Create Event')


class EditProfileForm(FlaskForm):
    """Form for editing user profile."""
    username = StringField(
        'Username', validators=[DataRequired()]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
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
