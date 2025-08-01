from typing import List, Dict, Any
from pydantic import BaseModel

class DocumentInput(BaseModel):
    '''
    Pydantic Document Schema for Validation.
    '''
    metadata: Dict[str, Any]
    page_content: str

class FollowUpRequest(BaseModel):
    session_id: str
    current_question: str
    source_documents: List[DocumentInput]
    