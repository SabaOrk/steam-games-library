from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_user, logout_user
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'secret_key_8rh9238-h892brb2398rb29brc2'
login_manager = LoginManager()
login_manager.init_app(app)

"""
MODELS
"""


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)


# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    release = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Title {self.title}>'


"""
VIEWS
"""


@app.route('/')
def index():
    games = Game.query.all()
    return render_template('index.html', games=games)


@app.route('/game/<int:id>')
def game(id):
    game = Game.query.get(id)
    return render_template('game.html', game=game)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    # If the user made a POST request, create a new user
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    # Renders sign_up template if user made a GET request
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by
    # filtering for the username
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the
        # same as the user's password
        if user is not None:
            if user.password == request.form.get("password"):
                # Use the login_user method to log in the user
                login_user(user)
                flash('You were successfully logged in')
                return redirect(url_for("index"))

        flash('Invalid username or password')
        # Redirect the user back to the home
        # (we'll create the home route in a moment)
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == '__main__':
    db.create_all()
    app.run()
