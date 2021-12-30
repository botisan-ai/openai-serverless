from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class SearchDocument(BaseModel):
    object = "search_result"
    document: int
    z_val: Optional[float]
    score: float
    text: str
    metadata: Optional[Dict[str, Any]]

class BetterAnswersOutput(BaseModel):
    object = "better_answer"
    answers: List[str]
    completion: str
    file: str
    model: str
    search_model: str
    prompt: Optional[str]
    selected_documents: List[SearchDocument]
