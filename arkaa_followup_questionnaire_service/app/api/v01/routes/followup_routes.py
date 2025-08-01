from fastapi import APIRouter
from api.v01.schema.followup_input_schema import FollowUpRequest
from api.v01.schema.followup_output_schema import FollowUpResponse
from api.v01.services.followup_manager import generate_followup_questions
import json 
from fastapi import HTTPException
from core.logging_config import set_logger

router = APIRouter()
router_logger = set_logger(__name__)

def clean_and_parse_questions(raw_questions: str):
    '''
    Parses the raw LLM response into JSON.
    Raises 400 error if parsing fails. 

    '''
    try:
        return json.loads(raw_questions)
    except json.JSONDecodeError as e:
        router_logger.error(f'Failed to parse the questions: {e}')
        return []

@router.post('/generate-followups', response_model=FollowUpResponse)
async def generate_qa(request: FollowUpRequest):
    """
    Endpoint to generate follow-up questions based on document chunks and user query.
    """
    
    router_logger.info(f"Recieved request for session_id={request.session_id}")
    try:
        questions = await generate_followup_questions(
            docs = request.source_documents,
            current_query = request.current_question,
            session_id= request.session_id
        )
        
        parsed_questions = clean_and_parse_questions(questions)

        router_logger.info(f'Sucessfully returned questions for session_id={request.session_id}')
        return {
            'session_id': request.session_id,
            'questions': parsed_questions
        }
    except Exception as e:
        router_logger.exception(f'Unexpected error during follow-up generation: {e}')
        return {
            'session_id': "",
            "questions": ""
        }