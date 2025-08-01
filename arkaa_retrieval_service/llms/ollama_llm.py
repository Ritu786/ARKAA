from llms.base_llm import BaseLLM
from app_utils.logger import set_logger
from langchain_ollama import ChatOllama

ollama_logger = set_logger(__name__)
class OllamaLLm(BaseLLM):
    '''
    A wrapper class for initializing and retireving a ChatOllama instance based 
    on configuration and environment settings.
    
    '''
    def __init__(self, config: dict):
        '''
        Initialization the Ollama Chat LLM with specified configuration.

        Args:
            config (dict): Dictionary containing temprature and other optional parameters.
        '''
        try:
            model = config.get('type','llama3')
            ollama_logger.info(f'Intializing {model} LLM through Ollama.')

            self.llm = ChatOllama(
                base_url='http://20.51.209.84:11434',
                model=model,
                temperature=config['temperature'],
                # disable_streaming=True,
                # tags=['qwen']
            )

            ollama_logger.info(f'{model} instance sucessfully created using Ollama.')

        except Exception as e:
            raise RuntimeError(f'Error While Initializing {model} LLm: {e}')

    def get_llm(self):
        return self.llm