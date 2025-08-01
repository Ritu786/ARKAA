from vectorstores.pgvector_store import PgVectorStore
from app_utils.config_loader import load_config_section
from app_utils.logger import set_logger
import yaml

vf_logger = set_logger(__name__)
def get_vectostore():
    '''
    Factory function to initialize and return the configured vector store instance.

    Returns:
        An instance of the vector store (e.g., PGVector).

    Raises:
        RuntimeError: If initialization fails.
        ValueError: If the vector store type is unsupported.
    '''
    try:
        vf_logger.info('Loading vectorstore configuration')
        config = load_config_section('vectorstore')

        vectorstore_type = config['type']

        vf_logger.debug(f"Vectorstore type detected: {vectorstore_type}")
        if vectorstore_type == 'pgvector':
            return PgVectorStore().get_store()
        else:
            raise ValueError(f'Unsupported Vectorsotre Type {vectorstore_type}')
    except Exception as e:
        vf_logger.exception("Error while initializing vector store")
        raise RuntimeError("Failed to initialize vector store") from e
    