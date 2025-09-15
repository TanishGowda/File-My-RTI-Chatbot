// src/pages/ProfilePage.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import '../authstyles.css';

function ProfilePage() {
  const { user, profile, signOut } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    try {
      await signOut();
      navigate('/auth');
    } catch (err) {
      console.error('Error signing out:', err);
    }
  };

  const handleBackToChat = () => {
    navigate('/chat');
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not available';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="auth-container">
      <div className="auth-heading">User Profile</div>
      <div className="auth-box" style={{ maxWidth: '500px' }}>
        <img src="/filemyrti.png" alt="FileMyRTI" className="auth-logo" />
        <h2>Account Information</h2>

        {/* User Avatar Section */}
        <div style={{
          textAlign: 'center',
          marginBottom: '30px',
          padding: '20px',
          backgroundColor: '#f8f9fa',
          borderRadius: '8px',
          border: '1px solid #e9ecef'
        }}>
          <div style={{
            width: '80px',
            height: '80px',
            borderRadius: '50%',
            backgroundColor: '#1976D2',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '32px',
            color: 'white',
            fontWeight: '600',
            margin: '0 auto 15px auto',
            position: 'relative'
          }}>
            {user?.email?.charAt(0).toUpperCase() || 'U'}
            <div style={{
              position: 'absolute',
              bottom: '2px',
              right: '2px',
              width: '16px',
              height: '16px',
              backgroundColor: '#28a745',
              borderRadius: '50%',
              border: '2px solid white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <svg width="8" height="8" viewBox="0 0 24 24" fill="white">
                <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
              </svg>
            </div>
          </div>
          
          <h3 style={{
            margin: '0 0 5px 0',
            fontSize: '20px',
            color: '#333',
            fontWeight: '600'
          }}>
            {user?.user_metadata?.full_name || user?.email?.split('@')[0] || 'User'}
          </h3>
          
          <p style={{
            margin: '0',
            color: '#666',
            fontSize: '14px'
          }}>
            {user?.email || 'No email provided'}
          </p>
        </div>

        {/* User Information */}
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          gap: '15px',
          marginBottom: '30px'
        }}>
          <div>
            <label style={{ 
              display: 'block', 
              fontSize: '12px', 
              color: '#666',
              marginBottom: '5px',
              fontWeight: '500'
            }}>
              Full Name
            </label>
            <div style={{ 
              fontSize: '16px',
              color: '#333',
              padding: '10px',
              backgroundColor: '#f8f9fa',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}>
              {user?.user_metadata?.full_name || profile?.full_name || 'Not provided'}
            </div>
          </div>

          <div>
            <label style={{ 
              display: 'block', 
              fontSize: '12px', 
              color: '#666',
              marginBottom: '5px',
              fontWeight: '500'
            }}>
              Email Address
            </label>
            <div style={{ 
              fontSize: '16px',
              color: '#333',
              padding: '10px',
              backgroundColor: '#f8f9fa',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}>
              {user?.email || 'Not provided'}
            </div>
          </div>

          <div>
            <label style={{ 
              display: 'block', 
              fontSize: '12px', 
              color: '#666',
              marginBottom: '5px',
              fontWeight: '500'
            }}>
              Account Status
            </label>
            <div style={{ 
              fontSize: '16px',
              color: '#28a745',
              padding: '10px',
              backgroundColor: '#d4edda',
              border: '1px solid #c3e6cb',
              borderRadius: '4px',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <span style={{ 
                width: '8px', 
                height: '8px', 
                backgroundColor: '#28a745', 
                borderRadius: '50%' 
              }}></span>
              Active
            </div>
          </div>

          <div>
            <label style={{ 
              display: 'block', 
              fontSize: '12px', 
              color: '#666',
              marginBottom: '5px',
              fontWeight: '500'
            }}>
              Member Since
            </label>
            <div style={{ 
              fontSize: '16px',
              color: '#333',
              padding: '10px',
              backgroundColor: '#f8f9fa',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}>
              {formatDate(user?.created_at)}
            </div>
          </div>

          <div>
            <label style={{ 
              display: 'block', 
              fontSize: '12px', 
              color: '#666',
              marginBottom: '5px',
              fontWeight: '500'
            }}>
              User ID
            </label>
            <div style={{ 
              fontSize: '12px',
              color: '#666',
              padding: '10px',
              backgroundColor: '#f8f9fa',
              border: '1px solid #ddd',
              borderRadius: '4px',
              fontFamily: 'monospace',
              wordBreak: 'break-all'
            }}>
              {user?.id || 'Not available'}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column', 
          gap: '10px'
        }}>
          <button 
            onClick={handleBackToChat}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: '#1976D2',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.target.style.backgroundColor = '#1565C0'}
            onMouseOut={(e) => e.target.style.backgroundColor = '#1976D2'}
          >
            Back to Chat
          </button>
          
          <button 
            onClick={handleSignOut}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              fontSize: '16px',
              cursor: 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.target.style.backgroundColor = '#c82333'}
            onMouseOut={(e) => e.target.style.backgroundColor = '#dc3545'}
          >
            Sign Out
          </button>
        </div>

        <div style={{ 
          marginTop: '20px', 
          fontSize: '14px', 
          textAlign: 'center',
          color: '#666'
        }}>
          <a className="muted-link" href="/terms">Terms and Conditions</a> | 
          <a className="muted-link" href="/privacy">Privacy Policy</a>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
