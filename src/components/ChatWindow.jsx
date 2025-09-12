// src/components/ChatWindow.jsx
import React, { useState, useEffect, useRef } from 'react';

const ChatWindow = ({ messages = [], onSend }) => {

  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  // Typing effect for branding text
  const fullText = 'Welcome to FileMyRTI !!!';
  const [typedText, setTypedText] = useState('');
  const [isFinished, setIsFinished] = useState(false); // 👈 New state

  useEffect(() => {
    setTypedText('');
    setIsFinished(false);

    setTimeout(() => {
      let index = 0;

      const typeNextChar = () => {
        setTypedText((prev) => {
          const next = prev + fullText.charAt(index);
          index++;
          if (index < fullText.length) {
            setTimeout(typeNextChar, 75);
          } else {
            setIsFinished(true);
          }
          return next;
        });
      };

      typeNextChar();
    }, 20);
  }, []);

  // Auto-resize textarea as user types
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = '0px';
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }, [input]);

  const sendMessage = () => {
    if (!input.trim()) return;
    if (typeof onSend === 'function') {
      onSend(input);
    }
    setInput('');
  };

  const hasUserMessage = Array.isArray(messages) && messages.some((m) => m.sender === 'user');
  const [highlightInput, setHighlightInput] = useState(false);

  const triggerHighlight = () => {
    if (!hasUserMessage) {
      setHighlightInput((prev) => !prev);
    }
  };

  useEffect(() => {
    if (hasUserMessage && highlightInput) {
      setHighlightInput(false);
    }
  }, [hasUserMessage]);

  return (
    <div className="chat-window">
      {!hasUserMessage && (
        <button
          className="temp-chat-icon"
          onClick={triggerHighlight}
          title="Start chatting"
          aria-label="Start chatting"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M4 6h16v9H9l-5 3V6z" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      )}
      {(() => {
        if (!hasUserMessage) {
          return (
            <div className="chat-landing">
              <div className="brand-row">
                <span className={`brand-text typewriter ${isFinished ? 'finished' : ''}`}>{typedText}</span>
              </div>
              <div className="chat-subtitle">Your RTI assistant • Ask anything about RTI</div>
              <div className={`chat-input-inner ${highlightInput ? 'outline-callout' : ''}`}>
                <button className="input-icon attach" title="Attach (coming soon)">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <path d="M7 13l5.586-5.586a2 2 0 112.828 2.828L9.828 16.828a4 4 0 11-5.657-5.657L12 3" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      sendMessage();
                    }
                  }}
                  rows={1}
                  placeholder="How can I help you.....?"
                />
                <button className="input-icon download" title="Download draft (coming soon)">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <path d="M12 3v10" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                    <path d="M8 11l4 4 4-4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M5 20h14" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                  </svg>
                </button>
                <button className="input-icon mic" title="Voice (coming soon)">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <rect x="9" y="3" width="6" height="12" rx="3" stroke="currentColor" strokeWidth="1.8"/>
                    <path d="M6 11v1a6 6 0 0012 0v-1" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                    <path d="M12 19v2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                  </svg>
                </button>
                <button className="send-circle" onClick={sendMessage} title="Send">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <path d="M4 11l15-7-7 15-1.5-6.5L4 11z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" fill="none"/>
                  </svg>
                </button>
              </div>
            </div>
          );
        }

        return (
          <>
            <div className="chat-history">
              {messages.map((msg, i) => (
                <div key={i} className={`message-row ${msg.sender}`}>
                  <div className={`avatar ${msg.sender}`}>{msg.sender === 'user' ? 'U' : 'R'}</div>
                  <div className={`message-bubble ${msg.sender}`}>
                    {msg.text.split('\n').map((line, idx) => (
                      <div key={idx}>{line}</div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="chat-input">
              <div className="chat-input-inner">
                <button className="input-icon attach" title="Attach (coming soon)">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <path d="M7 13l5.586-5.586a2 2 0 112.828 2.828L9.828 16.828a4 4 0 11-5.657-5.657L12 3" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      sendMessage();
                    }
                  }}
                  rows={1}
                  placeholder="How can I help you.....?"
                />
                <button className="input-icon download" title="Download draft (coming soon)">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <path d="M12 3v10" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                    <path d="M8 11l4 4 4-4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M5 20h14" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                  </svg>
                </button>
                <button className="input-icon mic" title="Voice (coming soon)">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <rect x="9" y="3" width="6" height="12" rx="3" stroke="currentColor" strokeWidth="1.8"/>
                    <path d="M6 11v1a6 6 0 0012 0v-1" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                    <path d="M12 19v2" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                  </svg>
                </button>
                <button className="send-circle" onClick={sendMessage} title="Send">
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <path d="M4 11l15-7-7 15-1.5-6.5L4 11z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" fill="none"/>
                  </svg>
                </button>
              </div>
            </div>
          </>
        );
      })()}

      {/* Footer Links */}
      <div style={{ textAlign: 'center', fontSize: '12px', color: '#888', marginBottom: '10px' }}>
        A product of <strong>Ranazonai Technologies</strong> | <a className="muted-link" href="/terms">Terms and Conditions</a> | <a className="muted-link" href="/privacy">Privacy Policy</a>
      </div>
    </div>
  );
};

export default ChatWindow;
