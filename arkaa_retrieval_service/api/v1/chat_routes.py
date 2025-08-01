from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_service import handle_chat
from chains.chain_factory import get_chain

# Initializing the API Router
router = APIRouter()


class ChatRequest(BaseModel):
    '''
    Request model for a chat interaction.

    Attributes:
        session_id (str): Unique ID to identify the user's chat session.
        question (str): The user's query or messsage to the chatbot.
    '''
    session_id : str
    question : str

@router.post('/ask')
async def chat_endpoint(request:ChatRequest):
    '''
    Chat endpoint that recieves a question from the user, and returns an RAG Generated answer.

    Args:
        request (ChatRequest): Contains the session id and the user's question.

    Returns:
        dict: A dictionary with the RAG Genrated 'answer' and the related 'source_documents'
    '''
    # Initializing the qa_chain, from chat_services.py
    qa_chain = get_chain(request.session_id)

    response = await handle_chat(qa_chain, request.question)
    return {
        'answer': response['answer'],
        'source_files': response['source_documents'],
        'session_id': request.session_id
    }