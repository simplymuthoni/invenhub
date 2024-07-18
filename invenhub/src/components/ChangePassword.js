// src/components/ChangePassword.js
import React, { useState } from 'react';
import { changePassword } from '../api/userApi';
import { useNavigate } from 'react-router-dom';

const ChangePassword = () => {
    const [passwords, setPasswords] = useState({ old_password: '', new_password: '' });
    const Navigate = useNavigate();

    const handleChange = (e) => {
        setPasswords({ ...passwords, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        await changePassword(token, passwords);
        Navigate.push('/');
    };

    return (
        <form onSubmit={handleSubmit}>
            <h1>Change Password</h1>
            <input type="password" name="old_password" value={passwords.old_password} onChange={handleChange} placeholder="Old Password" required />
            <input type="password" name="new_password" value={passwords.new_password} onChange={handleChange} placeholder="New Password" required />
            <button type="submit">Change Password</button>
        </form>
    );
};

export default ChangePassword;
