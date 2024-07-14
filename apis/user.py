from flask import request, jsonify, Blueprint
from bson.objectid import ObjectId
from extensions import user_collection
from extensions import bcrypt

user_api = Blueprint('users_api', __name__)

@user_api.route('/api/v1/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    if request.method == 'GET':
        # Check whether user_id is sent or not
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing user id"}), 400
        # Get details of user
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        return jsonify({"User": user, "success":True}), 200
    elif request.method == 'POST':
        # Get all details from some form
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phoneNumber")
        #balance = data.get("balance")
        password = data.get("password")
        role = data.get("role")
        # Check if all details are sent
        if name and email and phone and password and role:
            # Check if email and phone are unique
            user = user_collection.find_one({"email": email})
            if user:
                return jsonify({"error": "Email already exists"}), 400
            user = user_collection.find_one({"phoneNumber": phone})
            if user:
                return jsonify({"error": "Phone number already exists"}), 400
            # Create user
            # Should return a user id
            bcrypt_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user_details = {
            "name": name,
            "email": email,
            "phoneNumber": phone,
            #"balance": balance,
            "password": bcrypt_password,
            "role": role
            }
            user_id = user_collection.insert_one(user_details).inserted_id
            user_details["_id"] = str(user_id)
            return jsonify({"User": user_details, "success":True}), 201
        return jsonify({"error": "Missing data"}), 400
    elif request.method == 'PUT':
        # See what details need updating and update them
        data = request.get_json()
        user_id = data.get("user_id")
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phoneNumber")
        balance = data.get("balance")
        password = data.get("password")
        if not user_id:
            return jsonify({"error": "Missing user id"}), 400
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
        if name:
            # Change name
            user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": name}})
        if email:
            # Change email
            user = user_collection.find_one({"email": email})
            if not user: user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"email": email}})
        if phone:
            # Change phone
            user = user_collection.find_one({"phoneNumber": phone})
            if not user: user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"phoneNumber": phone}})
        if balance:
            # Change balance
            user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"balance": balance}})
        if password:
            # Change password
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"password": password}})
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        return jsonify({"message": "Updated successfully", "User": user, "success":True}), 200
    elif request.method == 'DELETE':
        # Delete the user if user_id is present and is valid
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"error": "Missing user id"}), 400
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
        # Delete user
        user_collection.delete_one({"_id": ObjectId(user_id)})
        return jsonify({"message": "Deleted successfully", "success": True}), 200
    
    return jsonify({"error": "Invalid method"})

@user_api.route('/api/v1/users', methods=['GET'])
def users():
    # Get all users
    users = user_collection.find()
    all_users = []
    for user in users:
        user["_id"] = str(user["_id"])
        all_users.append(user)
    return jsonify({"Users":all_users, "success":True}), 200