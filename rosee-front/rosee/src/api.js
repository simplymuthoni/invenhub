import axios from 'axios';

const API_URL = 'http://localhost:5000/api/rosee';

export const register = async (user) => {
  return await axios.post(`${API_URL}/register`, user);
};

export const login = async (credentials) => {
  return await axios.post(`${API_URL}/login`, credentials);
};

export const addItemToCart = async (item) => {
  return await axios.post(`${API_URL}/cart`, item);
};

export const getCartItems = async () => {
  return await axios.get(`${API_URL}/cart`);
};

export const createPayment = async (payment) => {
  return await axios.post(`${API_URL}/payment`, payment);
};

export const submitFeedback = async (feedback) => {
  return await axios.post(`${API_URL}/feedback`, feedback);
};

// Add more functions as needed for other endpoints
