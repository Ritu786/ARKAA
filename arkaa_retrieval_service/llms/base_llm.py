from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def get_llm():
        pass