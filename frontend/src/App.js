import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const sendQuery = async () => {
    if (!query) return; // Don't send empty queries
    setLoading(true);
    try {
      const result = await axios.post('http://127.0.0.1:5000/chat', { query });
      setResponse(result.data.response);
    } catch (error) {
      setResponse('Error: Unable to fetch response.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>AI Customer Support</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={sendQuery} disabled={loading}>
        {loading ? 'Sending...' : 'Send'}
      </button>
      {loading && <div className="loader"></div>}
      <p className="response">{response}</p>
    </div>
  );
}

export default App;