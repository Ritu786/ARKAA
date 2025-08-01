from app_utils.config_loader import load_config_section
from app_utils.logger import set_logger
from memory.base_memory import BaseMemory
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

pgm_logger = set_logger(__name__)

class PostgresMemory(BaseMemory):
    '''
        Initializes and returns a conversation memory backed by PostgreSQL,
        maintaining a fixed-size chat history buffer.
    '''
    def __init__(self):
        '''
        Loads memory-related configuration from the config file.

        '''
        try:
            self.memory_config = load_config_section('memory')
        except Exception as e:
            pgm_logger.exception('Failed to load memory configuration')
            raise RuntimeError('Could not load memory configuration') from e
            
    def get_memory(self,session_id):
        '''
            Returns a Postgres-backed ConversationBufferWindowMemory instance.

            Args:
                session_id (str): Unique identifier for the user session.

            Returns:
                ConversationBufferWindowMemory: Configured memory object.

            Raises:
                ValueError: If configuration values are missing or invalid.
        '''
        try:
            connection_string = self.memory_config['connection_string']
            window_size = self.memory_config['window_size']
            
            if not connection_string:
                raise ValueError('Postgres connection is missing in memory config.')
            
            pgm_logger.debug(f"Initializing PostgresChatMessageHistory for session_id: {session_id}")
            chat_history = PostgresChatMessageHistory(
                connection_string=connection_string,
                session_id=session_id
            )

            postgres_memory = ConversationBufferWindowMemory(
                memory_key='chat_history',
                k = window_size,
                chat_memory=chat_history,
                return_messages=True,
                output_key='answer'
            )
            pgm_logger.info("Postgres memory successfully initialized")
            return postgres_memory
        except ValueError as ve:
            pgm_logger.exception('Configuration validation error')
            raise ve
        except Exception as e:
            pgm_logger.exception('Error initializing Postgres Memory')
            raise RuntimeError('Failed to initialize Postres memory') from e