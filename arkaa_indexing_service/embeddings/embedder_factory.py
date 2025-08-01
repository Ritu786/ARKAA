from embeddings.openai_embedder import OpenAIEmbedder
from app_utils.logger import set_logger

ef_logger = set_logger(__name__)

def get_embeddings(emb_config):
    """
    Factory method to return appropriate embeddings based on the config.yaml
    """
    try:
        embeddings_type = emb_config.get('type','openai')
        ef_logger.info(f'Initiated the Embedding: {embeddings_type}')

        if embeddings_type == 'openai':
            return OpenAIEmbedder().get_embedder()
        else:
            ef_logger.error(f'Unsupported Embedding type: {embeddings_type}')
        
    except Exception as e:
        ef_logger.error(f"Failed to load embeddings: {str(e)}", exc_info=True)
    


