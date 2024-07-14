/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'LibraryManagementSystem';
const collection = 'users';

// The current database to use.
use(database);

// Create a new collection.
db.createCollection(collection);

// Create the 'users' collection and define the schema 
 db.createCollection('users', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['name', 'email', 'password'],
            properties: {
                name: { bsonType: 'string' },
                email: { bsonType: 'string',unique: true},
                phoneNumber: { bsonType: 'string',unique: true },
                password: { bsonType: 'string' },
                role: { bsonType: 'string' },
                balance: { bsonType: 'double', minimum: 0 },
            },
        },
    },
});



print('Users collection schema created successfully!');