from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]

# EXPECTATION: Use MongoDB transactions for atomic operations (checkout with stock decrement).
# MongoDB transactions require a replica set. See docker-compose.yml for setup.

async def init_db():
    """Initialize database indexes"""
    # Products
    await db.products.create_index([("stock", 1)])
    await db.products.create_index([("name", 1)])
    
    # Orders
    await db.orders.create_index([("userId", 1)])
    await db.orders.create_index([("createdAt", -1)])
    await db.orders.create_index([("idempotencyKey", 1)], unique=True, sparse=True)
    
    # Cart items (TTL index for expiration - bonus)
    await db.cart_items.create_index([("userId", 1)])
    await db.cart_items.create_index([("createdAt", 1)], expireAfterSeconds=86400)  # 24h TTL
    
    print("✓ Database indexes created")

