from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os
from dotenv import load_dotenv

from .routers import qa
from .models.schemas import HealthResponse

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Kenyan Leaders Q&A System",
    description="""
    Interactive Q&A System for Kenyan Political Leadership
    
    This API provides comprehensive information about Kenyan political leaders including:
    - County Governors and their profiles
    - Senators from all 47 counties
    - Members of County Assemblies (MCAs)
    - Members of Parliament (MPs)
    - Cabinet Secretaries and government officials
    - County Commissioners and administrative roles
    
    Powered by Google's Gemini 2.0 Flash AI for accurate, up-to-date responses.
    """,
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url=None  # Disable ReDoc
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js frontend (development)
        "https://assignment-frontend-virid.vercel.app",  # Vercel frontend (production)
        "https://*.vercel.app",  # All Vercel apps
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qa.router)

@app.get("/")
async def root():
    return {
        "message": "Kenyan Leaders Q&A System API", 
        "status": "running",
        "docs": "/docs",
        "example_endpoint": "/api/examples"
    }

@app.get(
    "/health", 
    response_model=HealthResponse,
    summary="API Health Check",
    description="Check the health status and configuration of the API service",
    responses={
        200: {"description": "API is healthy", "model": HealthResponse}
    },
    tags=["System"]
)
async def health_check():
    return HealthResponse(
        status="healthy", 
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        timestamp=datetime.now(),
        version="1.0.0"
    )