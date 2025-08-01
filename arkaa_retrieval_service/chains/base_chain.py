from abc import ABC, abstractmethod

class BaseChain(ABC):
    @abstractmethod
    def get_chain(self):
        pass