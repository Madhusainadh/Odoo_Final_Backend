const database = 'LibraryManagementSystem';
const collection = 'books';

// The current database to use.
use(database);

// Create 300 unique books
for (let i = 1; i <= 300; i++) {
    const authors = ['Author A', 'Author B', 'Author C']; // Add more authors as needed
    const randomAuthorIndex = Math.floor(Math.random() * authors.length);
    const randomStock = Math.floor(Math.random() * 50) + 1; // Random stock between 1 and 50

    db.getCollection('books').insertOne({
        ISBN: `9781234567${i}`, // Unique ISBN
        Date: new Date(), // Set publication date as needed
        Title: `Book Title ${i}`,
        Author: [authors[randomAuthorIndex]], // Single random author
        Genre: 'Fiction', // Set genre
        Image: `https://example.com/book${i}-cover.jpg`, // URL to book cover image
        Stock: randomStock,
        Price: Math.random() * 50 + 10, // Random price between 10 and 60
        'Books sold count': 0
    });
}
