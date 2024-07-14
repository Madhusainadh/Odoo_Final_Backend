// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('LibraryManagementSystem');




// Create 200 orders
const bookIds = []; // Assume you have an array of book IDs (populate this as needed)

function getRandomDate(startDate, endDate) {
    const startTimestamp = startDate.getTime();
    const endTimestamp = endDate.getTime();
    const randomTimestamp = Math.random() * (endTimestamp - startTimestamp) + startTimestamp;
    return new Date(randomTimestamp);
}

const startDate = new Date('2023-01-01');
const endDate = new Date('2024-07-13');

for (let i = 1; i <= 200; i++) {
    const randomUserId = Math.floor(Math.random() * 50) + 1; // Random user ID
    const randomBookId = bookIds[Math.floor(Math.random() * bookIds.length)]; // Random book ID
    const randomBuyDate = getRandomDate(startDate, endDate); // Random buy date
    const randomReturnDate = getRandomDate(randomBuyDate, endDate); // Random return date
    const randomPrice = Math.random() * 50 + 10; // Random price between 10 and 60

    db.getCollection('orders').insertOne({
        UserId: randomUserId,
        BookId: randomBookId,
        BuyDate: randomBuyDate,
        ReturnDate: randomReturnDate,
        Price: randomPrice
    });
}
