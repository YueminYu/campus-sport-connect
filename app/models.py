
"""
Models module defining database structures and relationships.
"""

from flask_login import UserMixin
from . import db, bcrypt

participants = db.Table('participants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    """Model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(15), nullable=True)  
    password = db.Column(db.String(60), nullable=False)
    preferred_sport = db.Column(db.String(200), nullable=True)
    avatar = db.Column(db.String(120), nullable=True)

    # Relationship to events created by the user
    events = db.relationship('Event', back_populates='creator', lazy=True)

    # Relationship to events the user has joined
    joined_events = db.relationship('Event', secondary=participants, back_populates='participants')

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
    date = db.Column(db.String(20), nullable=False)  # Already a string
    time = db.Column(db.String(20), nullable=False)  # Change this to string
    location = db.Column(db.String(100), nullable=False)
    max_participants = db.Column(db.Integer, nullable=False)
    current_participants = db.Column(db.Integer, default=0)
    background_image = db.Column(db.String(100), nullable=True)  # Add background image here
    telephone = db.Column(db.String(15), nullable=True)  # Add this line for the telephone field

    # Relationship to link Event with its creator
    creator = db.relationship('User', back_populates='events')

    # Relationship to link Event with participants
    participants = db.relationship('User', secondary=participants, back_populates='joined_events')

    @property
    def current_participants_count(self):
        return len(self.participants)

