from fastapi import APIRouter, HTTPException, Header
from ..core.db import db
from ..models.order import CartItemIn, CartItemOut
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/cart", tags=["cart"])

# EXPECTATION:
# - Use x-user-id header for user identification (simplified auth).
# - Store cart items in database with userId reference.
# - Handle invalid productId gracefully.

@router.post("/items", status_code=201)
async def add_cart_item(item: CartItemIn, x_user_id: str = Header(...)):
    """Add item to cart"""
    # Verify product exists and has sufficient stock
    try:
        product_id = ObjectId(item.productId)
    except:
        raise HTTPException(400, "Invalid product ID")
    
    product = await db.products.find_one({"_id": product_id})
    if not product:
        raise HTTPException(404, "Product not found")
    
    if product.get("stock", 0) < item.qty:
        raise HTTPException(400, f"Insufficient stock. Available: {product.get('stock', 0)}")
    
    # Check if item already in cart
    existing = await db.cart_items.find_one({
        "userId": x_user_id,
        "productId": item.productId
    })
    
    if existing:
        # Update quantity
        new_qty = existing["qty"] + item.qty
        if product.get("stock", 0) < new_qty:
            raise HTTPException(400, f"Insufficient stock. Available: {product.get('stock', 0)}")
        
        await db.cart_items.update_one(
            {"_id": existing["_id"]},
            {"$set": {"qty": new_qty, "updatedAt": datetime.utcnow()}}
        )
        cart_item_id = str(existing["_id"])
    else:
        # Create new cart item
        result = await db.cart_items.insert_one({
            "userId": x_user_id,
            "productId": item.productId,
            "productName": product["name"],
            "qty": item.qty,
            "priceCents": product["priceCents"],
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        })
        cart_item_id = str(result.inserted_id)
    
    return {
        "id": cart_item_id,
        "message": "Item added to cart"
    }

@router.get("/items")
async def get_cart_items(x_user_id: str = Header(...)):
    """Get all cart items for user"""
    cursor = db.cart_items.find({"userId": x_user_id})
    items = []
    async for doc in cursor:
        items.append({
            "id": str(doc["_id"]),
            "productId": doc["productId"],
            "productName": doc["productName"],
            "qty": doc["qty"],
            "priceCents": doc["priceCents"]
        })
    return {"items": items}

@router.delete("/items/{id}")
async def remove_cart_item(id: str, x_user_id: str = Header(...)):
    """Remove item from cart"""
    try:
        oid = ObjectId(id)
    except:
        raise HTTPException(400, "Invalid cart item ID")
    
    result = await db.cart_items.delete_one({
        "_id": oid,
        "userId": x_user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(404, "Cart item not found")
    
    return {"message": "Item removed from cart"}

