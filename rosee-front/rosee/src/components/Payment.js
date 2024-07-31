import React, { useState } from 'react';
import { createPayment } from '../api';

function Payment() {
  const [form, setForm] = useState({
    user_id: '',
    amount: '',
    payment_method: 'credit_card',
    payment_status: 'pending',
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await createPayment(form);
      alert(response.data.message);
    } catch (error) {
      alert('Error creating payment');
    }
  };

  return (
    <div>
      <h2>Payment</h2>
      <form onSubmit={handleSubmit}>
        <input type="number" name="user_id" placeholder="User ID" onChange={handleChange} />
        <input type="number" name="amount" placeholder="Amount" onChange={handleChange} />
        <select name="payment_method" onChange={handleChange}>
          <option value="credit_card">Credit Card</option>
          <option value="paypal">PayPal</option>
          <option value="bank_transfer">Bank Transfer</option>
        </select>
        <select name="payment_status" onChange={handleChange}>
          <option value="pending">Pending</option>
          <option value="success">Success</option>
          <option value="failed">Failed</option>
        </select>
        <button type="submit">Pay</button>
      </form>
    </div>
  );
}

export default Payment;
