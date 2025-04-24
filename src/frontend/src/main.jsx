import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './components/App';

// Mount the React app to a div with id "react-root" that we'll add to the HTML
ReactDOM.createRoot(document.getElementById('react-root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);