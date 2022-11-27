"""
this is our server file with all our routes and config stuff
"""

from flask import Flask, render_template, request, flash, url_for, redirect
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    UserMixin,
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["TESTING"] = False

# login config stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# initializing the db instance
db = SQLAlchemy(app)

# class Person(UserMixin, db.Model):
class Person(UserMixin, db.Model):
    """
    this is the model of my users database
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    university = db.Column(db.String(80), nullable=False)
    is_tutor = db.Column(db.Boolean, default=False, nullable=False)
    tutored_classes = db.relationship("Tutor")

    def __repr__(self):
        """
        idk just good to have
        """
        return "<User %r>" % self.username


class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    course_id = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(80), nullable=False)


with app.app_context():
    """
    this creates my database models if they havent been made yet
    """
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """
    returns the object of the user id turned in
    """

    return Person.query.get(int(user_id))


@app.before_first_request
def init_app():
    """
    making sure user is logged out just in case of cookies
    """

    logout_user()


@app.route("/")
def index():
    """
    this will be our home page for our project
    """

    return render_template("index2.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    this is our form for logging in
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        person = Person.query.filter_by(username=username).first()
        if person:
            if check_password_hash(person.password, password):
                print("loged in")
                login_user(person, remember=True)
                return redirect(url_for("dashboard"))
            else:
                print("wrong password!")
                # Read about bootstrap flash

    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """
    Logs user out and redirects to login page
    """
    logout_user()
    return redirect(url_for("log_in"))


@app.route("/sign-up", methods=["POST", "GET"])
def signup():
    """
    this is our form for sign-up
    """
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("user_email")
        university = request.form.get("university")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if password != password2:
            flash("Password does not match.", category="error")
        # add elif to check if username exist
        # Read about bootstrap flash
        else:
            new_user = Person(
                username=username,
                email=email,
                university=university,
                password=generate_password_hash(password, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))

    return render_template("sign-up.html")


@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    """
    this is the page that makes our dashboard
    """

    return render_template("dashboard.html")

@app.route("/account_settings", methods=["POST", "GET"])
@login_required
def account_settings():
    """
    this is the page that makes the users account settings
    """

    return render_template("account_settings.html")

@app.route("/find_a_friend", methods=["POST", "GET"])
@login_required
def find_a_friend():
    """
    this is the page allows users to find tutors
    """

    return render_template("find_a_friend.html")

if __name__ == "__main__":
    """
    this is the 'main function' which runs our app
    """

    app.run(debug=True)
