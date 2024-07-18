// src/components/Register.js
import React, { useState } from 'react';
import { register } from '../api/userApi';
import { useHistory } from 'react-router-dom';

const Register = () => {
    const [user, setUser] = useState({ name: '', phone_number: '', email: '', address: '', username: '' });
    const history = useHistory();

    const handleChange = (e) => {
        setUser({ ...user, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await register(user);
        history.push('/login');
    };

    return (
        <form onSubmit={handleSubmit}>
            <h1>Register</h1>
            <input name="name" value={user.name} onChange={handleChange} placeholder="Name" required />
            <input name="phone_number" value={user.phone_number} onChange={handleChange} placeholder="Phone Number" required />
            <input name="email" value={user.email} onChange={handleChange} placeholder="Email" required />
            <input name="address" value={user.address} onChange={handleChange} placeholder="Address" required />
            <input name="username" value={user.username} onChange={handleChange} placeholder="Username" required />
            <button type="submit">Register</button>
        </form>
    );
};

export default Register;
