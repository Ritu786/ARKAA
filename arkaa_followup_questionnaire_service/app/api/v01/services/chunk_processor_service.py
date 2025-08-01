from typing import List
from core.logging_config import set_logger

processor_logger = set_logger(__name__)

def process_chunks(docs: List):
    '''
    Merging page_content from a list of Document-like objects.

    Args:
        docs (List): List of documents, each expected to have 'page_content' attribute

    Returns:
        str: Combined string of page_contents seperated by newlines
    '''
    try:
        processor_logger.info(f'Start processing {len(docs)} document chunks.')
        processed_texts = []
        # iterating through each source_document
        for i, doc in enumerate(docs):
            # Skipping: if source_document doesn't posses page_content.
            if not hasattr(doc, 'page_content'):
                processor_logger.warning(f'Document at index {i} missing attribute "page_cntent". Skipping...')
                continue
            content = doc.page_content.strip()
            # Skipping: if source_document has empty page_content.
            if not content:
                processor_logger.debug(f'Document at index {i} has empty "page_content" after stripping. Skipping...')
                continue
            # Appending the page_contents into a list
            processed_texts.append(content)
        result = '\n\n'.join(processed_texts)
        processor_logger.info(f'Processed chunks combined length: {len(result)} characters.')
        return result
    except Exception as e:
        processor_logger.error(f'Error Occured in process_chunks: {e}', exc_info=True)
        processor_logger.info('Returning empty string...')
        return ''

