import React, { useState, useEffect } from 'react';
import './TranslationToggle.css';

const TranslationToggle = () => {
  const [isUrdu, setIsUrdu] = useState(false);

  // Function to translate text using backend API
  const translateText = async (text, targetLang = 'ur') => {
    try {
      // Use the proxy path that will be handled by Docusaurus dev server
      const response = await fetch('/translate/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          source_lang: 'auto',
          target_lang: targetLang
        }),
      });

      if (!response.ok) {
        throw new Error(`Translation API error: ${response.status}`);
      }

      const data = await response.json();
      return data.translated_text;
    } catch (error) {
      console.error('Translation error:', error);
      return text; // Return original text if translation fails
    }
  };

  // Function to translate the entire page content
  const translatePage = async (toUrdu) => {
    if (!toUrdu) {
      // Switch back to English - reload the page or remove translations
      document.querySelectorAll('[data-original-text]').forEach(element => {
        if (element.dataset.originalText) {
          element.textContent = element.dataset.originalText;
        }
      });
      return;
    }

    // Collect all text elements to translate
    const textElements = Array.from(document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, div, li, a, button, strong, em, i, b'));

    // Filter out elements that are likely to contain user-generated content or shouldn't be translated
    const elementsToTranslate = textElements.filter(el => {
      // Skip elements with certain classes or roles
      return !el.classList.contains('no-translate') &&
             !el.hasAttribute('role') &&
             el.textContent.trim().length > 0 &&
             el.children.length === 0; // Only translate elements with direct text content
    });

    // Translate each element
    for (const element of elementsToTranslate) {
      const originalText = element.textContent;

      // Store original text for later restoration
      if (!element.dataset.originalText) {
        element.dataset.originalText = originalText;
      }

      // Translate the text
      const translatedText = await translateText(originalText, 'ur');
      element.textContent = translatedText;
    }
  };

  const toggleTranslation = async () => {
    const newIsUrdu = !isUrdu;
    setIsUrdu(newIsUrdu);
    await translatePage(newIsUrdu);
  };

  return (
    <div className="translation-toggle">
      <button
        className={`translation-btn ${isUrdu ? 'urdu-mode' : 'english-mode'}`}
        onClick={toggleTranslation}
        title="Toggle between English and Urdu"
      >
        {isUrdu ? '🇺🇸 English' : '🇵🇰 Urdu'}
      </button>
    </div>
  );
};

export default TranslationToggle;