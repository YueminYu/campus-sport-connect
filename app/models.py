from . import db, bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    preferred_sport = db.Column(db.String(200), nullable=True)

    # Relationship to events
    events = db.relationship('Event', back_populates='creator', lazy=True)

    def set_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verifies the password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)


class Event(db.Model):
    """Model for storing event information."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sport_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    current_participants = db.Column(db.Integer, default=0)

    # Relationship to link Event with User
    creator = db.relationship('User', back_populates='events')
