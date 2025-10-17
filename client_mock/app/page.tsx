'use client';
import { useEffect, useState } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:4000';
const USER_ID = 'test-user-123';

export default function OrdersMockClient() {
  const [products, setProducts] = useState<any[]>([]);
  const [cart, setCart] = useState<any[]>([]);
  const [orders, setOrders] = useState<any[]>([]);

  useEffect(() => {
    fetchProducts();
    fetchCart();
    fetchOrders();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await fetch(`${API_BASE}/products?limit=100`);
      const data = await res.json();
      setProducts(data.items || []);
    } catch (err) {
      console.error('Failed to fetch products:', err);
    }
  };

  const fetchCart = async () => {
    try {
      const res = await fetch(`${API_BASE}/cart/items`, {
        headers: { 'x-user-id': USER_ID }
      });
      const data = await res.json();
      setCart(data.items || []);
    } catch (err) {
      console.error('Failed to fetch cart:', err);
    }
  };

  const fetchOrders = async () => {
    try {
      const res = await fetch(`${API_BASE}/orders`, {
        headers: { 'x-user-id': USER_ID }
      });
      const data = await res.json();
      setOrders(data.items || []);
    } catch (err) {
      console.error('Failed to fetch orders:', err);
    }
  };

  const addToCart = async (productId: string, qty: number) => {
    try {
      const res = await fetch(`${API_BASE}/cart/items`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': USER_ID
        },
        body: JSON.stringify({ productId, qty })
      });
      if (res.ok) {
        fetchCart();
      } else {
        const err = await res.json();
        alert(`Error: ${err.detail || 'Failed to add to cart'}`);
      }
    } catch (err) {
      alert(`Failed: ${err}`);
    }
  };

  const removeFromCart = async (id: string) => {
    try {
      await fetch(`${API_BASE}/cart/items/${id}`, {
        method: 'DELETE',
        headers: { 'x-user-id': USER_ID }
      });
      fetchCart();
    } catch (err) {
      alert(`Failed: ${err}`);
    }
  };

  const checkout = async () => {
    if (!confirm('Proceed with checkout?')) return;
    
    const idempotencyKey = `checkout-${Date.now()}-${Math.random()}`;
    try {
      const res = await fetch(`${API_BASE}/orders/checkout`, {
        method: 'POST',
        headers: {
          'x-user-id': USER_ID,
          'idempotency-key': idempotencyKey
        }
      });
      if (res.ok) {
        alert('Order created successfully!');
        fetchCart();
        fetchOrders();
        fetchProducts(); // Refresh to show updated stock
      } else {
        const err = await res.json();
        alert(`Error: ${err.detail || 'Checkout failed'}`);
      }
    } catch (err) {
      alert(`Failed: ${err}`);
    }
  };

  const cartTotal = cart.reduce((sum, item) => sum + (item.priceCents * item.qty), 0);

  return (
    <div className="container">
      <div className="card">
        <h1 style={{ marginBottom: '1rem' }}>Orders & Checkout API - Client Mock</h1>
        <p style={{ color: '#666', fontSize: '0.875rem' }}>
          Test cart management, idempotent checkout, and transaction handling.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div className="card">
          <h2 style={{ marginBottom: '1rem' }}>Products</h2>
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {products.map(p => (
                <tr key={p.id}>
                  <td>{p.name}</td>
                  <td>${(p.priceCents / 100).toFixed(2)}</td>
                  <td>{p.stock}</td>
                  <td>
                    <button 
                      className="btn" 
                      onClick={() => addToCart(p.id, 1)}
                      disabled={p.stock === 0}
                    >
                      Add to Cart
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div>
          <div className="card">
            <h2 style={{ marginBottom: '1rem' }}>Shopping Cart</h2>
            {cart.length === 0 && <p style={{ color: '#999' }}>Cart is empty</p>}
            {cart.length > 0 && (
              <>
                <table className="table">
                  <thead>
                    <tr>
                      <th>Item</th>
                      <th>Qty</th>
                      <th>Price</th>
                      <th></th>
                    </tr>
                  </thead>
                  <tbody>
                    {cart.map(item => (
                      <tr key={item.id}>
                        <td>{item.productName}</td>
                        <td>{item.qty}</td>
                        <td>${(item.priceCents * item.qty / 100).toFixed(2)}</td>
                        <td>
                          <button className="btn" onClick={() => removeFromCart(item.id)}>
                            Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <strong>Total: ${(cartTotal / 100).toFixed(2)}</strong>
                  <button className="btn btn-primary" onClick={checkout}>
                    Checkout
                  </button>
                </div>
              </>
            )}
          </div>

          <div className="card">
            <h2 style={{ marginBottom: '1rem' }}>Order History</h2>
            {orders.length === 0 && <p style={{ color: '#999' }}>No orders yet</p>}
            {orders.map(order => (
              <div key={order.id} style={{ borderBottom: '1px solid #eee', paddingBottom: '0.5rem', marginBottom: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ fontWeight: 600 }}>${(order.totalCents / 100).toFixed(2)}</span>
                  <span style={{ fontSize: '0.875rem', color: '#666' }}>
                    {new Date(order.createdAt).toLocaleString()}
                  </span>
                </div>
                <div style={{ fontSize: '0.875rem', color: '#666' }}>
                  {order.items.length} item(s) • {order.status}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

