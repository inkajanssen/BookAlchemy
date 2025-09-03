from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book
from datetime import datetime

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

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Create a route to get all books and add books"""
    if request.method == 'POST':
        author_name = request.form.get('name')
        birth_date_str = request.form.get('birthdate')
        date_of_death_str = request.form.get('date_of_death')

        # Convert str to date
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        date_of_death = None
        if date_of_death_str:
            date_of_death = datetime.strptime(date_of_death_str,'%Y-%m-%d').date()

        new_author = Author(author_name=author_name, birth_date=birth_date,
                            date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        return f"{author_name} was added successfully to the database!"
    return render_template('add_author.html')


if __name__ == "__main__":
    # Done once to create database, comment out after
    #with app.app_context():
        #db.create_all()

    app.run(host="0.0.0.0", port=5000)
