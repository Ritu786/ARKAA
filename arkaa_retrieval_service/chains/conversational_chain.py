from langchain.chains import ConversationalRetrievalChain
from prompts.conversational_prompt import get_conversational_prompt
from chains.base_chain import BaseChain
from app_utils.logger import set_logger

cchain_logger = set_logger(__name__)

class ConversationalRChain(BaseChain):
    '''
    A wraper for building a LangChainConversationalRetirevalChain
    with custom prompt, retirever, and memory components

    Args:
        llm: A Language model instance.
        retriever: A retirever object fetching relevant documents.
        memory: A memory object for maintaining the conversational context.
    
    Methods:
        get_chain(): Retunrs the fully constructred conversational chain.
    
    '''
    def __init__(self, llm, retriever, memory):
        try:
            cchain_logger.info('Initializing the conversational chain')

            # Construct the ConversationalRetirevalChain with a custom prompt and memory.
            self.conversational_chain = ConversationalRetrievalChain.from_llm(
                llm = llm,
                retriever = retriever,
                memory = memory,
                return_source_documents = True,
                combine_docs_chain_kwargs = {'prompt': get_conversational_prompt()}
            )
        except Exception as e:
            cchain_logger.exception(f'Failed to Initialize the ConversationRetrievalChain {e}')
    def get_chain(self):
        '''
        Returns: The instantiated ConversationalRetrievalChain Object.
        '''
        try:
            cchain_logger.info('Returning ConversationalChain.')
            return self.conversational_chain
        except Exception as e:
            cchain_logger.exception(f'Error returning the chain object: {e}')
            raise RuntimeError('Failed to return conversational chain.')
    

