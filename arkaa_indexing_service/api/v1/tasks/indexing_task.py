from api.v1.celery_worker import celery_app
from api.v1.services.ingest_service import ingest_files
from app_utils.logger import set_logger

task_logger = set_logger(__name__)

# Running the task run index, enabling retires thrice after 60 secs.
"""
name = folder.module.function,
time_limit = hard time limit for each task. (Each task max 30 mins)
soft_time_limit = warning before hard time limit 
rate_limit = Number of Tasks per limir (10 tasks per min)
bind = True: for retries
"""
@celery_app.task(
        name="tasks.indexing_task.run_indexing",
        time_limit=1800,
        soft_time_limit=1500, 
        rate_limit="10/m",
        bind=True, 
        max_retries=3, 
        default_retry_delay=60
    )
def run_indexing(self, file_path: str, collection_name: str, base_path: str = ''):
    """
    Celery task that triggers the ingestion pipeline for documents.

    Args:
        file_path: File Path.
        collection_name: Target collection in Vector Database.
        base_path: Used if file paths are relative.

    Returns:
        dict: Ingestion summary (sucess count, failed files)
    """
    try:
        task_logger.info(f'[Task] Starting Indexing: {file_path} file into collection {collection_name}')
        result = ingest_files(file_path, collection_name, base_path)
        task_logger.info(f'Indexing complete: {result}')
        return result
    except Exception as exc:
        task_logger.error(f'[Fatal Error] Indexing task failed:{exc}', exc_info=True)
        raise self.retry(exc=exc)