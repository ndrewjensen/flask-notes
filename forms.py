from click import password_option
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email



class SignUpForm(FlaskForm):
    """Form for a user to sign up"""

    username = StringField("Set Username:",
                            validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField("Set Password:",
                            validators=[InputRequired(), Length(min=1)])

    email = StringField("Email:",
                            validators=[InputRequired(), Length(min=1), Email()])

    first_name = StringField("First Name:",
                            validators=[InputRequired(), Length(min=1, max=30)])

    last_name = StringField("Last Name:",
                            validators=[InputRequired(), Length(min=1, max=30)])

class LoginForm(FlaskForm):
    username = StringField("Username:",
                            validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField("Password:",
                            validators=[InputRequired(), Length(min=1)])