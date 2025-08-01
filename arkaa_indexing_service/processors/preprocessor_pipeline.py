from langchain_core.documents import Document
from typing import List
from processors.translator.translator_factory import get_translator
from processors.translation_process import translate_if_needed
from app_utils.logger import set_logger

pre_logger = set_logger(__name__)

class PreProcessPipeline:
    '''
    Pipeline to preprocess documents including translation if needed.
    '''
    def __init__(self):
        self.translator = get_translator()

    def process_documents(self, docs: List[Document]):
        '''
        Processes documents by detetcing language and translating if needed.

        Agrs:
            docs (list[Document]): List of documents to process.

        Returns:
            list[Document]: List of processed documents.

        '''
        processed_docs = []

        for doc in docs:
            try:
                # Translating docs based on the classifying chunks
                translated_doc = translate_if_needed(doc, self.translator)
                processed_docs.append(translated_doc)
            except Exception as e:
                pre_logger.error(f'Error during processing documents: {e}')

        pre_logger.info(f'Successfully processed {len(processed_docs)} documents')
        return processed_docs