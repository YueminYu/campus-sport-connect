"""
Routes module defining all application routes and their handlers.
"""

import os
import uuid
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app, session, jsonify
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)
from werkzeug.utils import secure_filename
from . import db, bcrypt
from .models import User, Event
from .forms import (
    RegistrationForm, LoginForm, CreateEventForm, 
    EditProfileForm, ChangePasswordForm
)
from datetime import datetime, timedelta
import pytz

main_routes = Blueprint('main_routes', __name__)



SPORT_BACKGROUND_IMAGES = {
    'basketball': 'basketball_court.png',
    'badminton': 'badminton_court.png',
    'football': 'football_court.png',
    'soccer': 'soccer_court.png',
    # Default option if no match
    'default': 'background.png'
}



@main_routes.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@main_routes.route('/join_event/<int:event_id>', methods=['POST'])
@login_required
def join_event(event_id):
    """Allow a user to join an event if they are not the organizer and if the event isn't full."""
    event = Event.query.get_or_404(event_id)
    
    # Check if the user is not the organizer
    if event.user_id == current_user.id:
        flash("You cannot join your own event.", "warning")
        return redirect(url_for('main_routes.view_all_events'))

    # Check if the user is already a participant
    if current_user in event.participants:
        flash("You are already part of this event!", "info")
        return redirect(url_for('main_routes.view_all_events'))

    # Check if the event is full
    if event.current_participants_count >= event.max_participants:
        flash("The event is full. You cannot join.", "warning")
    else:
        # Add the user to the participants list
        event.participants.append(current_user)
        db.session.commit()
        flash("You have joined the event!", "success")
    
    return redirect(url_for('main_routes.view_all_events'))

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')

        user = User(
            username=form.username.data,
            email=form.email.data,
            telephone=form.telephone.data,  # Save telephone number
            password=hashed_password,
            preferred_sport=', '.join(
                [sport for sport in ['Basketball', 'Football', 'Soccer', 'Badminton'] if getattr(form, sport.lower()).data]
            )
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please log in.', 'success')
        return redirect(url_for('main_routes.login'))

    return render_template('register.html', form=form)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main_routes.home'))
        flash('Login failed. Please check your email and password.', 'danger')

    return render_template('login.html', form=form)

@main_routes.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    return redirect(url_for('main_routes.login'))



from datetime import datetime

@main_routes.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
         # Determine background image dynamically
        background_image = SPORT_BACKGROUND_IMAGES.get(
            form.sport_type.data.lower(),  # Convert to lowercase for consistency
            SPORT_BACKGROUND_IMAGES['default']
        )
        # Ensure that max_participants is greater than or equal to 1
        if form.max_participants.data < 1:
            flash('Max participants must be at least 1.', 'danger')
            return render_template('create_event.html', form=form)

        # Create the event instance
        event = Event(
            sport_type=form.sport_type.data,
            date=form.date.data.strftime('%Y-%m-%d'),  
            time=form.time.data.strftime('%H:%M:%S'), 
            location=form.location.data,
            max_participants=form.max_participants.data,
            user_id=current_user.id,
            background_image=background_image 
        )
        # Add the creator as a participant if there is space available
        if event.current_participants_count < event.max_participants:
            event.participants.append(current_user)
        else:
            flash('Event is full, cannot add creator as participant.', 'danger')
            return render_template('create_event.html', form=form)

        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('main_routes.view_all_events'))
    
    return render_template('create_event.html', form=form)

from flask import url_for

@main_routes.route('/get_sport_image/<sport_type>', methods=['GET'])
def get_sport_image(sport_type):
    image_filename = SPORT_BACKGROUND_IMAGES.get(
        sport_type.lower(),
        SPORT_BACKGROUND_IMAGES['default']
    )
    image_url = url_for('static', filename=image_filename)
    return jsonify({'image_url': image_url})


@main_routes.route('/profile')
@login_required
def profile():
    """Display the user's profile."""
    return render_template('profile.html', current_user=current_user)

@main_routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit the user's profile, including avatar upload and sports interests."""
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_dir = os.path.join(current_app.root_path, 'static/uploads/avatars')
            os.makedirs(avatar_dir, exist_ok=True)
            avatar_filename = f"{uuid.uuid4().hex}_{secure_filename(form.avatar.data.filename)}"
            avatar_path = os.path.join(avatar_dir, avatar_filename)
            form.avatar.data.save(avatar_path)
            current_user.avatar = f'uploads/avatars/{avatar_filename}'
        
        # Update user information, including telephone
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.telephone = form.telephone.data  # Save the telephone number

        sports_selected = []
        if form.basketball.data:
            sports_selected.append('Basketball')
        if form.football.data:
            sports_selected.append('Football')
        if form.soccer.data:
            sports_selected.append('Soccer')
        if form.badminton.data:
            sports_selected.append('Badminton')

        current_user.preferred_sport = ', '.join(sports_selected)
        # current_user.username = form.username.data
        # current_user.email = form.email.data
        # current_user.telephone = form.telephone.data 
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main_routes.profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.telephone.data = current_user.telephone  
        form.basketball.data = 'Basketball' in (current_user.preferred_sport or '')
        form.football.data = 'Football' in (current_user.preferred_sport or '')
        form.soccer.data = 'Soccer' in (current_user.preferred_sport or '')
        form.badminton.data = 'Badminton' in (current_user.preferred_sport or '')

    return render_template('edit_profile.html', form=form)

def parse_date(date_string):
    """Attempt to parse a date string with multiple possible formats."""
    for fmt in ('%Y-%m-%d', '%Y/%m/%d'):
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    # If the date string cannot be parsed, return None
    return None

@main_routes.route('/view_my_events', methods=['GET'])
@login_required
def view_my_events():
    """Display events created by the logged-in user."""
    # Get the current time as a naive datetime
    central_tz = pytz.timezone('America/Chicago')
    now = datetime.now(central_tz).replace(tzinfo=None)

    # Get all events created by the current user
    all_events = Event.query.filter_by(user_id=current_user.id).all()

    # Split events into upcoming and past based on the current time
    upcoming_events = []
    past_events = []

    for event in all_events:
        event_date = parse_date(event.date)
        if event_date:
            if event_date > now:
                upcoming_events.append(event)
            else:
                past_events.append(event)

    return render_template('view_my_events.html', upcoming_events=upcoming_events, past_events=past_events)


@main_routes.route('/view_all_events', methods=['GET'])
@login_required
def view_all_events():
    """Display all events in the system."""
    # Get the current time as a naive datetime
    central_tz = pytz.timezone('America/Chicago')
    now = datetime.now(central_tz).replace(tzinfo=None)

    # Get all events in the database
    all_events = Event.query.all()

    # Split events into upcoming and past based on the current time
    upcoming_events = []
    past_events = []

    for event in all_events:
        event_date = parse_date(event.date)
        if event_date:
            if event_date > now:
                upcoming_events.append(event)
            else:
                past_events.append(event)

    return render_template('view_all_events.html', upcoming_events=upcoming_events, past_events=past_events)

@main_routes.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Allow the user to change their password."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Incorrect current password.', 'danger')
            return redirect(url_for('main_routes.change_password'))

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been changed. Please log in again.', 'success')
        logout_user()
        return redirect(url_for('main_routes.login'))

    return render_template('change_password.html', form=form)

@main_routes.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    """Allow the organizer or a participant to delete an event."""
    event = Event.query.get_or_404(event_id)
    if event.user_id == current_user.id:
        db.session.delete(event)
        db.session.commit()
        flash("Event deleted successfully.", "success")
    elif current_user in event.participants:
        event.participants.remove(current_user)
        db.session.commit()
        flash("You have left the event.", "success")
    else:
        flash("You are not authorized to delete this event.", "danger")

    return redirect(url_for('main_routes.view_all_events'))


from datetime import datetime

@main_routes.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """Edit an event if the logged-in user is the organizer."""
    event = Event.query.get_or_404(event_id)
    
    # Ensure only the event owner can access the edit page
    if event.user_id != current_user.id:
        flash('You are not authorized to edit this event.', 'danger')
        return redirect(url_for('main_routes.view_my_events'))

    # Create the form object, prepopulate fields with event data
    form = CreateEventForm()

    # Populate the form with current event details when the request is GET
    if request.method == 'GET':
        try:
            event_date = datetime.strptime(event.date, '%Y-%m-%d').date()
            event_time = datetime.strptime(event.time, '%H:%M:%S').time()

            form.sport_type.data = event.sport_type
            form.date.data = event_date
            form.time.data = event_time
            form.location.data = event.location
            form.max_participants.data = event.max_participants
            # Remove background_image prepopulation since it is dynamically determined
        except ValueError:
            flash("Error in parsing event date or time.", "danger")

    # Update event details from the form on form submission (POST)
    if form.validate_on_submit():
        try:
            # Update event details
            event.sport_type = form.sport_type.data
            event.date = form.date.data.strftime('%Y-%m-%d')  # Update with formatted date
            event.time = form.time.data.strftime('%H:%M:%S')  # Update with formatted time
            event.location = form.location.data
            event.max_participants = form.max_participants.data
            # Dynamically determine background_image
            event.background_image = SPORT_BACKGROUND_IMAGES.get(
                form.sport_type.data.lower(),
                SPORT_BACKGROUND_IMAGES['default']
            )

            # Commit the changes to the database
            db.session.commit()
            flash('Event updated successfully!', 'success')
            return redirect(url_for('main_routes.view_all_events'))
        except Exception as e:
            db.session.rollback()
            print("Error updating event:", e)
            flash("An error occurred while updating the event. Please try again.", 'danger')
    else:
        # If form validation fails, print the errors
        if form.errors:
            print("Form validation failed. Errors:", form.errors)

    return render_template('edit_event.html', form=form, event=event)



@main_routes.route('/user/<int:user_id>')
@login_required
def view_user_profile(user_id):
    """View another user's profile based on their user ID."""
    user = User.query.get_or_404(user_id)
    return render_template('view_profile.html', user=user)
