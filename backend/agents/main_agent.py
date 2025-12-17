"""
Main controller agent that orchestrates sub-agents based on intent detection
System Prompt (Section 5.1): You are the MAIN CONTROLLER AGENT. Your job:
Receive user message in English.
Detect intent.
Route: Translation → Translator Agent
       Search → Knowledge Agent
       Reasoning/Coding → Task Agent
Merge results.
Return clean and structured answer.
Avoid hallucination. Ask for clarification if needed.
"""
import logging
from typing import Dict, Any, List
from agents.translator import translate_agent
from agents.knowledge_agent import knowledge_agent
from agents.task_agent import task_agent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def detect_intent(message: str) -> str:
    """
    Detect the intent of the user message using keyword-based classification.

    Args:
        message: User input message in English

    Returns:
        Detected intent: 'translation', 'search', 'reasoning_coding', or 'unknown'
    """
    message_lower = message.lower().strip()

    # Translation intent detection
    translation_keywords = [
        "translate", "translation", "language", "spanish", "french", "german",
        "italian", "chinese", "japanese", "korean", "portuguese", "russian",
        "hindi", "arabic", "convert", "from english", "to english", "multilingual"
    ]

    # Search/Knowledge intent detection
    search_keywords = [
        "what is", "who is", "when", "where", "how", "why", "search", "find",
        "tell me", "explain", "define", "describe", "information", "know",
        "fact", "question", "answer", "lookup", "research", "details"
    ]

    # Reasoning/Coding intent detection
    coding_reasoning_keywords = [
        "code", "program", "function", "algorithm", "calculate", "compute",
        "solve", "problem", "debug", "python", "javascript", "java", "c++",
        "implement", "write", "create", "develop", "analyze", "reason",
        "logic", "math", "equation", "formula", "script"
    ]

    # Count matches for each intent
    translation_matches = sum(1 for keyword in translation_keywords if keyword in message_lower)
    search_matches = sum(1 for keyword in search_keywords if keyword in message_lower)
    coding_matches = sum(1 for keyword in coding_reasoning_keywords if keyword in message_lower)

    # Determine intent based on highest match count
    if translation_matches > 0 and translation_matches >= search_matches and translation_matches >= coding_matches:
        return "translation"
    elif search_matches > 0 and search_matches >= coding_matches:
        return "search"
    elif coding_matches > 0:
        return "reasoning_coding"
    else:
        # Additional check for more specific patterns
        if any(pattern in message_lower for pattern in ["write code", "create function", "implement"]):
            return "reasoning_coding"
        elif any(pattern in message_lower for pattern in ["what is", "how do", "explain"]):
            return "search"
        else:
            return "unknown"


async def merge_results(results: List[str], intent: str) -> str:
    """
    Merge results from multiple agents or processing steps.

    Args:
        results: List of results from different processing steps
        intent: The detected intent that guided processing

    Returns:
        Merged and formatted result
    """
    if not results:
        return "No results to merge."

    # If there's only one result, return it directly
    if len(results) == 1:
        return results[0]

    # For multiple results, format them in a structured way
    merged_result = f"Here are the results for your {intent} request:\n\n"

    for i, result in enumerate(results, 1):
        merged_result += f"Result {i}:\n{result}\n\n"

    return merged_result.strip()


async def route_message(message: str, user_id: str, preferred_language: str) -> str:
    """
    Main agent that detects intent and routes to appropriate sub-agent
    following the system prompt from section 5.1.

    Args:
        message: User input message in English
        user_id: ID of the requesting user
        preferred_language: User's preferred language for responses

    Returns:
        Response from the appropriate sub-agent with merged results if needed
    """
    try:
        logger.info(f"Processing message: {message[:50]}...")

        # Step 1: Detect intent
        intent = await detect_intent(message)
        logger.info(f"Detected intent: {intent}")

        # Step 2: Route to appropriate sub-agent based on intent
        results = []

        if intent == "translation":
            logger.info("Routing to Translation Agent")
            result = await translate_agent(message, preferred_language)
            results.append(result)
        elif intent == "search":
            logger.info("Routing to Knowledge Agent")
            result = await knowledge_agent(message, user_id)
            results.append(result)
        elif intent == "reasoning_coding":
            logger.info("Routing to Task Agent")
            result = await task_agent(message, user_id)
            results.append(result)
        else:
            # For unknown intent, default to knowledge agent for general information
            logger.info("Unknown intent, routing to Knowledge Agent")
            result = await knowledge_agent(message, user_id)
            results.append(result)

        # Additional processing for complex requests that might need multiple agents
        if "compare" in message.lower() or "and" in message.lower():
            # For comparison requests, we might want to get additional context
            if intent in ["search", "reasoning_coding"]:
                # Get additional information from knowledge agent
                additional_result = await knowledge_agent(message, user_id)
                if additional_result not in results:
                    results.append(additional_result)

        # Step 3: Merge results if multiple results exist
        final_result = await merge_results(results, intent)

        # Step 4: Return clean and structured answer
        logger.info("Message processing completed successfully")
        return final_result

    except Exception as e:
        logger.error(f"Error in main agent processing: {str(e)}")
        return f"I encountered an error processing your request: {str(e)}"