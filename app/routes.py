"""
Routes module defining all application routes and their handlers.
"""

import os
import uuid
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app
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

main_routes = Blueprint('main_routes', __name__)




SPORT_BACKGROUND_IMAGES = {
    'Badminton': 'images/badminton_court.png',
    'Football': 'images/football_court.png',
    'Soccer': 'images/soccer_court.png',
    # Default option if no match
    'default': 'images/background.png'
}



@main_routes.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@main_routes.route('/join_event/<int:event_id>', methods=['POST'])
@login_required
def join_event(event_id):
    """Allow a user to join an event if they are not the organizer."""
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        if current_user not in event.participants:
            event.participants.append(current_user)
            db.session.commit()
            flash("You have joined the event!", "success")
        else:
            flash("You are already part of this event!", "info")
    else:
        flash("You cannot join your own event.", "warning")
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
            password=hashed_password
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



@main_routes.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        # Get the background image path from the form data
        background_image = request.form.get("background_image", "images/background.png")
        
        # Create the event instance (excluding background_image from the database)
        event = Event(
            sport_type=form.sport_type.data,
            date=form.date.data,
            time=form.time.data,
            location=form.location.data,
            user_id=current_user.id,
            max_participants=form.max_participants.data
        )
        event.participants.append(current_user)

        db.session.add(event)
        db.session.commit()
        
        # Flash a success message and redirect to the all events page
        flash('Your event has been created!', 'success')
        return redirect(url_for('main_routes.view_all_events'))

    return render_template('create_event.html', form=form)



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
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main_routes.profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.basketball.data = 'Basketball' in (current_user.preferred_sport or '')
        form.football.data = 'Football' in (current_user.preferred_sport or '')
        form.soccer.data = 'Soccer' in (current_user.preferred_sport or '')
        form.badminton.data = 'Badminton' in (current_user.preferred_sport or '')

    return render_template('edit_profile.html', form=form)

@main_routes.route('/view_my_events', methods=['GET'])
@login_required
def view_my_events():
    """Display events created by the logged-in user."""
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('view_my_events.html', events=events)

@main_routes.route('/view_all_events', methods=['GET'])
@login_required
def view_all_events():
    """Display all events in the system."""
    events = Event.query.all()
    return render_template('view_all_events.html', events=events)

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

@main_routes.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    """Edit an event if the logged-in user is the organizer."""
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        flash('You are not authorized to edit this event.', 'danger')
        return redirect(url_for('main_routes.view_my_events'))

    form = CreateEventForm(obj=event)
    if form.validate_on_submit():
        event.sport_type = form.sport_type.data
        event.date = form.date.data
        event.time = form.time.data
        event.location = form.location.data
        event.max_participants = form.max_participants.data
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('main_routes.view_my_events'))

    return render_template('edit_event.html', form=form, event=event)

@main_routes.route('/user/<int:user_id>')
@login_required
def view_user_profile(user_id):
    """View another user's profile based on their user ID."""
    user = User.query.get_or_404(user_id)
    return render_template('view_profile.html', user=user)
