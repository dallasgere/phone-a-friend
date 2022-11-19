"""
this is our server file with all our routes and config stuff
"""

from flask import Flask, render_template
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    '''
    this will be our home page for our project
    '''

    return render_template('index.html')

if __name__ == '__main__':
    '''
    this is the 'main function' which runs our app
    '''

    app.run(debug=True)