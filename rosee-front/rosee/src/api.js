import axios from 'axios';

const API_URL = 'http://localhost:5000/api/rosee';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL,
});

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
export const getItems = () => api.get('/items');

export const login = (provider) => api.get(`/login/${provider}`);

export const handleOAuthCallback = (provider, params) => api.get(`/callback/${provider}`, { params });

export default api;

// Add more functions as needed for other endpoints
