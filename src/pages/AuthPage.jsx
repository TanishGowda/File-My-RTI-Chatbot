// src/pages/AuthPage.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../authstyles.css';

function AuthPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { signIn, signInWithGoogle, user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) {
      navigate('/chat');
    }
  }, [user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const { error } = await signIn(email, password);
      if (error) {
        setError(error.message);
      } else {
        navigate('/chat');
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignIn = async () => {
    setError('');
    setLoading(true);

    try {
      const { error } = await signInWithGoogle();
      if (error) {
        setError(error.message);
      }
    } catch (err) {
      setError('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-heading">Welcome to FileMyRTI</div>
      <div className="auth-box">
        <img src="/filemyrti.png" alt="FileMyRTI" className="auth-logo" />
        <h2>Login / Sign Up</h2>

        {error && (
          <div style={{ 
            color: '#ff4444', 
            fontSize: '14px', 
            marginBottom: '10px',
            textAlign: 'center',
            padding: '8px',
            backgroundColor: '#ffe6e6',
            borderRadius: '4px'
          }}>
            {error}
          </div>
        )}

        <form className="auth-form" onSubmit={handleSubmit}>
          <input 
            type="email" 
            placeholder="Email" 
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
          <input 
            type="password" 
            placeholder="Password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Signing in...' : 'Login'}
          </button>
        </form>

        <div className="divider">or</div>

        <button 
          className="google-btn" 
          onClick={handleGoogleSignIn}
          disabled={loading}
        >
          <span className="google-icon" aria-hidden="true">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="18" height="18">
              <path fill="#FFC107" d="M43.611,20.083h-1.611v-0.083H24v8h11.303c-1.651,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12 s5.373-12,12-12c3.059,0,5.842,1.153,7.96,3.04l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24 s8.955,20,20,20s20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/>
              <path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.463,16.108,18.855,12,24,12c3.059,0,5.842,1.153,7.96,3.04l5.657-5.657 C34.046,6.053,29.268,4,24,4C16.318,4,9.66,8.337,6.306,14.691z"/>
              <path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.191-5.238C29.181,35.091,26.715,36,24,36 c-5.202,0-9.616-3.317-11.278-7.946l-6.53,5.032C9.505,39.556,16.227,44,24,44z"/>
              <path fill="#1976D2" d="M43.611,20.083h-1.611v-0.083H24v8h11.303c-0.793,2.236-2.231,4.166-4.084,5.487 c0.001-0.001,0.002-0.001,0.003-0.002l6.191,5.238C36.955,39.06,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"/>
            </svg>
          </span>
          <span>{loading ? 'Signing in...' : 'Continue with Google'}</span>
        </button>

        <div style={{ marginTop: '15px', fontSize: '14px', textAlign: 'center' }}>
          Don't have an account? <Link to="/signup">Sign up</Link>
          <div style={{ marginTop: '10px' }}>
            <a className="muted-link" href="/terms">Terms and Conditions</a> | <a className="muted-link" href="/privacy">Privacy Policy</a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AuthPage;
