from flask import request, jsonify, Blueprint
import requests
from datetime import date
from extensions import book_collection
from bson.objectid import ObjectId

book_api = Blueprint('books_api', __name__)

@book_api.route('/api/v1/book', methods=['GET','POST', 'PUT', 'DELETE'])
def book():
    if request.method == 'GET':
        book_id = request.args.get("book_id")
        if not book_id:
            return jsonify({"error": "Missing Book ID"})
        # Get details of book
        book = book_collection.find_one({"_id": ObjectId(book_id)})
        book["_id"] = str(book["_id"])
        return jsonify({"Book": book, "success":True}), 200
    elif request.method == 'POST':
        isbn = request.args.get("isbn")
        stock = request.args.get("stock") or 100
        price = request.args.get("price") or 300
        genre = request.args.get("genre")
        if isbn and genre:
            # Check if book already exists
            # If it does change stock and price
            r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}').json()
            if r['totalItems'] == 0:
                return jsonify({"error": "No books found"})
            title = r['items'][0]['volumeInfo']['title']
            author = r['items'][0]['volumeInfo']['authors']
            published_date = r['items'][0]['volumeInfo']['publishedDate']
            image = r['items'][0]['volumeInfo']['imageLinks']['thumbnail']
            added_date = date.today()
            added_date = added_date.strftime("%Y-%m-%d")
            book_details = {
                "isbn": isbn,
                "title": title,
                "authors": author,
                "published_date": published_date,
                "stock": stock,
                "price": price,
                "genre": genre,
                "image": image,
                "added_date": added_date
            }
            book_id = book_collection.insert_one(book_details).inserted_id
            book_details["_id"] = str(book_id)
            return book_details, 201
        return jsonify({"error": "Missing data"})
    elif request.method == 'PUT':
        book_id = request.args.get("book_id")
        isbn = request.args.get("isbn")
        stock = request.args.get("stock")
        price = request.args.get("price")
        genre = request.args.get("genre")
        if not book_id:
            return jsonify({"error": "Missing Book ID"})
        book = book_collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return jsonify({"error": "Book not found"})
        if stock:
            # Increment or decrement stock
            book_collection.update_one({"_id": ObjectId(book_id)}, {"$set": {"stock": stock}})
        if price:
            # Change price
            book_collection.update_one({"_id": ObjectId(book_id)}, {"$set": {"price": price}})
        if genre:
            # Change genre
            book_collection.update_one({"_id": ObjectId(book_id)}, {"$set": {"genre": genre}})
        book = book_collection.find_one({"_id": ObjectId(book_id)})
        book["_id"] = str(book["_id"])
        return jsonify({"message": "Updated successfully", "Book": book, "success":True}), 200
    elif request.method == 'DELETE':
        book_id = request.args.get("book_id")
        if not book_id:
            return jsonify({"error": "Missing Book ID"})
        # Delete book
        book = book_collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return jsonify({"error": "Book not found"})
        book_collection.delete_one({"_id": ObjectId(book_id)})
        return jsonify({"message": "Deleted successfully", "success":True}), 200
    
    return jsonify({"error": "Invalid method"})

@book_api.route('/api/v1/books', methods=['GET'])
def books():
    title = request.args.get("title")
    author = request.args.get("author")
    genre = request.args.get("genre")
    # Get all books
    find = {"title": title, "authors": author, "genre": genre}
    for key in list(find.keys()):
        if not find[key]:
            del find[key]
    books = book_collection.find(find)
    all_books = []
    for book in books:
        book["_id"] = str(book["_id"])
        all_books.append(book)
    return jsonify({"Books": all_books, "success": True}), 200