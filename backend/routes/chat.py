"""
Chat endpoint implementation with full flow:
- Verify auth token
- Translate message to English
- Route to main agent
- Get vector context from Qdrant
- Stream agent response
- Translate back to user language
- Store in vector DB
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.requests import Request
from fastapi.responses import StreamingResponse

from auth.verify import get_current_user  # Using the existing auth system
from agents.main_agent import route_message
from agents.translator import translate_agent
from agents.knowledge_agent import knowledge_agent_instance
from db.qdrant import qdrant_service

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=10000)
    language: str = Field(default="en", min_length=2, max_length=10)


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    language: str
    timestamp: str
    user_id: str


@router.post("/", response_class=StreamingResponse)
async def chat_endpoint(request: Request) -> StreamingResponse:
    """
    Main chat endpoint that implements the full flow:
    1. Verify auth token
    2. Translate message to English
    3. Get vector context from Qdrant
    4. Route to main agent
    5. Translate back to user language
    6. Store in vector DB
    7. Stream agent response
    """
    try:
        # Step 1: Verify auth token
        current_user = await get_current_user(request)
        user_id = current_user["user_id"]

        # Parse the JSON body
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid JSON body")

        # Validate required fields
        message = body.get("message", "")
        language = body.get("language", "en")
        request_user_id = body.get("user_id")

        # More comprehensive validation
        if not message or not message.strip():
            raise HTTPException(status_code=400, detail="Message is required and cannot be empty")

        if len(message) > 10000:  # Limit message length
            raise HTTPException(status_code=400, detail="Message is too long (max 10000 characters)")

        if not isinstance(message, str):
            raise HTTPException(status_code=400, detail="Message must be a string")

        if not isinstance(language, str) or len(language) < 2 or len(language) > 10:
            raise HTTPException(status_code=400, detail="Language must be a valid string between 2 and 10 characters")

        # Validate that user_id from body matches authenticated user (if provided in body)
        if request_user_id and request_user_id != current_user["user_id"]:
            raise HTTPException(status_code=403, detail="User ID in request does not match authenticated user")

        logger.info(f"Chat request from user {current_user['user_id']} in language {language}")

        # Step 2: Translate message to English (if needed)
        original_message = message
        message_in_english = original_message

        if language.lower() != 'en':
            # Translate to English for processing
            translation_result = await translate_agent(
                f"Translate the following message to English: {original_message}",
                "en"
            )
            # Extract the translated text from the result
            if translation_result.startswith("Translated to en:"):
                message_in_english = translation_result[len("Translated to en:"):].strip()
            else:
                message_in_english = translation_result

        logger.info(f"Message translated to English: {message_in_english[:50]}...")

        # Step 3: Get vector context from Qdrant (search for relevant context)
        context_results = await qdrant_service.search_vectors(
            query=message_in_english,
            user_id=user_id,
            limit=3
        )

        # Format context results for the agent
        context_str = ""
        if context_results:
            context_messages = [result["message"] for result in context_results]
            context_str = "\n".join(context_messages)

        # Include context in the message for the agent
        full_message = message_in_english
        if context_str.strip():
            full_message = f"Context: {context_str}\n\nQuestion: {message_in_english}"

        # Step 4: Route to main agent
        agent_response = await route_message(
            message=full_message,
            user_id=current_user["user_id"],
            preferred_language="en"  # Agent works in English
        )

        logger.info(f"Agent response received: {agent_response[:50]}...")

        # Step 5: Translate back to user language (if needed)
        final_response = agent_response
        if language.lower() != 'en':
            # Translate back to user's preferred language
            translation_result = await translate_agent(
                agent_response,
                language
            )
            # Extract the translated text from the result
            if f"Translated to {language}:" in translation_result:
                final_response = translation_result[len(f"Translated to {language}:"):].strip()
            else:
                final_response = translation_result

        # Step 6: Store in vector DB (store both the original message and response)
        # Store user message
        await qdrant_service.upsert_vector(
            user_id=current_user["user_id"],
            message=original_message,
            metadata={
                "type": "user_message",
                "language": language,
                "timestamp": int(datetime.now().timestamp())
            }
        )

        # Store AI response
        await qdrant_service.upsert_vector(
            user_id=current_user["user_id"],
            message=agent_response,  # Store the English version for retrieval
            metadata={
                "type": "ai_response",
                "language": "en",
                "user_language": language,
                "timestamp": int(datetime.now().timestamp())
            }
        )

        # Step 7: Stream agent response back to client
        async def generate_response():
            # Send the response as a JSON object
            response_data = {
                "response": final_response,
                "language": language,
                "timestamp": datetime.now().isoformat(),
                "user_id": current_user["user_id"],
                "done": True
            }
            yield f"data: {json.dumps(response_data)}\n\n"

        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*"
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Alternative endpoint with more explicit streaming for token-by-token response
@router.post("/stream", response_class=StreamingResponse)
async def chat_stream_endpoint(request: Request) -> StreamingResponse:
    """
    Streaming chat endpoint that streams the agent's response token by token
    """
    async def event_generator():
        try:
            # Step 1: Verify auth token
            current_user = await get_current_user(request)
            user_id = current_user["user_id"]

            # Parse the JSON body
            try:
                body = await request.json()
            except Exception:
                yield f"data: {json.dumps({'type': 'error', 'error': 'Invalid JSON body', 'done': True})}\n\n"
                return

            # Validate required fields
            message = body.get("message", "")
            language = body.get("language", "en")
            request_user_id = body.get("user_id")

            # More comprehensive validation
            if not message or not message.strip():
                yield f"data: {json.dumps({'type': 'error', 'error': 'Message is required and cannot be empty', 'done': True})}\n\n"
                return

            if len(message) > 10000:  # Limit message length
                yield f"data: {json.dumps({'type': 'error', 'error': 'Message is too long (max 10000 characters)', 'done': True})}\n\n"
                return

            if not isinstance(message, str):
                yield f"data: {json.dumps({'type': 'error', 'error': 'Message must be a string', 'done': True})}\n\n"
                return

            if not isinstance(language, str) or len(language) < 2 or len(language) > 10:
                yield f"data: {json.dumps({'type': 'error', 'error': 'Language must be a valid string between 2 and 10 characters', 'done': True})}\n\n"
                return

            # Validate that user_id from body matches authenticated user (if provided in body)
            if request_user_id and request_user_id != current_user["user_id"]:
                yield f"data: {json.dumps({'type': 'error', 'error': 'User ID in request does not match authenticated user', 'done': True})}\n\n"
                return

            logger.info(f"Streaming chat request from user {current_user['user_id']} in language {language}")

            # Step 2: Translate message to English (if needed)
            original_message = message
            message_in_english = original_message

            if language.lower() != 'en':
                # Send translation progress event
                yield f"data: {json.dumps({'type': 'progress', 'message': 'Translating to English...'})}\n\n"

                # Translate to English for processing
                translation_result = await translate_agent(
                    f"Translate the following message to English: {original_message}",
                    "en"
                )
                # Extract the translated text from the result
                if translation_result.startswith("Translated to en:"):
                    message_in_english = translation_result[len("Translated to en:"):].strip()
                else:
                    message_in_english = translation_result

            logger.info(f"Message translated to English: {message_in_english[:50]}...")

            # Step 3: Get vector context from Qdrant
            yield f"data: {json.dumps({'type': 'progress', 'message': 'Retrieving context...'})}\n\n"

            context_results = await qdrant_service.search_vectors(
                query=message_in_english,
                user_id=current_user["user_id"],
                limit=3
            )

            # Format context results for the agent
            context_str = ""
            if context_results:
                context_messages = [result["message"] for result in context_results]
                context_str = "\n".join(context_messages)

            # Include context in the message for the agent
            full_message = message_in_english
            if context_str.strip():
                full_message = f"Context: {context_str}\n\nQuestion: {message_in_english}"

            # Step 4: Route to main agent and get response
            yield f"data: {json.dumps({'type': 'progress', 'message': 'Processing with AI...'})}\n\n"

            agent_response = await route_message(
                message=full_message,
                user_id=current_user["user_id"],
                preferred_language="en"
            )

            logger.info(f"Agent response received: {agent_response[:50]}...")

            # Step 5: Translate back to user language (if needed)
            if language.lower() != 'en':
                yield f"data: {json.dumps({'type': 'progress', 'message': 'Translating back to your language...'})}\n\n"

                # Translate back to user's preferred language
                translation_result = await translate_agent(
                    agent_response,
                    language
                )
                # Extract the translated text from the result
                if f"Translated to {language}:" in translation_result:
                    final_response = translation_result[len(f"Translated to {language}:"):].strip()
                else:
                    final_response = translation_result
            else:
                final_response = agent_response

            # Step 6: Store in vector DB
            yield f"data: {json.dumps({'type': 'progress', 'message': 'Saving to memory...'})}\n\n"

            # Store user message
            await qdrant_service.upsert_vector(
                user_id=current_user["user_id"],
                message=original_message,
                metadata={
                    "type": "user_message",
                    "language": language,
                    "timestamp": int(datetime.now().timestamp())
                }
            )

            # Store AI response
            await qdrant_service.upsert_vector(
                user_id=current_user["user_id"],
                message=agent_response,
                metadata={
                    "type": "ai_response",
                    "language": "en",
                    "user_language": language,
                    "timestamp": int(datetime.now().timestamp())
                }
            )

            # Step 7: Stream the final response
            response_data = {
                "type": "final_response",
                "response": final_response,
                "language": language,
                "timestamp": datetime.now().isoformat(),
                "user_id": current_user["user_id"],
                "done": True
            }
            yield f"data: {json.dumps(response_data)}\n\n"

        except Exception as e:
            logger.error(f"Error in streaming chat endpoint: {str(e)}")
            error_data = {
                "type": "error",
                "error": f"Internal server error: {str(e)}",
                "done": True
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )