from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

# Configure the app
import os
app.config.from_object(os.environ['APP_SETTINGS'])

# Create sqlalchemy database object
db = SQLAlchemy(app)

# According to sensei, this must be imported after SQLAlch is called on app.
# Consider adding the 'db = SQLAlchemy(app)' line to the .wsgi file.
# This is necessary because of the circular dependency.
from project.users.views import users_blueprint
from project.home.views import home_blueprint
from project.errors.views import error_blueprint

# Register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(error_blueprint)

from models import User

login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

login_manager.login_view = 'home.homepage'
login_manager.login_message = 'You must be logged in!'