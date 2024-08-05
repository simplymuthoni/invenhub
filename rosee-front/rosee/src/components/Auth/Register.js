import React, { useState } from 'react';
import { Container, Form, Button } from 'react-bootstrap';
import api from '../../api';

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    api.post('/register', formData).then(response => {
      // Handle successful registration (e.g., redirect to login)
    }).catch(error => {
      console.error('Registration error:', error);
    });
  };

  return (
    <Container>
      <h2>Register</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group>
          <Form.Label>Username</Form.Label>
          <Form.Control 
            type="text" 
            name="username" 
            value={formData.username} 
            onChange={handleChange} 
            required 
          />
        </Form.Group>
        <Form.Group>
          <Form.Label>Email</Form.Label>
          <Form.Control 
            type="email" 
            name="email" 
            value={formData.email} 
            onChange={handleChange} 
            required 
          />
        </Form.Group>
        <Form.Group>
          <Form.Label>Password</Form.Label>
          <Form.Control 
            type="password" 
            name="password" 
            value={formData.password} 
            onChange={handleChange} 
            required 
          />
        </Form.Group>
        <Button type="submit">Register</Button>
      </Form>
    </Container>
  );
}

export default Register;
