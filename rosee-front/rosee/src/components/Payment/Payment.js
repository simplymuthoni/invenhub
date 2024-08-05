import React, { useState, useEffect } from 'react';
import { Container, Form, Button } from 'react-bootstrap';
import api from '../../api';

function Payment() {
  const [paymentData, setPaymentData] = useState({
    cardNumber: '',
    expiryDate: '',
    cvv: ''
  });

  const handleChange = (e) => {
    setPaymentData({
      ...paymentData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Implement Stripe payment processing here
    api.post('/payment', paymentData).then(response => {
      // Handle successful payment
    }).catch(error => {
      console.error('Payment error:', error);
    });
  };

  return (
    <Container>
      <h2>Payment</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group>
          <Form.Label>Card Number</Form.Label>
          <Form.Control 
            type="text" 
            name="cardNumber" 
            value={paymentData.cardNumber} 
            onChange={handleChange} 
            required 
          />
        </Form.Group>
        <Form.Group>
          <Form.Label>Expiry Date</Form.Label>
          <Form.Control 
            type="text" 
            name="expiryDate" 
            value={paymentData.expiryDate} 
            onChange={handleChange} 
            required 
          />
        </Form.Group>
        <Form.Group>
          <Form.Label>CVV</Form.Label>
          <Form.Control 
            type="text" 
            name="cvv" 
            value={paymentData.cvv} 
            onChange={handleChange} 
            required 
          />
        </Form.Group>
        <Button type="submit">Pay Now</Button>
      </Form>
    </Container>
  );
}

export default Payment;
