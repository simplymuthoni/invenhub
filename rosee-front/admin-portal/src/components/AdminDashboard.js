import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ItemList from './ItemList';
import Reports from './Reports';
import LoggedInUsers from './LoggedInUsers';

const AdminDashboard = () => {
    const [admin, setAdmin] = useState(null);

    useEffect(() => {
        const fetchSession = async () => {
            try {
                const response = await axios.get('/api/admin/session');
                setAdmin(response.data);
            } catch (error) {
                console.error('No active session');
            }
        };
        fetchSession();
    }, []);

    return (
        <div>
            <h2>Admin Dashboard</h2>
            {admin ? (
                <div>
                    <p>Welcome, {admin.admin_email}</p>
                    <ItemList />
                    <Reports />
                    <LoggedInUsers />
                </div>
            ) : (
                <p>Please log in</p>
            )}
        </div>
    );
};

export default AdminDashboard;
