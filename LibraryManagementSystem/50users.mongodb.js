/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'LibraryManagementSystem';
const collection = 'users';

// The current database to use.
use(database);

// Create 50 unique users
for (let i = 51; i <= 100; i++) {
    db.getCollection('users').insertOne({
        name: `User${i}`,
        email: `user${i}@example.com`,
        phoneNumber: `+91${Math.floor(Math.random() * 9000000000) + 1000000000}`,
        password: `password${i}`,
        role: "User",
        balance: Math.floor(Math.random() * 1000) + 1
    });
}


