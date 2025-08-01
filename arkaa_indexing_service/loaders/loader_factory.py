from loaders.pypdf_loader import PiPDFLoader
from loaders.doc_loader import docLoader
from loaders.unstruct_pdf_loader import unstructPdfLoader
from loaders.base_loader import BaseLoader
from app_utils.logger import set_logger
from app_utils.exceptions import LoaderNotFound

factory_logger = set_logger(__name__)

LOADER_MAPPING = {
     "pypdf": PiPDFLoader,
     "unstruct-pdf": unstructPdfLoader,
     "unstruct-docx": docLoader,
}

def get_loader(loader_config, file_path: str) -> BaseLoader:
        
        """
        Factory method to return the appropriate loader instance based on
        the file extenstions.
        Supports  .pdf & .docx files; raises an error for unsupported formats.

        Args:
        file_path (str):  Path of the file for extraction.
                
        """
        try:
            factory_logger.info(f"Loading started for: {file_path}")
            ext = file_path.lower()
            # IF file name endswith .pdf
            if ext.endswith('.pdf'):
                loader_name = loader_config.get('default_pdf', 'pypdf')
                loader_params = loader_config.get(loader_name, {})
                factory_logger.debug(f"Selected {loader_name} Loader for: {file_path}")
            elif ext.endswith('.docx'):
                 loader_name = loader_config.get('default_docx','unstruct-docx')
                 loader_params = loader_config.get(loader_name,{})
            else:
                error_msg = f'Unsupported file format: {file_path}'
                factory_logger.error(error_msg)
                raise LoaderNotFound(error_msg)
            
            loader_class = LOADER_MAPPING.get(loader_name)

            if not loader_class:
                 raise LoaderNotFound(f'No Loader for type" {loader_name}')
            
            factory_logger.debug(f'Selected {loader_name} loader for: {file_path}')
            return loader_class(**loader_params)
            
        except Exception as e:
             factory_logger.exception(f'Loader Selection Failed for {file_path}: {e}')
             raise
            
