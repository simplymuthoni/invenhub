import React, { useEffect, useState } from 'react';
import { getCartItems, addItemToCart } from '../api';

function Cart() {
  const [cart, setCart] = useState([]);

  useEffect(() => {
    async function fetchCart() {
      const response = await getCartItems();
      setCart(response.data);
    }
    fetchCart();
  }, []);

  const handleAddItem = async (item_id) => {
    try {
      await addItemToCart({ item_id, quantity: 1 });
      const response = await getCartItems();
      setCart(response.data);
    } catch (error) {
      alert('Error adding item to cart');
    }
  };

  return (
    <div>
      <h2>Cart</h2>
      <ul>
        {cart.map((cartItem) => (
          <li key={cartItem.item.id}>
            {cartItem.item.name} - Quantity: {cartItem.quantity}
            <button onClick={() => handleAddItem(cartItem.item.id)}>Add more</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Cart;
