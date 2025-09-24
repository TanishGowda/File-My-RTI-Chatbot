// src/pages/ChatPage.jsx
import React, { useMemo, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiClient } from '../lib/api';
import { supabase } from '../lib/supabase';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import '../chatstyles.css';

const ChatPage = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isBotThinking, setIsBotThinking] = useState(false);
  const [isTemporaryChat, setIsTemporaryChat] = useState(false);
  const [temporaryMessages, setTemporaryMessages] = useState([]);
  const { user, signOut, loading: authLoading } = useAuth();
  const navigate = useNavigate();

  // State persistence keys
  const STORAGE_KEYS = {
    ACTIVE_CONVERSATION: 'filemyrti_active_conversation',
    CONVERSATIONS: 'filemyrti_conversations',
    MESSAGES: 'filemyrti_messages',
    TEMPORARY_CHAT: 'filemyrti_temporary_chat',
    TEMPORARY_MESSAGES: 'filemyrti_temporary_messages'
  };

  const activeConversation = useMemo(() => {
    if (!Array.isArray(conversations) || conversations.length === 0) {
      return null;
    }
    return conversations.find(c => c.id === activeId) || conversations[0];
  }, [conversations, activeId]);

  // State persistence functions
  const saveStateToStorage = () => {
    try {
      localStorage.setItem(STORAGE_KEYS.ACTIVE_CONVERSATION, activeId || '');
      localStorage.setItem(STORAGE_KEYS.CONVERSATIONS, JSON.stringify(conversations));
      localStorage.setItem(STORAGE_KEYS.MESSAGES, JSON.stringify(messages));
      localStorage.setItem(STORAGE_KEYS.TEMPORARY_CHAT, JSON.stringify(isTemporaryChat));
      localStorage.setItem(STORAGE_KEYS.TEMPORARY_MESSAGES, JSON.stringify(temporaryMessages));
    } catch (error) {
      console.warn('Failed to save state to localStorage:', error);
    }
  };

  const loadStateFromStorage = () => {
    try {
      const savedActiveId = localStorage.getItem(STORAGE_KEYS.ACTIVE_CONVERSATION);
      const savedConversations = localStorage.getItem(STORAGE_KEYS.CONVERSATIONS);
      const savedMessages = localStorage.getItem(STORAGE_KEYS.MESSAGES);
      const savedTemporaryChat = localStorage.getItem(STORAGE_KEYS.TEMPORARY_CHAT);
      const savedTemporaryMessages = localStorage.getItem(STORAGE_KEYS.TEMPORARY_MESSAGES);

      return {
        activeId: savedActiveId || null,
        conversations: savedConversations ? JSON.parse(savedConversations) : [],
        messages: savedMessages ? JSON.parse(savedMessages) : [],
        isTemporaryChat: savedTemporaryChat ? JSON.parse(savedTemporaryChat) : false,
        temporaryMessages: savedTemporaryMessages ? JSON.parse(savedTemporaryMessages) : []
      };
    } catch (error) {
      console.warn('Failed to load state from localStorage:', error);
      return {
        activeId: null,
        conversations: [],
        messages: [],
        isTemporaryChat: false,
        temporaryMessages: []
      };
    }
  };

  const clearStoredState = () => {
    try {
      Object.values(STORAGE_KEYS).forEach(key => {
        localStorage.removeItem(key);
      });
    } catch (error) {
      console.warn('Failed to clear stored state:', error);
    }
  };

  // Save state to localStorage whenever it changes
  useEffect(() => {
    if (user && !loading) {
      saveStateToStorage();
    }
  }, [activeId, conversations, messages, isTemporaryChat, temporaryMessages, user, loading]);

  // Load conversations on component mount
  useEffect(() => {
    console.log('ChatPage mounted, user:', user);
    console.log('User type:', typeof user);
    console.log('User truthy:', !!user);
    console.log('Auth loading:', authLoading);
    
    if (user) {
      console.log('User is authenticated, checking for cached state...');
      
      // Check if we have cached state first
      const savedState = loadStateFromStorage();
      const hasCachedState = savedState.conversations.length > 0 || savedState.activeId;
      
      if (hasCachedState) {
        console.log('✅ Has cached state, restoring immediately');
        // Restore cached state immediately
        setConversations(savedState.conversations);
        setActiveId(savedState.activeId);
        setMessages(savedState.messages);
        setIsTemporaryChat(savedState.isTemporaryChat);
        setTemporaryMessages(savedState.temporaryMessages);
        setLoading(false);
        
        // Load fresh data in background
        console.log('🔄 Syncing with server in background...');
        loadConversations(true);
      } else {
        console.log('No cached state, loading from server...');
        loadConversations();
      }
    } else if (!authLoading) {
      console.log('No user and auth not loading, not loading conversations');
    } else {
      console.log('Auth still loading...');
    }
  }, [user, authLoading]);

  const loadMessages = async (conversationId) => {
    try {
      console.log('🔄 Loading messages for conversation:', conversationId);
      const response = await apiClient.getMessages(conversationId);
      console.log('📡 LoadMessages API response:', response);
      
      if (response.success && Array.isArray(response.data)) {
        const messagesWithIds = response.data.map((msg, index) => ({
          id: `${msg.sender}_${Date.now()}_${index}_${Math.random().toString(36).substr(2, 9)}`,
          text: msg.text || msg.content || '',
          sender: msg.sender || 'bot',
          timestamp: msg.timestamp || msg.created_at || new Date().toISOString()
        }));
        
        console.log('📝 Loaded messages:', messagesWithIds);
        console.log('📝 Message count:', messagesWithIds.length);
        setMessages(messagesWithIds);
      } else {
        console.log('❌ No messages found for conversation:', conversationId);
        setMessages([]);
      }
    } catch (error) {
      console.error('❌ Error loading messages:', error);
      setMessages([]);
    }
  };

  const loadConversations = async (isBackgroundSync = false) => {
    try {
      // Only show loading if this is not a background sync
      if (!isBackgroundSync) {
        setLoading(true);
      }
      console.log('🔄 Loading conversations for user:', user?.id, isBackgroundSync ? '(background sync)' : '');
      
      // First, try to restore state from localStorage
      const savedState = loadStateFromStorage();
      console.log('💾 Loaded saved state:', savedState);
      
      // Use the API client which handles authentication properly
      const response = await apiClient.getConversations();
      console.log('📡 Raw API response:', response);
      
      if (response.success) {
        const convs = Array.isArray(response.data) ? response.data : [];
        
        // Process conversations from database
        const conversationsWithTitles = convs.map(conv => ({
          id: conv.id || '',
          title: conv.title || 'New Chat',
          messages: conv.messages || [],
          created_at: conv.created_at || new Date().toISOString(),
          updated_at: conv.updated_at || new Date().toISOString()
        }));
        
        // Filter out any "New Chat" entries from database
        const existingConversations = conversationsWithTitles.filter(conv => conv.title !== 'New Chat');
        
        // Sort existing conversations by updated_at (most recent first)
        existingConversations.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
        
        console.log('📊 Found existing conversations:', existingConversations.length);
        console.log('📋 Existing conversation titles:', existingConversations.map(c => c.title));
        
        // Check if this is a background sync and we already have state
        if (isBackgroundSync && conversations.length > 0) {
          console.log('🔄 Background sync: updating conversations list while preserving New Chat');
          // Update conversations list but ensure New Chat is present if it was there before
          const hasNewChat = conversations.some(conv => conv.title === 'New Chat');
          let finalConversations = existingConversations;
          
          if (hasNewChat) {
            // Find the existing New Chat from current state
            const existingNewChat = conversations.find(conv => conv.title === 'New Chat');
            if (existingNewChat) {
              finalConversations = [existingNewChat, ...existingConversations];
            }
          }
          
          setConversations(finalConversations);
          return;
        }
        
        // Check if we have a saved active conversation that still exists
        let restoredActiveId = null;
        let restoredMessages = [];
        let restoredTemporaryChat = false;
        let restoredTemporaryMessages = [];
        
        if (savedState.activeId && savedState.activeId !== 'temp-chat') {
          // Check if the saved active conversation still exists in the database
          const savedConversationExists = existingConversations.find(conv => conv.id === savedState.activeId);
          if (savedConversationExists) {
            console.log('✅ Found saved active conversation in database:', savedState.activeId);
            restoredActiveId = savedState.activeId;
            // Load messages for this conversation
            try {
              const messagesResponse = await apiClient.getMessages(savedState.activeId);
              if (messagesResponse.success && messagesResponse.data) {
                restoredMessages = messagesResponse.data.map((msg, index) => ({
                  id: `${msg.sender}_${Date.now()}_${index}_${Math.random().toString(36).substr(2, 9)}`,
                  sender: msg.sender, 
                  text: msg.content,
                  timestamp: msg.created_at
                }));
                console.log('✅ Restored messages for active conversation:', restoredMessages.length);
              }
            } catch (error) {
              console.warn('⚠️ Failed to load messages for restored conversation:', error);
            }
          } else {
            console.log('⚠️ Saved active conversation not found in database, will create new chat');
          }
        } else if (savedState.activeId === 'temp-chat' && savedState.isTemporaryChat) {
          // Restore temporary chat state
          console.log('✅ Restoring temporary chat state');
          restoredTemporaryChat = true;
          restoredTemporaryMessages = savedState.temporaryMessages || [];
          restoredActiveId = 'temp-chat';
        }
        
        // If no valid saved state, create a new chat
        if (!restoredActiveId) {
          const newChat = {
            id: `new-chat-${Date.now()}`,
            title: 'New Chat',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            messages: []
          };
          
          console.log('🆕 Creating new chat with ID:', newChat.id);
          restoredActiveId = newChat.id;
          restoredMessages = [];
        }
        
        // Set up conversations list
        let finalConversations = existingConversations;
        
        // Always ensure there's a "New Chat" available
        const hasNewChat = existingConversations.some(conv => conv.title === 'New Chat') || 
                          (restoredActiveId && restoredActiveId.startsWith('new-chat-'));
        
        if (!hasNewChat) {
          // Create a new "New Chat" if none exists
          const newChat = {
            id: `new-chat-${Date.now()}`,
            title: 'New Chat',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            messages: []
          };
          finalConversations = [newChat, ...existingConversations];
        } else if (restoredActiveId && restoredActiveId.startsWith('new-chat-')) {
          // Use the restored new chat
          const newChat = {
            id: restoredActiveId,
            title: 'New Chat',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            messages: []
          };
          finalConversations = [newChat, ...existingConversations];
        }
        
        // Apply restored state (only if not background sync)
        if (!isBackgroundSync) {
          setConversations(finalConversations);
          setActiveId(restoredActiveId);
          setMessages(restoredMessages);
          setIsTemporaryChat(restoredTemporaryChat);
          setTemporaryMessages(restoredTemporaryMessages);
        } else {
          // Background sync: just update conversations list
          setConversations(finalConversations);
        }
        
        console.log('✅ State restored successfully:', {
          activeId: restoredActiveId,
          messageCount: restoredMessages.length,
          isTemporaryChat: restoredTemporaryChat,
          temporaryMessageCount: restoredTemporaryMessages.length
        });

      } else {
        console.error('❌ Failed to load conversations:', response);
        setError('Failed to load conversations');
        setConversations([]);
      }
    } catch (err) {
      console.error('❌ Error loading conversations:', err);
      
      // Only handle errors if this is not a background sync
      if (!isBackgroundSync) {
        setConversations([]);
        
        // Try to restore from localStorage as fallback
        const savedState = loadStateFromStorage();
        if (savedState.conversations.length > 0) {
          console.log('🔄 Using saved state as fallback');
          setConversations(savedState.conversations);
          setActiveId(savedState.activeId);
          setMessages(savedState.messages);
          setIsTemporaryChat(savedState.isTemporaryChat);
          setTemporaryMessages(savedState.temporaryMessages);
        } else {
          // Create a new chat as last resort
          try {
            console.log('🔄 Creating new chat as last resort...');
            await handleNewChat();
          } catch (newChatError) {
            console.error('❌ Error creating new chat:', newChatError);
            setError('Failed to load conversations and create new chat');
          }
        }
      } else {
        console.log('⚠️ Background sync failed, but keeping current state');
      }
    } finally {
      // Only set loading to false if this is not a background sync
      if (!isBackgroundSync) {
        setLoading(false);
      }
    }
  };


  const handleNewChat = async () => {
    try {
      console.log('🔄 Creating new chat...');
      
      // Exit temporary chat mode if active
      if (isTemporaryChat) {
        console.log('🔄 Exiting temporary chat mode');
        setIsTemporaryChat(false);
        setTemporaryMessages([]);
      }
      
      // Create a fresh "New Chat" locally (no backend call needed)
      const newConv = {
        id: `new-chat-${Date.now()}`,
        title: 'New Chat',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        messages: []
      };
      
      console.log('✅ Creating new conversation with title:', newConv.title, 'ID:', newConv.id);
      
      // Remove any existing "New Chat" entries before adding the new one
      setConversations(prev => {
        const filtered = prev.filter(conv => conv.title !== 'New Chat');
        return [newConv, ...filtered];
      });
      
      setActiveId(newConv.id);
      
      // Don't set any messages - let ChatWindow show the landing page welcome screen
      setMessages([]);
      
      console.log('✅ New Chat created successfully:', newConv.id);
      console.log('✅ New Chat is now active and shows welcome screen');
    } catch (err) {
      console.error('❌ Error creating new chat:', err);
      setError('Failed to create new chat');
    }
  };

  const handleDeleteConversation = async (conversationId, event) => {
    event.stopPropagation(); // Prevent triggering conversation selection
    
    // Don't allow deletion of "New Chat" conversations
    const conversation = conversations.find(conv => conv.id === conversationId);
    if (conversation?.title === 'New Chat') {
      console.log('❌ Cannot delete New Chat conversation');
      return;
    }
    
    // Show confirmation dialog
    const confirmed = window.confirm('Are you sure you want to delete this conversation? This action cannot be undone.');
    if (!confirmed) return;

    try {
      console.log('🗑️ Deleting conversation:', conversationId);
      const response = await apiClient.deleteConversation(conversationId);
      
      if (response.success) {
        console.log('✅ Conversation deleted successfully');
        
        // Remove from conversations list
        setConversations(prev => prev.filter(conv => conv.id !== conversationId));
        
        // If the deleted conversation was active, handle the transition
        if (activeId === conversationId) {
          // Get remaining conversations after deletion
          const remainingConversations = conversations.filter(conv => conv.id !== conversationId);
          
          if (remainingConversations.length > 0) {
            // Select the first remaining conversation
            const nextConversation = remainingConversations[0];
            setActiveId(nextConversation.id);
            
            // Load messages for the new active conversation
            if (nextConversation.title === 'New Chat') {
              // Show landing page welcome screen for New Chat
              setMessages([]);
            } else {
              // Load messages from API for existing conversation
              try {
                const messagesResponse = await apiClient.getMessages(nextConversation.id);
                if (messagesResponse.success && messagesResponse.data) {
                  const formattedMessages = messagesResponse.data.map((msg, index) => ({
                    id: `${msg.sender}_${Date.now()}_${index}_${Math.random().toString(36).substr(2, 9)}`,
                    sender: msg.sender, 
                    text: msg.content,
                    timestamp: msg.created_at
                  }));
                  setMessages(formattedMessages);
                } else {
                  setMessages([]);
                }
              } catch (error) {
                console.error('❌ Error loading messages for new active conversation:', error);
                setMessages([]);
              }
            }
          } else {
            // No conversations left, create a new one
            await handleNewChat();
          }
        }
      } else {
        console.error('❌ Failed to delete conversation:', response);
        alert('Failed to delete conversation. Please try again.');
      }
    } catch (error) {
      console.error('❌ Error deleting conversation:', error);
      alert('Error deleting conversation. Please try again.');
    }
  };

  const handleEditMessage = (messageId, newText) => {
    console.log('✏️ Editing message:', messageId, 'with new text:', newText);
    
    // Find the message to ensure it's a bot message
    const messageToEdit = messages.find(msg => msg.id === messageId);
    if (!messageToEdit) {
      console.error('❌ Message not found:', messageId);
      return;
    }
    
    if (messageToEdit.sender !== 'bot') {
      console.error('❌ Cannot edit user messages, only bot messages can be edited');
      alert('You can only edit bot responses, not your own messages.');
      return;
    }
    
    // Update the message in the messages state
    setMessages(prevMessages => 
      prevMessages.map(msg => 
        msg.id === messageId 
          ? { ...msg, text: newText }
          : msg
      )
    );
    
    // Also update the conversation in the conversations state
    setConversations(prevConversations =>
      prevConversations.map(conv => {
        if (conv.id === activeId) {
          return {
            ...conv,
            messages: conv.messages.map(msg =>
              msg.id === messageId
                ? { ...msg, text: newText }
                : msg
            )
          };
        }
        return conv;
      })
    );
    
    console.log('✅ Bot message edited successfully');
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

  const activateTemporaryChat = () => {
    console.log('🔄 Activating temporary chat');
    setIsTemporaryChat(true);
    setTemporaryMessages([]);
    setActiveId('temp-chat');
    setMessages([]);
  };

  const handleSend = async (text, attachedFile = null) => {
    if (!activeId) return;

    try {
      // Set bot thinking state
      setIsBotThinking(true);
      
      // Handle temporary chat differently
      if (isTemporaryChat) {
        console.log('🔄 Sending message in temporary chat mode');
        
        // Add user message to temporary messages
        const userMessage = { 
          id: `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          sender: 'user', 
          text,
          ...(attachedFile && { attachedFile: { name: attachedFile.name, type: attachedFile.type } })
        };
        
        setTemporaryMessages(prev => [...prev, userMessage]);
        
        // Send to backend but don't store in database
        // Use FormData for consistency with regular chat
        const formData = new FormData();
        formData.append('message', text);
        formData.append('conversation_id', ''); // Empty string for temporary chat
        formData.append('user_id', user?.id || "8558702c-5437-47b8-87e2-e70576d1c77d");
        
        if (attachedFile) {
          formData.append('file', attachedFile);
        }
        
        // Get auth token
        const { data: { session } } = await supabase.auth.getSession();
        const authToken = session?.access_token || "test-token";
        
        const response = await fetch('http://localhost:8000/api/v1/chat/send', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${authToken}`
            // Note: Don't set Content-Type for FormData, let browser set it with boundary
          },
          body: formData
        });
        
        const data = await response.json();
        
        if (data.message) {
          const botMessage = {
            id: `bot_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            sender: 'bot',
            text: data.message,
            timestamp: new Date().toISOString()
          };
          
          setTemporaryMessages(prev => [...prev, botMessage]);
        } else {
          const errorMessage = {
            id: `bot_error_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            sender: 'bot',
            text: 'Sorry, I encountered an error. Please try again.',
            timestamp: new Date().toISOString()
          };
          
          setTemporaryMessages(prev => [...prev, errorMessage]);
        }
        
        setIsBotThinking(false);
        return;
      }
      
      // Regular chat handling
      const currentConv = conversations.find(conv => conv.id === activeId);
      const messages = currentConv?.messages || [];
      // Check if this is the first user message (conversation has 0 messages or only bot welcome message)
      const isFirstUserMessage = messages.length === 0 || (messages.length === 1 && messages[0].sender === 'bot');
      let newTitle = null;
      let conversationId = activeId;
      
      console.log('🔄 Sending message:', {
        activeId: activeId,
        currentConv: currentConv?.title,
        isFirstUserMessage: isFirstUserMessage,
        messageText: text
      });
      
      // If this is a "New Chat" and first user message, the backend will create the conversation
      // We'll update the frontend with the new conversation ID when we get the response
      if (currentConv?.title === 'New Chat' && isFirstUserMessage) {
        console.log('🎯 This is a New Chat with first user message - backend will create conversation');
        newTitle = generateConversationTitle(text);
      }

      // Add user message to UI immediately
      const userMessage = { 
        id: `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        sender: 'user', 
        text,
        ...(attachedFile && { attachedFile: { name: attachedFile.name, type: attachedFile.type } })
      };
      
      // Update messages state immediately
      setMessages(prev => [...prev, userMessage]);
      
      setConversations(prev => prev.map(conv => {
        if (conv.id !== activeId) return conv;
        
        const updatedConv = {
          ...conv,
          messages: [...messages, userMessage]
        };
        
        // Update conversation title if this is the first user message
        if (newTitle) {
          updatedConv.title = newTitle;
        }
        
        return updatedConv;
      }));

      // Prepare form data for file upload
      const formData = new FormData();
      formData.append('message', text);
      formData.append('conversation_id', conversationId);
      formData.append('user_id', user?.id || "8558702c-5437-47b8-87e2-e70576d1c77d");
      
      if (attachedFile) {
        formData.append('file', attachedFile);
      }

      // Send message to AI backend using direct fetch with real auth token
      console.log('📤 Sending message to AI:', text, attachedFile ? `with file: ${attachedFile.name}` : '');
      
      // Get auth token from Supabase
      const { data: { session } } = await supabase.auth.getSession();
      const authToken = session?.access_token || 'test-token';
      
      const response = await fetch('http://localhost:8000/api/v1/chat/send', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`
          // Note: Don't set Content-Type for FormData, let browser set it with boundary
        },
        body: formData
      });
      
      const data = await response.json();
      console.log('📥 AI response:', data);
      
      if (data.message) {
        // Check if we got a new conversation ID from the backend
        if (data.conversation_id && data.conversation_id !== conversationId) {
          console.log('🔄 Updating conversation ID from backend:', data.conversation_id);
          conversationId = data.conversation_id;
          
          // Update the conversation ID in frontend state
          setConversations(prev => prev.map(conv => 
            conv.id === activeId 
              ? { ...conv, id: conversationId, title: newTitle || conv.title }
              : conv
          ));
          setActiveId(conversationId);
        }
        
        // Add bot response to UI
        const botMessage = { 
          id: `bot_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          sender: 'bot', 
          text: data.message 
        };
        
        // Update messages state
        setMessages(prev => [...prev, botMessage]);
        
        setConversations(prev => prev.map(conv => {
          if (conv.id !== conversationId) return conv;
          return {
            ...conv,
            messages: [...conv.messages, botMessage]
          };
        }));
      } else {
        console.error('❌ No message in AI response:', data);
        setError('Failed to get AI response');
      }
    } catch (err) {
      console.error('❌ Error sending message:', err);
      setError('Failed to send message');
      
      // Add error message to UI
      const errorMessage = { 
        id: `bot_error_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        sender: 'bot', 
        text: 'Sorry, I encountered an error. Please try again.' 
      };
      
      setMessages(prev => [...prev, errorMessage]);
      setConversations(prev => prev.map(conv => {
        if (conv.id !== activeId) return conv;
        return {
          ...conv,
          messages: [...conv.messages, errorMessage]
        };
      }));
    } finally {
      // Stop bot thinking state
      setIsBotThinking(false);
    }
  };

  const handleSelectConversation = async (id) => {
    console.log('🔄 SELECTING CONVERSATION:', id);
    
    // Exit temporary chat mode if switching to a regular conversation
    if (isTemporaryChat) {
      console.log('🔄 Exiting temporary chat mode');
      setIsTemporaryChat(false);
      setTemporaryMessages([]);
    }
    
    // Find the conversation to get its title
    const conversation = conversations.find(conv => conv.id === id);
    console.log('📋 Selected conversation:', conversation?.title);
    console.log('📋 Conversation details:', conversation);
    
    // Set active conversation immediately
    setActiveId(id);
    
    // Check if this is a "New Chat" conversation
    if (conversation?.title === 'New Chat') {
      console.log('🆕 This is a New Chat - showing landing page welcome screen');
      // Don't set any messages - let ChatWindow show the landing page welcome screen
      setMessages([]);
      return;
    }
    
    // For existing conversations, load messages from API
    try {
      console.log('🔍 Loading messages for conversation:', id);
      const response = await apiClient.getMessages(id);
      console.log('📡 Messages API response:', response);
      
      if (response.success && response.data && response.data.length > 0) {
        // Format messages for display
        const formattedMessages = response.data.map((msg, index) => ({
          id: `${msg.sender}_${Date.now()}_${index}_${Math.random().toString(36).substr(2, 9)}`,
          sender: msg.sender, 
          text: msg.content,
          timestamp: msg.created_at
        }));
        
        console.log('✅ Loaded messages for conversation:', id, 'Count:', formattedMessages.length);
        console.log('📝 Message details:', formattedMessages.map(m => ({ sender: m.sender, text: m.text.substring(0, 100) + '...' })));
        setMessages(formattedMessages);
        
        // Update the conversation in memory with the loaded messages
        setConversations(prev => prev.map(conv => 
          conv.id === id 
            ? { ...conv, messages: formattedMessages }
            : conv
        ));
        
      } else {
        console.log('❌ No messages found for conversation:', id);
        setMessages([]);
      }
    } catch (error) {
      console.error('❌ Error loading messages for conversation:', id, error);
      setMessages([]);
    }
  };

  const handleSignOut = async () => {
    try {
      // Clear stored state before signing out
      clearStoredState();
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
          onDelete={handleDeleteConversation}
          onSignOut={handleSignOut}
          user={user}
        />
        <ChatWindow
          key={activeId}
          messages={isTemporaryChat ? temporaryMessages : messages}
          onSend={handleSend}
          isBotThinking={isBotThinking}
          onEditMessage={handleEditMessage}
          isTemporaryChat={isTemporaryChat}
          onActivateTemporaryChat={activateTemporaryChat}
        />
      </div>
    </div>
  );
};

export default ChatPage;
