// src/pages/TermsPage.jsx
import React from 'react';
import '../styles.css';

function TermsPage() {
  return (
    <div style={{ maxWidth: '920px', margin: '40px auto', padding: '0 16px', lineHeight: 1.6 }}>
      <h1>FileMyRTI AI Bot — Terms & Conditions</h1>
      <p><strong>Effective Date:</strong> 9th Sep 2025</p>
      <p>
        Welcome to FileMyRTI AI Bot (“we,” “our,” “us”). By using our AI-powered RTI drafting service available at
        filemyrti.com, you agree to the following Terms & Conditions. Please read carefully before proceeding.
      </p>
      <h3>1. Nature of Service</h3>
      <ul>
        <li>FileMyRTI AI Bot is a technology-enabled drafting assistant that helps users prepare Right to Information (RTI) applications.</li>
        <li>We are not a government portal and are not affiliated with any government department.</li>
        <li>The service provides draft RTI applications in legally accepted formats which you can:
          <ul>
            <li>Download and file yourself, or</li>
            <li>Request us to file on your behalf (paid service).</li>
          </ul>
        </li>
      </ul>
      <h3>2. Eligibility</h3>
      <ul>
        <li>Only Indian citizens are legally permitted to file RTI applications under the RTI Act, 2005.</li>
        <li>By using this service, you confirm that you are an Indian citizen.</li>
      </ul>
      <h3>3. User Responsibilities</h3>
      <ul>
        <li>You agree to provide accurate and truthful information (name, address, email, phone number, details of your RTI request).</li>
        <li>You agree not to misuse the service for:
          <ul>
            <li>Submitting false or fraudulent information.</li>
            <li>Requesting information outside the scope of the RTI Act (e.g., personal questions, reasons, opinions, or exempted information under Section 8).</li>
            <li>Non-RTI related conversations (the bot is limited to RTI drafting only).</li>
          </ul>
        </li>
      </ul>
      <h3>4. Drafting Limitations</h3>
      <ul>
        <li>The AI Bot uses advanced language models to generate RTI drafts. However:
          <ul>
            <li>Drafts are suggestions and may require review for accuracy.</li>
            <li>You are responsible for ensuring correctness before submission.</li>
            <li>We do not guarantee acceptance of every RTI application by the concerned Public Authority.</li>
          </ul>
        </li>
      </ul>
      <h3>5. Filing on Your Behalf</h3>
      <ul>
        <li>If you opt for paid filing:
          <ul>
            <li>Payment will be processed securely through Razorpay or similar gateways.</li>
            <li>Once confirmed, an Application Number will be generated and sent to your email.</li>
            <li>We commit to filing your RTI with the appropriate Public Information Officer (PIO) within 24 hours (excluding Sundays/holidays).</li>
          </ul>
        </li>
      </ul>
      <h3>6. Refunds & Cancellations</h3>
      <ul>
        <li>Draft downloads are free.</li>
        <li>Paid filing service is non-refundable once the application is submitted to the authority.</li>
        <li>If your payment is processed but filing cannot be completed due to reasons attributable to us, a full refund will be issued.</li>
      </ul>
      <h3>7. Limitation of Liability</h3>
      <ul>
        <li>We are not liable for:
          <ul>
            <li>Delays or failures by government departments in responding to RTI applications.</li>
            <li>Rejection of RTI applications by the PIO.</li>
            <li>Losses arising from user-provided incorrect/incomplete information.</li>
          </ul>
        </li>
      </ul>
      <h3>8. Intellectual Property</h3>
      <ul>
        <li>All content, design, and technology of FileMyRTI are protected by copyright and intellectual property laws.</li>
        <li>You may use drafts generated solely for your personal RTI purposes.</li>
      </ul>
      <h3>9. Modifications</h3>
      <ul>
        <li>We reserve the right to update these Terms & Conditions at any time. Updates will be posted on this page with a revised effective date.</li>
      </ul>
      <h3>10. Governing Law</h3>
      <ul>
        <li>These Terms shall be governed by and construed in accordance with the laws of India.</li>
        <li>Jurisdiction: Hyderabad, Telangana.</li>
      </ul>
    </div>
  );
}

export default TermsPage;


