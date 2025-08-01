from fastapi import APIRouter, HTTPException
from api.v1.schemas.ingest_schema import IngestRequest
from api.v1.tasks.indexing_task import run_indexing

router = APIRouter()

@router.post('/start-indexing')
def start_indexing(payload: IngestRequest):
    '''
        Trigger background indexing via celery.
        Accepts file paths, collection name, and optional base path.
    '''
    try:
        job_ids = []
        # extacting paths from input request. 
        extracted_paths = [item.path for item in payload.file_paths]

        for file_path in extracted_paths:
            # running indexing task
            task = run_indexing.delay(
                file_path = file_path,
                collection_name = payload.collection_name,
                base_path = payload.base_path  or ''
            )

            job_ids.append(
                {
                    "job_id": task.id,
                    "status": "queued",
                    "file_path": file_path
                }
            )
        return {"job_id": job_ids,"message":f"{len(job_ids)} indexing jobs queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
