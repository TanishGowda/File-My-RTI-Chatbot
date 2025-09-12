import React from 'react';

function ThemeToggle({ darkMode, setDarkMode }) {
  return (
    <button className="theme-toggle" onClick={() => setDarkMode(!darkMode)}>
      {darkMode ? '🌙 Dark' : '☀️ Light'}
    </button>
  );
}

export default ThemeToggle;
