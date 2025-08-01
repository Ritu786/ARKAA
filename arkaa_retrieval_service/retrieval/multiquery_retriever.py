from retrieval.base_retriever import BaseRetriever
from retrieval.vector_retriever import VectorRetriever
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
import os 
from app_utils.logger import set_logger
from dotenv import load_dotenv

mq_logger = set_logger(__name__)

class MultiQueryRetr(BaseRetriever):
    '''
    LangChain Multi-Query retiriever that rephrases the original query using an LLM and fetches
    results from a vector store using multiple perspective of the query.
    '''
    def __init__(self, vectorstore, top_k):
        '''
        Initializes the multi-query retriever with a base retriever and LLM for query expansion.

        Args:
            vectorstore: Vector store instance to retrieve documents from.
            top_k (int): Number of top documents to retrieve.

        '''
        try:
            mq_logger.info("Initializing MultiQueryRetriever")

            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                mq_logger.error("OPENAI_API_KEY not found in environment")
                raise ValueError("Missing OPENAI_API_KEY in environment variables")

            # base retriever
            base_retriever = VectorRetriever(vectorstore, top_k).get_retriever()

            # LLM for Query Re-Phrasing
            # Improvement: Flexible to change LLM
            self.q_llm = ChatOpenAI(openai_api_key=api_key)

            # Build Multi-Query Retriever
            self.mq_retriever = MultiQueryRetriever.from_llm(
                retriever = base_retriever,
                llm = self.q_llm,
                include_original = True
            )
            mq_logger.debug('MultiQueryRetriever successfully initialized')
        except Exception as e:
            mq_logger.exception('Failed to initialize MultiQueryRetriever')
            raise RuntimeError('Error while creating MultiQueryRetriever') from e

    def get_retriever(self):
        """
        Returns the initialized multi-query retriever.

        Returns:
            MultiQueryRetriever: The configured retriever instance.
        """
        return self.mq_retriever