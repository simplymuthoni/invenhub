// src/api/userApi.js
import axios from 'axios';

const API_URL = 'http://localhost:5000/api/users';

export const register = async (user) => {
    const response = await axios.post(`${API_URL}/register`, user);
    return response.data;
};

export const login = async (credentials) => {
    const response = await axios.post(`${API_URL}/login`, credentials);
    return response.data;
};

export const logout = async () => {
    const response = await axios.post(`${API_URL}/logout`);
    return response.data;
};

export const resetPassword = async (username) => {
    const response = await axios.post(`${API_URL}/reset_password`, { username });
    return response.data;
};

export const changePassword = async (token, passwords) => {
    const response = await axios.post(`${API_URL}/change_password`, passwords, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
