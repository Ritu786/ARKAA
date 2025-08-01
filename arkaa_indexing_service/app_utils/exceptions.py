class LoaderNotFound(Exception):
    '''
    Raised when no suitable loader is found for a file type.
    '''
    pass

class TextTooLongError(Exception):
    '''
    Raised when the input text exceeds the allowed chaacters limit for Google Translator.
    '''
    def __init__(self,  message="Input text exceeds the character limit for this translator."):
        self.message = message
        super().__init__(self.message)

class EmbeddingInitializationError(Exception):
    '''
    Rasied when embedding is unable to initialize.
    '''
    def __init__(self, message='Failed to initalize Embedder'):
        self.message = message
        super().__init__(self.message)