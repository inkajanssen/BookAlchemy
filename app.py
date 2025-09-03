from flask import Flask,flash, render_template, request, redirect, url_for
from flask.cli import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book
from datetime import datetime
import dotenv

#Initialize Flask app
app = Flask(__name__)
#Secret key for flash
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
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
    order_by = request.args.get('order_by')
    search_keyword = request.args.get('search_keyword')

    query = Book.query
    if search_keyword:
        query = query.filter(Book.book_title.ilike(f"%{search_keyword}%"))

    if order_by == 'author':
        books = query.join(Author).order_by(Author.author_name).all()
    else:
        books = query.order_by(Book.book_title).all()
        order_by = 'title'

    if not books and search_keyword:
        message = f"No book was found with the keyword {search_keyword}"
        return render_template('home.html', message=message, search_keyword= search_keyword)

    return render_template('home.html', books= books,
                           order_by= order_by, search_keyword=search_keyword)


@app.route('/add_author', methods=['GET','POST'])
def add_author():
    """Create a route to add authors"""
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


@app.route('/add_book', methods=['GET','POST'])
def add_book():
    """Create a route to add books"""
    authors = Author.query.order_by(Author.author_name).all()

    if request.method == 'POST':
        book_title = request.form.get('title')
        book_isbn = request.form.get('isbn')
        author_id_str = request.form.get('author_id')
        publication_date_str = request.form.get('publication_date')

        # Convert str to data
        try:
            publication_date = datetime.strptime(publication_date_str,
                                                 '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return "Error: Invalid publication date", 400

        if not author_id_str:
            return "Error: Please select an author", 400
        try:
            author_id = int(author_id_str)
        except ValueError:
            return "Error: Invalid author ID", 400

        # Create book
        new_author = Book(book_isbn = book_isbn ,publication_date=
        publication_date,book_title= book_title,author_id = author_id)

        # add to db
        db.session.add(new_author)
        db.session.commit()
        return f"{book_title} was successfully added to the database!"

    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['Post'])
def delete_book(book_id):

    book_to_delete = Book.query.get(book_id)

    if not book_to_delete:
        flash('Book not found!')
        return redirect(url_for('home'))

    db.session.delete(book_to_delete)
    db.session.commit()

    flash(f"Book {book_to_delete} has sucessfully been deleted")
    return redirect(url_for('home'))


if __name__ == "__main__":
    # Done once to create database, comment out after
    #with app.app_context():
        #db.create_all()

    app.run(host="0.0.0.0", port=5000)
