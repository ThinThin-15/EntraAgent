import React, { useEffect, useRef } from 'react';
import Message from './Message';

const MessageList = ({ messages }) => {
  const messagesEndRef = useRef(null);

  // Auto-scroll to the bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="messages px-4 pb-4 pt-2 flex-grow-1 overflow-y-auto align-items-stretch">
      {messages.length === 0 ? (
        <div id="placeholder-wrapper" className="d-flex flex-grow-1 justify-content-center align-items-center w-100">
          <div id="placeholder-message" className="text-center text-muted my-3">
            <div className="header">Getting Started with Agents Using Azure AI Foundry</div>
            Type your message below. You can start casually with something fun like "Tell me a joke," or ask specifically about the Azure Search files, such as "What is Contoso Galaxy Innovations product?"
          </div>
        </div>
      ) : (
        messages.map((message, index) => (
          <Message key={index} content={message.content} role={message.role} />
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;