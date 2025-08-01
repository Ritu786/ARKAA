import langid
from app_utils.logger import set_logger


langdetect_logger = set_logger(__name__)

def detect_language(text: str):
    '''
    Detects the language of a given text using langid

    Args:
        text (str): The input text to detect the lnaguage of.

    Retuns:
        str: The ISO 639-1 language code (e.g. 'en', 'ar')
    
    Rasies:
        ValueError:  if the input text is empty or detection fails.
    '''

    if not text or not text.strip():
        langdetect_logger.warning('Empty text recieved for language detection')
    try:
        # Using Langid for Language detection
        lang, _ = langid.classify(text)
        return lang
    except Exception as e:
        langdetect_logger.error(f'Language detection failed: {str(e)}')
