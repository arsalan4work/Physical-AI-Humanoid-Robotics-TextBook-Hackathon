from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    context_window: Optional[int] = 5
    user_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class TextSelectionRequest(BaseModel):
    selected_text: str
    question: str
    context_window: Optional[int] = 5