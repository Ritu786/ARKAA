from app_utils.config_loader import load_config_section
from memory.postgres_memory import PostgresMemory
from app_utils.logger import set_logger


mf_logger = set_logger(__name__)

def get_memory(session_id):
    '''
    Initializes and returns memory object based on configured memory type.

    Args:
        session_id (str): Unique Identifier for the user's session. 
    
    Returns:
        A memory object (e.g., PostgresMemory instance.)
    
    Raises:
        ValueError: if the memory type is unsupported or misconfigured.
        RuntimeError: If memroy initialzation fails. 
    '''
    try:
        mf_logger.info('Loading memory configuration.')
        memory_config = load_config_section('memory')
        memory_type = memory_config['type']

        mf_logger.debug(f'Configured memory type: {memory_type}')

        if memory_type == 'postgres-memory':
            mf_logger.info('Initializing PostgresMemory...')
            return PostgresMemory().get_memory(session_id=session_id)
        else:
            mf_logger.error(f'Unsupported Memory Type: {memory_type}')
            raise ValueError(f'Unsupported Memory Type: {memory_type}')
        
    except ValueError as ve:
        mf_logger.exception('Inavlid Memory configuration')
        raise ve
    except Exception as e:
        mf_logger.exception('Unexpected error during memory initialization')
        raise RuntimeError('Failed to initialize Memory') from e
        
        

    

