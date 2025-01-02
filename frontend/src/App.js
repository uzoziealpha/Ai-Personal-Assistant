import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Bar, Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './App.css';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend);

function App() {
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('en');
  const [isTyping, setIsTyping] = useState(false);
  const [metrics, setMetrics] = useState([]);
  const [score, setScore] = useState(0);
  const [email, setEmail] = useState('');
  const [showLogs, setShowLogs] = useState(false); // Toggle logs box

  // Send query to the backend
  const sendQuery = async () => {
    if (!query) return;
    setLoading(true);
    setIsTyping(true);
    try {
      const result = await axios.post('http://127.0.0.1:5000/chat', { query, language });
      setChatHistory([...chatHistory, { query, response: result.data.response, type: 'text' }]);
      setQuery('');
      setScore(result.data.score); // Update score
    } catch (error) {
      setChatHistory([...chatHistory, { query, response: 'Error: Unable to fetch response.', type: 'text' }]);
    } finally {
      setLoading(false);
      setIsTyping(false);
    }
  };

  // Voice input
  const startVoiceInput = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = language;
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
    };
    recognition.start();
  };

  // Voice output
  const speakResponse = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language;
    window.speechSynthesis.speak(utterance);
  };

  // Speak the last response
  useEffect(() => {
    if (chatHistory.length > 0) {
      const lastResponse = chatHistory[chatHistory.length - 1].response;
      speakResponse(lastResponse);
    }
  }, [chatHistory]);

  // Fetch metrics
  useEffect(() => {
    axios.get('http://127.0.0.1:5000/metrics')
      .then(response => setMetrics(response.data))
      .catch(error => console.error(error));
  }, []);

  // File upload
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
      setChatHistory([...chatHistory, { query: "Uploaded file", response: response.data.message, type: 'text' }]);
    })
    .catch(error => {
      setChatHistory([...chatHistory, { query: "Uploaded file", response: 'Error: Unable to upload file.', type: 'text' }]);
    });
  };

  // Export logs as PDF
  const handleExportPDF = () => {
    window.open('http://127.0.0.1:5000/export-pdf', '_blank');
  };

  // Send logs via email
  const handleSendEmail = () => {
    axios.post('http://127.0.0.1:5000/send-email', { email })
      .then(response => alert(response.data.message))
      .catch(error => alert(error.response.data.error));
  };

  // Chat bubble component
  const ChatBubble = ({ message, isUser }) => {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className={`chat-bubble ${isUser ? 'user' : 'bot'}`}
      >
        {message.type === 'text' && <p>{message.text}</p>}
        {message.type === 'image' && <img src={message.url} alt="Chat media" className="chat-media" />}
        {message.type === 'link' && (
          <a href={message.url} target="_blank" rel="noopener noreferrer">
            {message.text}
          </a>
        )}
      </motion.div>
    );
  };

  // Chart data
  const queryVolumeData = {
    labels: metrics.map((_, index) => `Query ${index + 1}`),
    datasets: [{
      label: 'Query Length',
      data: metrics.map(metric => metric.query.length),
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }]
  };

  const responseLengthData = {
    labels: metrics.map((_, index) => `Query ${index + 1}`),
    datasets: [{
      label: 'Response Length',
      data: metrics.map(metric => metric.response.length),
      backgroundColor: 'rgba(153, 102, 255, 0.2)',
      borderColor: 'rgba(153, 102, 255, 1)',
      borderWidth: 1
    }]
  };

  return (
    <div className="App">
      <h1>AI Customer Support</h1>
      <div className="main-container">
        <div className="chat-container">
          <div className="chat-history">
            {chatHistory.map((chat, index) => (
              <div key={index} className="chat-message">
                <ChatBubble message={{ text: chat.query, type: 'text' }} isUser={true} />
                <ChatBubble message={{ text: chat.response, type: 'text' }} isUser={false} />
              </div>
            ))}
            {isTyping && (
              <div className="typing-indicator">
                <span>Bot is typing...</span>
                <div className="typing-animation">
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                </div>
              </div>
            )}
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question..."
              onKeyPress={(e) => e.key === 'Enter' && sendQuery()}
            />
            <button onClick={sendQuery} disabled={loading}>
              {loading ? 'Sending...' : 'Send'}
            </button>
            <button onClick={startVoiceInput}>🎤</button>
            <input type="file" onChange={handleFileUpload} />
          </div>
        </div>
        <div className="logs-container">
          <button onClick={() => setShowLogs(!showLogs)}>
            {showLogs ? 'Hide Logs' : 'Show Logs'}
          </button>
          {showLogs && (
            <div className="logs-box">
              <h2>Query Logs</h2>
              {metrics.map((metric, index) => (
                <div key={index} className="log-item">
                  <p><strong>Query:</strong> {metric.query}</p>
                  <p><strong>Response:</strong> {metric.response}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
      <div className="dashboard">
        <h2>Metrics Dashboard</h2>
        <div className="charts">
          <div className="chart-container">
            <Bar data={queryVolumeData} />
          </div>
          <div className="chart-container">
            <Line data={responseLengthData} />
          </div>
        </div>
      </div>
      <div className="score">
        <h2>Your Score: {score}</h2>
        {score >= 10 && <span>🎖️ Bronze Badge</span>}
        {score >= 20 && <span>🥈 Silver Badge</span>}
        {score >= 30 && <span>🥇 Gold Badge</span>}
      </div>
      <div className="export-options">
        <button onClick={handleExportPDF}>Export Logs as PDF</button>
        <div>
          <input
            type="email"
            placeholder="Enter email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button onClick={handleSendEmail}>Send Logs via Email</button>
        </div>
      </div>
    </div>
  );
}

export default App;