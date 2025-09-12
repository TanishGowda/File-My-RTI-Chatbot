// src/pages/PrivacyPage.jsx
import React from 'react';
import '../styles.css';

function PrivacyPage() {
  return (
    <div style={{ maxWidth: '920px', margin: '40px auto', padding: '0 16px', lineHeight: 1.6 }}>
      <h1>FileMyRTI AI Bot — Privacy Policy</h1>
      <p><strong>Effective Date:</strong> 9th Sep 2025</p>
      <p>
        At FileMyRTI, your privacy is important to us. This Privacy Policy explains how we collect, use, and safeguard your
        data when you use our AI Bot.
      </p>
      <h3>1. Information We Collect</h3>
      <ul>
        <li><strong>Personal Information:</strong> Name, email, phone number, postal address (for drafting RTI applications).</li>
        <li><strong>RTI Application Details:</strong> Information you request under RTI (application numbers, department names, etc.).</li>
        <li><strong>Payment Information:</strong> Processed securely via third-party gateways (we do not store card/UPI details).</li>
        <li><strong>Usage Data:</strong> Device type, IP address, browser type, and interaction logs for security and analytics.</li>
      </ul>
      <h3>2. How We Use Your Information</h3>
      <ul>
        <li>To generate RTI drafts accurately.</li>
        <li>To process and confirm payments (if you choose paid filing).</li>
        <li>To file your RTI with the correct authority.</li>
        <li>To send confirmation emails, updates, and tracking numbers.</li>
        <li>To improve our AI bot’s accuracy and user experience.</li>
      </ul>
      <h3>3. Data Sharing</h3>
      <ul>
        <li>We do not sell or rent your personal data.</li>
        <li>Your details are shared only with:
          <ul>
            <li>The relevant government authority (for filing your RTI).</li>
            <li>Payment gateways (for secure transaction processing).</li>
          </ul>
        </li>
        <li>Internal staff/RTI experts who handle filing are bound by strict confidentiality.</li>
      </ul>
      <h3>4. Data Security</h3>
      <ul>
        <li>All data is encrypted during transmission (HTTPS/TLS).</li>
        <li>Stored data is protected with access controls and periodic audits.</li>
        <li>Draft RTI chats may be anonymized and used for service improvement.</li>
      </ul>
      <h3>5. Your Rights</h3>
      <ul>
        <li>You may request deletion of your account and data at any time by contacting us.</li>
        <li>You may request a copy of your stored RTI drafts and submissions.</li>
      </ul>
      <h3>6. Data Retention</h3>
      <ul>
        <li>RTI drafts and user details are retained for 90 days to allow tracking and appeals, after which they may be deleted or anonymized.</li>
        <li>Payment and legal compliance data may be retained as per applicable laws.</li>
      </ul>
      <h3>7. Third-Party Links</h3>
      <ul>
        <li>Our platform may contain links to official government RTI portals or blogs. We are not responsible for the privacy practices of external sites.</li>
      </ul>
      <h3>8. Changes to Policy</h3>
      <ul>
        <li>We may update this Privacy Policy periodically. Changes will be posted on this page with the revised date.</li>
      </ul>
      <h3>9. Contact Us</h3>
      <p>
        For questions or requests about this policy, contact:<br/>
        📧 admin@filemyrti.com<br/>
        📍 Hyderabad, Telangana, India
      </p>
    </div>
  );
}

export default PrivacyPage;


