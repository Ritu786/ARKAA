from app_utils.config_loader import load_config_section
from retrieval.vector_retriever import VectorRetriever
from retrieval.multiquery_retriever import MultiQueryRetr
from app_utils.logger import set_logger

rf_logger = set_logger(__name__)


def get_retriever(vectorstore):
    """
    Initializes and returns a retriever based on configuration.

    Args:
        vectorstore: The vector database used for retrieval.

    Returns:
        A retriever instance as per the configuration.

    Raises:
        ValueError: If the retriever type is unsupported or config is invalid.
    """
    try:
        rf_logger.info('Loading retriever configuration')
        config = load_config_section('retriever')
        retriever_type = config['type']
        top_k = config['top_k']

        rf_logger.debug(f'Retriever type from config: {retriever_type}, top_k: {top_k}')

        if retriever_type == 'multi-query':
            return MultiQueryRetr(vectorstore,top_k=top_k).get_retriever()
        elif retriever_type == 'vector':
            return VectorRetriever(vectorstore, top_k=top_k).get_retriever()
        else:
            rf_logger.error(f'Unsupported retriever type: {retriever_type}')
            raise ValueError(f'Unsupported retriever type: {retriever_type}')
    except Exception as e:
        rf_logger.exception("Failed to initialize retriever")
        raise RuntimeError("Could not initialize retriever") from e
        

