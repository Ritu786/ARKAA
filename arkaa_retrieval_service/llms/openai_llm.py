from llms.base_llm import BaseLLM
from app_utils.logger import set_logger
from langchain_openai import ChatOpenAI
import os

openaillm_logger = set_logger(__name__)

class OpenAILLM(BaseLLM):
    '''
    A wrapper class for initializing and retireving a ChatOpenAI instance based 
    on configuration and environment settings.

    '''
    def __init__(self, config: dict):
        '''
        Initialization the OpenAI Chat LLM with specified configuration.

        Args:
            config (dict): Dictionary containing temprature and other optional parameters.
        '''
        try:
            model = config.get('type','gpt-4o')
            openaillm_logger.info(f'Initializing OpenAI LLM: {model}')

            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                openaillm_logger.error('OPENAI_API_KEY not found in environment')
                raise ValueError('OPENAI_API_KEY not set in environment variables')
            
            self.llm = ChatOpenAI(
                openai_api_key = api_key,
                model=model,
                temperature=config['temperature'],
                max_tokens=1024,
                max_retries=2,
                model_kwargs={
                    "top_p":0.4
                }
            )
            openaillm_logger.debug(f'OpenAI LLM {model} instance successfully created.')

        except Exception as e:
            openaillm_logger.exception(f'Failed to initialize OpenAI LLM {model}')
            raise RuntimeError(f'Error while creating OpenAI LLM {model}') from e
    
    def get_llm(self):
        '''
        Returns the instantiated LLM. 

        Returns:
            ChatOpenAI: An instance of the OpenAI LLM.
        '''
        return self.llm