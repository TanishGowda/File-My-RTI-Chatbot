// src/components/ProfileModal.jsx
import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import '../authstyles.css';

function ProfileModal({ isOpen, onClose }) {
  const { user, profile, signOut } = useAuth();

  const handleSignOut = async () => {
    try {
      await signOut();
      onClose();
    } catch (err) {
      console.error('Error signing out:', err);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Not available';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Account Information</h2>
          <button className="modal-close" onClick={onClose} title="Close">
            ×
          </button>
        </div>
        
        <div className="modal-body">
          {/* Main Profile Section - Horizontal Layout */}
          <div className="profile-main-section">
            {/* Left Side - Avatar and Basic Info */}
            <div className="profile-left">
              <div className="profile-avatar">
                {user?.email?.charAt(0).toUpperCase() || 'U'}
                <div className="profile-status-indicator">
                  <svg width="10" height="10" viewBox="0 0 24 24" fill="white">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                  </svg>
                </div>
              </div>
              
              <h3 className="profile-name">
                {user?.user_metadata?.full_name || user?.email?.split('@')[0] || 'User'}
              </h3>
              
              <p className="profile-email">
                {user?.email || 'No email provided'}
              </p>

              {/* Status Badge */}
              <div className="profile-status-badge">
                <span className="status-dot"></span>
                Active
              </div>
            </div>

            {/* Right Side - Detailed Information and Buttons */}
            <div className="profile-right">
              {/* Information Grid */}
              <div className="profile-info-grid">
                {/* Full Name */}
                <div className="profile-info-item">
                  <label>Full Name</label>
                  <div className="profile-info-value">
                    {user?.user_metadata?.full_name || profile?.full_name || 'Not provided'}
                  </div>
                </div>

                {/* Email Address */}
                <div className="profile-info-item">
                  <label>Email Address</label>
                  <div className="profile-info-value">
                    {user?.email || 'Not provided'}
                  </div>
                </div>

                {/* Member Since */}
                <div className="profile-info-item">
                  <label>Member Since</label>
                  <div className="profile-info-value">
                    {formatDate(user?.created_at)}
                  </div>
                </div>
              </div>

              {/* Sign Out Button */}
              <div className="profile-actions">
                <button className="profile-signout-btn" onClick={handleSignOut}>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <polyline points="16,17 21,12 16,7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    <line x1="21" y1="12" x2="9" y2="12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  Sign Out
                </button>
              </div>
            </div>
          </div>

          <div className="profile-footer">
            <a className="muted-link" href="/terms">Terms and Conditions</a> | 
            <a className="muted-link" href="/privacy">Privacy Policy</a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfileModal;
