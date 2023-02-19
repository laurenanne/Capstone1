from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, InputRequired


class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6)])


class NewUserForm(FlaskForm):
    """New User Signup Form"""

    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6)])
    image_url = StringField(
        'Image URL', default='/static/images/userimage.jpeg')


class EditUserForm(FlaskForm):
    """User Edit Form"""

    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6)])
    image_url = StringField(
        'Image URL', default='/static/images/userimage.jpeg')
