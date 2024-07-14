from flask import Flask, request, jsonify
from extensions import bcrypt, book_collection, user_collection, transaction_collection
import requests
from datetime import date
from bson.objectid import ObjectId

app = Flask(__name__)

bcrypt.init_app(app)

from apis.book import book_api
from apis.user import user_api

app.register_blueprint(book_api)
app.register_blueprint(user_api)

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