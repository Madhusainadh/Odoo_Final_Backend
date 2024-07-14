from flask import Flask, request, jsonify
from extensions import bcrypt, user_collection
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bcrypt.init_app(app)

from apis.book import book_api
from apis.user import user_api
from apis.transactions import transaction_api

app.register_blueprint(book_api)
app.register_blueprint(user_api)
app.register_blueprint(transaction_api)

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
    user["_id"] = str(user["_id"])
    return jsonify({"message": "Logged in successfully", "User":user, "success": True}), 200

if __name__ == '__main__':
    app.run()