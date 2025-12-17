# **AI Multilingual Chatbot System — Full `spec.md` **  
Uses: **FastAPI (backend) + Next.js (frontend) + Better-auth + Qdrant + OpenAI Agents SDK + Sub-Agents + ChatKit UI + Translation Layer.**

---

## **1. System Overview**
A secure multilingual AI chatbot system where:  
- User **must sign in** to access the chatbot.  
- Backend handles **auth verification**, translation, routing to LLM sub-agents, vector search (Qdrant), and logging.  
- Frontend provides **ChatKit AI Chat UI**, language selector, and protected routes.  
- OpenAI **Agents SDK** orchestrates main agent + sub-agents.

---

## **2. Core Features**
### **2.1 Authentication**
- Users must sign in before accessing chatbot UI.  
- Supported options: **Better-auth**  
- Backend verifies auth using middleware.  
- Auth stores: userID, email, preferred language.

### **2.2 Language Translation**
- User chooses any language.  
- System uses a **Translation Layer**:
  - Incoming messages → Translated to English (use python automation).

### **2.3 Chatbot UI**
- Uses **OpenAI ChatKit JS** for front-end chat experience.  
- Custom top bar: model selector, language selector, logout button.  
- Supports file uploads, images, streaming responses.

---

## **3. Backend Architecture (FastAPI)**

### **3.1 Backend Modules**
/backend
/auth
- verify.py
/routes
- chat.py
- translate.py
- auth.py
- vector.py
/agents
- main_agent.py
- translator.py
- knowledge_agent.py
- task_agent.py
/db
- qdrant.py
/utils
- tokenizer.py
- text_cleaner.py
main.py


### **3.2 Backend Responsibilities**
- Validate login tokens.  
- Translate incoming/outgoing messages.  
- Forward requests to **main agent**.  
- Perform Qdrant vector search.  
- Store chat history.
- Stream responses to frontend.

---

## **4. Qdrant Vector DB**

### **4.1 Collection Structure**
collection: "chatbot_memory"
vectors: `def get_embedding(text):
    """Get embedding vector from Cohere Embed v3"""
    response = cohere_client.embed(
        model="embed-english-v3.0",
        input_type="search_query",  # Use search_query for queries
        texts=[text],
    )
    return response.embeddings[0]  # Return the first embedding
`
payload:
user_id: string
message: string
timestamp: int
metadata: {topic, lang, agent}


### **4.2 Vector Operations**
- Insert messages.  
- Retrieve top-k search results.  
- Provide memory context to main agent.

---

## **5. Main Agent Design**

### **5.1 System Prompt**
You are the MAIN CONTROLLER AGENT.
Your job:

Receive user message in English.
Detect intent.
Route:
Translation → Translator Agent
Search → Knowledge Agent
Reasoning/Coding → Task Agent
Merge results.
Return clean and structured answer.
Avoid hallucination. Ask for clarification if needed.


---

## **6. Frontend Architecture (Next.js)**

### **6.1 Folder Structure**
/frontend
/app
/chat
page.tsx
/api
chat/route.ts
layout.tsx
/components
ChatUI.tsx
LanguageSelector.tsx
ProtectedRoute.tsx
/lib
auth.ts
axios.ts
env


### **6.2 Frontend Responsibilities**
- User login.  
- Only authenticated users access chatbot.  
- ChatKit UI for messaging.  
- Maintain language state.  
- Send messages → backend `/chat` route.  
- Stream answer back to UI.

---

## **7. API Endpoints**

### **7.1 POST `/auth/verify`**
Validates frontend token.

### **7.2 POST `/chat`**
Main endpoint that:  
1. Verifies user token.  
2. Translates message to English.  
3. Sends to main agent.  
4. Translates to user language.  
5. Streams response back.

### **7.3 POST `/vector/upsert`**
Save embeddings.

### **7.4 POST `/vector/search`**
Search memory.

---

## **8. Workflow (End-to-End)**

### **Step 1 — User Logs In**
- Next.js → better-auth  [https://www.better-auth.com/docs]
- Token received → added to all requests.

### **Step 2 — User Enters Message**
Frontend sends:
{
message: "Hola, cómo estás?",
lang: "es",
user_id: "...",
token: "..."
}


### **Step 3 — Backend Auth Verification**
FastAPI verifies token → OK.

### **Step 4 — Translation Layer**
Translate Spanish → English.

### **Step 5 — Final Result**
LLM → translate to Spanish → stream to UI.

---

## **9. Safety + Anti-Hallucination**
- Fixed routing rules.   
- Clear steps → no ambiguity.  

---