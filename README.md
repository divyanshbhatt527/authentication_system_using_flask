Authentication System Flask
This is a Flask-based authentication system for web applications. It provides user registration, login, logout, and profile management features. The system supports both traditional email/password authentication and OAuth2 authentication via Google.

Features
User registration with email and password
User login and logout
OAuth2 authentication with Google
User profile management (update profile details and profile picture)
User profile visibility settings (public or private)

Installation
Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/your-username/authentication-system-flask.git
Navigate to the project directory:

bash
Copy code
cd authentication-system-flask
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Configure the environment variables:

Create a .env file in the root directory.
Define the following variables:
plaintext
Copy code
FLASK_APP=app
FLASK_ENV=development  # or production in a production environment
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=your_database_uri
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
Run the application:

bash
Copy code
flask run
Open http://localhost:5000 in your web browser to access the application.

Usage
Register a new account using your email and password.
Log in with your credentials or use the Google OAuth2 login option.
Update your profile details and profile picture in the profile section.
Log out when you're done using the application.
