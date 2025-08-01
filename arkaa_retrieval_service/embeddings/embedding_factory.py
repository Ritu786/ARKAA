from app_utils.logger import set_logger
from embeddings.openai_embedding import get_openai_embeddings
from app_utils.config_loader import  load_config_section
from dotenv import load_dotenv

load_dotenv()

ef_logger = set_logger(__name__)

def get_embedding():
    '''
    Initialized and returns an embedding model based on configuration.

    Returns:
        Embedding model instance (e.g. OpenAI, Nomic..etc)

    Rasies:
        ValueError: If the embedding type is unsupported.
        RuntimeError: For any unexpected errors during initialization.
    '''
    try:
        ef_logger.info('Loading embedding configuration')
        config = load_config_section("embedding")
        embedding_type = config.get("type", "openai")
        ef_logger.debug(f'Embedding type from cofnig: {embedding_type}')

        if embedding_type == "openai":
            ef_logger.info('Initializing OpenAI embeddings')
            return get_openai_embeddings()
        else:
            ef_logger.error(f"Unsupported embedding type: {embedding_type}")
    except ValueError as va:
        ef_logger.exception('Configuration error during embedding initialization.')
        raise va
    except Exception as e:
        ef_logger.exception(f'Unexpected Error {e} While Initializing embeddings.')
