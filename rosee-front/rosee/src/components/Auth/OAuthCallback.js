import React, { useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { handleOAuthCallback } from '../../api';

function OAuthCallback() {
  const { provider } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    handleOAuthCallback(provider, params).then(response => {
      // Store JWT or handle user session as needed
      navigate.push('/dashboard');
    }).catch(error => {
      console.error('OAuth callback error:', error);
      navigate.push('/login');
    });
  }, [provider, navigate]);

  return (
    <div>
      <h2>Logging in with {provider}</h2>
    </div>
  );
}

export default OAuthCallback;
