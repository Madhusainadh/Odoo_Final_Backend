from flask import request, jsonify, Blueprint
from bson.objectid import ObjectId
from datetime import date, timedelta
from extensions import user_collection, transaction_collection, book_collection, borrow_collection

transaction_api = Blueprint('transactions_api', __name__)

@transaction_api.route('/api/v1/transaction', methods=['GET','POST'])
def transaction():
    if request.method == 'GET':
        user_id = request.args.get("user_id")
        # Get all transactions of user
        transactions = transaction_collection.find({"user_id": user_id})
        for transaction in transactions:
            transaction["_id"] = str(transaction["_id"])
        return jsonify({"message": "User transactions", "Transactions": transactions, "success":True}), 200
    elif request.method == 'POST':
        user_id = request.args.get("user_id")
        book_ids = request.args.get("book_ids")
        quantities = request.args.get("quantities")
        if not user_id or book_ids or quantities:
            return jsonify({"error": "Missing data"})
        result = {"book_not_found":[], "stock_not_available":[], "insufficient_balance":[], "borrowed_books":[]}
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"})
        for i in range(len(book_ids)):
            book = book_collection.find_one({"isbn": book_ids[i]})
            # Check if book exists
            if not book:
                result["book_not_found"].append(book_ids[i])
                continue
            # Check if stock is available
            if book['stock'] < quantities[i]:
                result["stock_not_available"].append(book_ids[i])
                continue
            # Check if user has enough balance
            if user['balance'] < book['price']:
                result["insufficient_balance"].append(book_ids[i])
                continue
            # Create transaction
            borrow_details = {
                "user_id": str(user["_id"]),
                "book_id": str(book['_id']),
                "quantity": quantities[i],
                "buy_date": date.today().strftime("%Y-%m-%d"),
                "return_date": None
            }
            user["balance"] -= book['price'] * quantities[i]
            result["borrowed_books"].append(borrow_details)
            '''transaction_details = {
                "user_id": str(user["_id"]),
                "quantity": quantities[i],
                "total": book['price'] * quantities[i],
                "remaining_balance": user["balance"]
            }'''
        return jsonify({"message": "Transaction successful", "Details": result}), 201
        
    return jsonify({"error": "Invalid method"})

@transaction_api.route('/api/v1/return', methods=['POST'])
def return_book():
    user_id = request.args.get("user_id")
    book_id = request.args.get("book_id")
    late_fee = 0
    if user_id and book_id:
        # Check if book is borrowed by user
        borrow = borrow_collection.find_one({"user_id": user_id, "book_id": book_id})
        if not borrow:
            return jsonify({"error": "Book not borrowed by user"})
        # Update transaction
        return_date = borrow["return_date"]
        if not return_date:
            return jsonify({"error": "Book already returned"})
        issue_date = borrow["buy_date"]
        return_date = date.today().strftime("%Y-%m-%d")
        if return_date > issue_date + timedelta(days=30):
            late_fee += 100 * (return_date - issue_date) / 7
        return jsonify({"message": "Book returned successfully", "Late Fee Charged":late_fee}), 201
    return jsonify({"error": "Missing data"})