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
    username = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    university = db.Column(db.String(120), unique=False, nullable=False)
    is_tutor = db.Column(db.Boolean, default=False, nullable=False)
    tutored_classes = db.relationship("Tutor")

    def __repr__(self):
        """
        idk just good to have
        """
        return "<User %r>" % self.username


class Post(db.Model):
    """
    this is the model of my post database
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    course = db.Column(db.String(120), unique=False, nullable=False)
    contact_method = db.Column(db.String(120), unique=False, nullable=False)
    university = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        """
        idk just good to have
        """
        return "<User %r>" % self.username


class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    course_id = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(120), nullable=False)


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
def welcome_page():
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
    return redirect(url_for("login"))


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

    for i in Person.query.filter_by(username=current_user.username):
        username = i.username
        email = i.email
        password = i.password
        university = i.university

    return render_template(
        "account_settings.html",
        name=username,
        email=email,
        password=password,
        university=university,
    )


@app.route("/find_a_friend", methods=["POST", "GET"])
@login_required
def find_a_friend():
    """
    this is the page allows users to find tutors
    """
    subjects = []
    names = []
    contacts = []
    schools = []

    if request.method == "POST":

        course = request.form.get("subject")

        for i in Post.query.filter_by(course=course):
            subjects.append(i.course)
            names.append(i.name)
            contacts.append(i.contact_method)
            schools.append(i.university)

        size = len(subjects)

        return render_template(
            "find_a_friend.html",
            subjects=subjects,
            names=names,
            contacts=contacts,
            size=size,
            schools=schools,
        )

    return render_template(
        "find_a_friend.html",
        subjects=subjects,
        names=names,
        contacts=contacts,
        schools=schools,
    )


@app.route("/become_a_friend", methods=["POST", "GET"])
@login_required
def become_a_friend():
    """
    this is the page allows users to become tutors
    """

    if request.method == "POST":
        subject = request.form.get("subject")
        name = request.form.get("name")
        contact = request.form.get("contact")

        new_post = Post(
            name=name,
            course=subject,
            contact_method=contact,
            university=current_user.university,
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("find_a_friend"))

    return render_template("become_a_friend.html")


@app.route("/manage_listings", methods=["POST", "GET"])
@login_required
def manage_listings():
    """
    this is the page allows tutors to manage listings
    """

    return render_template("manage_listings.html")


if __name__ == "__main__":
    """
    this
    this is the 'main function' which runs our app
    """

    app.run(debug=True)
