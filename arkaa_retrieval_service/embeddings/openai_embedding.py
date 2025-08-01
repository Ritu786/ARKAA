import os 
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from app_utils.logger import set_logger


load_dotenv()
opaiembd_logger = set_logger(__name__)

def get_openai_embeddings(config: dict=None):
    """
    Initializes and returns an OpenAIEmbeddings instance.

    Args:
        config (dict, optional): Configuration dictionary to specify embedding model name.
                                 Defaults to 'text-embedding-ada-002' if not provided.

    Returns:
        OpenAIEmbeddings: An instance configured with the API key and specified model.

    Raises:
        ValueError: If the OpenAI API key is not found in the environment.
        RuntimeError: For unexpected errors during initialization.
    """
    try:
        opaiembd_logger.info('Fetching OpenAI  API Key from .env')
        api_key = os.getenv('OPENAI_API_KEY')


        if not api_key:
            opaiembd_logger.error('OPENAI_API_KEY is not found in .env variables.')
            raise ValueError('OPENAI API KEY NOT FOUND in .env')
        
        model = config.get("model", "text-embedding-ada-002") if config else "text-embedding-ada-002"
        opaiembd_logger.debug(f'Using embedding model: {model}')

        opaiembd_logger.info('Creating OpenAIEmbeddings instance')
        return OpenAIEmbeddings(
            model=model,
            openai_api_key = api_key
        )
    except ValueError as ve:
        opaiembd_logger.exception('COnfiguration error in get_openai_embeddings')
        raise ve

    except Exception as e:
        opaiembd_logger.exception(f'Unexpected error while creating OpenAIEmbeddings')
        raise RuntimeError('Failed to initialize OpenAI Embeddings') from e

