from flask import request, jsonify, Blueprint
from bson.objectid import ObjectId
from datetime import date, timedelta
from extensions import user_collection, transaction_collection, book_collection, borrow_collection

transaction_api = Blueprint('transactions_api', __name__)

@transaction_api.route('/api/v1/borrow', methods=['GET','POST'])
def borrow():
    if request.method == 'GET':
        user_id = request.args.get("user_id")
        book_id = request.args.get("book_id")
        if user_id:
            # Get all borrowed books of user
            borrows = borrow_collection.find({"user_id": user_id})
            user_borrows = []
            for borrow in borrows:
                borrow["_id"] = str(borrow["_id"])
                user_borrows.append(borrow)
            return jsonify({"message": "User borrowed books", "Borrows": user_borrows, "success":True}), 200
        elif book_id:
            # Get all users who borrowed book
            borrows = borrow_collection.find({"book_id": book_id})
            book_borrows = []
            for borrow in borrows:
                borrow["_id"] = str(borrow["_id"])
                book_borrows.append(borrow)
            return jsonify({"message": "Users who borrowed book", "Borrows": book_borrows, "success":True}), 200
        return jsonify({"error": "Please send either user_id or book_id"})
    elif request.method == 'POST':
        data = request.get_json()
        user_id = data.get("user_id")
        book_id = data.get("book_id")
        return_date = data.get("return_date")
        quantity = data.get("quantity")
        price = data.get("price")
        if not user_id and not book_id and not return_date and not quantity and not price:
            return jsonify({"error": "Missing data"})
        # Check if user and book exists
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        book = book_collection.find_one({"_id": ObjectId(book_id)})
        if not user:
            return jsonify({"error": "User not found"})
        if not book:
            return jsonify({"error": "Book not found"})
        # Check if stock is available
        print(book)
        if int(quantity) > book['Stock']:
            return jsonify({"error": "Stock not available"})
        # Check if user has enough balance
        if int(price) > user['balance']:
            return jsonify({"error": "Insufficient balance"})
        user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": user["balance"] - int(price)}})
        book_collection.update_one({"_id": ObjectId(book_id)}, {"$set": {"Stock": book["Stock"] - int(quantity)}})
        borrow_details = {
            "user_id": user_id,
            "book_id": book_id,
            "buy_date": date.today().strftime("%Y-%m-%d"),
            "return_date": return_date,
            "status": "borrowed",
            "quantity": quantity,
            "price": price
        }
        borrow_id = borrow_collection.insert_one(borrow_details).inserted_id
        borrow_details["_id"] = str(borrow_id)
        return jsonify({"message": "Book borrowed successfully", "Borrow": borrow_details, "success":True}), 201

@transaction_api.route('/api/v1/orders', methods=['GET'])
def orders():
    orders = borrow_collection.find()
    all_orders = []
    for order in orders:
        order["_id"] = str(order["_id"])
        all_orders.append(order)
    return jsonify({"message": "All orders", "Orders": all_orders, "success":True}), 200

@transaction_api.route('/api/v1/return', methods=['POST'])
def return_book():
    user_id = request.args.get("user_id")
    book_id = request.args.get("book_id")
    late_fee = 0
    if not user_id and not book_id:
        return jsonify({"error": "Missing data"})
    borrow = borrow_collection.find_one({"user_id": user_id, "book_id": book_id})
    if not borrow:
        return jsonify({"error": "Book not borrowed by user"})
    if borrow["status"] == "returned":
        return jsonify({"error": "Book already returned"})
    # Update transaction
    return_date = date.today().strftime("%Y-%m-%d")
    expected_date = borrow["return_date"]
    if expected_date > return_date:
        # Late fees : 100Rs per week
        late_fee += 100 * (expected_date - return_date) / 7
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": user["balance"] - late_fee}})
    borrow_collection.update_one({"_id": borrow["_id"]}, {"$set": {"status": "returned"}})
    borrow = borrow_collection.find_one({"_id": borrow["_id"]})
    borrow["_id"] = str(borrow["_id"])
    return jsonify({"message": "Book returned successfully", "Borrow Details":borrow}), 201