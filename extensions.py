from flask_bcrypt import Bcrypt
from pymongo import MongoClient

bcrypt = Bcrypt()

client = MongoClient('mongodb+srv://nagamohan419:9eTO6BFXFhfTgKfh@cluster0.t6axvvf.mongodb.net/')
db = client['LibraryManagementSystem']
book_collection = db["books"]
user_collection = db["users"]
transaction_collection = db["transactions"]