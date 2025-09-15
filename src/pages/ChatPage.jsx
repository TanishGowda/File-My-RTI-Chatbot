// src/pages/ChatPage.jsx
import React, { useMemo, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiClient } from '../lib/api';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import '../chatstyles.css';

const ChatPage = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user, signOut, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  const activeConversation = useMemo(() => 
    conversations.find(c => c.id === activeId) || conversations[0], 
    [conversations, activeId]
  );

  // Load conversations on component mount
  useEffect(() => {
    console.log('ChatPage mounted, user:', user);
    console.log('User type:', typeof user);
    console.log('User truthy:', !!user);
    console.log('Auth loading:', authLoading);
    if (user) {
      console.log('User is authenticated, loading conversations...');
      loadConversations();
    } else if (!authLoading) {
      console.log('No user and auth not loading, not loading conversations');
    } else {
      console.log('Auth still loading...');
    }
  }, [user, authLoading]);

  const loadConversations = async () => {
    try {
      setLoading(true);
      console.log('Loading conversations...');
      
      // First test if backend is reachable
      try {
        const testResponse = await fetch('http://localhost:8000/api/v1/chat/conversations', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token'
          }
        });
        console.log('Backend test response status:', testResponse.status);
        if (testResponse.status === 200) {
          console.log('Backend is reachable!');
        } else {
          console.log('Backend returned status:', testResponse.status);
        }
      } catch (testError) {
        console.error('Backend test failed:', testError);
      }
      
      // Add timeout to prevent hanging
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Request timeout')), 15000)
      );
      
      // Use direct fetch instead of API client for now
      const response = await Promise.race([
        fetch('http://localhost:8000/api/v1/chat/conversations', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token'
          }
        }).then(res => res.json()),
        timeoutPromise
      ]);
      
      if (response.success) {
        const convs = response.data || [];
        console.log('Loaded conversations:', convs.length);
        
        // Ensure all conversations have proper titles
        const conversationsWithTitles = convs.map(conv => ({
          ...conv,
          title: conv.title || 'New Chat'
        }));
        
        setConversations(conversationsWithTitles);
        
        // Set active conversation to the first one or create a new one
        if (conversationsWithTitles.length > 0) {
          setActiveId(conversationsWithTitles[0].id);
        } else {
          // Only try to create new chat if we haven't already tried
          if (!activeId) {
            console.log('No conversations found, creating new chat...');
            await handleNewChat();
          }
        }
      } else {
        console.error('Failed to load conversations:', response);
        setError('Failed to load conversations');
      }
    } catch (err) {
      console.error('Error loading conversations:', err);
      if (err.message === 'Request timeout') {
        console.log('Conversations timed out, creating new chat...');
        // Create a new chat as fallback
        try {
          await handleNewChat();
        } catch (newChatError) {
          console.error('Error creating new chat:', newChatError);
          setError('Failed to load conversations and create new chat');
        }
      } else {
        setError('Failed to load conversations');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = async () => {
    try {
      console.log('Creating new chat...');
      
      // Use direct fetch instead of API client
      const response = await fetch('http://localhost:8000/api/v1/chat/conversations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test-token'
        },
        body: JSON.stringify({ title: 'New Chat' })
      });
      
      const data = await response.json();
      console.log('Create conversation response:', data);
      
      if (data.success) {
        const newConv = {
          ...data.data,
          title: 'New Chat', // Ensure title is set
          messages: [
            { sender: 'bot', text: 'Hi! Tell me what RTI you want to draft today.' },
          ],
        };
        console.log('Creating new conversation with title:', newConv.title);
        setConversations(prev => [newConv, ...prev]);
        setActiveId(newConv.id);
        console.log('New chat created successfully:', newConv.id);
      } else {
        console.error('Failed to create new chat:', data);
        setError('Failed to create new chat');
      }
    } catch (err) {
      console.error('Error creating new chat:', err);
      setError('Failed to create new chat');
    }
  };

  const generateConversationTitle = (userMessage) => {
    // Generate a meaningful title from the first user message
    console.log('Generating title for message:', userMessage);
    const words = userMessage.trim().split(' ');
    if (words.length <= 3) {
      console.log('Short message, using full text:', userMessage);
      return userMessage;
    }
    
    // Take first few words and add ellipsis if needed
    const title = words.slice(0, 4).join(' ');
    const finalTitle = title.length < userMessage.length ? title + '...' : title;
    console.log('Generated title:', finalTitle);
    return finalTitle;
  };

  const handleSend = async (text) => {
    if (!activeId) return;

    try {
      // Add user message to UI immediately
      setConversations(prev => prev.map(conv => {
        if (conv.id !== activeId) return conv;
        
        // Check if this is the first user message (only bot message exists)
        const isFirstUserMessage = conv.messages.length === 1 && conv.messages[0].sender === 'bot';
        console.log('Conversation state:', {
          id: conv.id,
          title: conv.title,
          messageCount: conv.messages.length,
          isFirstUserMessage,
          messages: conv.messages
        });
        
        const updatedConv = {
          ...conv,
          messages: [...conv.messages, { sender: 'user', text }]
        };
        
        // Update conversation title if this is the first user message
        if (conv.title === 'New Chat' && isFirstUserMessage) {
          updatedConv.title = generateConversationTitle(text);
          console.log('Updating conversation title to:', updatedConv.title);
        }
        
        return updatedConv;
      }));

      // Send message to AI backend using direct fetch
      console.log('Sending message to AI:', text);
      const response = await fetch('http://localhost:8000/api/v1/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test-token'
        },
        body: JSON.stringify({
          message: text,
          conversation_id: activeId,
          user_id: "550e8400-e29b-41d4-a716-446655440000"
        })
      });
      
      const data = await response.json();
      console.log('AI response:', data);
      
      if (data.message) {
        // Add bot response to UI
        setConversations(prev => prev.map(conv => {
          if (conv.id !== activeId) return conv;
          return {
            ...conv,
            messages: [...conv.messages, { 
              sender: 'bot', 
              text: data.message 
            }]
          };
        }));
      } else {
        console.error('No message in AI response:', data);
        setError('Failed to get AI response');
      }
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message');
    }
  };

  const handleSelectConversation = async (id) => {
    console.log('Selecting conversation:', id);
    setActiveId(id);
    
    // Check if conversation already has messages in state
    const conversation = conversations.find(conv => conv.id === id);
    if (conversation && conversation.messages && conversation.messages.length > 0) {
      console.log('Conversation already has messages in state, no need to load');
      return;
    }
    
    // For now, just initialize with empty messages if none exist
    // The backend API for getting messages might not be working properly
    console.log('Initializing conversation with empty messages');
    setConversations(prev => prev.map(conv => 
      conv.id === id 
        ? { ...conv, messages: conv.messages || [] }
        : conv
    ));
    
    // TODO: Implement proper message loading from backend when API is fixed
    // try {
    //   console.log('Loading messages for conversation:', id);
    //   const response = await apiClient.getMessages(id);
    //   
    //   if (response.success) {
    //     const messages = response.data || [];
    //     console.log('Loaded messages from backend:', messages);
    //     setConversations(prev => prev.map(conv => 
    //       conv.id === id 
    //         ? { ...conv, messages: messages.map(msg => ({ 
    //             sender: msg.sender, 
    //             text: msg.content 
    //           })) }
    //         : conv
    //     ));
    //   } else {
    //     console.log('No messages found in backend for conversation:', id);
    //   }
    // } catch (err) {
    //   console.error('Error loading messages:', err);
    //   // Don't show error to user, just continue with empty messages
    // }
  };

  const handleSignOut = async () => {
    try {
      await signOut();
      navigate('/auth');
    } catch (err) {
      console.error('Error signing out:', err);
    }
  };

  if (loading || authLoading) {
    return (
      <div className={`app ${darkMode ? 'dark' : ''}`}>
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column',
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh',
          fontSize: '18px'
        }}>
          <div>Loading...</div>
          <div>User: {user ? 'Present' : 'Not present'}</div>
          <div>Auth Loading: {authLoading ? 'Yes' : 'No'}</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`app ${darkMode ? 'dark' : ''}`}>
        <div style={{ 
          display: 'flex', 
          flexDirection: 'column',
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh',
          fontSize: '18px',
          gap: '20px'
        }}>
          <div style={{ color: '#ff4444' }}>Error: {error}</div>
          <button 
            onClick={loadConversations}
            style={{
              padding: '10px 20px',
              backgroundColor: '#4f46e5',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`app ${darkMode ? 'dark' : ''}`}>
      <div className={`chat-layout ${sidebarOpen ? '' : 'sidebar-collapsed'}`}>
        <Sidebar
          darkMode={darkMode}
          setDarkMode={setDarkMode}
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
          conversations={conversations}
          activeId={activeId}
          onSelect={handleSelectConversation}
          onNewChat={handleNewChat}
          onSignOut={handleSignOut}
          user={user}
        />
        <ChatWindow
          key={activeId}
          messages={activeConversation?.messages || []}
          onSend={handleSend}
        />
      </div>
    </div>
  );
};

export default ChatPage;
