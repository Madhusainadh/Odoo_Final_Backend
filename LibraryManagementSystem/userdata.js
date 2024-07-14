// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('LibraryManagementSystem');

// Create a new document in the collection.
db.getCollection('users').insertOne(
    {name: "NagaMohan", 
     email: "nagamohan419@gmail.com",
     phoneNumber:"+919959761957",
     password:"nagamohan#421",
     role:"Admin",
     balance:1000

});


db.users.updateOne( { name: "NagaMohan" }, { $set: { email: 'NagaMohanBurugupalli@Nagamohan.onmicrosoft.com' } } ) 


// Create 50 unique users
for (let i = 1; i <= 50; i++) {
    db.getCollection('users').insertOne({
        name: `User${i}`,
        email: `user${i}@example.com`,
        phoneNumber: `+91${Math.floor(Math.random() * 9000000000) + 1000000000}`,
        password: `password${i}`,
        role: "User",
        balance: Math.floor(Math.random() * 1000) + 1
    });
}
