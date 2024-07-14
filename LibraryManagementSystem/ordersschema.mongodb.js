/* global use, db */
// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

const database = 'LibraryManagementSystem';
const collection = 'orders';

// The current database to use.
use(database);



// Create a new collection.
db.createCollection(collection);

db.createCollection("orders", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            properties: {
                UserId: { bsonType: "string" },
                BookId: { bsonType: "string" },
                BuyDate: {
                    bsonType: "date",
                    format: "date-time"
                },
                ReturnDate: {
                    bsonType: "date",
                    format: "date-time"
                },
                Price: { bsonType: "double" }
            },
            required: ["UserId", "BookId", "BuyDate", "Price"],
            uniqueItems: ["UserId", "BookId"]
        }
    }
});
