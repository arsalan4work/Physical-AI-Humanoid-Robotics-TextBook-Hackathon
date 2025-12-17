import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import ChatBot from '../components/ChatBot';
import TranslationToggle from '../components/TranslationToggle';
import { useLocation } from '@docusaurus/router';

export default function ChatPage() {
  const location = useLocation();
  const [initialSelectedText, setInitialSelectedText] = useState('');

  useEffect(() => {
    // Extract selected text from URL parameters
    const params = new URLSearchParams(location.search);
    const selectedText = params.get('selectedText');
    if (selectedText) {
      setInitialSelectedText(decodeURIComponent(selectedText));
    }
  }, [location]);

  return (
    <Layout title="AI Tutor Chat" description="Physical AI & Humanoid Robotics Tutor">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--12">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h1>Physical AI & Humanoid Robotics Tutor</h1>
              <TranslationToggle />
            </div>
            <p>
              Ask questions about the textbook content, or select text on any page and ask follow-up questions.
              Our AI tutor will provide answers based on the Physical AI & Humanoid Robotics textbook.
            </p>
            {initialSelectedText && (
              <div className="alert alert--info" style={{ marginBottom: '1rem' }}>
                <p><strong>Context:</strong> "{initialSelectedText.substring(0, 100)}{initialSelectedText.length > 100 ? '...' : ''}"</p>
              </div>
            )}
            <div style={{ maxWidth: '800px', margin: '0 auto' }}>
              <ChatBot initialSelectedText={initialSelectedText} />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}