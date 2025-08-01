from abc import ABC, abstractmethod

class BaseEmbedder(ABC):
    '''
    Abstract base calsss for embedding model initializers.
    '''
    @abstractmethod
    def get_embedder(self):
        '''
        Returns the embedding object that supports embed_dccouments().

        '''
        pass

    