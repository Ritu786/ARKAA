from abc import ABC, abstractmethod

class BaseVectorStore(ABC):
    @abstractmethod
    def store_documents(self, documents, embedding_model, collection_name):
        pass
