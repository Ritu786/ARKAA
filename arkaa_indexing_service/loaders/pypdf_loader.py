from .base_loader import BaseLoader
from langchain_community.document_loaders import PyPDFLoader
from app_utils.logger import set_logger
from app_utils.validators import validate_file_path
from app_utils.yaml_loader import load_config
import time


pypdf_logger = set_logger(__name__)

# Default setting chunking by page if not specified. 


class PiPDFLoader(BaseLoader):
    """
        Loader class for processing PDF files using PyPDFLoader from LangChain.

        Attributes:
            mode (str): The chunking strategy to use, Defaults to 'page'.
    """
    def __init__(self, mode: str = "page"):
        '''
        Initializing the loader with specific paramters.

        Args:
            mode (str): Chunking mode for PDF, defaults to 'page'.
        '''
        self.mode = mode

    def load(self, file_path:str):
        """
        
            Loads and processes a PDF file.

            Args:
                file_path (str): The path to the PDF file.
            
            Returns:
                List[Documents]: A List of chunked Document Objects
        
        """
        # Validate that the file path exists.
        validate_file_path(file_path)
        pypdf_logger.info(f'Started file Processing {file_path}...in mode {self.mode}')
        try:
            start_time = time.time()
            # PYPDF Loader using chunking mode
            loader = PyPDFLoader(
                file_path,
                mode=self.mode
            )
            end_time = time.time()
            elapsed = end_time - start_time
            pypdf_logger.info(f'Loaded and chunked: {file_path} in {elapsed:.2f} seconds')
            return loader.load()
        except Exception as e:
            pypdf_logger.error(f'Failed to load {file_path}. Error: {str(e)}')
            raise