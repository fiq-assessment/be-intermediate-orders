"""Seed script to populate database with sample products"""
import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URI = "mongodb://localhost:27017/?replicaSet=rs0"
DB_NAME = "interview_db"

PRODUCTS = [
    ("Laptop", "High-performance laptop for work and gaming", 129999, 10),
    ("Keyboard", "Mechanical keyboard with RGB lighting", 12999, 25),
    ("Mouse", "Wireless gaming mouse", 7999, 30),
    ("Monitor", "27-inch 4K monitor", 39999, 8),
    ("Headphones", "Noise-cancelling wireless headphones", 24999, 15),
    ("Webcam", "1080p webcam for video calls", 8999, 20),
    ("USB Hub", "7-port USB 3.0 hub", 2999, 50),
    ("Desk Lamp", "LED desk lamp with adjustable brightness", 4999, 35),
]

async def seed_data():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    
    # Clear existing data
    await db.products.delete_many({})
    await db.cart_items.delete_many({})
    await db.orders.delete_many({})
    
    # Insert sample products
    products = []
    for name, desc, price, stock in PRODUCTS:
        products.append({
            "name": name,
            "description": desc,
            "priceCents": price,
            "stock": stock,
            "category": "Electronics",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        })
    
    result = await db.products.insert_many(products)
    print(f"✓ Inserted {len(result.inserted_ids)} products")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_data())

