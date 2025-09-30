// src/components/ChatWindow.jsx
import React, { useState, useEffect, useRef } from 'react';
import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } from 'docx';
import { saveAs } from 'file-saver';
import { supabase } from '../lib/supabase';

const ChatWindow = ({ messages = [], onSend, isBotThinking = false, onEditMessage, isTemporaryChat = false, onActivateTemporaryChat }) => {

  const [input, setInput] = useState('');
  const [attachedFile, setAttachedFile] = useState(null);
  const [isProcessingFile, setIsProcessingFile] = useState(false);

  // Simple Markdown renderer for basic formatting
  const renderMarkdown = (text) => {
    if (!text) return '';

    return text
      // Links [text](url) - must be done before other formatting
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="chat-link">$1</a>')
      // Bold text **text** or __text__
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/__(.*?)__/g, '<strong>$1</strong>')
      // Italic text *text* or _text_
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/_(.*?)_/g, '<em>$1</em>')
      // Bullet points - item
      .replace(/^- (.*$)/gm, '<li>$1</li>')
      // Numbered lists 1. item
      .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
      // Line breaks
      .replace(/\n/g, '<br>')
      // Double line breaks for paragraphs
      .replace(/\n\n/g, '</p><p>')
      // Wrap in paragraph tags
      .replace(/^(.*)$/gm, '<p>$1</p>')
      // Clean up empty paragraphs
      .replace(/<p><\/p>/g, '')
      // Clean up paragraph tags around list items
      .replace(/<p><li>/g, '<li>')
      .replace(/<\/li><\/p>/g, '</li>')
      // Wrap consecutive list items in ul
      .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
      // Clean up nested ul tags
      .replace(/<ul><ul>/g, '<ul>')
      .replace(/<\/ul><\/ul>/g, '</ul>');
  };
  const [isListening, setIsListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [copiedMessageId, setCopiedMessageId] = useState(null);
  const [editingMessageId, setEditingMessageId] = useState(null);
  const [editText, setEditText] = useState('');
  const [rtiFilingModalOpen, setRtiFilingModalOpen] = useState(false);
  const [rtiFilingData, setRtiFilingData] = useState({
    fullName: '',
    phoneNumber: '',
    email: '',
    address: '',
    attachedFile: null
  });
  const [showWordPreview, setShowWordPreview] = useState(false);
  const [wordPreviewContent, setWordPreviewContent] = useState('');
  const [paymentProcessing, setPaymentProcessing] = useState(false);
  const [paymentSuccess, setPaymentSuccess] = useState(false);
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);
  const recognitionRef = useRef(null);

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

  // Initialize speech recognition
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();

      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onstart = () => {
        setIsListening(true);
        console.log('🎤 Speech recognition started');
      };

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log('🎤 Speech recognized:', transcript);
        setInput(prev => prev + (prev ? ' ' : '') + transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('🎤 Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
        console.log('🎤 Speech recognition ended');
      };

      setSpeechSupported(true);
    } else {
      console.log('🎤 Speech recognition not supported');
      setSpeechSupported(false);
    }
  }, []);

  // Auto-resize textarea as user types
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;

    // Reset height to auto to get the natural height
    el.style.height = 'auto';

    // Calculate the new height, but limit it to a maximum
    const newHeight = Math.min(el.scrollHeight, 80); // Reduced max height to 80px for thinner appearance

    // Set the new height
    el.style.height = `${newHeight}px`;

    // Ensure minimum height
    if (newHeight < 28) {
      el.style.height = '28px';
    }
  }, [input]);

  const handleFileSelect = (event) => {
    console.log('File selection triggered');
    console.log('Event:', event);
    console.log('Files:', event.target.files);

    const file = event.target.files[0];
    if (file) {
      console.log('File selected:', file.name, file.type, file.size);
      // Check if it's a supported file type
      const allowedTypes = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
      ];
      const allowedExtensions = ['.pdf', '.docx', '.txt'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

      if (allowedTypes.includes(file.type) || allowedExtensions.includes(fileExtension)) {
        console.log('Supported file accepted');
        setIsProcessingFile(true);
        setAttachedFile(file);
        // Simulate processing time (you can remove this in production)
        setTimeout(() => {
          setIsProcessingFile(false);
        }, 1000);
      } else {
        console.log('Unsupported file rejected');
        alert('Please select a PDF, Word document (.docx), or text file (.txt).');
        event.target.value = ''; // Clear the input
      }
    } else {
      console.log('No file selected');
    }
  };

  const removeAttachedFile = () => {
    setAttachedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const startVoiceRecording = () => {
    if (!speechSupported) {
      alert('Speech recognition is not supported in this browser. Please use Chrome or Edge.');
      return;
    }

    if (isListening) {
      // Stop recording
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    } else {
      // Start recording
      if (recognitionRef.current) {
        recognitionRef.current.start();
      }
    }
  };

  const copyToClipboard = async (text, messageId) => {
    try {
      await navigator.clipboard.writeText(text);
      console.log('Text copied to clipboard');

      // Show visual feedback
      setCopiedMessageId(messageId);

      // Reset the visual feedback after 2 seconds
      setTimeout(() => {
        setCopiedMessageId(null);
      }, 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);

      // Show visual feedback for fallback too
      setCopiedMessageId(messageId);
      setTimeout(() => {
        setCopiedMessageId(null);
      }, 2000);
    }
  };

  const startEditing = (messageId, text) => {
    setEditingMessageId(messageId);
    setEditText(text);
  };

  const cancelEditing = () => {
    setEditingMessageId(null);
    setEditText('');
  };

  const saveEdit = (messageId) => {
    if (editText.trim()) {
      // Update the message in the parent component
      onEditMessage?.(messageId, editText);
      setEditingMessageId(null);
      setEditText('');
    }
  };

  // Function to generate Word document for RTI filing
  const generateRtiWordDocument = async (messageText) => {
    try {
      // Create document content with proper formatting
      const docContent = [
        new Paragraph({
          text: "Your RTI Draft",
          heading: HeadingLevel.TITLE,
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 }
        }),
        new Paragraph({
          text: "Generated by FileMyRTI Assistant",
          alignment: AlignmentType.CENTER,
          spacing: { after: 600 }
        }),
        new Paragraph({
          text: "─".repeat(50),
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 }
        })
      ];

      // Parse and add formatted content
      const formattedParagraphs = parseMarkdownToWord(messageText);
      docContent.push(...formattedParagraphs);

      // Add footer
      docContent.push(
        new Paragraph({
          text: "",
          spacing: { before: 800 }
        }),
        new Paragraph({
          text: "─".repeat(50),
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 }
        }),
        new Paragraph({
          text: `Generated on ${new Date().toLocaleDateString()} by FileMyRTI Assistant`,
          alignment: AlignmentType.CENTER,
          size: 20
        })
      );

      // Create the document
      const doc = new Document({
        sections: [{
          properties: {},
          children: docContent
        }]
      });

      // Generate blob
      const blob = await Packer.toBlob(doc);
      return blob;
    } catch (error) {
      console.error('Error generating Word document:', error);
      throw error;
    }
  };

  // Function to handle RTI filing button click
  const handleRtiFiling = async (messageText) => {
    try {
      // Generate Word document
      const wordBlob = await generateRtiWordDocument(messageText);

      // Create file object
      const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
      const filename = `RTI_Draft_${timestamp}.docx`;
      const file = new File([wordBlob], filename, { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });

      // Set the attached file in the form data
      setRtiFilingData(prev => ({
        ...prev,
        attachedFile: file
      }));

      // Store the original message text for preview
      setWordPreviewContent(messageText);

      // Open the modal
      setRtiFilingModalOpen(true);
    } catch (error) {
      console.error('Error preparing RTI filing:', error);
      alert('Error preparing RTI filing. Please try again.');
    }
  };

  // Function to preview Word document content
  const handleWordPreview = () => {
    setShowWordPreview(true);
  };

  // Function to close Word preview
  const closeWordPreview = () => {
    setShowWordPreview(false);
  };

  // Razorpay integration functions
  const loadRazorpayScript = () => {
    return new Promise((resolve) => {
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  const handleRazorpayPayment = async () => {
    if (!rtiFilingData.fullName || !rtiFilingData.phoneNumber || !rtiFilingData.email || !rtiFilingData.address) {
      alert('Please fill in all required fields');
      return;
    }

    if (!rtiFilingData.attachedFile) {
      alert('Please attach the RTI draft document');
      return;
    }

    setPaymentProcessing(true);

    try {
      // Load Razorpay script
      const razorpayLoaded = await loadRazorpayScript();
      if (!razorpayLoaded) {
        throw new Error('Failed to load Razorpay');
      }

      // Create payment order
      const formData = new FormData();
      formData.append('full_name', rtiFilingData.fullName);
      formData.append('phone_number', rtiFilingData.phoneNumber);
      formData.append('email', rtiFilingData.email);
      formData.append('address', rtiFilingData.address);
      formData.append('file', rtiFilingData.attachedFile);

      const { data: { session } } = await supabase.auth.getSession();
      const authToken = session?.access_token;

      const response = await fetch('/api/v1/rti-applications/create-payment', {
      method: 'POST',
      headers: authToken ? { Authorization: `Bearer ${authToken}` } : {},
      body: formData
    });

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.message || 'Failed to create payment');
      }

      const { order_id, amount, currency, key_id, application_data } = result.data;

      // Configure Razorpay options
      const options = {
        key: key_id,
        amount: amount,
        currency: currency,
        name: 'FileMyRTI',
        description: 'RTI Application Filing Fee',
        order_id: order_id,
        handler: async function (response) {
          try {
            // Verify payment
            const verifyResponse = await fetch('/api/v1/rti-applications/verify-payment', {
            method: 'POST',
            headers: {
             'Content-Type': 'application/x-www-form-urlencoded',
              ...(authToken ? { Authorization: `Bearer ${authToken}` } : {})
           },
             body: new URLSearchParams({
             payment_id: response.razorpay_payment_id,
             order_id: response.razorpay_order_id,
             signature: response.razorpay_signature,
             application_data: JSON.stringify(application_data)
          })
       });

            const verifyResult = await verifyResponse.json();

            if (verifyResult.success) {
              setPaymentSuccess(true);
              // Don't auto-close the modal - let user close it manually
            } else {
              throw new Error(verifyResult.message || 'Payment verification failed');
            }
          } catch (error) {
            console.error('Payment verification error:', error);
            alert('Payment verification failed. Please contact support.');
          }
        },
        prefill: {
          name: rtiFilingData.fullName,
          email: rtiFilingData.email,
          contact: rtiFilingData.phoneNumber
        },
        theme: {
          color: '#007bff'
        }
      };

      // Open Razorpay checkout
      const razorpay = new window.Razorpay(options);
      razorpay.open();

    } catch (error) {
      console.error('Payment error:', error);
      alert('Payment failed. Please try again.');
    } finally {
      setPaymentProcessing(false);
    }
  };

  // Function to parse Markdown and convert to Word document content
  const parseMarkdownToWord = (text) => {
    const lines = text.split('\n');
    const paragraphs = [];

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      if (!line) {
        // Empty line - add spacing
        paragraphs.push(new Paragraph({
          text: "",
          spacing: { after: 200 }
        }));
        continue;
      }

      // Check for bold text **text** or __text__
      const boldRegex = /\*\*(.*?)\*\*|__(.*?)__/g;
      const italicRegex = /\*(.*?)\*|_(.*?)_/g;

      // Check if line starts with bullet points
      if (line.startsWith('- ') || line.startsWith('• ')) {
        const bulletText = line.substring(2);
        paragraphs.push(new Paragraph({
          children: [
            new TextRun({
              text: "• ",
              bold: true,
              size: 24
            }),
            ...parseInlineFormatting(bulletText)
          ],
          spacing: { after: 150 },
          indent: { left: 720 } // 0.5 inch indent
        }));
      }
      // Check if line starts with numbered list
      else if (/^\d+\.\s/.test(line)) {
        const match = line.match(/^(\d+\.\s)(.*)/);
        if (match) {
          paragraphs.push(new Paragraph({
            children: [
              new TextRun({
                text: match[1],
                bold: true,
                size: 24
              }),
              ...parseInlineFormatting(match[2])
            ],
            spacing: { after: 150 },
            indent: { left: 720 } // 0.5 inch indent
          }));
        }
      }
      // Check for headings (lines that are all bold)
      else if (line.startsWith('**') && line.endsWith('**') && line.length > 4) {
        const headingText = line.replace(/\*\*/g, '');
        paragraphs.push(new Paragraph({
          children: [
            new TextRun({
              text: headingText,
              bold: true,
              size: 28 // Larger font for headings
            })
          ],
          spacing: { before: 300, after: 200 }
        }));
      }
      // Regular paragraph
      else {
        paragraphs.push(new Paragraph({
          children: parseInlineFormatting(line),
          spacing: { after: 200 }
        }));
      }
    }

    return paragraphs;
  };

  // Function to parse inline formatting (bold, italic)
  const parseInlineFormatting = (text) => {
    const runs = [];
    let currentText = text;

    // Process bold text first
    currentText = currentText.replace(/\*\*(.*?)\*\*|__(.*?)__/g, (match, p1, p2) => {
      const boldText = p1 || p2;
      const beforeText = currentText.substring(0, currentText.indexOf(match));
      const afterText = currentText.substring(currentText.indexOf(match) + match.length);

      if (beforeText) {
        runs.push(new TextRun({ text: beforeText, size: 24 }));
      }
      runs.push(new TextRun({ text: boldText, bold: true, size: 24 }));

      currentText = afterText;
      return '';
    });

    // Process italic text
    currentText = currentText.replace(/\*(.*?)\*|_(.*?)_/g, (match, p1, p2) => {
      const italicText = p1 || p2;
      const beforeText = currentText.substring(0, currentText.indexOf(match));
      const afterText = currentText.substring(currentText.indexOf(match) + match.length);

      if (beforeText) {
        runs.push(new TextRun({ text: beforeText, size: 24 }));
      }
      runs.push(new TextRun({ text: italicText, italics: true, size: 24 }));

      currentText = afterText;
      return '';
    });

    // Add remaining text
    if (currentText) {
      runs.push(new TextRun({ text: currentText, size: 24 }));
    }

    return runs.length > 0 ? runs : [new TextRun({ text: text, size: 24 })];
  };

  const downloadLatestBotResponse = () => {
    // Find the latest bot response
    const latestBotMessage = messages
      .filter(msg => msg.sender === 'bot')
      .pop(); // Get the last bot message

    if (!latestBotMessage) {
      alert('No bot response found to download');
      return;
    }

    try {
      // Create document content with proper formatting
      const docContent = [
        new Paragraph({
          text: "Your RTI Draft",
          heading: HeadingLevel.TITLE,
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 }
        }),
        new Paragraph({
          text: "Generated by FileMyRTI Assistant",
          alignment: AlignmentType.CENTER,
          spacing: { after: 600 }
        }),
        new Paragraph({
          text: "─".repeat(50),
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 }
        })
      ];

      // Parse and add formatted content
      const formattedParagraphs = parseMarkdownToWord(latestBotMessage.text);
      docContent.push(...formattedParagraphs);

      // Add footer
      docContent.push(
        new Paragraph({
          text: "",
          spacing: { before: 800 }
        }),
        new Paragraph({
          text: "─".repeat(50),
          alignment: AlignmentType.CENTER,
          spacing: { after: 200 }
        }),
        new Paragraph({
          text: `Generated on ${new Date().toLocaleDateString()} by FileMyRTI Assistant`,
          alignment: AlignmentType.CENTER,
          size: 20
        })
      );

      // Create the document
      const doc = new Document({
        sections: [{
          properties: {},
          children: docContent
        }]
      });

      // Generate and download the document
      Packer.toBlob(doc).then(blob => {
        const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
        const filename = `RTI_Response_${timestamp}.docx`;
        saveAs(blob, filename);
        console.log('Word document downloaded successfully');
      }).catch(error => {
        console.error('Error generating Word document:', error);
        alert('Error generating Word document. Please try again.');
      });

    } catch (error) {
      console.error('Error creating Word document:', error);
      alert('Error creating Word document. Please try again.');
    }
  };

  const sendMessage = () => {
    if (!input.trim() && !attachedFile) return;
    if (typeof onSend === 'function') {
      onSend(input, attachedFile);
    }
    setInput('');
    setAttachedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const hasUserMessage = Array.isArray(messages) && messages.length > 0;

  // Debug logging
  console.log('🎭 ChatWindow - messages prop:', messages);
  console.log('🎭 ChatWindow - messages length:', messages?.length || 0);
  console.log('🎭 ChatWindow - hasUserMessage:', hasUserMessage);
  console.log('🎭 ChatWindow - messages array:', Array.isArray(messages));
  const [highlightInput, setHighlightInput] = useState(false);

  // Wave animation component for bot thinking
  const WaveAnimation = () => (
    <div className="wave-animation">
      <div className="wave-dots">
        <span className="wave-dot">.</span>
        <span className="wave-dot">.</span>
        <span className="wave-dot">.</span>
      </div>
    </div>
  );

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
      {!hasUserMessage && !isTemporaryChat && (
        <button
          className="temp-chat-icon"
          onClick={onActivateTemporaryChat}
          title="Start temporary chat (not saved)"
          aria-label="Start temporary chat"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path d="M4 6h16v9H9l-5 3V6z" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </button>
      )}

      {isTemporaryChat && (
        <div className="temporary-chat-indicator">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" fill="currentColor"/>
          </svg>
          <span>Temporary Chat - Not Saved</span>
        </div>
      )}
      {(() => {
        if (!hasUserMessage) {
          return (
            <div className="chat-landing">
              <div className="brand-row">
                <span className={`brand-text typewriter ${isFinished ? 'finished' : ''}`}>{typedText}</span>
              </div>
              <div className="chat-subtitle">Your RTI assistant • Ask anything about RTI</div>
              <div className={`chat-input-inner ${highlightInput ? 'outline-callout' : ''}`} style={{ position: 'relative' }}>
                <input
                  type="file"
                  ref={fileInputRef}
                  accept=".pdf,.docx,.txt"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                />
                <button
                  className="input-icon attach"
                  title="Attach PDF"
                  onClick={() => {
                    console.log('Attach button clicked');
                    console.log('fileInputRef.current:', fileInputRef.current);
                    fileInputRef.current?.click();
                  }}
                >
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
                  placeholder="Type your query..."
                  className={attachedFile ? 'has-file' : ''}
                />
                {attachedFile && (
                  <div className="file-indicator">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    {attachedFile.name.split('.').pop().toUpperCase()}
                    <button
                      className="remove-file-btn"
                      onClick={removeAttachedFile}
                      title="Remove file"
                    >
                      <svg width="8" height="8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                        <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      </svg>
                    </button>
                  </div>
                )}
                <button className="input-icon download" title="Download latest bot response as Word document" onClick={downloadLatestBotResponse}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <path d="M12 3v10" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                    <path d="M8 11l4 4 4-4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M5 20h14" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                  </svg>
                </button>
                <button
                  className={`input-icon mic ${isListening ? 'listening' : ''} ${!speechSupported ? 'disabled' : ''}`}
                  title={speechSupported ? (isListening ? 'Stop recording' : 'Start voice recording') : 'Voice not supported'}
                  onClick={startVoiceRecording}
                  disabled={!speechSupported}
                >
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
                  <div className={`message-bubble ${msg.sender}`}>
                    {msg.sender === 'bot' && editingMessageId === msg.id ? (
                      <div className="edit-container">
                        <div className="edit-header">
                          <h4>✏️ Edit Response</h4>
                          <p>Make your changes to the bot's response below</p>
                        </div>
                        <textarea
                          value={editText}
                          onChange={(e) => setEditText(e.target.value)}
                          className="edit-textarea"
                          rows="12"
                          placeholder="Edit the response... Make your changes here and click Save when done."
                        />
                        <div className="edit-buttons">
                          <button
                            className="edit-save-btn"
                            onClick={() => saveEdit(msg.id)}
                            title="Save changes"
                          >
                            Save
                          </button>
                          <button
                            className="edit-cancel-btn"
                            onClick={cancelEditing}
                            title="Cancel editing"
                          >
                            Cancel
                          </button>
                        </div>
                      </div>
                    ) : (
                      <>
                        <div
                          className="message-content"
                          dangerouslySetInnerHTML={{
                            __html: renderMarkdown(msg.text)
                          }}
                        />
                        {msg.sender === 'bot' && (
                          <div className="message-actions">
                            <button
                              className={`copy-button ${copiedMessageId === msg.id ? 'copied' : ''}`}
                              onClick={() => copyToClipboard(msg.text, msg.id)}
                              title={copiedMessageId === msg.id ? "Copied!" : "Copy response"}
                              aria-label={copiedMessageId === msg.id ? "Copied!" : "Copy response"}
                            >
                              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" stroke="currentColor" strokeWidth="2"/>
                              </svg>
                            </button>
                            <button
                              className="edit-button"
                              onClick={() => startEditing(msg.id, msg.text)}
                              title="Edit response"
                              aria-label="Edit response"
                            >
                              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                              </svg>
                            </button>
                            <button
                              className="rti-filing-button"
                              onClick={() => handleRtiFiling(msg.text)}
                              title="File RTI with us"
                              aria-label="File RTI with us"
                            >
                              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                                <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2"/>
                                <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" strokeWidth="2"/>
                                <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" strokeWidth="2"/>
                                <polyline points="10,9 9,9 8,9" stroke="currentColor" strokeWidth="2"/>
                              </svg>
                            </button>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              ))}
              {isBotThinking && (
                <div className="message-row bot">
                  <div className="message-bubble bot">
                    <WaveAnimation />
                  </div>
                </div>
              )}
            </div>

            <div className="chat-input">
              <div className="chat-input-inner" style={{ position: 'relative' }}>
                <input
                  type="file"
                  ref={fileInputRef}
                  accept=".pdf,.docx,.txt"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                />
                <button
                  className="input-icon attach"
                  title="Attach PDF"
                  onClick={() => {
                    console.log('Attach button clicked');
                    console.log('fileInputRef.current:', fileInputRef.current);
                    fileInputRef.current?.click();
                  }}
                >
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
                  placeholder="..."
                  className={attachedFile ? 'has-file' : ''}
                />
                {attachedFile && (
                  <div className="file-indicator">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    {attachedFile.name.split('.').pop().toUpperCase()}
                    <button
                      className="remove-file-btn"
                      onClick={removeAttachedFile}
                      title="Remove file"
                    >
                      <svg width="8" height="8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                        <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      </svg>
                    </button>
                  </div>
                )}
                <button className="input-icon download" title="Download latest bot response as Word document" onClick={downloadLatestBotResponse}>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img">
                    <path d="M12 3v10" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                    <path d="M8 11l4 4 4-4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M5 20h14" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
                  </svg>
                </button>
                <button
                  className={`input-icon mic ${isListening ? 'listening' : ''} ${!speechSupported ? 'disabled' : ''}`}
                  title={speechSupported ? (isListening ? 'Stop recording' : 'Start voice recording') : 'Voice not supported'}
                  onClick={startVoiceRecording}
                  disabled={!speechSupported}
                >
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
                {attachedFile && (
                  <div className="file-indicator">
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    {attachedFile.name.split('.').pop().toUpperCase()}
                    <button
                      className="remove-file-btn"
                      onClick={removeAttachedFile}
                      title="Remove file"
                    >
                      <svg width="8" height="8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                        <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                      </svg>
                    </button>
                  </div>
                )}
              </div>
            </div>
          </>
        );
      })()}

      {/* Footer Links */}
      <div style={{ textAlign: 'center', fontSize: '12px', color: '#888', marginBottom: '10px' }}>
        A product of <strong>Ranazonai Technologies</strong> | <a className="muted-link" href="/terms">Terms and Conditions</a> | <a className="muted-link" href="/privacy">Privacy Policy</a>
      </div>

      {/* RTI Filing Modal */}
      {rtiFilingModalOpen && (
        <div className="modal-overlay" onClick={() => {
          setRtiFilingModalOpen(false);
          if (paymentSuccess) {
            setPaymentSuccess(false);
            setRtiFilingData({
              fullName: '',
              phoneNumber: '',
              email: '',
              address: '',
              attachedFile: null
            });
          }
        }}>
          <div className="rti-filing-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="header-left">
                <div className="logo-section">
                  <img src="/filemyrti.png" alt="FileMyRTI" className="modal-logo" />
                  <div className="logo-text">
                    <h2>FileMyRTI</h2>
                    <p>Professional RTI Filing Service</p>
                  </div>
                </div>
              </div>
              <button
                className="modal-close-btn"
                onClick={() => {
                  setRtiFilingModalOpen(false);
                  if (paymentSuccess) {
                    setPaymentSuccess(false);
                    setRtiFilingData({
                      fullName: '',
                      phoneNumber: '',
                      email: '',
                      address: '',
                      attachedFile: null
                    });
                  }
                }}
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" strokeWidth="2"/>
                  <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </button>
            </div>

            <div className="modal-content">
              <div className="content-grid">
                <div className="left-panel">
                  <div className="form-section">
                    <h3>Your Details</h3>
                    <form className="rti-filing-form">
                      <div className="form-row">
                        <div className="form-group">
                          <label htmlFor="fullName">Full Name *</label>
                          <input
                            type="text"
                            id="fullName"
                            value={rtiFilingData.fullName}
                            onChange={(e) => setRtiFilingData(prev => ({ ...prev, fullName: e.target.value }))}
                            placeholder="Enter your full name"
                            required
                          />
                        </div>

                        <div className="form-group">
                          <label htmlFor="phoneNumber">Phone Number *</label>
                          <input
                            type="tel"
                            id="phoneNumber"
                            value={rtiFilingData.phoneNumber}
                            onChange={(e) => setRtiFilingData(prev => ({ ...prev, phoneNumber: e.target.value }))}
                            placeholder="Enter your phone number"
                            required
                          />
                        </div>
                      </div>

                      <div className="form-group">
                        <label htmlFor="email">Email ID *</label>
                        <input
                          type="email"
                          id="email"
                          value={rtiFilingData.email}
                          onChange={(e) => setRtiFilingData(prev => ({ ...prev, email: e.target.value }))}
                          placeholder="Enter your email address"
                          required
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor="address">Address *</label>
                        <textarea
                          id="address"
                          value={rtiFilingData.address}
                          onChange={(e) => setRtiFilingData(prev => ({ ...prev, address: e.target.value }))}
                          placeholder="Enter your complete address"
                          rows="3"
                          required
                        />
                      </div>
                    </form>
                  </div>
                </div>

                <div className="right-panel">
                  <div className="attachment-section">
                    <h3>RTI Draft Document</h3>
                    <div className="file-attachment">
                      {rtiFilingData.attachedFile ? (
                        <div className="attached-file" onClick={handleWordPreview} style={{ cursor: 'pointer' }}>
                          <div className="file-icon">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                              <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2"/>
                            </svg>
                          </div>
                          <div className="file-details">
                            <span className="file-name">{rtiFilingData.attachedFile.name}</span>
                            <span className="file-size">
                              {(rtiFilingData.attachedFile.size / 1024).toFixed(1)} KB
                            </span>
                          </div>
                          <div className="preview-hint">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" strokeWidth="2"/>
                              <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2"/>
                            </svg>
                            <span>Click to preview</span>
                          </div>
                        </div>
                      ) : (
                        <div className="no-file">
                          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                            <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2"/>
                          </svg>
                          <p>RTI draft will be automatically attached</p>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="payment-section">
                    <h3>Payment Details</h3>
                    <div className="payment-info">
                      <div className="fee-display">
                        <span className="fee-label">RTI Filing Fee</span>
                        <span className="fee-amount">₹99</span>
                      </div>
                      <p className="payment-note">Complete payment to submit your RTI application</p>
                    </div>
                    <button
                      className="razorpay-payment-btn"
                      onClick={handleRazorpayPayment}
                      disabled={paymentProcessing || paymentSuccess}
                    >
                      {paymentProcessing ? 'Processing...' : paymentSuccess ? 'Payment Successful!' : 'Pay'}
                    </button>

                    {/* Payment Method Logos */}
                    <div className="payment-logos">
                      <img src="/razorpay.png" alt="Razorpay" className="payment-logo-img" />
                      <img src="/upi-logo.png" alt="UPI" className="payment-logo-img" />
                      <img src="/visa-logo.png" alt="VISA" className="payment-logo-img" />
                      <img src="/mastercard-logo.png" alt="MasterCard" className="payment-logo-img" />
                    </div>
                    <p className="payment-methods-text">Secure payment powered by Razorpay</p>
                    {paymentSuccess && (
                      <div className="payment-success-overlay">
                        <div className="payment-success-content">
                          <h2>Payment Successful!</h2>
                          <h3>✅ Thank you for filing your RTI with FileMyRTI!</h3>
                          <p>Your application will be processed and filed within 12–24 hours.</p>
                          <p>If we need any additional details, our team will contact you.</p>
                          <p>📩 For any queries or extra assistance, reach us at <strong>admin@filemyrti.com</strong> or call/WhatsApp us on <strong>+91 99111 00589</strong>.</p>
                          <button
                            className="close-success-btn"
                            onClick={() => {
                              setRtiFilingModalOpen(false);
                              setPaymentSuccess(false);
                              setRtiFilingData({
                                fullName: '',
                                phoneNumber: '',
                                email: '',
                                address: '',
                                attachedFile: null
                              });
                            }}
                          >
                            Close
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <div className="modal-footer-text">
                <p><strong>We'll contact you, if any additional information is required</strong></p>
                <p><strong>Thank you for using FileMyRTI</strong></p>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* Word Document Preview Modal */}
      {showWordPreview && (
        <div className="modal-overlay" onClick={closeWordPreview}>
          <div className="word-preview-modal" onClick={(e) => e.stopPropagation()}>
            <div className="preview-header">
              <h3>RTI Draft Preview</h3>
              <button
                className="modal-close-btn"
                onClick={closeWordPreview}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" strokeWidth="2"/>
                  <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </button>
            </div>
            <div className="preview-content">
              <div
                className="word-preview-text"
                dangerouslySetInnerHTML={{
                  __html: renderMarkdown(wordPreviewContent)
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWindow;