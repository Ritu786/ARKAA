from processors.translator.base_translator import BaseTranslator
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
import os 
from dotenv import load_dotenv
from app_utils.logger import set_logger
from prompts.openai_translator_prompt import OPENAI_TRANSLATOR


load_dotenv()
openaitrans_logger = set_logger(__name__)


class OpenAITranslator(BaseTranslator):
    '''
    Translator that uses OpenAI LLM to translate text from Arabic to English using a prompt temaplte. 

    This translator assumes the input is Arabic and uses a prompt-based chain for translation.
    '''
    def __init__(self, source_lang: str='ar', target_lang: str = 'en'):
        '''
        Initializes the LLM translator with the given API Key & temperature. 

        Args:
            api_key (str, optional):  OpenAI API KEY, if not provided, it will use the OPENAI_API_KEY from .env file. 
            temperature (float): Contorls randomness of the output (default: 0)
        
        '''
        self.source_lang = source_lang
        self.target_lang = target_lang
        try:
            self.api_key = os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            self.template = OPENAI_TRANSLATOR
            self.prompt = PromptTemplate.from_template(self.template)

            # Setup Open AI LLM
            self.translator_llm = OpenAI(openai_api_key=self.api_key, temperature=0)

            # Conversational Chain
            self.chain = ( self.prompt | self.translator_llm )
        except Exception as e:
            openaitrans_logger.error(f'Failed to initialize OpenAI Translator: {str(e)}')
    
    def translate(self, text):
        '''
        Translates the input Arabic text to English using LLM.

        Args:
            text (str): Arabic text to translate.
        
            Returns:
                str: Translated English text.

            Raises:
                RuntimeError:  if translation Fails. 
        
        '''
        try:
            openaitrans_logger.debug('Sending text to LLM for translation...')
            response = self.chain.invoke(text)
            openaitrans_logger.debug('Translation successful...')
            return response
        except Exception as e:
            openaitrans_logger.error(f'Translation Failed: {str(e)}')
