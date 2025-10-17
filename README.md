# BE • Intermediate • 90-Min Exercise — Orders & Checkout with Transactions

**Timebox:** 90 minutes. Do as much as you can; leave notes under "Trade-offs & Next Steps".

> This repo includes boilerplate and comments that outline expectations and requirements. Please follow them and keep scope tight.

## What's Provided
- FastAPI backend skeleton with MongoDB via motor
- Docker Compose setup with MongoDB service
- Minimal Next.js client_mock for cart/checkout UI
- Pydantic models and routing structure

## Problem Statement
Implement an orders system with cart management, transactional stock decrement, and idempotent checkout. The checkout endpoint should use idempotency keys to prevent duplicate orders, and stock updates must be atomic using MongoDB transactions. Orders should be retrieved with cursor-based pagination for scalability.

## Tasks (Must-have)
1. Implement POST /cart/items to add items (use x-user-id header for user identification)
2. Implement DELETE /cart/items/{id} to remove cart items
3. Implement POST /checkout with idempotency-key header
4. Ensure checkout atomically decrements stock using MongoDB transactions
5. Store idempotency keys to prevent duplicate order creation
6. Implement GET /orders with cursor pagination sorted by createdAt desc
7. Add proper indexes on orders (userId, createdAt) and products (stock)

## Expected Solution (Checklist)
- Correct API contracts/state handling.
- Pagination implemented (cursor).
- Error/loading/empty states.
- Basic a11y (labels, keyboard access).
- Reasonable structure & naming.
- Idempotent checkout endpoint.
- Atomic stock updates via transactions.

## Bonus (If time permits)
- Implement cart expiration (TTL)
- Add order status tracking (pending/confirmed/shipped)
- Handle insufficient stock gracefully
- Add integration tests for transaction rollback

## Clone & Run

```bash
git clone https://github.com/yourorg/be-intermediate-orders
cd be-intermediate-orders

# Start MongoDB
docker compose up -d

# Install and run API
cd server
cp .env.example .env
pip install -r requirements.txt
python app/seed/seed.py  # Seed sample products
uvicorn app.main:app --reload --port 4000

# Optional: Run client mock
cd client_mock
pnpm i
cp .env.example .env
pnpm dev
```

API at http://localhost:4000, Client mock at http://localhost:3000

## Submission

Push your work to a branch named `{your-name}` and update this README with:
- Run steps, assumptions, trade-offs, next steps.
- Notes on transaction handling and idempotency implementation.

---

© 2025 yourorg – For interview use only.

