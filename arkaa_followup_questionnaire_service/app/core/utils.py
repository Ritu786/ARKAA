import tiktoken
from core.logging_config import set_logger

utils_logger = set_logger(__name__)

def truncate_text(text: str, max_tokens: int = 3000, model: str = 'gpt-4o'):
    '''
    Truncates te input text to the specified tken limit based on the model's tokenization.

    Args:
        text (str): The input string to tokenize and truncate.
        max_tokens (int): Maximum token allowed.
        model (str): The OpenAI model name for token encoding. 
    
    Returns:
        str: The truncated text.
    '''
    try:
        # Defining the encoder.
        encoding = tiktoken.encoding_for_model(model)
    
    except KeyError:
        # Defining cl100k_base encoder used by latest OpenAI models
        encoding = tiktoken.get_encoding('cl100k_base')
    
    # Encoding the processed text to tokens
    tokens = encoding.encode(text)

    # trimming the output tokens within max_tokens
    truncated = tokens[:max_tokens]

    utils_logger.debug(f"Original tokens: {len(tokens)}, Truncated to: {len(truncated)}")

    # returning the decoded text
    return encoding.decode(truncated)
