import React, { useState, useEffect } from 'react';
import MessageList from './MessageList';
import ChatForm from './ChatForm';

const ChatContainer = () => {
  const [messages, setMessages] = useState([]);
  const [isGenerating, setIsGenerating] = useState(false);

  const addMessage = (content, role) => {
    setMessages(prev => [...prev, { content, role }]);
  };

  const handleSubmit = async (userMessage) => {
    if (!userMessage.trim()) return;
    
    // Add user message to the chat
    addMessage(userMessage, 'user');
    setIsGenerating(true);
    
    try {
      // Call the existing API endpoint
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });
      
      const data = await response.json();
      addMessage(data.message, 'assistant');
    } catch (error) {
      console.error('Error sending message:', error);
      addMessage('Sorry, there was an error processing your request.', 'assistant');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="chat-container d-flex flex-column h-100">
      <MessageList messages={messages} />
      <div id="generating-message" style={{ display: isGenerating ? 'block' : 'none' }}>
        Generating response...
      </div>
      <ChatForm onSubmit={handleSubmit} isGenerating={isGenerating} />
    </div>
  );
};

export default ChatContainer;