// src/components/Logout.js
import React from 'react';
import { logout } from '../api/userApi';
import { useHistory } from 'react-router-dom';

const Logout = () => {
    const history = useHistory();

    const handleLogout = async () => {
        await logout();
        history.push('/login');
    };

    return <button onClick={handleLogout}>Logout</button>;
};

export default Logout;
