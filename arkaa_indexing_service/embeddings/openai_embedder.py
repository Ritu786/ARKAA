from embeddings.base_embedder import BaseEmbedder
from langchain_openai import OpenAIEmbeddings
from app_utils.exceptions import EmbeddingInitializationError
from app_utils.logger import set_logger
import os 

openaiemb_logger = set_logger(__name__)

class OpenAIEmbedder(BaseEmbedder):
    def __init__(self, api_key: str = None):
        
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError('OpenAI API Key not provided or set in environment.')
        try:
            self.embedder = OpenAIEmbeddings(openai_api_key=self.api_key)
            openaiemb_logger.info('OpenAI Embedder initialized successfully.')
        except Exception as e:
            openaiemb_logger.error(f'Failed to initialized OpenAI Embedder: {e}')
            raise EmbeddingInitializationError(f'OpenAI Embedder error: {e}')
            
    def get_embedder(self):
        return self.embedder
