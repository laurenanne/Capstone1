from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.validators import Length, InputRequired


class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6)])


class NewUserForm(FlaskForm):
    """New User Signup Form"""

    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name')
    username = StringField('Username',validators=[
                           InputRequired(), Length(min=5, max=50)])
    password = PasswordField('Password',validators=[
                             InputRequired(), Length(min=6)])
    image_url = StringField(
        'Image URL', default='/static/images/userimage.jpeg')


class EditUserForm(FlaskForm):
    """User Edit Form"""

    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name')
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=5, max=50)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=6)])
    image_url = StringField(
        'Image URL', default='/static/images/userimage.jpeg')


class WizardNameForm(FlaskForm):
    """Wizard Name Generator"""

    first_name = StringField('First Name', validators=[InputRequired()])
    birth_month = SelectField(
        'Birth Month', choices=[('Jan', 'Jan'), ('Feb', 'Feb'), ('Mar', 'Mar'), ('Apr', 'Apr'), ('May', 'May'), ('Jun', 'Jun'), ('Jul', 'Jul'), ('Aug', 'Aug'), ('Sep', 'Sep'), ('Oct', 'Oct'), ('Nov', 'Nov'), ('Dec', 'Dec')],  validators=[InputRequired()])
    fav_color = SelectField('Favorite Color', choices=[(
                            'red', 'Red'), ('orange', 'Orange'), ('yellow', 'Yellow'), ('green', 'Green'), ('blue', 'Blue'), ('purple', "Purple"), ('pink', 'Pink')], validators=[InputRequired()])
