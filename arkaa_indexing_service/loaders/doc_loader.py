from .base_loader import BaseLoader
from unstructured.partition.docx import partition_docx
from unstructured.chunking.title import chunk_by_title
from langchain_core.documents import Document
from app_utils.logger import set_logger
from app_utils.validators import validate_file_path
import time



doc_logger = set_logger(__name__)


class docLoader(BaseLoader):
    """
        Loader class for processing docx files using partition_docx from unstructured.io.
    """
    def __init__(self, strategy: str = 'hi_res', model: str = 'yolox', chunk_max_char: int = 4000, chunk_overlap: int = 104):
        """
            Initializing loader with loader specific parameters.

            Args:
                strategy (str): The parsing strategy to use, Defaults to 'hi_res'.
                model (str): The model used to parse the document, Model name, default 'yolox'.
                chunk_max_char (int): Max characters per chunk, default 4000.
                chunk_overlap (int): Overlap size between chunks, default 104.
        """
        self.strategy = strategy
        self.model = model
        self.chunk_max_char = int(chunk_max_char)
        self.chunk_overlap = int(chunk_overlap)

        if self.chunk_max_char <= 0:
            raise ValueError("chunk_max_char must be positive")
        if self.chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        
    def load(self, file_path):
        """
            Loads and processes a PDF file.

            Args:
                file_path (str): The path to the PDF file.
                    
            Returns:
                List[Documents]: A List of chunked Document Objects
        """
        validate_file_path(file_path)
        doc_logger.info(f'Started file Processing {file_path}...')
        try:
            start_time = time.time()
            # ParitionDocx from unstructured.io
            docx_elements = partition_docx(
                filename=file_path,
                strategy=self.strategy,
                infer_table_structure=True,
                hi_res_model_name=self.model,
                languages= ['eng','ara'],
                encoding = 'utf-8'
            )
            doc_logger.debug(f'Chunking...{file_path} using chunk_by_titile')
            chunked_doc_elements = chunk_by_title(docx_elements, max_characters=self.chunk_max_char, overlap=self.chunk_overlap, overlap_all=True)        
            end_time = time.time()
            elapsed = end_time - start_time
            doc_logger.info(f'Loaded and chunked: {file_path} in {elapsed:.2f} seconds')


            # Normalizing Documents...
            normalized_documents = []

            for chunked_doc_element in chunked_doc_elements:
                raw_text = chunked_doc_element.text
                if not raw_text.strip():
                    continue

                metadata = (
                    chunked_doc_element.metadata.to_dict()  if hasattr(chunked_doc_element.metadata, 'to_dict')
                    else chunked_doc_element.metadata or {}
                )

                
                if not metadata or 'filename' not in metadata:
                    doc_logger.warning(f'Skipping chunk due to missing metadata or filename for {file_path}')
                    continue

                metadata['source'] = metadata.get('filename', file_path)
                normalized_documents.append(Document(page_content=raw_text, metadata=metadata))
                
            doc_logger.info(f'{len(normalized_documents)} valid chunks extracetd from {file_path}')

            return normalized_documents
        except Exception as e:
            doc_logger.error(f'Failed to load {file_path}. Error: {str(e)}')
            raise
    
