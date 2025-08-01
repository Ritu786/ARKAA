import requests
import uuid
import json
import os
from dotenv import load_dotenv
from processors.translator.base_translator import BaseTranslator
from app_utils.logger import set_logger

# Load environment variables from .env file.
load_dotenv()

mstrans_logger = set_logger(__name__)

class MicrosoftTranslator(BaseTranslator):
    '''
    A translator class that interfaces with Microsoft Azure's Translator Text API.
    Translates text from a source language to a target language using cloud-based translation.

    '''
    def __init__(self, source_lang: str = 'ar', target_lang: str = 'en'):
        '''
        Initialize the Microsoft Translator with source & target languages.

        Args:
            source_lang (str): Source Language code  (default is 'ar' for Arabic).
            target_lang (str): Target Language code (default is 'en' for english).

        Raises:
            ValueError: if the API key is not set in the environment.        
        '''
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.api_key = os.getenv('MS_TRANSLATOR_KEY')
        self.region = os.getenv('MS_TRANSLATOR_REGION', 'eastus')
        self.endpoint = os.getenv('MS_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com')

        if not self.api_key:
            raise ValueError('Microsoft Translator API key not found in environment.')
        
    def translate(self, text: str):
        '''
        Translate a given text using Microsoft Translator API.

        Args:
            text (str): The input text to be translated.

        Returns:
            str: The translated text in the target language.

        Raises:
            RuntimeError: If the API request fails or the response is malformed.
        
        '''
        path = "/translate"
        constructed_url = self.endpoint + path

        # Translation parameters
        params = {
            'api-version': '3.0',
            'from': self.source_lang,
            'to': [self.target_lang]
        }
        
        # Microsoft Translator API requires specific headers including region and subscription key
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Ocp-Apim-Subscription-Region': self.region,
            'Content-type': 'application/json',
            'ass-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': text
        }]

        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()

        # Extract translated text from the API response
        translated_text = response[0]['translations'][0]['text']

        return translated_text

      