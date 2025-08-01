from langchain_core.documents import Document
from processors.translator.base_translator import BaseTranslator
from processors.language_detector import detect_language
from app_utils.logger import set_logger

translate_logger = set_logger(__name__)

# Supporting only Arabic & English

def translate_if_needed(doc: Document, translator:BaseTranslator):
  '''
  Translates the document content to English if it's in Arabic.

  Args:
    doc (Document): LangChain Document object containing content and metadata.
    translator (BaseTranslator): An initialized translator implementing a 'translate(text)' method.

  Returns:
    Document: Translated document if needed, otherwise original Document.
  
  '''
  try:
    lang = detect_language(doc.page_content)
    if lang == 'ar':
            translate_logger.info("Arabic detected. Translating...")
            translated_text = translator.translate(doc.page_content)
            return Document(page_content=translated_text, metadata=doc.metadata)
    else:
        translate_logger.info('Non-Arabic content detected. No Translation needed.')
        return doc

  except Exception as e:
      translate_logger.error(f'Translation for the doc: {e}')
      return doc
    