// src/pages/FileRTIPage.jsx
import React from 'react';
import '../authstyles.css';

function FileRTIPage() {
  return (
    <div className="auth-container">
      <div className="auth-box" style={{ maxWidth: '520px', width: '100%' }}>
        <img src="/filemyrti.png" alt="FileMyRTI" className="auth-logo" />
        <h2 style={{ fontSize: '28px', marginTop: '6px' }}>File the RTI with Us?</h2>

        <form className="auth-form" style={{ width: '100%' }}>
          <input type="text" placeholder="Full Name" />
          <input type="email" placeholder="Email" />
          <input type="tel" placeholder="Mobile Number" />
          <textarea placeholder="Address" rows={4} style={{ padding: '10px', borderRadius: '6px', border: '1px solid #ccc', resize: 'vertical' }} />
        </form>

        <div style={{ marginTop: '16px', width: '100%' }}>
          <button className="razorpay-btn" type="button" title="Pay now (UI only)">
            <span>Pay with Razorpay • ₹199</span>
          </button>
        </div>
        <div style={{ marginTop: '12px', fontSize: '12px', color: '#888' }}>
          <a className="muted-link" href="/terms">Terms and Conditions</a> | <a className="muted-link" href="/privacy">Privacy Policy</a>
        </div>
      </div>
    </div>
  );
}

export default FileRTIPage;


