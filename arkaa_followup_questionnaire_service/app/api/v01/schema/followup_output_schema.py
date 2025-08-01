from typing import List, Dict
from pydantic import BaseModel

class QuestionAnswer(BaseModel):
    question: str
    answer: str

class FollowUpResponse(BaseModel):
    session_id: str
    questions: List[QuestionAnswer]