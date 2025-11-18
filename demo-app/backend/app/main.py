"""
Developer Productivity Dashboard - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import routers
try:
    from app.api.v1 import metrics
    # from app.api.v1 import auth  # Commented out until dependencies are set up
except ImportError:
    from api.v1 import metrics
    # from api.v1 import auth  # Commented out until dependencies are set up

# Create FastAPI app
app = FastAPI(
    title="Developer Productivity Dashboard API",
    description="Real-time developer productivity metrics and insights",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])  # Commented out
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "healthy",
        "service": "Developer Productivity Dashboard API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("🚀 Developer Productivity Dashboard API starting...")
    print(f"📝 API Documentation: http://localhost:8000/docs")
    print(f"📚 ReDoc Documentation: http://localhost:8000/redoc")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("👋 Developer Productivity Dashboard API shutting down...")

