import os
import secrets
import string
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import logout_user, current_user, login_required, login_user
from werkzeug.utils import secure_filename
from .forms import ProfileForm
from .models import db, User, update_admin_user
from . import  google

bp = Blueprint('routes', __name__)

def generate_random_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(12)) 


@bp.route('/')
def index():
    update_admin_user()
    if current_user.is_authenticated:
        users = User.query.all()
        return render_template('index.html', users=users)
    else:
        return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            flash('Login successful', 'success')
            login_user(user)
            print(f'user with username {username} logged in.')
            print(f'Current user is {current_user.is_authenticated}')
            return redirect(url_for('routes.index'))
        else:
            flash('Invalid username or password', 'error')
            print('Incorrect credentials.')

    return render_template('login.html')

# Google OAuth login route
@bp.route('/login/google')
def login_google():
    return google.authorize(callback=url_for('routes.authorized', _external=True))

# Tokengetter function for Google OAuth
@google.tokengetter
def get_google_oauth_token():
    if 'google_token' in session:
        return session['google_token']
    return None

# Callback route for handling Google OAuth response
@bp.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        flash('Access denied: You denied the request to sign in with Google.', 'error')
        return redirect(url_for('routes.index'))

    session['google_token'] = (resp['access_token'], '')
    
    token = get_google_oauth_token()
    if token is None:
        flash('Failed to retrieve OAuth token.', 'error')
        return redirect(url_for('routes.index'))
    
    user_info = google.get('userinfo')
    if user_info.status != 200:
        flash('Failed to fetch user information from Google.', 'error')
        return redirect(url_for('routes.index'))

    email = user_info.data['email']
    
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
    else:
        password = generate_random_password()
        new_user = User(username=email, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)

    flash('Logged in successfully!', 'success')
    return redirect(url_for('routes.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address is already in use', 'error')
            return redirect(url_for('routes.register'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)  
        flash('Registration successful', 'success')
        return redirect(url_for('routes.index'))

    return render_template('register.html')


@bp.route('/logout')
@login_required
def logout():
    session.pop('google_token', None)
    logout_user()  
    flash('You have been logged out', 'success')
    print(f'User logged out')
    return redirect(url_for('routes.index'))


@bp.route('/user/<username>')
@login_required
def view_user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        if current_user == user or user.is_public or current_user.is_admin:
            return render_template('user_profile.html', user=user)
        else:
            flash("You don't have permission to view this profile.", 'error')
            print('Unauthorized request!')
            return redirect(url_for('routes.index'))
    else:
        flash("User not found.", 'error')
        return redirect(url_for('routes.index'))

UPLOAD_FOLDER = 'app\static\profile_photos'


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def get_profile():
    form = ProfileForm()
    if request.method == 'POST':
        current_user.name = request.form['name']
        current_user.username = request.form['username']
        current_user.bio = request.form['bio']
        current_user.phone = request.form['phone']
        current_user.email = request.form['email']
        current_user.is_public = request.form['visibility'] == 'public'
        if request.form['password']:
            print('Password changed!')
            current_user.set_password(request.form['password'])
        photo = request.files.get('photo')
        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(UPLOAD_FOLDER, filename))
            current_user.photo = filename
        elif form.photo_url.data:
            current_user.photo = form.photo_url.data

        db.session.commit()
        flash('Profile Updated!')
        print(f'user profile updated ')

    return render_template('profile.html', form=form)
