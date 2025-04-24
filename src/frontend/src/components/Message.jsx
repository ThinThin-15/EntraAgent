import React from 'react';
import ReactMarkdown from 'react-markdown';

const Message = ({ content, role }) => {
  const isUser = role === 'user';
  
  return (
    <div className={`toast-container position-static w-100 d-flex flex-column align-items-stretch ${isUser ? 'user' : ''}`}>
      <div className={`toast fade show w-75 rounded-3 ${isUser ? 'align-self-end' : 'align-self-start'}`}>
        <div className="toast-body message-content">
          {isUser ? (
            content
          ) : (
            <ReactMarkdown>
              {content}
            </ReactMarkdown>
          )}
        </div>
      </div>
    </div>
  );
};

export default Message;