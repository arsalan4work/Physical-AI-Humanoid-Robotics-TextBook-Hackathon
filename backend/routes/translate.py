"""
Translation services endpoint
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import logging
from utils.translation_service import translation_service

router = APIRouter()

logger = logging.getLogger(__name__)


class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str = "en"


class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str


@router.post("/translate")
async def translate_text(request: TranslationRequest):
    """
    Translate text from source language to target language
    """
    try:
        # If source language is auto, detect it
        if request.source_lang == "auto":
            detected_lang = translation_service.detect_language(request.text)
            source_lang = detected_lang
        else:
            source_lang = request.source_lang

        # Perform translation
        translated_text = translation_service.translate_text(
            request.text,
            source_lang=source_lang,
            target_lang=request.target_lang
        )

        return TranslationResponse(
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=request.target_lang
        )
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail="Translation service error")