"""
Translation service module for the AI Multilingual Chatbot System
Provides translation functionality between any language and English
"""
from typing import Optional
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    """
    Service class for handling translation between any language and English
    """

    def __init__(self):
        """
        Initialize the translation service
        """
        pass

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text

        Args:
            text (str): Input text to detect language for

        Returns:
            str: Detected language code (e.g., 'en', 'es', 'fr', 'ur')
        """
        try:
            detected_lang = detect(text)
            return detected_lang
        except LangDetectException as e:
            logger.error(f"Language detection failed: {e}")
            # Default to English if detection fails
            return "en"
        except Exception as e:
            logger.error(f"Unexpected error during language detection: {e}")
            return "en"

    def translate_to_english(self, text: str, source_lang: str = "auto") -> str:
        """
        Translate text to English

        Args:
            text (str): Input text to translate
            source_lang (str): Source language code (default: "auto" for detection)

        Returns:
            str: Translated text in English
        """
        try:
            if source_lang == "auto":
                source_lang = self.detect_language(text)

            if source_lang == "en":
                # If text is already in English, return as is
                return text

            # Translate to English
            translator = GoogleTranslator(source=source_lang, target="en")
            translated_text = translator.translate(text)
            return translated_text if translated_text else text
        except Exception as e:
            logger.error(f"Translation to English failed: {e}")
            # Return original text if translation fails
            return text

    def translate_from_english(self, text: str, target_lang: str) -> str:
        """
        Translate text from English to target language

        Args:
            text (str): Input text in English to translate
            target_lang (str): Target language code (e.g., 'es', 'fr', 'ur')

        Returns:
            str: Translated text in target language
        """
        try:
            if target_lang == "en":
                # If target language is English, return as is
                return text

            # Translate from English to target language
            translator = GoogleTranslator(source="en", target=target_lang)
            translated_text = translator.translate(text)
            return translated_text if translated_text else text
        except Exception as e:
            logger.error(f"Translation from English failed: {e}")
            # Return original text if translation fails
            return text

    def translate_text(self, text: str, source_lang: str = "auto", target_lang: str = "en") -> str:
        """
        Generic translation function

        Args:
            text (str): Input text to translate
            source_lang (str): Source language code (default: "auto")
            target_lang (str): Target language code (default: "en")

        Returns:
            str: Translated text
        """
        try:
            if source_lang == "auto":
                source_lang = self.detect_language(text)

            if source_lang == target_lang:
                # If source and target languages are the same, return as is
                return text

            # Use appropriate translation method based on target language
            if target_lang == "en":
                return self.translate_to_english(text, source_lang)
            else:
                # If we need to translate from non-English to non-English,
                # first translate to English then to target
                if source_lang != "en":
                    text = self.translate_to_english(text, source_lang)
                return self.translate_from_english(text, target_lang)
        except Exception as e:
            logger.error(f"Generic translation failed: {e}")
            return text


# Create a singleton instance
translation_service = TranslationService()