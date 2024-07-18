// src/components/Login.js
import React, { useState } from 'react';
import { login } from '../api/userApi';
import { useHistory } from 'react-router-dom';

const Login = () => {
    const [credentials, setCredentials] = useState({ username: '', password: '' });
    const history = useHistory();

    const handleChange = (e) => {
        setCredentials({ ...credentials, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await login(credentials);
        history.push('/');
    };

    return (
        <form onSubmit={handleSubmit}>
            <h1>Login</h1>
            <input name="username" value={credentials.username} onChange={handleChange} placeholder="Username" required />
            <input type="password" name="password" value={credentials.password} onChange={handleChange} placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
    );
};

export default Login;
