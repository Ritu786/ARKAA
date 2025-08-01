from app_utils.config_loader import load_config_section
from llms.llm_factory import get_llm
from retrieval.retriever_factory import get_retriever
from vectorstores.vectorstore_factory import get_vectostore
from memory.memory_factory import get_memory
from chains.conversational_chain import ConversationalRChain
from app_utils.logger import set_logger

cf_logger = set_logger(__name__)


def get_chain(session_id):
    '''
    Intitializes and returns a chain instance based on configuration.

    Args:
        session_id (str): Unique Identifier for the user session.
    
    Returns:
        A ready-to-use chain instance based on the specified configuration.

    Raises:
        ValueError: if the specified chain type in the config is not supported.
    
    '''
    try:
        cf_logger.info(f'Initializing chain for session: {session_id}')

        # Load chain type from config
        chain_config = load_config_section('chains')
        chain_type = chain_config['type']
        cf_logger.debug(f'Chain type fron cofig: {chain_type}.')

        # Initalize the llm
        llm = get_llm()
        cf_logger.debug('LLM initialized sucessfully.')

        if chain_type == 'conversational':
            # Set Up Vectorsotre and retriever.
            db = get_vectostore()
            retriever = get_retriever(db)
            cf_logger.debug('Retriever Initialized with vector store.')

            # Set Up memeory context for the session.
            memory = get_memory(session_id=session_id)
            cf_logger.debug('Session memory initialized.')

            cf_logger.info('Returning conversational retireval chain')
            return ConversationalRChain(llm,retriever,memory).get_chain()
        else:
            cf_logger.error(f'Unsupported chain type: {chain_type}')
            raise ValueError(f'Unsupported chain type: {chain_type}')
        
    except ValueError as ve:
        cf_logger.exception(f'Unexpected error {ve} during chain setup.')
