from vectorstores.base_vectorstore import BaseVectorStore
from langchain_postgres.vectorstores import PGVector
from langchain_community.vectorstores.utils import filter_complex_metadata
from app_utils.logger import set_logger

pg_logger = set_logger(__name__)



class PGVectorStore(BaseVectorStore):
    def __init__(self, collection_name: str,connection_string: str, embed_model, use_jsonb: bool = True):
        self.collection_name = collection_name
        self.connection_string = connection_string
        self.embed_model = embed_model
        self.use_jsonb = use_jsonb
  
    

    def store_documents(self, documents):
        """
        Storing Documents within the Vector Database.

        Args:
        documents: chunks of the document.

        Return:
        db: LangChain datbase instance.
        """
        try:
            pg_logger.info(f'Storing {len(documents)} docs into PGVector: {self.collection_name}')
            # Creating & Storing Embeddings 
            db = PGVector.from_documents(
                embedding=self.embed_model,
                documents = filter_complex_metadata(documents),
                collection_name=self.collection_name,
                connection=self.connection_string,
                use_jsonb=self.use_jsonb
            )
            return db
        except Exception as e:
            pg_logger.error(f"Failed to store documents in PgVector: {str(e)}")
            raise
        