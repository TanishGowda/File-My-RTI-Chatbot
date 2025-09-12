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
        <button className="new-chat-button" onClick={() => (window.location.href = '/file-rti')}>
          File RTI With Us
        </button>
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
          className="account-button"
          onClick={() => setAccountOpen((v) => !v)}
          aria-haspopup="menu"
          aria-expanded={accountOpen}
          title="Account"
        >
          <span className="account-avatar" aria-hidden>
            {/* Guest icon placeholder; later swap with Google avatar */}
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="1.8"/>
              <path d="M4 20c0-4 4-6 8-6s8 2 8 6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
            </svg>
          </span>
          <span className="account-label">Guest</span>
        </button>

        {accountOpen && (
          <div className="account-menu" role="menu">
            <button className="account-menu-item" role="menuitem" onClick={() => setAccountOpen(false)}>
              <span className="menu-icon" aria-hidden>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="1.8"/>
                  <path d="M4 20c0-4 4-6 8-6s8 2 8 6" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                </svg>
              </span>
              <span>Profile</span>
            </button>
            <button className="account-menu-item" role="menuitem" onClick={() => setAccountOpen(false)}>
              <span className="menu-icon" aria-hidden>
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="3.5" stroke="currentColor" strokeWidth="1.8"/>
                  <path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.64 5.64l1.41 1.41M16.95 16.95l1.41 1.41M18.36 5.64l-1.41 1.41M7.05 16.95l-1.41 1.41" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                </svg>
              </span>
              <span>Settings</span>
            </button>
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
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
