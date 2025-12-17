import React, { useState, useEffect, useCallback } from 'react';
import { useLocation } from '@docusaurus/router';

const TextSelectionHandler = ({ children }) => {
  const [selectedText, setSelectedText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [popupPosition, setPopupPosition] = useState({ x: 0, y: 0 });
  const location = useLocation();

  // Function to handle text selection
  const handleSelection = useCallback((event) => {
    const selectedText = window.getSelection().toString().trim();

    if (selectedText && selectedText.length > 10) { // Only consider meaningful selections
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        setSelectedText(selectedText);
        setPopupPosition({
          x: rect.left + window.scrollX,
          y: rect.top + window.scrollY - 40 // Position above the selection
        });
        setShowPopup(true);
      }
    } else {
      setShowPopup(false);
    }
  }, []);

  // Close popup when navigating to different pages
  useEffect(() => {
    setShowPopup(false);
    setSelectedText('');
  }, [location]);

  // Add event listeners
  useEffect(() => {
    document.addEventListener('mouseup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, [handleSelection]);

  // Function to handle question about selected text
  const handleAskQuestion = () => {
    if (selectedText) {
      // Navigate to chat page with selected text
      const encodedText = encodeURIComponent(selectedText);
      window.location.href = `/chat?selectedText=${encodedText}`;
    }
  };

  return (
    <>
      {children}
      {showPopup && (
        <div
          className="text-selection-popup"
          style={{
            position: 'absolute',
            left: `${popupPosition.x}px`,
            top: `${popupPosition.y}px`,
            zIndex: 10000,
            backgroundColor: '#2563eb',
            color: 'white',
            padding: '8px 12px',
            borderRadius: '4px',
            fontSize: '14px',
            cursor: 'pointer',
            boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
          }}
          onClick={handleAskQuestion}
        >
          Ask AI Tutor
        </div>
      )}
      <style jsx>{`
        .text-selection-popup:hover {
          background-color: #1d4ed8;
        }
      `}</style>
    </>
  );
};

export default TextSelectionHandler;