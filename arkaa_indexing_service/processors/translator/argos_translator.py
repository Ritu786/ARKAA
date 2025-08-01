from processors.translator import base_translator
import argostranslate.package
import argostranslate.translate
from app_utils.logger import set_logger

ags_logger = set_logger(__name__)

class ArgosTranslator():
    '''
    Translator using Argos Translate (offline, open-source)

    Automatically installs the necessary packages for the given source and target languages.

    Attributes:
     source_lang (str): Source language code (default: 'ar')
     target_lang (str): Target language code (default: 'en')
    '''
    def __init__(self, source_lang: str = 'ar', target_lang: str = 'en'):
        '''
        Initalizes the ArgosTranslator with specified source and target language,
        and ensures the necessary translation package is installed.
        '''
        self.source_lang = source_lang
        self.target_lang = target_lang
        self._install_package_if_needed()

    def _install_package_if_needed(self):
        '''
        Checks and installs the Argos translation package if not already available.

        Rasies:
            ValueError: If no suitable translation package is found. 
        '''
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        try:
            # Installing the Required Language packages 
            package = next(
                filter(
                    lambda x: x.from_code == self.source_lang and x.to_code == self.target_lang,
                    available_packages
                )
            )
            ags_logger.info(f'Installing Argos package for {self.source_lang} -> {self.target_lang}..')
            argostranslate.package.install_from_path(package.download())
            ags_logger.info('Successfully Installed translation pacakge...')
        except StopIteration:
            ags_logger.error(f'No Argos translation package found for {self.source_lang} -> {self.target_lang}')
        except Exception as e:
            ags_logger.exception(f'Unexpected error during package installation: {e}')
            raise
    
    def translate(self, text: str) -> str:
        '''
        Translates the input text using Argos Translate. 

        Args:
            text (str): Text to be translated. 
        
        Returns:
           Exception: if translation fails.
        
        '''
        try:
            ags_logger.debug(f'Translating text from {self.source_lang} to {self.target_lang}')
            translated_text = argostranslate.translate.translate(text, self.source_lang, self.target_lang)
            ags_logger.debug('Translation successful...')
            return translated_text
        except Exception as e:
            ags_logger.error(f'Translation failed: {str(e)}')
            raise