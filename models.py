"""
this is my models file which will conatin all my database models
"""

from flask import Flask, render_template, request
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from server import app
from flask_login import (
    UserMixin,
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)

# login config stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_form"

db = SQLAlchemy(app)

# class Person(UserMixin, db.Model):
class Person(UserMixin, db.Model):
    """
    this is the model of my users database
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    university = db.Column(db.String(80), nullable=False)
    is_tutor = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        """
        idk just good to have
        """
        return "<User %r>" % self.username
