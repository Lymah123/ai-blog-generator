from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api import routes

# Create database tables
@asynccontextmanager
async def lifespan(app: APIRouter):
   
   # Startup
   Base.metadata.create_all(bind=engine)
   yield

   # Shutdown
   # await engine.dispose()

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.APP_ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.APP_ENVIRONMENT == "development" else None
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, prefix="/api/v1", tags=["Blogs"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Blog Generator API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
        }

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy", "environment": settings.APP_ENVIRONMENT}
