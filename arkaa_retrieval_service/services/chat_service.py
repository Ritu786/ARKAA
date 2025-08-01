async def handle_chat(qa_chain, question: str):
    '''
    Executes the conversational chain. 
    De-Deuplicate the source files.

    Args:
        session_id (str): Unique ID Per User. Helps to manage session store chat history.
        question (str): User Query.
    
    Returns:
        dict : answer & source_documents 
    '''

    # Assigning the response & answer
    response = qa_chain.invoke(
        {
            'question': question,
            'chat_history': []
        }
    )
    answer =  response['answer']

    # Extract file paths from metadata of source documents 
    # Set to remove the duplication of files
    source_paths = {}

    # Iterating through source_documents, parsing 'source' from each chunk
    if 'source_documents' in response:
        source_paths = {source_doc.metadata['source'] for source_doc in response['source_documents']}
    
    return {
        'answer': answer,
        'source_documents': list(source_paths)
    }

