from app import db, create_app  # Import your app factory
from app.models import User

# Create the Flask application instance
app = create_app()

# Set up the application context
with app.app_context():
    # Fetch all users from the database
    users = User.query.all()

    # Display each user's information
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Password: {user.password}, Preferred Sport: {user.preferred_sport}")