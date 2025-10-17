from fastapi import APIRouter, HTTPException, Header
from ..core.db import db, client
from ..models.order import OrderOut
from bson import ObjectId
from datetime import datetime
import base64

router = APIRouter(prefix="/orders", tags=["orders"])

# EXPECTATION:
# - Implement cursor-based pagination.
# - Sort by createdAt desc by default.
# - Return order items with product details.

@router.get("")
async def list_orders(
    x_user_id: str = Header(...),
    cursor: str | None = None,
    limit: int = 20
):
    """List user orders with cursor pagination"""
    query = {"userId": x_user_id}
    
    # Decode cursor
    if cursor:
        try:
            cursor_data = base64.b64decode(cursor).decode('utf-8')
            last_created_at = datetime.fromisoformat(cursor_data)
            query["createdAt"] = {"$lt": last_created_at}
        except:
            raise HTTPException(400, "Invalid cursor")
    
    # Fetch orders
    cursor_db = db.orders.find(query).sort("createdAt", -1).limit(limit + 1)
    orders = []
    async for doc in cursor_db:
        orders.append(doc)
    
    # Check if there are more items
    has_more = len(orders) > limit
    if has_more:
        orders = orders[:limit]
    
    # Generate next cursor
    next_cursor = None
    if has_more and orders:
        last_order = orders[-1]
        next_cursor = base64.b64encode(
            last_order["createdAt"].isoformat().encode('utf-8')
        ).decode('utf-8')
    
    # Format response
    items = []
    for order in orders:
        items.append({
            "id": str(order["_id"]),
            "userId": order["userId"],
            "items": order["items"],
            "totalCents": order["totalCents"],
            "status": order.get("status", "confirmed"),
            "createdAt": order["createdAt"]
        })
    
    return {
        "items": items,
        "nextCursor": next_cursor
    }

@router.post("/checkout", status_code=201)
async def checkout(
    x_user_id: str = Header(...),
    idempotency_key: str = Header(None, alias="idempotency-key")
):
    """
    Checkout cart and create order.
    
    EXPECTATION:
    - Use idempotency-key header to prevent duplicate orders.
    - Use MongoDB transaction to atomically:
      1. Decrement product stock
      2. Create order
      3. Clear cart
    - Handle insufficient stock gracefully.
    """
    if not idempotency_key:
        raise HTTPException(400, "idempotency-key header is required")
    
    # Check if order already exists with this idempotency key
    existing_order = await db.orders.find_one({"idempotencyKey": idempotency_key})
    if existing_order:
        return {
            "id": str(existing_order["_id"]),
            "message": "Order already processed (idempotent)",
            "idempotent": True
        }
    
    # Get cart items
    cart_cursor = db.cart_items.find({"userId": x_user_id})
    cart_items = []
    async for item in cart_cursor:
        cart_items.append(item)
    
    if not cart_items:
        raise HTTPException(400, "Cart is empty")
    
    # Start transaction
    async with await client.start_session() as session:
        async with session.start_transaction():
            # Verify stock and prepare order items
            order_items = []
            total_cents = 0
            
            for cart_item in cart_items:
                product = await db.products.find_one(
                    {"_id": ObjectId(cart_item["productId"])},
                    session=session
                )
                
                if not product:
                    raise HTTPException(400, f"Product {cart_item['productId']} not found")
                
                if product["stock"] < cart_item["qty"]:
                    raise HTTPException(
                        400,
                        f"Insufficient stock for {product['name']}. Available: {product['stock']}"
                    )
                
                # Decrement stock
                await db.products.update_one(
                    {"_id": product["_id"]},
                    {"$inc": {"stock": -cart_item["qty"]}},
                    session=session
                )
                
                # Add to order
                order_items.append({
                    "productId": str(product["_id"]),
                    "productName": product["name"],
                    "qty": cart_item["qty"],
                    "priceCents": product["priceCents"]
                })
                total_cents += product["priceCents"] * cart_item["qty"]
            
            # Create order
            order_doc = {
                "userId": x_user_id,
                "items": order_items,
                "totalCents": total_cents,
                "status": "confirmed",
                "idempotencyKey": idempotency_key,
                "createdAt": datetime.utcnow()
            }
            result = await db.orders.insert_one(order_doc, session=session)
            
            # Clear cart
            await db.cart_items.delete_many({"userId": x_user_id}, session=session)
    
    return {
        "id": str(result.inserted_id),
        "message": "Order created successfully",
        "totalCents": total_cents
    }

