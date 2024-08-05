import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import CartItem from './CartItem';
import api from '../../api';

function Cart() {
  const [cartItems, setCartItems] = useState([]);

  useEffect(() => {
    api.getCartItems().then(response => {
      setCartItems(response.data);
    }).catch(error => {
      console.error('Error fetching cart items:', error);
    });
  }, []);

  const handleRemove = (itemId) => {
    api.removeCartItem(itemId).then(() => {
      setCartItems(cartItems.filter(item => item.id !== itemId));
    }).catch(error => {
      console.error('Error removing cart item:', error);
    });
  };

  return (
    <Container>
      <Row>
        {cartItems.map(item => (
          <Col key={item.id} md={4}>
            <CartItem item={item} onRemove={() => handleRemove(item.id)} />
          </Col>
        ))}
      </Row>
      <Button variant="primary" href="/payment">Proceed to Payment</Button>
    </Container>
  );
}

export default Cart;
