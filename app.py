from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db, Note
from forms import SignUpForm, LoginForm, OnlyCSRFForm, NoteForm

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
    form = OnlyCSRFForm() #QUESTION:do we need both here and above?
    notes = user.notes

    return render_template('user.html', user = user, form = form, notes = notes)

@app.post('/logout')
def log_out_user():
    """Log out user in session"""

    form = OnlyCSRFForm() #QUESTION:do we need both here and above?

    if form.validate_on_submit():
        flash("Successfully logged out!")
        session.pop("username", None)

        return redirect("/")

    return redirect(f"/users/{session['username']}")

@app.post('/users/<username>/delete')
def delete_user(username):
    """delete all of a users posts and delete the user"""

    if "username" not in session or session["username"] != username:
        flash("You Shall Not Pass")
        return redirect('/login')

    user = User.query.get_or_404(username)
    notes = user.notes
    form = OnlyCSRFForm() 


    if form.validate_on_submit():
        flash("User Deleted!")
        for note in notes:
            db.session.delete(note) #QUESTION: there is an SQLalchemy method for this right?
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        session.pop("username", None)
    
    return redirect("/")





###############################################################################
# Notes Routes

@app.route('/users/<username>/notes/add', methods=["GET","POST"])
def display_note_form_or_add_note(username):
    """GET: Display a form to add notes.
       POST: Add a new note and redirect to /users/<username>"""

    if "username" not in session or session["username"] != username:
        flash("You Shall Not Pass")
        return redirect('/login')


    form = NoteForm()

    if not form.validate_on_submit():
        return render_template("newnote.html", form = form)

    title = form.title.data
    content = form.content.data

    note = Note(title=title, content=content, owner=username)
    db.session.add(note)
    db.session.commit()

    flash(f"{note.title} successfully created.")

    return redirect(f'/users/{username}')

@app.route('/notes/<int:note_id>/update', methods=["GET","POST"])
def edit_note(note_id):
    """Edit a note"""

    note = Note.query.get_or_404(note_id)
    user = note.user

    if "username" not in session or session["username"] != user.username:
        flash("You Shall Not Pass")
        return redirect('/login')

    form = NoteForm(obj=note)

    if not form.validate_on_submit():
        return render_template("updatenote.html", form = form)

    note.title = form.title.data
    note.content = form.content.data

    db.session.commit()

    flash(f"{note.title} successfully edited.")

    return redirect(f'/users/{user.username}')

@app.post('/notes/<int:note_id>/delete')
def delete_note(note_id):
    """delete a note"""

    note = Note.query.get_or_404(note_id)
    user = note.user
    form = OnlyCSRFForm() 

    if "username" not in session or session["username"] != user.username:
        flash("You Shall Not Pass")
        return redirect('/login')

    if form.validate_on_submit():
        flash("Note Deleted!")
        db.session.delete(note)
        db.session.commit()
    
    return redirect(f"/users/{session['username']}")

    