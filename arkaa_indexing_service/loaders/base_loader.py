from abc import ABC, abstractmethod

class BaseLoader(ABC):
    @abstractmethod
    def load(self, file_path):
        '''
        Loads and returns the document content in unified format.
        Should return a list of 'Document' objects or dicts depending on the pipeline.
        '''
        pass