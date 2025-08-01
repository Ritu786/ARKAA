from llms.openai_llm import OpenAILLM
from llms.ollama_llm import OllamaLLm
from app_utils.config_loader import load_config_section
from app_utils.logger import set_logger


llmf_logger = set_logger(__name__)

def get_llm():
    '''
    Loads and returns a language model (LLM) instance based on configuration.

    Returns:
         An LLM instance (e.g., OpenAI LLM).
    
    Raises:
        ValueError: if the LLM type is unsupported or missing.
        RuntimeError: if an unexpected error occurs during initialization.
    '''
    try:
        config = load_config_section('llm')
        # llm_type = config['type']
        framework = config.get('framework','openai').lower()

        if framework == 'openai':
            llmf_logger.info('Initializing {framework}')
            return OpenAILLM(config).get_llm()
        elif framework == 'ollama':
            llmf_logger.info('Initializing {framework}')
            return OllamaLLm(config).get_llm()
        else:
            llmf_logger.error(f'Unsupported LLM Framework:{framework}')
            raise ValueError(f'Unsupported LLM Framework:{framework}')
        
    except ValueError as ve:
        llmf_logger.exception('Configuration error in get_llm')
        raise ve
    except Exception as e:
        llmf_logger.exception('Unexpected error while initializing llm.')
        raise RuntimeError('Failed to initialize llm') from e