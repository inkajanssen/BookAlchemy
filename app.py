from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book

#Initialize Flask app
app = Flask(__name__)
#Define base dir for app and URI
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir,
                                                    'data/library.sqlite')}"
# Initialize database with Flask
db.init_app(app)


@app.route('/', methods=['GET'])
def home():
    """
    Renders home page of app
    """
    return render_template('home.html')


if __name__ == "__main__":
    # Done once to create database, comment out after
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000)
