import React, { useState } from 'react';

const ChatForm = ({ onSubmit, isGenerating }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isGenerating) {
      onSubmit(message);
      setMessage('');
    }
  };

  const clearChat = () => {
    // We'll implement this to match the existing functionality
    window.location.reload();
  };

  return (
    <div id="chat-area" className="text-light px-4 py-2 rounded-top text-dark d-flex flex-column justify-content-center background-user">
      <form id="chat-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <button 
            type="button" 
            className="btn btn-outline-dark" 
            onClick={clearChat}
            aria-label="Start a new chat">
            <i className="bi bi-arrow-repeat" aria-hidden="true"></i>
          </button>
          <i className="bi bi-body-text input-group-text dark-border" aria-hidden="true"></i>
          <input 
            id="message" 
            name="message" 
            className="form-control form-control-sm dark-border" 
            type="text" 
            placeholder="Your Message" 
            aria-label="Ask ChatGPT"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            disabled={isGenerating}
          />
          <button 
            type="submit" 
            className="btn btn-outline-dark" 
            style={{ borderLeftWidth: 0 }} 
            aria-label="Submit"
            disabled={isGenerating}>
            Send <i className="bi bi-send-fill" aria-hidden="true"></i>
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatForm;