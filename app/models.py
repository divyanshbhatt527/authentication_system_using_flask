from flask_login import UserMixin
from . import db, login_manager

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.String(120))  
    name = db.Column(db.String(100))   
    bio = db.Column(db.Text)          
    phone = db.Column(db.String(20))    
    is_public = db.Column(db.Boolean, default=True)  
    is_admin = db.Column(db.Boolean, default=False) 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    

@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return None
    try:
        return User.query.get(int(user_id))
    except ValueError:
        return None


def update_admin_user():
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user:
        admin_user.is_admin = True
        db.session.commit()





