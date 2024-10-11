from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'your_secret_key'  # Use a secure key
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#     db.init_app(app)
#     bcrypt.init_app(app)
#     login_manager.init_app(app)

#     from .models import User  # Import User model after app is created

#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))

#     from .routes import main_routes
#     app.register_blueprint(main_routes)

#     return app

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Use a secure key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Protect user session after login
    login_manager.login_view = 'main_routes.login'  # Redirect unauthenticated users
    login_manager.login_message_category = 'info'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
