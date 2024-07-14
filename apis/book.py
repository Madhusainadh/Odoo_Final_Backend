from flask import request, jsonify, Blueprint
import requests
from datetime import date
from extensions import book_collection
from bson.objectid import ObjectId

book_api = Blueprint('books_api', __name__)

@book_api.route('/api/v1/book', methods=['GET','POST', 'PUT', 'DELETE'])
def book():
    if request.method == 'GET':
        # Check whether book_id is sent or not
        book_id = request.args.get("book_id")
        if not book_id:
            return jsonify({"error": "Missing Book ID"}), 400
        # Get details of book
        book = book_collection.find_one({"_id": ObjectId(book_id)})
        book["_id"] = str(book["_id"])
        return jsonify({"Book": book, "success":True}), 200
    elif request.method == 'POST':
        # Get all details from some form
        data = request.get_json()
        isbn = data.get("isbn")
        stock = data.get("stock")
        price = data.get("price")
        genre = data.get("genre")
        # Check if book already exists
        book = book_collection.find_one({"isbn": isbn})
        if book:
            return jsonify({"error": "Book already exists"}), 400
        # Check if all details are sent
        if isbn and genre and stock and price:
            # Use google books api to get book details
            r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}').json()
            if r['totalItems'] == 0:
                return jsonify({"error": "No books found"}), 404
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
        return jsonify({"error": "Missing data"}), 400
    elif request.method == 'PUT':
        # Update any details of book
        data = request.get_json()
        book_id = data.get("book_id")
        isbn = data.get("isbn")
        stock = data.get("stock")
        price = data.get("price")
        genre = data.get("genre")
        if not book_id:
            return jsonify({"error": "Missing Book ID"}), 400
        book = book_collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return jsonify({"error": "Book not found"}), 404
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
        # Delete book if book_id is present and is valid
        book_id = request.args.get("book_id")
        if not book_id:
            return jsonify({"error": "Missing Book ID"}), 400
        book = book_collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return jsonify({"error": "Book not found"}), 404
        book_collection.delete_one({"_id": ObjectId(book_id)})
        return jsonify({"message": "Deleted successfully", "success":True}), 200
    
    return jsonify({"error": "Invalid method"}), 400

@book_api.route('/api/v1/books', methods=['POST'])
def books():
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    genre = data.get("genre")
    # Get all books based on search parameters
    find = {"title": title, "authors": author, "genre": genre}
    for key in list(find.keys()):
        if not find[key]:
            del find[key]
    if len(find.keys()) == 0:
        books = book_collection.find()
    else:
        books = book_collection.find(find)
    all_books = []
    for book in books:
        book["_id"] = str(book["_id"])
        all_books.append(book)
    print(all_books)
    return jsonify({"Books": all_books, "success": True}), 200