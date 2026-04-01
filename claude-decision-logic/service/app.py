"""
FastAPI application factory and main entry point.

Wires together the decision engine service with FastAPI routing,
middleware, and error handling.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import sys
import os

# Ensure service module can import engine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .routes import router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Sets up:
    - Routes from decision service
    - CORS middleware
    - Error handlers
    - Metadata
    """
    app = FastAPI(
        title="Decision Execution Engine",
        description="Decision evaluation and execution platform",
        version="0.1.0",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routes
    app.include_router(router)

    # Custom error handler for validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Validation error",
                "errors": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Internal server error: {str(exc)}",
            },
        )

    return app


# Create application instance for ASGI servers
app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
