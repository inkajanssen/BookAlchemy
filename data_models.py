from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String(255), nullable= False)
    birth_date = Column(Date, nullable= False)
    date_of_death = Column(Date, nullable= True)

    def __str__(self):
        if self.date_of_death:
            return f"Name: {self.author_name}, Birthdate: {self.birth_date}, Deathdate: {self.date_of_death}"
        else:
            return f"Name: {self.author_name}, Birthdate: {self.birth_date}"

    def __repr__(self):
        return (f"Author(author_name='{self.author_name}', birth_date='"
                f"{self.birth_date}', date_of_death='{self.date_of_death}',"
                f"author_id={self.author_id})")


class Book(db.Model):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(VARCHAR, nullable=False, unique=True)
    publication_date = Column(Date, nullable=True)
    book_title = Column(String(255), nullable= False)
    author_id = Column(Integer, ForeignKey('authors.author_id'))

    author = relationship("Author", backref="BOOKS")

    def __str__(self):
        return (f"Name: {self.book_title}, ISBN: {self.book_isbn}, Publication Date:"
                f" {self.publication_date}")


    def __repr__(self):
        return (f"Book(book_title='{self.book_title}', publication_date='"
                f"{self.publication_date}', book_isbn='{self.book_isbn}',"
                f"author_id={self.author_id}), book_id={self.book_id}")

