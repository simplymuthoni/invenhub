import React from 'react';
import { Card } from 'react-bootstrap';

function CartSummary({ cartItems }) {
  const getTotal = () => {
    return cartItems.reduce((total, item) => total + item.price, 0).toFixed(2);
  };

  return (
    <Card>
      <Card.Body>
        <Card.Title>Cart Summary</Card.Title>
        <Card.Text>
          Total Items: {cartItems.length}
        </Card.Text>
        <Card.Text>
          Total Price: ${getTotal()}
        </Card.Text>
      </Card.Body>
    </Card>
  );
}

export default CartSummary;
