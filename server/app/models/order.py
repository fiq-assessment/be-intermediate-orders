from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CartItemIn(BaseModel):
    """Add item to cart"""
    productId: str
    qty: int = Field(..., gt=0)

class CartItemOut(BaseModel):
    """Cart item response"""
    id: str
    productId: str
    productName: str
    qty: int
    priceCents: int

class OrderItemOut(BaseModel):
    """Order item in response"""
    productId: str
    productName: str
    qty: int
    priceCents: int

class OrderOut(BaseModel):
    """Order response"""
    id: str
    userId: str
    items: List[OrderItemOut]
    totalCents: int
    status: str
    createdAt: datetime
    idempotencyKey: Optional[str] = None

