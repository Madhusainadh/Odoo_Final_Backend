from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from datetime import date
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
# Replace string with cluster connection string
client = MongoClient('mongodb+srv://nagamohan419:9eTO6BFXFhfTgKfh@cluster0.t6axvvf.mongodb.net/')
# Replace with database name
db = client['LibraryManagementSystem']
user_collection = db["users"]
book_collection = None
transaction_collection = None
#borrowed_collection = db['borrowed']

bcrypt = Bcrypt(app)

@app.route('/api/v1/login', methods=['POST'])
def login():
    email = request.args.get("email")
    phone = request.args.get("phoneNumber")
    password = request.args.get("password")
    if (not email and not phone) or not password:
        return jsonify({"error": "Missing email or password"}), 400
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    # Check if user exists
    # Check if password is correct
    if email:
        user = user_collection.find_one({"email": email, "password": hashed_password})
    else:
        user = user_collection.find_one({"phoneNumber": phone, "password": hashed_password})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 400
    # Return user details
    return jsonify({"message": "Logged in successfully", "success": True}), 200

@app.route('/api/v1/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    if request.method == 'GET':
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing user id"})
        # Get details of user
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        return jsonify({"User": user, "success":True}), 200
    elif request.method == 'POST':
        name = request.args.get("name")
        email = request.args.get("email")
        phone = request.args.get("phoneNumber")
        balance = request.args.get("balance")
        password = request.args.get("password")
        role = request.args.get("role")
        if name and email and phone and balance and password and role:
            # Check if email and phone are unique
            # Create user
            # Should return a user id
            bcrypt_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user_details = {
            "name": name,
            "email": email,
            "phoneNumber": phone,
            "balance": balance,
            "password": bcrypt_password,
            "role": role
            }
            user_id = user_collection.insert_one(user_details).inserted_id
            user_details["user_id"] = str(user_id)
            return jsonify({"User": user_details, "success":True}), 201
        return jsonify({"error": "Missing data"})
    elif request.method == 'PUT':
        user_id = request.args.get("user_id")
        name = request.args.get("name")
        email = request.args.get("email")
        phone = request.args.get("phone")
        balance = request.args.get("balance")
        password = request.args.get("password")
        if not user_id:
            return jsonify({"error": "Missing user id"})
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"})
        if name:
            # Change name
            user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": name}})
        if email:
            # Change email
            user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"email": email}})
        if phone:
            # Change phone
            user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"phoneNumber": phone}})
        if balance:
            # Change address
            user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": balance}})
        if password:
            # Change password
            user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"password": password}})
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        return jsonify({"message": "Updated successfully", "User": user, "success":True}), 200
    elif request.method == 'DELETE':
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing user id"})
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"})
        # Delete user
        user_collection.delete_one({"_id": ObjectId(user_id)})
        return jsonify({"message": "Deleted successfully", "success": True}), 200
    
    return jsonify({"error": "Invalid method"})

@app.route('/api/v1/users', methods=['GET'])
def users():
    # Get all users
    users = user_collection.find()
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify({"Users":users, "success":True}), 200

@app.route('/api/v1/book', methods=['GET','POST', 'PUT', 'DELETE'])
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
        return jsonify({"message": "Updated successfully", "book_id": book_id, "success":True}), 200
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

@app.route('/api/v1/books', methods=['GET'])
def books():
    author = request.args.get("author")
    genre = request.args.get("genre")
    # Get all books
    if author and genre:
        # Get books by author and genre
        books = book_collection.find({"authors": author, "genre": genre})
    elif author:
        # Get books by author
        books = book_collection.find({"authors": author})
    elif genre:
        # Get books by genre
        books = book_collection.find({"genre": genre})
    else:
        books = book_collection.find()
        
    for book in books:
        book["_id"] = str(book["_id"])
    return jsonify({"message": "All books"}), 200

@app.route('/api/v1/transaction', methods=['GET','POST'])
def transaction():
    if request.method == 'GET':
        user_id = request.args.get("user_id")
        # Get all transactions of user
        transactions = transaction_collection.find({"user_id": user_id})
        return jsonify({"message": "User transactions"})
    elif request.method == 'POST':
        user_id = request.args.get("user_id")
        isbns = request.args.get("isbn")
        quantities = request.args.get("quantity")
        if not user_id or isbns or quantities:
            return jsonify({"error": "Missing data"})
        result = {"book_not_found":[], "stock_not_available":[], "insufficient_balance":[]}
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"})
        for i in range(len(isbns)):
            book = book_collection.find_one({"isbn": isbns[i]})
            # Check if book exists
            if not book:
                result["book_not_found"].append(isbns[i])
                continue
            # Check if stock is available
            if book['stock'] < quantities[i]:
                result["stock_not_available"].append(isbns[i])
                continue
            # Check if user has enough balance
            if user['balance'] < book['price']:
                result["insufficient_balance"].append(isbns[i])
                continue
            # Create transaction
            borrow_details = {
                "user_id": user["_id"],
                "book_id": book['_id'],
                "quantity": quantities[i],
                "buy_date": date.today().strftime("%Y-%m-%d")
            }
            user["balance"] -= book['price'] * quantities[i]
            transaction_details = {
                "user_id": user["_id"],
                "quantity": quantities[i],
                "total": book['price'] * quantities[i],
                "remaining_balance": user["balance"]
            }
        return jsonify({"message": "Transaction successful"}), 201
        
    return jsonify({"error": "Invalid method"})

@app.route('/api/v1/return', methods=['POST'])
def return_book():
    user_id = request.args.get("user_id")
    isbn = request.args.get("isbn")
    if user_id and isbn:
        # Check if book is borrowed by user
        # Update transaction
        return jsonify({"message": "Book returned successfully"}), 201
    return jsonify({"error": "Missing data"})

if __name__ == '__main__':
    app.run()