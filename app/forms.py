from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, URL

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    phone = StringField('Phone')
    email = StringField('Email', validators=[DataRequired(), Email()])
    visibility = SelectField('Visibility', choices=[('public', 'Public'), ('private', 'Private')])
    photo = FileField('Photo')
    photo_url = StringField('Photo URL', validators=[URL()])
