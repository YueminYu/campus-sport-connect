from flask import (
    Blueprint, render_template, redirect, url_for, flash, request
)
from . import db, bcrypt
from .models import User, Event
from .forms import (
    RegistrationForm, LoginForm, CreateEventForm, 
    EditProfileForm, ChangePasswordForm
)
from flask_login import (
    login_user, logout_user, login_required, current_user
)

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    # Fetch all events from the database
    events = Event.query.all() if current_user.is_authenticated else []
    return render_template('home.html', events=events)


@main_routes.route('/join_event/<int:event_id>', methods=['POST'])
@login_required
def join_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Ensure the user is not joining their own event
    if event.user_id != current_user.id:
        # Add the user to the event's participants
        if current_user not in event.participants:
            event.participants.append(current_user)
            db.session.commit()
            flash("You have joined the event!", "success")
        else:
            flash("You are already part of this event!", "info")
    else:
        flash("You cannot join your own event.", "warning")
    
    return redirect(url_for('main_routes.home'))




@main_routes.route('/register', methods=['GET', 'POST'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main_routes.home'))  # Redirect to home
        flash('Login failed. Please check your email and password.', 'danger')

    return render_template('login.html', form=form)



@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_routes.login'))


@main_routes.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        event = Event(
            sport_type=form.sport_type.data,
            date=form.date.data,
            time=form.time.data,
            location=form.location.data,
            user_id=current_user.id,
            max_participants=form.max_participants.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('main_routes.view_events'))

    return render_template('create_event.html', form=form)


@main_routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)


@main_routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
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


@main_routes.route('/view_events', methods=['GET'])
def view_events():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('view_events.html', events=events)


@main_routes.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
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
    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        flash('You are not authorized to delete this event.', 'danger')
        return redirect(url_for('main_routes.view_events'))

    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully.', 'success')
    return redirect(url_for('main_routes.view_events'))


@main_routes.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        flash('You are not authorized to edit this event.', 'danger')
        return redirect(url_for('main_routes.view_events'))

    form = CreateEventForm(obj=event)

    if form.validate_on_submit():
        event.sport_type = form.sport_type.data
        event.date = form.date.data
        event.time = form.time.data
        event.location = form.location.data
        event.max_participants = form.max_participants.data

        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('main_routes.view_events'))

    return render_template('edit_event.html', form=form, event=event)
