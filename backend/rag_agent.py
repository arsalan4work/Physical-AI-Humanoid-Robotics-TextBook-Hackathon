from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled, function_tool
import os
from dotenv import load_dotenv
from agents import enable_verbose_stdout_logging
from typing import List, Dict, Any
import logging

from config import settings
from retrieval import get_vector_retriever

# Enable verbose logging for debugging
enable_verbose_stdout_logging()

# Load environment variables
load_dotenv()
set_tracing_disabled(disabled=True)

# Initialize OpenAI client (using settings from config)
if settings.gemini_api_key:
    provider = AsyncOpenAI(
        api_key=settings.gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=provider
    )
elif settings.openai_api_key:
    provider = AsyncOpenAI(
        api_key=settings.openai_api_key,
    )
    model = OpenAIChatCompletionsModel(
        model="gpt-4o",
        openai_client=provider
    )
else:
    # Fallback - this should ideally be configured properly
    raise ValueError("Either GEMINI_API_KEY or OPENAI_API_KEY must be set in environment")

logger = logging.getLogger(__name__)

class RAGAgent:
    def __init__(self):
        """Initialize the RAG Agent with OpenAI Agents SDK and retrieval tools"""
        self.vector_retriever = get_vector_retriever()

        # Create the agent with RAG-specific instructions
        self.agent = Agent(
            name="Physical AI & Humanoid Robotics Tutor",
            instructions="""
You are an AI tutor for the Physical AI & Humanoid Robotics textbook.
Your role is to answer questions about Physical AI, Humanoid Robotics, and related topics based on the textbook content.

To answer questions:
1. First, use the `retrieve_context` tool to find relevant information from the textbook
2. Use ONLY the content returned from the tool to answer the question
3. If the answer is not in the retrieved content, say "I don't know based on the textbook content"
4. Always cite the source URLs where the information was found
5. Provide clear, educational responses appropriate for students learning about Physical AI and Humanoid Robotics
6. If asked about concepts not covered in the textbook, acknowledge the limitation and suggest consulting additional resources
            """,
            model=model,
            tools=[self.retrieve_context]
        )

        logger.info("RAG Agent initialized successfully")

    @function_tool
    def retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from the Physical AI & Humanoid Robotics textbook

        Args:
            query: The question or topic to search for in the textbook

        Returns:
            List of documents with text content and source information
        """
        try:
            logger.info(f"Retrieving context for query: {query}")

            # Use the vector retriever to find relevant documents
            documents = self.vector_retriever.search(query, limit=5)

            logger.info(f"Retrieved {len(documents)} documents for query: {query[:50]}...")

            # Format the results for the agent
            formatted_results = []
            for doc in documents:
                formatted_results.append({
                    "text": doc["text"],
                    "url": doc["url"],
                    "relevance_score": doc["score"]
                })

            return formatted_results

        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return [{"text": "Error retrieving context from textbook", "url": "", "relevance_score": 0.0}]

    def process_query(self, query: str) -> str:
        """
        Process a user query using the RAG agent

        Args:
            query: The user's question

        Returns:
            The agent's response
        """
        try:
            logger.info(f"Processing query: {query}")

            # Run the agent with the user query
            result = Runner.run_sync(
                self.agent,
                input=query,
            )

            response = result.final_output
            logger.info(f"Agent response generated successfully")

            return response

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return "I'm sorry, I encountered an error processing your request. Please try again."

    def process_text_selection_query(self, selected_text: str, question: str) -> str:
        """
        Process a query based on selected text context

        Args:
            selected_text: The text that was selected by the user
            question: The follow-up question about the selected text

        Returns:
            The agent's response
        """
        try:
            # Combine the selected text with the question for better context
            combined_query = f"Given this text: '{selected_text}', {question}"

            logger.info(f"Processing text selection query: {combined_query}")

            # Run the agent with the combined query
            result = Runner.run_sync(
                self.agent,
                input=combined_query,
            )

            response = result.final_output
            logger.info(f"Text selection query response generated successfully")

            return response

        except Exception as e:
            logger.error(f"Error processing text selection query: {str(e)}")
            return "I'm sorry, I encountered an error processing your request. Please try again."

# Global instance for use in other modules
rag_agent = None

def get_rag_agent() -> RAGAgent:
    """Get or create the global RAG agent instance"""
    global rag_agent
    if rag_agent is None:
        rag_agent = RAGAgent()
    return rag_agent

if __name__ == "__main__":
    # Test the RAG agent
    print("Initializing RAG Agent...")
    agent = get_rag_agent()

    print("\nTesting basic query...")
    response = agent.process_query("What is physical AI?")
    print(f"Response: {response}")

    print("\nTesting text selection query...")
    response = agent.process_text_selection_query(
        "Physical AI combines principles of physics and artificial intelligence",
        "Can you explain this concept further?"
    )
    print(f"Response: {response}")