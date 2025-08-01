from api.v01.services.chunk_processor_service import process_chunks
from api.v01.services.prompt_service import define_prompt
from api.v01.services.qa_service import create_qa
from core.utils import truncate_text
from core.logging_config import set_logger

followup_manager = set_logger(__name__)
async def generate_followup_questions(docs, current_query: str, session_id: str):
    """
    Genrates follow-up questions using the provided documents and query.

    Args:
        docs (List[Document]): List of document chunks.
        current_query (str): The Current user question.
        session_id (str): Session Identifier for tracking.
    
    Returns:
        str: Generated follow-up questions as single string.
    
    """
    try:
        followup_manager.info(f"Session [{session_id}]: Starting follow-up question generation.")
        # Step 1: Processing the chunks into plane text.
        processed_text = process_chunks(docs)

        # Step 2: Truncating the text to avoid LLM Token limit
        truncated_chunks = truncate_text(processed_text,6500)

        # Step 3: Defining the prompt
        q_prompt = define_prompt(truncated_chunks, current_query)

        # Step 4: Generating the Questions
        questions = await create_qa(q_prompt)
        followup_manager.info(f'Session [{session_id}]: Successfully generated questions.')
        
        return questions

    except Exception as e:
         followup_manager.error(f'Session [{session_id}]: Failed to generate follow-up questions: {e}', exc_info=True)
         return ""

