print("Starting Flask application...")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
app = Flask(__name__)

app.config['DEBUG'] = True
app.secret_key = '717d86f0a025f4cab9c01367c12ebc96'  # Set the generated secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\hp\\Desktop\\Authentication_system_flask\\instance\\app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.login_view = 'routes.login'

@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return None
    try:
        return User.query.get(int(user_id))
    except ValueError:
        return None

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='459788608630-qqil5534t970282t416pjm3knml2slvf.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

db = SQLAlchemy(app)

# Register blueprints (routes)
from .routes import bp
app.register_blueprint(bp)

# Import the User model after db is initialized
from .models import User

# Create the database tables
with app.app_context():
    db.create_all()


    


