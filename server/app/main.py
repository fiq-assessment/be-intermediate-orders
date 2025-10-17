from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.db import init_db
from .routers import cart, orders

app = FastAPI(
    title="Orders & Checkout API",
    version="1.0.0",
    description="Interview exercise: Intermediate BE - Orders with Transactions"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(cart.router)
app.include_router(orders.router)

@app.on_event("startup")
async def startup_event():
    """Initialize database indexes on startup"""
    await init_db()

@app.get("/health")
async def health():
    return {"ok": True, "service": "orders-api"}

