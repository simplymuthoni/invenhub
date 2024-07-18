// src/components/ResetPassword.js
import React, { useState } from 'react';
import { resetPassword } from '../api/userApi';
import { useHistory } from 'react-router-dom';

const ResetPassword = () => {
    const [username, setUsername] = useState('');
    const history = useHistory();

    const handleChange = (e) => {
        setUsername(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await resetPassword(username);
        history.push('/login');
    };

    return (
        <form onSubmit={handleSubmit}>
            <h1>Reset Password</h1>
            <input name="username" value={username} onChange={handleChange} placeholder="Username" required />
            <button type="submit">Reset Password</button>
        </form>
    );
};

export default ResetPassword;
