from pydantic import BaseModel
from typing import List, Optional, Tuple

class  FilePathItem(BaseModel):
    id: int
    path: str

class IngestRequest(BaseModel):
    file_paths: List[FilePathItem]
    collection_name: str
    base_path: Optional[str] = None