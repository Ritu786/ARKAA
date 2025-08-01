from processors.translator.argos_translator import ArgosTranslator
from processors.translator.google_translator import DeepGoogleTranslator
from processors.translator.microsoft_translator import MicrosoftTranslator
from processors.translator.openai_translator import OpenAITranslator
from app_utils.logger import set_logger
from app_utils.yaml_loader import load_config

trans_manager_logger = set_logger(__name__)
config = load_config()
t_config = config.get('translator')

def get_translator():
    '''
    Factory method to return the appropriate translator based on configuration.

    Supported types: 'google', 'argos', 'microsoft', 'openai'

    Returns:
        BaseTranslator: An instance of the selected translator.
    
    '''
    try:

        # Translation type. 
        translator_type = t_config.get('type')
        trans_manager_logger.info(f'Using the Translator {translator_type}')

        # Source Lang to Target Lang
        source_lang = t_config.get('source_lang')
        target_lang = t_config.get('target_lang')

        trans_manager_logger.info(f'Initializing translator: {translator_type} ({source_lang} -> {target_lang})')

        if translator_type == 'google':
            return DeepGoogleTranslator(source_lang,target_lang)
        elif translator_type == 'argos':
            return ArgosTranslator(source_lang, target_lang) 
        elif translator_type == 'microsoft':
            return MicrosoftTranslator(source_lang, target_lang)
        elif translator_type == 'openai':
            return OpenAITranslator(source_lang, target_lang)
        else:
            trans_manager_logger.error(f'Unsupported Translator type: {translator_type}')
    except Exception as e:
        trans_manager_logger.exception(f'Failed to initialize translator: {str(e)}')
        raise