from click import password_option
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email

class OnlyCSRFForm(FlaskForm):
    """CSRF token for POST requests without forms"""


################################################################################
#USER FORMS
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
    """Form to log in"""
    username = StringField("Username:",
                            validators=[InputRequired(), Length(min=1, max=20)])

    password = PasswordField("Password:",
                            validators=[InputRequired(), Length(min=1)])


################################################################################
# NOTES FORMS

class NoteForm (FlaskForm):
    """Form to add/edit a note"""

    title = StringField("Title",
                        validators=[InputRequired(), Length(min=1, max=100)])
    content = TextAreaField("Content",
                        validators=[InputRequired(), Length(min=1)])


