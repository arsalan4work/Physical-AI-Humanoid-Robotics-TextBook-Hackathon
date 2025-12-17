# AI Multilingual Chatbot System - Architecture Plan

## 1. Overview

This document outlines the architectural plan for the AI Multilingual Chatbot System, designed to provide secure, multilingual AI assistance with vector-based memory and sub-agent orchestration. The system implements authentication, translation, and AI agent routing as specified in the feature requirements.

## 2. Architecture Overview

### 2.1 System Architecture
The system follows a microservices architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   External      │
│   (Next.js)     │◄──►│   (FastAPI)      │◄──►│   Services      │
│                 │    │                  │    │                 │
│ • ChatKit UI    │    │ • Auth Module    │    │ • OpenAI APIs   │
│ • Auth Guard    │    │ • Translation    │    │ • Cohere Embed  │
│ • Language Sel  │    │ • Vector Ops     │    │ • Qdrant DB     │
│ • Protected R.  │    │ • Agent Router   │    │ • Better-auth   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 2.2 Technology Stack
- **Frontend**: Next.js 14+, React, ChatKit UI
- **Backend**: FastAPI, Python 3.11+
- **Authentication**: Better-auth
- **Database**: Qdrant Vector Database
- **AI Services**: OpenAI Agents SDK, Cohere Embeddings
- **Translation**: Custom Translation Layer
- **Deployment**: Containerized services

## 3. Component Design

### 3.1 Backend Architecture

#### 3.1.1 Directory Structure
```
/backend
├── /auth
│   └── verify.py          # Authentication verification
├── /routes
│   ├── chat.py           # Chat endpoint
│   ├── translate.py      # Translation endpoint
│   ├── auth.py           # Auth routes
│   └── vector.py         # Vector operations
├── /agents
│   ├── main_agent.py     # Main controller agent
│   ├── translator.py     # Translation sub-agent
│   ├── knowledge_agent.py # Knowledge retrieval agent
│   └── task_agent.py     # Task processing agent
├── /db
│   └── qdrant.py         # Qdrant database operations
├── /utils
│   ├── tokenizer.py      # Text tokenization
│   └── text_cleaner.py   # Text cleaning utilities
└── main.py              # Application entry point
```

#### 3.1.2 Auth Module (`/auth/verify.py`)
- Validates authentication tokens
- Verifies user permissions
- Returns user context (ID, email, preferred language)

#### 3.1.3 Routes Module
- **`/chat`**: Main chat endpoint with auth verification, translation, and agent routing
- **`/translate`**: Translation services endpoint
- **`/auth`**: Authentication-related endpoints
- **`/vector`**: Vector database operations (upsert, search)

#### 3.1.4 Agents Module
- **Main Agent**: Orchestrates sub-agents based on intent detection
- **Translator Agent**: Handles translation tasks
- **Knowledge Agent**: Performs vector search and knowledge retrieval
- **Task Agent**: Handles reasoning and coding tasks

### 3.2 Frontend Architecture

#### 3.2.1 Directory Structure
```
/frontend
├── /app
│   ├── /chat
│   │   └── page.tsx     # Main chat page
│   ├── /api
│   │   └── chat/route.ts # API route for chat
│   └── layout.tsx       # Root layout
├── /components
│   ├── ChatUI.tsx       # ChatKit UI wrapper
│   ├── LanguageSelector.tsx # Language selector
│   └── ProtectedRoute.tsx # Auth guard component
├── /lib
│   ├── auth.ts          # Auth utilities
│   └── axios.ts         # HTTP client configuration
└── /env                 # Environment variables
```

## 4. Data Flow Architecture

### 4.1 Message Processing Flow
```
1. User enters message in UI (e.g., Spanish)
2. Frontend sends: {message, lang, user_id, token}
3. Backend verifies token via auth middleware
4. Translation layer converts to English
5. Main agent detects intent and routes:
   - Translation → Translator Agent
   - Search → Knowledge Agent (with Qdrant vector search)
   - Reasoning/Coding → Task Agent
6. Results merged and translated back to user language
7. Response streamed to UI via ChatKit
8. Message stored in Qdrant with embedding
```

### 4.2 Vector Database Schema
- **Collection**: `chatbot_memory`
- **Embedding Function**:
  ```python
  def get_embedding(text):
      """Get embedding vector from Cohere Embed v3"""
      response = cohere_client.embed(
          model="embed-english-v3.0",
          input_type="search_query",  # Use search_query for queries
          texts=[text],
      )
      return response.embeddings[0]  # Return the first embedding
  ```
- **Payload Structure**:
  ```json
  {
    "user_id": "string",
    "message": "string",
    "timestamp": "int",
    "metadata": {
      "topic": "string",
      "lang": "string",
      "agent": "string"
    }
  }
  ```

## 5. Security Architecture

### 5.1 Authentication Flow
- Better-auth handles user registration/login
- JWT tokens issued upon successful authentication
- Token validation on all protected endpoints
- Session management with configurable expiration

### 5.2 Data Protection
- All user data encrypted in transit (TLS)
- Authentication tokens validated server-side
- Input sanitization at API boundaries
- Rate limiting to prevent abuse

## 6. Performance Architecture

### 6.1 Caching Strategy
- API response caching for frequently accessed data
- Embedding caching to avoid recomputation
- Session state caching for active conversations

### 6.2 Scalability Considerations
- Stateless API services for horizontal scaling
- Database connection pooling
- Asynchronous processing for long-running operations
- CDN for static assets

## 7. Integration Architecture

### 7.1 External Service Integrations
- **OpenAI API**: Main LLM interactions
- **Cohere API**: Embedding generation
- **Qdrant**: Vector database operations
- **Better-auth**: Authentication services

### 7.2 API Contract Standards
- RESTful API design principles
- Consistent error response format
- Comprehensive API documentation
- Versioning strategy for API evolution

## 8. Monitoring and Observability

### 8.1 Logging Strategy
- Structured logging with correlation IDs
- Request/response logging for debugging
- Performance metric collection
- Security event logging

### 8.2 Health Checks
- Application health endpoints
- Database connectivity checks
- External service availability monitoring
- Resource utilization monitoring

## 9. Deployment Architecture

### 9.1 Containerization
- Docker containers for all services
- Environment-based configuration
- Multi-stage builds for optimization
- Health check integration

### 9.2 Infrastructure
- Container orchestration (Docker Compose/Kubernetes)
- Load balancing for API services
- Database replication for Qdrant
- SSL termination at edge

## 10. Risk Mitigation

### 10.1 Security Risks
- Input validation to prevent injection attacks
- Authentication token security
- API rate limiting to prevent abuse
- Data privacy compliance (GDPR, etc.)

### 10.2 Performance Risks
- Circuit breakers for external service calls
- Graceful degradation when services are unavailable
- Resource limits to prevent system overload
- Monitoring and alerting for performance issues

## 11. Quality Assurance

### 11.1 Testing Strategy
- Unit tests for all business logic
- Integration tests for API endpoints
- End-to-end tests for critical user flows
- Performance tests for scalability validation

### 11.2 Code Quality
- Static analysis and linting
- Code review requirements
- Automated testing pipelines
- Documentation standards