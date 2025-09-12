// src/pages/ChatPage.jsx
import React, { useMemo, useState } from 'react';
import Sidebar from '../components/Sidebar';
import ChatWindow from '../components/ChatWindow';
import '../chatstyles.css';

const ChatPage = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [conversations, setConversations] = useState([
    {
      id: 'c1',
      title: 'RTI for Passport Delay',
      messages: [
        { sender: 'bot', text: 'Hi! Tell me what RTI you want to draft today.' },
      ],
    },
  ]);
  const [activeId, setActiveId] = useState('c1');

  const activeConversation = useMemo(() => conversations.find(c => c.id === activeId) || conversations[0], [conversations, activeId]);

  const handleNewChat = () => {
    const newId = `c${Date.now()}`;
    const newConv = {
      id: newId,
      title: 'New Chat',
      messages: [
        { sender: 'bot', text: 'Hi! Tell me what RTI you want to draft today.' },
      ],
    };
    setConversations([newConv, ...conversations]);
    setActiveId(newId);
  };

  const handleSend = (text) => {
    setConversations(prev => prev.map(conv => {
      if (conv.id !== activeConversation.id) return conv;
      const updated = { ...conv, messages: [...conv.messages, { sender: 'user', text }] };
      return updated;
    }));
  };

  const handleSelectConversation = (id) => setActiveId(id);

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
