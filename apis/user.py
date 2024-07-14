from flask import request, jsonify, Blueprint
from bson.objectid import ObjectId
from extensions import user_collection
from extensions import bcrypt

user_api = Blueprint('users_api', __name__)

@user_api.route('/api/v1/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
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
            user = user_collection.find_one({"email": email})
            if user:
                return jsonify({"error": "Email already exists"})
            user = user_collection.find_one({"phoneNumber": phone})
            if user:
                return jsonify({"error": "Phone number already exists"})
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

@user_api.route('/api/v1/users', methods=['GET'])
def users():
    # Get all users
    users = user_collection.find()
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify({"Users":users, "success":True}), 200