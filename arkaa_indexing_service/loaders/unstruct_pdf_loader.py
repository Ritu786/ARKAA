from .base_loader import BaseLoader
from langchain_core.documents import Document
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title
from app_utils.logger import set_logger
from app_utils.validators import validate_file_path
import time 


unstpdf_logger = set_logger(__name__)


class unstructPdfLoader(BaseLoader):
    '''
    Loader class for processing PDF files using Partition_PDF from Unstructured.io.
    '''
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

            Chunking using chunk_by_title from unstrucutred.io.

            Attributes:
                max_characters (int): max number of characters in a single chunk.
                overlap (int): number of characters to overlap between each chunk.
            
                    
            Returns:
                List[Documents]: A List of chunked Document Objects
        """
        validate_file_path(file_path)
        unstpdf_logger.info(f'Started file Processing {file_path}...')
        try:
            start_time = time.time()
            # ParitionPDF from unstruct.io
            pdf_elements = partition_pdf(
                filename=file_path,
                strategy=self.strategy,
                infer_table_structure=True,
                hi_res_model_name=self.model,
                languages= ['eng','ara'],
                encoding = 'utf-8'
            )
            unstpdf_logger.debug(f'Chunking...{file_path}')
            chunked_pdf_elements = chunk_by_title(pdf_elements, max_characters=self.chunk_max_char, overlap=self.chunk_overlap, overlap_all=True)
            end_time = time.time()
            elapsed = end_time - start_time
            unstpdf_logger.info(f'Loaded and chunked: {file_path} in {elapsed:.2f} seconds')

             # Normalizing Documents...
            normalized_pdf_documents = []

            for chunked_pdf_element in chunked_pdf_elements:
                raw_text = chunked_pdf_element.text
                if not raw_text.strip():
                    continue

                metadata = (
                    chunked_pdf_element.metadata.to_dict()  if hasattr(chunked_pdf_element.metadata, 'to_dict')
                    else chunked_pdf_element.metadata or {}
                )

                
                if not metadata or 'filename' not in metadata:
                    unstpdf_logger.warning(f'Skipping chunk due to missing metadata or filename for {file_path}')
                    continue

                metadata['source'] = metadata.get('filename', file_path)
                normalized_pdf_documents.append(Document(page_content=raw_text, metadata=metadata))
            
            unstpdf_logger.info(f'{len(normalized_pdf_documents)} valid chunks extracetd from {file_path}')
            return normalized_pdf_documents
        except Exception as e:
            unstpdf_logger.error(f'Failed to load {file_path}. Error: {str(e)} ')
            raise
    

       
