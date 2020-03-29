# app>catalog>routes.py
from app import db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.book import book
from app.book.models import Book, Publication
from app.book.forms import EditBookForm, CreateBookForm

# Use a default value
@book.route('/book')
def display_books():
    books = Book.query.all()
    return render_template('book.html', books=books)

@book.route("/publisher/<publisher_id>")
def display_publisher(publisher_id):
    publisher = Publication.query.filter_by(id=publisher_id).first()
    publisher_books = Book.query.filter_by(pub_id=publisher_id).all()
    return render_template('publisher.html', publisher=publisher, publisher_books=publisher_books)

@book.route('/book/delete/<book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if request.method=='POST':
        db.session.delete(book)
        db.session.commit()
        flash("Book delete successfully")
        return redirect(url_for('book.display_books'))
    return render_template('delete_book.html', book=book)

@book.route('/book/edit/<book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get(book_id)
    form = EditBookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.format = form.format.data
        book.num_pages = form.num_pages.data
        db.session.add(book)
        db.session.commit()
        flash('Book edited successfully!')
        return(redirect(url_for('book.display_books')))
    return render_template('edit_book.html', form=form)

@book.route('/book/create/<pub_id>', methods=['GET', 'POST'])
@login_required
def create_book(pub_id):
    form = CreateBookForm()
    form.pub_id.data = pub_id

    if form.validate_on_submit():
        book = Book(title = form.title.data, author=form.author.data, avg_rating=form.avg_rating.data, book_format=form.format.data, image=form.img_url.data, num_pages=form.num_pages.data, pub_id=form.pub_id.data)

        db.session.add(book)
        db.session.commit()

        flash('Book added successfully!')

        return(redirect(url_for('book.display_publisher', publisher_id=pub_id)))
    return render_template('create_book.html', form=form, pub_id=pub_id)