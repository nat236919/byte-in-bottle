import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.v1.api_main_router import api_v1_router


load_dotenv()


app = FastAPI(
    title='Byte in Bottle API',
    description='Powered by bytes. Driven by attitude.',
    version='0.1.0',
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
