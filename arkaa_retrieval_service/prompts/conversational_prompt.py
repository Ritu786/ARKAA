from langchain.prompts import ChatPromptTemplate
from app_utils.logger import set_logger

prompt_logger = set_logger(__name__)

def get_conversational_prompt():
    '''
    Defines the Prompt

    Returns:
        Prompt: LangChain Prompt Instance.
    '''
    conversational_template ="""
            Answer the Question based on the following context:
            {context}
            Answer the Question Based on the above context: {question}.
            Provide a detailed answer
            Don't give information not mentioned in the CONTEXT INFORMATION.
            Do not say "according to the context" or "mentioned in the context" or similar.
            If user is mentioning prvious chat, try to answer from History: {chat_history}
    """
    prompt_logger.info('Initializes the LangChain Prompt Template...')
    conversational_prompt = ChatPromptTemplate.from_template(conversational_template)
    return conversational_prompt

