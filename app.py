from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
from forms import SignUpForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'euhtnidhe4536789uidjthudne'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
connect_db(app)
db.create_all()

@app.get('/')
def root():
    """render homepage"""
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

        return redirect('/secret')

    return render_template("signup.html", form = form)

# @app.post('/register')
# @app.get('/login')
# @app.post('/login')
# @app.get('/secret')




