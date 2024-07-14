# Library Management System Backend

A backend API server for a Library Management System

## Installation

Clone the github repository

Open a shell window or a cmd window

Navigate to the folder and run

```bash
    pip install -r requirements.txt
```

This will download all the dependancies

To run the server, type

```bash
    python app.py
```

## API Endpoints

All endpoints start with `http://localhost:5000/api/v1`

POST `/login` : Takes a json input like `{"email":<email>, "password":<password>}` or `{"phoneNumber":<phone>, "password":<password>}`. Checks to see if user exists and if their password is correct

GET `/user` : Takes a `user_id` parameter and returns the details of the user

POST `/user` : Takes a json input like `{"name":<name>, "email": <email>, "phoneNumber" <phone>, "password": <password>, "role": <role>}` and creates a user object in the database.

PUT `/user` : Takes a json input like `{"user_id": <user_id>, "name":<name>, "email": <email>, "phoneNumber" <phone>, "password": <password>, "role": <role>}` and updates the specified field of the user associated with `user_id`.

DELETE `/user` : Takes a `user_id` parameter and deletes the user

GET `/users`: Retrieves details of all the users

GET `/book`: Takes a `book_id` parameter and returns the details of the book

POST `/book`: Take a json input like `{"isbn": <isbn>, "stock": <stock>, "price": <price>, "genre": <genre>}` and pings the Google Book api with `isbn` to get more details, then creates a Book object in the database

PUT `/book`: Take a json input like `{"book_id": <book_id>, "isbn": <isbn>, "stock": <stock>, "price": <price>, "genre": <genre>}` and updates the specified field of the book associated with `book_id` or `isbn`.

DELETE `/book`: Takes a `book_id` parameter and deletes the book

GET `/books`: Takes a json input like `{"title": <title>, "author": <author>, "genre": <genre>}` and retrievs all books that match the parameters, if any parameter is not provided then it will be ignored.

GET `/order`: Retrieves all order of a particular user based on `user_id` or all orders for a particular book based on `book_id`

POST `/order`: Takes a json input like `{"user_id": <user_id>, "book_id": <book_id>, "return_date" <return_date>, "price": <price>, "quantity": <quantity>}` and performs a borrow transaction.

GET `/orders`: Retrieves all the orders

POST `/return`: Takes `user_id` and `book_id` as input and performs a return transaction.
