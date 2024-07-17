// src/components/Register.js
import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
    const [user, setUser] = useState({
        name: '',
        phoneNumber: '',
        email: '',
        address: '',
        username: '',
    });

    const [message, setMessage] = useState('');

    const handleChange = (e) => {
        setUser({
            ...user,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/users/register', user);
            setMessage(response.data.message);
        } catch (error) {
            setMessage(error.response.data.message);
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name:</label>
                    <input type="text" name="name" value={user.name} onChange={handleChange} required />
                </div>
                <div>
                    <label>Phone Number:</label>
                    <input type="text" name="phoneNumber" value={user.phoneNumber} onChange={handleChange} required />
                </div>
                <div>
                    <label>Email:</label>
                    <input type="email" name="email" value={user.email} onChange={handleChange} required />
                </div>
                <div>
                    <label>Address:</label>
                    <input type="text" name="address" value={user.address} onChange={handleChange} required />
                </div>
                <div>
                    <label>Username:</label>
                    <input type="text" name="username" value={user.username} onChange={handleChange} required />
                </div>
                <button type="submit">Register</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Register;
