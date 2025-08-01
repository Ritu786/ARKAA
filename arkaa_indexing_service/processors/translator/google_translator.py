from processors.translator.base_translator import BaseTranslator
from deep_translator import GoogleTranslator
from app_utils.exceptions import TextTooLongError
from app_utils.logger import set_logger

gtrans_logger = set_logger(__name__)

class DeepGoogleTranslator(BaseTranslator):
    '''
    Translator using Deep Translator's Google Translate API (free version).

    Supports automatic language detection and handles upto 5000 chacters per request.

    Attributes:
        source_lang (str): Source language code (default: 'auto').
        target_lang (str): Target language code (default: 'en').
    '''
    def __init__(self, source_lang: str = 'auto', target_lang: str = 'en'):
        '''
        Initializes the translator with source and target language codes.
        '''
        self.source_lang = source_lang
        self.target_lang = target_lang
        try:
            self.translator = GoogleTranslator(source=self.source_lang, target=self.target_lang)
        except Exception as e:
            gtrans_logger.error(f'Failed to initialize GoogleTranslator: {str(e)}')
            raise RuntimeError(f'Initialization failed: {str(e)}')
    def translate(self, text: str) -> str:
        '''
        Translates a given text to the target language.

        Args:
            text (str): The text to be translated.
        
        Returns:
            str: The translated text.

        Raises:
            RuntimeError: If translation fails.
        '''
        try:
            gtrans_logger.debug(f'Translating text with GoogleTranslator...')
            translated = self.translator.translate(text)
            gtrans_logger.debug(f'Translation successful...')
            return translated
        except Exception as e:
            gtrans_logger.error(f'Translation failed: {str(e)}')
            raise RuntimeError(f'Translation Failed: {str(e)}')

