# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

# db = SQLAlchemy()
# bcrypt = Bcrypt()
# login_manager = LoginManager()


# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'your_secret_key'  # Use a secure key
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#     db.init_app(app)
#     bcrypt.init_app(app)
#     login_manager.init_app(app)

#     # Protect user session after login
#     login_manager.login_view = 'main_routes.login'  # Redirect unauthenticated users
#     login_manager.login_message_category = 'info'

#     from .models import User

#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))

#     from .routes import main_routes
#     app.register_blueprint(main_routes)

#     return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Set up login redirection
    login_manager.login_view = 'main_routes.login'
    login_manager.login_message_category = 'info'

    # Import User model and create tables immediately
    with app.app_context():
        from .models import User  # Avoid circular imports
        db.create_all()  # Create the database tables

    # Load the user from session
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app

