from retrieval.base_retriever import BaseRetriever
from app_utils.logger import set_logger

v_logger = set_logger(__name__)

class VectorRetriever(BaseRetriever):
    '''
    Basic retiriever using vector store similarity search. 

    '''
    def __init__(self, v_db, top_k: int=3):
        '''
        Initializes the vector retriever with a given vector DB and top_k value.

        Args:
            v_db: A vector database object with `.as_retriever()` method.
            top_k (int): Number of top results to retrieve.
        '''
        try:
            v_logger.debug(f"Initializing VectorRetriever with top_k={top_k}")
            self.retriever = v_db.as_retriever(search_kwargs={'k': top_k})
            v_logger.info("VectorRetriever successfully initialized")
        except Exception as e:
            v_logger.exception("Error initializing VectorRetriever")
            raise RuntimeError("Failed to initialize VectorRetriever") from e
    def get_retriever(self):
        """
        Returns the configured retriever instance.

        Returns:
            A retriever object configured to retrieve top-k results.
        """
        return self.retriever