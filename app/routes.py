from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db, bcrypt
from .models import User, Event
from .forms import RegistrationForm, LoginForm, CreateEventForm, EditProfileForm
from flask_login import login_user, logout_user, login_required, current_user

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    return render_template('base.html')

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please log in.', 'success')
        return redirect(url_for('main_routes.login'))  # Redirect to login page
    return render_template('register.html', form=form)


@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)  # Log in the user
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main_routes.profile'))  # Redirect to profile page
        else:
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
        event = Event(sport_type=form.sport_type.data, date=form.date.data, time=form.time.data,
                      location=form.location.data, created_by=current_user.id, max_participants=form.max_participants.data)
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('main_routes.home'))
    return render_template('create_event.html', form=form)

@main_routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)

@main_routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required  # Ensure only logged-in users can access this route
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        # Update user data from the form inputs
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Convert the list of sports to a comma-separated string before saving
        current_user.preferred_sport = ','.join(form.sports.data)

        # Commit the changes to the database
        db.session.commit()

        # Flash success message and redirect to profile page
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main_routes.profile'))

    elif request.method == 'GET':
        # Populate the form fields with the current user’s data
        form.username.data = current_user.username
        form.email.data = current_user.email

        # Convert the stored comma-separated string back into a list for the form
        form.sports.data = (
            current_user.preferred_sport.split(',') 
            if current_user.preferred_sport else []
        )

    # Render the edit profile template with the form
    return render_template('edit_profile.html', form=form)

@main_routes.route('/view_events', methods=['GET'])
def view_events():
    # Fetch and display events specific to the user or general events
    events = Event.query.filter_by(created_by=current_user.id).all()
    return render_template('view_events.html', events=events)
