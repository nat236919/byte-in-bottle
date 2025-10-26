import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.v1.api_main_router import api_v1_router
from api.services.config_service import config_service


# Load environment variables
load_dotenv()

# FastAPI application instance
app = FastAPI(
    title=config_service.get_api_title(),
    description=config_service.get_project_description(),
    version=config_service.get_project_version(),
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('ALLOWED_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Register Routers
app.include_router(router=api_v1_router)
