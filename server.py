"""
this is our server file with all our routes and config stuff
"""

from flask import Flask, render_template, request
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from models import db, Person
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
login_manager.login_view = "login_form"

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

    return render_template("index.html")


@app.route("/login_form", methods=["POST", "GET"])
def login_form():
    """
    this is our form for logging in
    """

    return render_template("login_form.html")


@login_required
@app.route("/dashboard", methods=["POST", "GET"])
def dasshboard():
    """
    this is the page that makes our dashboard
    """

    return render_template("dashboard.html")


if __name__ == "__main__":
    """
    this is the 'main function' which runs our app
    """

    app.run(debug=True)
