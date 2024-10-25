from app import db, create_app  # Import your app factory
from app.models import User, Event  # Import the new Event model

# Create the Flask application instance
app = create_app()

# Set up the application context
with app.app_context():
    # Fetch all users from the database
    users = User.query.all()

    # Display each user's information and their events
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Preferred Sport: {user.preferred_sport}")
        
        # Fetch and display the events created by the user
        user_events = Event.query.filter_by(user_id=user.id).all()
        if user_events:
            print("  Events:")
            for event in user_events:
                print(f"    Event ID: {event.id}, Sport: {event.sport_type}, Date: {event.date}, "
                      f"Time: {event.time}, Location: {event.location}, "
                      f"Participants: {event.current_participants}/{event.max_participants}")
        else:
            print("  No events created.")
