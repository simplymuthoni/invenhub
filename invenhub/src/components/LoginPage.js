import React, { useState } from 'react';
import axios from 'axios';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [resetRequired, setResetRequired] = useState(false);
  const [newPassword, setNewPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/users/login', {
        username,
        password,
      });
      setMessage(response.data.message);
    } catch (error) {
      if (error.response.status === 403) {
        setResetRequired(true);
        setMessage('You need to reset your password before logging in.');
      } else {
        setMessage('Login failed.');
      }
    }
  };

  const handleResetPassword = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/users/reset_password', {
        username,
        new_password: newPassword,
      });
      setMessage(response.data.message);
      setResetRequired(false);
    } catch (error) {
      setMessage('Password reset failed.');
    }
  };

  return (
    <div>
      <h1>Login</h1>
      {message && <p>{message}</p>}
      {!resetRequired ? (
        <div>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
        </div>
      ) : (
        <div>
          <h2>Reset Password</h2>
          <input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <button onClick={handleResetPassword}>Reset Password</button>
        </div>
      )}
    </div>
  );
};

export default LoginPage;
