from vectorstores.base_vectorstore import BaseVectorStore
from app_utils.config_loader import load_config_section
from langchain_postgres import PGVector
from embeddings.embedding_factory import get_embedding
import yaml
from app_utils.logger import set_logger

pg_logger = set_logger(__name__)

class PgVectorStore(BaseVectorStore):
    """
    A vector store implementation using PostgreSQL with pgvector extension.
    """
    def __init__(self):
        self.embedding = get_embedding()
        self.config = load_config_section("vectorstore")
    
    def get_store(self):
        """
            Instantiates and returns a PGVector store.

            Returns:
                PGVector instance configured with embeddings and DB connection.
        """
        try:
            pg_logger.info('Creating PGVector store instance')
            return PGVector(
                embeddings=self.embedding,
                connection=self.config['connection_string'],
                collection_name=self.config['collection_name'],
                use_jsonb=True
            )
        except Exception as e:
            pg_logger.exception('Failed to create PgVector store.')
            raise RuntimeError('Failed to create PGvector store instance.') from e