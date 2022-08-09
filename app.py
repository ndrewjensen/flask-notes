from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
from forms import SignUpForm, LoginForm, OnlyCSRFForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'euhtnidhe4536789uidjthudne'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
connect_db(app)
db.create_all()

@app.get('/')
def root():
    """redirects to register page"""
    return redirect('/register')


@app.route('/register', methods = ['GET', 'POST'])
def show_user_signup():
    "Show a user registration page"
    form = SignUpForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User().register(username,
                                   password,
                                   email,
                                   first_name,
                                   last_name)

        db.session.add(new_user)
        db.session.commit()

        flash(f"{username} created, {first_name} {last_name}")

        session["username"] = new_user.username

        return redirect(f'/users/{new_user.username}')

    return render_template("signup.html", form = form)


@app.route('/login', methods = ['GET','POST'])
def display_login_form():
    """Show a form that when submitted will login a user. Form accepts
    a username and a password."""
    if "username" in session:
        return redirect(f"/users/{session['username']}")


    form = LoginForm()

    if not form.validate_on_submit():
        return render_template("login.html", form = form)

    username = form.username.data
    password = form.password.data

    user = User().authenticate(username,
                                password)

    if not user:
        flash("Incorrect username and/or password")
        return render_template("login.html", form = form)

    session["username"] = user.username

    flash(f"{username} successfully logged in.")

    return redirect(f'/users/{user.username}')


@app.get('/users/<username>')
def display_user_details(username):
    "Display user details"
    if "username" not in session or session["username"] != username:
        flash("You Shall Not Pass")
        return redirect('/login')

    user = User.query.get_or_404(username)

    form = OnlyCSRFForm()

    return render_template('user.html', user = user, form = form)

@app.post('/logout')
def log_out_user():
    """Log out user in session"""

    form = OnlyCSRFForm() #do we need both here and above?

    if form.validate_on_submit():
        flash("Successfully logged out!")
        session.pop("username", None)

        return redirect("/")

    return redirect(f"/users/{session['username']}")





