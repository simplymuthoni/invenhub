import React, { useState } from 'react';
import { registerAdmin, loginAdmin, getSession, logoutAdmin } from './api';

const App = () => {
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [adminSession, setAdminSession] = useState(null);

    const handleRegister = async () => {
        const response = await registerAdmin({ email, name, password });
        setMessage(response.message);
    };

    const handleLogin = async () => {
        const response = await loginAdmin({ email, password });
        setMessage(response.message);
        if (response.admin) {
            setAdminSession(response.admin);
        }
    };

    const handleLogout = async () => {
        const response = await logoutAdmin();
        setMessage(response.message);
        setAdminSession(null);
    };

    const handleGetSession = async () => {
        const response = await getSession();
        if (response.admin_id) {
            setAdminSession(response);
        } else {
            setMessage(response.error);
        }
    };

    return (
        <div>
            <h1>Admin Dashboard</h1>
            <div>
                <h2>Register</h2>
                <input type="text" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
                <input type="text" placeholder="Name" value={name} onChange={e => setName(e.target.value)} />
                <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                <button onClick={handleRegister}>Register</button>
            </div>
            <div>
                <h2>Login</h2>
                <input type="text" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
                <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                <button onClick={handleLogin}>Login</button>
            </div>
            <div>
                <h2>Session</h2>
                <button onClick={handleGetSession}>Get Session</button>
                <button onClick={handleLogout}>Logout</button>
            </div>
            <div>
                {adminSession && (
                    <div>
                        <h3>Admin Session</h3>
                        <p>ID: {adminSession.admin_id}</p>
                        <p>Email: {adminSession.admin_email}</p>
                    </div>
                )}
            </div>
            <div>
                <p>{message}</p>
            </div>
        </div>
    );
};

export default App;
