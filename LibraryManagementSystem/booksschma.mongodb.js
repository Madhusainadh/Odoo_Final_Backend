
const database = 'LibraryManagementSystem';
const collection = 'books';

// The current database to use.
use(database);

// Create a new collection.
db.createCollection(collection);


db.createCollection("books", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            properties: {
                ISBN: {
                    bsonType: "string",
                    description: "Unique ISBN number for each book"
                },
                Date: { bsonType: "string" },
                Title: { bsonType: "string" },
                Author: { bsonType: "string" },
                Genre: { bsonType: "string" },
                Image: { bsonType: "string" },
                Stock: { bsonType: "int" },
                Price: { bsonType: "double" },
                Book_Sold_Count: { bsonType: "int" }
            },
            required: ["ISBN"],
            uniqueItems: ["ISBN"]
        }
    }
});

