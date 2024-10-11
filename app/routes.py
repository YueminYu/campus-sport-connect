from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db, bcrypt
from .models import User, Event
from .forms import RegistrationForm, LoginForm, CreateEventForm
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
        flash('Your account has been created!', 'success')
        return redirect(url_for('main_routes.login'))
    return render_template('register.html', form=form)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main_routes.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@main_routes.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect(url_for('login')) 

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