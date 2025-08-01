import os
from app_utils.logger import set_logger
from loaders.loader_factory import get_loader
from processors.preprocessor_pipeline import PreProcessPipeline
from embeddings.embedder_factory import get_embeddings
from vectorstores.vectorstore_factory import get_vectorstore
from app_utils.yaml_loader import load_config


config = load_config()

# Defining Loader config
loader_config = config.get("loader", {})

# Defining Vectorstore config
vs_config = config.get('vectorstore')

# Defining embedding model Config
emb_config = config.get('embeddings',{})

main_logger = set_logger(__name__)

def ingest_files(file_path: str, collection_name: str, base_path: str = ''):
    '''
    Ingesting Pipeline for creating embeddings of Doc...

    Args:
        file_path: File Path.
        collection_name: container within the vectostore to store the emebddings.
        base_path: if file_paths contain relative paths and are located outside the server then base_path should also be included.
    '''

    main_logger.info(f'Starting ingestion for collection: {collection_name}')

    # Initializing the Processor Pipeline
    processor_pipeline = PreProcessPipeline()

    # Initializing the Embedding Model
    try:
        embed_model = get_embeddings(emb_config=emb_config)
    except Exception as e:
        main_logger.error(f'Failed to initialize the embedder: {e}', exc_info=True)
        return {
            "status": "Failed",
            "reason": "Embedder initialization failed."
        }
    
    # Initializng the vectorstore
    try:
        vectorstore = get_vectorstore(vs_config=vs_config, collection_name=collection_name, embed_model=embed_model)
    except Exception as e:
        main_logger.error(f'Failed to initialize the vectorstore: {e}', exc_info=True)
        return {
            "status": "Failed",
            "reason": "Vectorstore initialization failed."
        }  
   
    file_path = os.path.abspath(os.path.join(base_path, file_path)) if base_path else os.path.abspath(file_path)

    # If file doesn't exist
    if not os.path.isfile(file_path):
        main_logger.warning(f'Skipping: {file_path} does not exist or is not a file')
        return {
            "status": "failed",
            "file": file_path,
            "reason": "File Does not Exist."
        }
          
    try:
        # Loader
        main_logger.info(f'Processing file: {file_path}')

        loader = get_loader(loader_config=loader_config,file_path=file_path)
        documents = loader.load(file_path)
        # Pre-Processing where we are using language detection & translation
        processed_documents = processor_pipeline.process_documents(documents)
        
        # Storing it in the vectorstore...
        vectorstore.store_documents(
            documents=processed_documents
        )

        return {
            "status": "Success"
        }
    
    except Exception as e:
        main_logger.error(f'[Error] Failed to process {file_path}: {e}', exc_info=True)
        return {
            "status": "Failed",
            "file": file_path,
            "reason": str(e)
        }