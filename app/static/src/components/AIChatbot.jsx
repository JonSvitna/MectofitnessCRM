import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const AIChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Welcome message
  useEffect(() => {
    const welcomeMsg = {
      text: "👋 Hi! I'm your AI Fitness Assistant. I can help you with:\n\n" +
            "• Creating workout programs\n" +
            "• Exercise recommendations\n" +
            "• Nutrition advice\n" +
            "• Client management tips\n" +
            "• Training best practices\n\n" +
            "How can I assist you today?",
      sender: 'ai',
      timestamp: new Date()
    };
    setMessages([welcomeMsg]);
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Keyboard shortcut (Ctrl+/ or Cmd+/)
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        setIsOpen(prev => !prev);
      }
      if (e.key === 'Escape' && isOpen) {
        e.preventDefault();
        setIsOpen(false);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  // Add body class for sidebar detection
  useEffect(() => {
    document.body.classList.add('has-sidebar');
    return () => document.body.classList.remove('has-sidebar');
  }, []);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chatbot/', {
        message: inputValue,
        history: messages.slice(-10) // Send last 10 messages for context
      });

      if (response.data.success) {
        const aiMessage = {
          text: response.data.response,
          sender: 'ai',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error('Failed to get response');
      }
    } catch (error) {
      console.error('Chatbot error:', error);
      const errorMessage = {
        text: "Sorry, I'm having trouble connecting. Please try again later.",
        sender: 'ai',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Chatbot Button */}
      <button
        onClick={toggleChat}
        className="ai-chatbot-button"
        aria-label="Open AI Assistant"
        title="AI Assistant (Ctrl+/)"
      >
        🤖
      </button>

      {/* Chatbot Window */}
      {isOpen && (
        <div className="ai-chatbot-window active">
          {/* Header */}
          <div className="chatbot-header">
            <h3>🤖 AI Fitness Assistant</h3>
            <button
              onClick={toggleChat}
              className="chatbot-close"
              aria-label="Close chatbot"
            >
              ×
            </button>
          </div>

          {/* Messages */}
          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>
                <div className={`message-avatar ${msg.sender}`}>
                  {msg.sender === 'ai' ? '🤖' : '👤'}
                </div>
                <div className={`message-content ${msg.sender}`}>
                  {msg.text.split('\n').map((line, i) => (
                    <span key={i}>
                      {line}
                      {i < msg.text.split('\n').length - 1 && <br />}
                    </span>
                  ))}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="chat-message ai typing-indicator">
                <div className="message-avatar ai">🤖</div>
                <div className="message-content ai">
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="chatbot-input-area">
            <input
              type="text"
              className="chatbot-input"
              placeholder="Ask me anything about fitness..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              autoComplete="off"
            />
            <button
              className="chatbot-send"
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              aria-label="Send message"
            >
              <span>➤</span>
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default AIChatbot;
