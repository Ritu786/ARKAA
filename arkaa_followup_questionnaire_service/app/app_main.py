from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v01.routes.followup_routes import router as questions_router

# Defning the Fast API
app = FastAPI(
    title='Follow-Up Question Generator',
    description='API that generates follow up questions.',
    version='1.0.0'
)

# CORS Set-up: * for dev, for prod allow only trusted origins
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True, # Cannot be true, as aollow_orgins = '*',
    allow_methods = ['*'],
    allow_headers = ['*'],
)

# Register the Routes
app.include_router(questions_router,prefix='/api/v01')