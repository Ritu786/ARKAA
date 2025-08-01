from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.ingest_route import router as ingest_router

app = FastAPI(
    title='Embed-Everything',
    description='API that Embedds the dcocuments',
    version= '1.0.0'
)

# CROS Set-Up: * for dev, fro prod allow only trusted origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    # allow_credentials = True, # Cannot be true, as allow_origins = '*'
    allow_methods = ['*'],
    allow_headers = ['*'],
)

app.include_router(ingest_router, prefix='/ingest',tags=['Ingestion'])

