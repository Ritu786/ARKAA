from vectorstores.pgvector_store import PGVectorStore
from app_utils.logger import set_logger

vsf_logger = set_logger(__name__)

def get_vectorstore(vs_config, collection_name:str, embed_model=None):
    '''
        Chooses the vectorstore based on config.yaml
    '''
    try:
        # VectorStore Type
        store_type = vs_config.get('type')

        # Connection String
        connection_string = vs_config.get('connection_string')

        # Collection Name
        collection_name = collection_name

        use_jsonb = vs_config.get('use_jsonb', True)
        vsf_logger.info(f'Initializing vectorstore: {store_type}')

        if store_type == 'pgvector':
            return PGVectorStore(collection_name, connection_string, embed_model, use_jsonb)
        else:
            raise ValueError(f'Unsupported vectorstore type: {store_type}')
    except Exception as e:
        vsf_logger.error(f'Failed to load vectorstore config: {str(e)}', exc_info=True)
        raise
