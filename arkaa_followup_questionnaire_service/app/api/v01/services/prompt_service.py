from core.logging_config import set_logger

prompt_logger = set_logger(__name__)
def define_prompt(docs_text: str, current_query: str) -> str:
    """
    Constructs a structured prompt for the LLM to generate follow-up questions.

    Args:
        docs_text (str): Combined text extracted from document chunks. 
        current_query (str): The current user query to geenrate follow-ups from. 

    Return:
        str: A formatted prompt string rwasy to be sent to the LLM.
    
    """
    try:
        # For empty input parmaters.
        if not docs_text or not current_query:
            prompt_logger.warning('Empty "docs_text" or "current_query" recieved.')

        prompt_logger.info('Defining prompt for follow-up question generation')
        # Defining the prompt
        qa_prompt = f"""
        
        You are a assistant tasked to generate follow-up questions and answers.Based on the following context, generate insightful follow-up 5 questions. 

        # INSTRUCTIONS
            1. Respond ONLY with the questions and answers.
            2. DO NOT INCLUDE 'I DON'T KNOW' WITHIN THE QUESTIONS.
            3. DO NOT INCLUDE 'FROM THE DOCUMENT' and 'FROM THE CONTEXT' WITHIN THE QUESTIONS.
            4. CURRENT QUESTION SHOULD NOT BE PRESENT IN THE FOLLOW UP QUESTIONS.
            5. CREATE RELEVANT QUESTIONS BASED ON THE CONTEXT. CONEXT SHOULD BE ABLE TO ANSWER THE QUESTIONS.
            6. Build Questions similar to CURRENT QUERY
            7. Return ONLY a valid JSON array (do not include triple backticks or markdown formatting).


            # CONTEXT
            {docs_text}

            # CURRENT QUERY
            {current_query}

            # OUTPUT FORMAT in JSON FORMAT
            Generate question-answer pair in the following format
            {{
                "question": "...",
                "answer": "..."
                
            }}
            """.strip()
        
        prompt_logger.debug(f'Prompt length: {len(qa_prompt)} characters')
        return qa_prompt
    except Exception as e:
        prompt_logger.error(f'Error generating prompt: {e}', exc_info=True)
        return ""
        
