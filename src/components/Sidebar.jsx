// src/components/Sidebar.jsx
import React, { useEffect, useRef, useState } from 'react';

const Sidebar = ({
  darkMode,
  setDarkMode,
  conversations = [],
  activeId,
  onSelect,
  onNewChat,
  sidebarOpen,
  setSidebarOpen,
  user,
  onSignOut,
}) => {
  const [accountOpen, setAccountOpen] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setAccountOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={`sidebar ${sidebarOpen ? '' : 'collapsed'}`}>
      <button
        className="sidebar-toggle"
        onClick={() => setSidebarOpen && setSidebarOpen(!sidebarOpen)}
        aria-label={sidebarOpen ? 'Collapse sidebar' : 'Expand sidebar'}
        title={sidebarOpen ? 'Collapse' : 'Expand'}
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 6l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
      <div className="sidebar-branding">
        <img src="/filemyrti.png" alt="FileMyRTI" className="sidebar-logo" />
      </div>

      <div className="new-chat-wrapper">
        <button className="new-chat-button" onClick={onNewChat}>＋ New chat</button>
      </div>

      <div className="sidebar-separator" />

      <div className="conversation-wrapper">
        <ul className="conversation-list">
          {conversations.map((conv) => (
            <li
              key={conv.id}
              className={`conversation-item ${activeId === conv.id ? 'active' : ''}`}
              onClick={() => onSelect && onSelect(conv.id)}
            >
              <div className="conversation-title">{conv.title}</div>
            </li>
          ))}
        </ul>
      </div>

      <div className="sidebar-footer" ref={menuRef}>
        <button
          className="file-rti-button"
          onClick={() => (window.location.href = '/file-rti')}
        >
          <span className="file-rti-icon" aria-hidden>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <polyline points="10,9 9,9 8,9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </span>
          <span className="file-rti-label">File RTI with us</span>
        </button>
        <button
          className="account-button"
          onClick={() => setAccountOpen((v) => !v)}
          aria-haspopup="menu"
          aria-expanded={accountOpen}
          title={user ? "Account" : "Guest Account"}
        >
          <span className="account-avatar" aria-hidden>
            {user ? (
              // Show user's first letter or Google avatar
              <div style={{
                width: '18px',
                height: '18px',
                borderRadius: '50%',
                backgroundColor: '#007bff',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '10px',
                fontWeight: 'bold'
              }}>
                {user.email?.charAt(0).toUpperCase() || 'U'}
              </div>
            ) : (
              // Guest icon
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="1.8"/>
                <path d="M4 20c0-4 4-6 8-6s8 2 8 6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
              </svg>
            )}
          </span>
          <span className="account-label">
            {user ? (user.user_metadata?.full_name || user.email?.split('@')[0] || 'User') : 'Guest'}
          </span>
        </button>

        {accountOpen && (
          <div className="account-menu" role="menu">
            {user && (
              <button 
                className="account-menu-item" 
                role="menuitem" 
                onClick={() => {
                  setAccountOpen(false);
                  window.location.href = '/profile';
                }}
              >
                <span className="menu-icon" aria-hidden>
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="1.8"/>
                    <path d="M4 20c0-4 4-6 8-6s8 2 8 6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                  </svg>
                </span>
                <span>Profile</span>
              </button>
            )}
            
            <button
              className="account-menu-item"
              role="menuitemcheckbox"
              aria-checked={!!darkMode}
              onClick={() => {
                setDarkMode(!darkMode);
                setAccountOpen(false);
              }}
            >
              <span className="menu-icon" aria-hidden>
                {darkMode ? (
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="4" stroke="currentColor" strokeWidth="1.8"/>
                    <path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M19.07 4.93l-1.41 1.41M6.34 17.66l-1.41 1.41" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                  </svg>
                ) : (
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </span>
              <span>{darkMode ? 'Light mode' : 'Dark mode'}</span>
            </button>
            
            {user && onSignOut && (
              <button 
                className="account-menu-item" 
                role="menuitem" 
                onClick={() => {
                  setAccountOpen(false);
                  onSignOut();
                }}
                style={{ color: '#dc3545' }}
              >
                <span className="menu-icon" aria-hidden>
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                    <polyline points="16,17 21,12 16,7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                    <line x1="21" y1="12" x2="9" y2="12" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </span>
                <span>Sign Out</span>
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
