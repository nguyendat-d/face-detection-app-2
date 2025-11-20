import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Auth.css';

export default function Login({ setLoggedIn }) {
  const [emailOrUsername, setEmailOrUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const login = async () => {
    if (emailOrUsername.includes('@') && !emailOrUsername.endsWith('@gmail.com')) {
      alert('Email must be a valid @gmail.com address!');
      return;
    }

    const res = await axios.post(`${API_URL}/login`, {
      emailOrUsername,
      password,
    });
    if (res.data.success) setLoggedIn(true);
    else alert('Login failed');
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <div className="auth-form">
        <input
          className="auth-input"
          placeholder="Email or Username"
          onChange={(e) => setEmailOrUsername(e.target.value)}
        />
        <input
          className="auth-input"
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="button" onClick={login}>
          Login
        </button>
        <button className="button button-success" onClick={() => navigate('/register')}>
          Don't have an account? Register
        </button>
      </div>
    </div>
  );
}