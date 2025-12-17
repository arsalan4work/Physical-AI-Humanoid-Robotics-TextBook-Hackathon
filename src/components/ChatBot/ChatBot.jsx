import React, { useState, useRef, useEffect } from 'react';
import './ChatBot.css';

const ChatBot = ({ initialSelectedText = '' }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(initialSelectedText);
  const messagesEndRef = useRef(null);

  // Function to scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  // Function to call the backend API
  const callApi = async (data) => {
    try {
      // Use the proxy path that will be handled by Docusaurus dev server
      const response = await fetch('/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: data.query || data.question,
          language: data.language || 'en',
          user_id: data.user_id || 'anonymous'
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const result = await response.json();
      return {
        answer: result.response,
        sources: [],
        confidence: 0.9
      };
    } catch (error) {
      console.error('API call error:', error);
      throw error;
    }
  };

  // Function to handle sending a message
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the API request
      const apiData = {
        query: inputValue,
        user_id: null,
        language: 'en'  // Default to English
      };

      // If we have selected text, we can include it as context
      if (selectedText) {
        apiData.question = `Context: ${selectedText}\nQuestion: ${inputValue}`;
        // Clear selected text after using it
        setSelectedText('');
      }

      const apiResponse = await callApi(apiData);

      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        text: apiResponse.answer,
        sender: 'bot',
        sources: apiResponse.sources || [],
        confidence: apiResponse.confidence,
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        error: true,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Function to clear chat
  const handleClearChat = () => {
    setMessages([]);
    setSelectedText('');
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h3>Physical AI & Humanoid Robotics Tutor</h3>
        <div className="header-controls">
          <button className="clear-chat-btn" onClick={handleClearChat}>
            Clear Chat
          </button>
        </div>
      </div>

      {selectedText && (
        <div className="selected-text-preview">
          <strong>Selected Text:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
        </div>
      )}

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your Physical AI & Humanoid Robotics tutor.</p>
            <p>You can ask me questions about the textbook content, or select text and ask follow-up questions.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
            >
              <div className="message-content">
                <div className="message-text">{message.text}</div>
                {message.sender === 'bot' && message.sources && message.sources.length > 0 && (
                  <div className="sources">
                    <strong>Sources:</strong>
                    <ul>
                      {message.sources.slice(0, 3).map((source, index) => (
                        <li key={index}>
                          <a href={source} target="_blank" rel="noopener noreferrer">
                            {source.length > 50 ? source.substring(0, 50) + '...' : source}
                          </a>
                        </li>
                      ))}
                      {message.sources.length > 3 && (
                        <li>... and {message.sources.length - 3} more sources</li>
                      )}
                    </ul>
                  </div>
                )}
                {message.sender === 'bot' && message.confidence !== undefined && !message.error && (
                  <div className="confidence">
                    Confidence: {(message.confidence * 100).toFixed(0)}%
                  </div>
                )}
                {message.error && (
                  <div className="error-message">
                    Error occurred while processing your request
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        {selectedText && (
          <div className="input-hint">
            Selected text will be used as context for your question
          </div>
        )}
        <div className="input-container">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about Physical AI & Humanoid Robotics..."
            className="chat-input"
            rows="3"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;