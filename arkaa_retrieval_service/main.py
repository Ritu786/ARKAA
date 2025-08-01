from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.chat_routes import router as chat_router

# Defining the FastAPI App.
app = FastAPI(
    title='Q&A Chat using RAG',
    description='API that answer to the user queries using RAG technique',
    version='1.0.0'
)

# CORS Set-up: * for dev, for prod allow only trusted origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    # allow_credentials = True, # Cannot be true, as allow_orgins = '*'
    allow_methods = ['*'],
    allow_headers = ['*'],
)

# Register Routes
app.include_router(chat_router,prefix='/chat',tags=['Chat'])