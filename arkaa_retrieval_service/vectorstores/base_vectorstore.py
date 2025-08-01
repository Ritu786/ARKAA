from abc import ABC, abstractmethod

class BaseVectorStore(ABC):
    @abstractmethod
    def get_store(self):
        pass