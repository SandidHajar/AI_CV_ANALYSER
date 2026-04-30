import sys
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

try:
    from app.main import app
except Exception as e:
    # If the app fails to import (e.g. database driver issues on Vercel), 
    # we catch it and create a dummy app to display the error.
    error_traceback = traceback.format_exc()
    print("Failed to load app:", error_traceback)
    
    app = FastAPI()
    
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    async def catch_all(path_name: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Failed to initialize backend application",
                "detail": str(e),
                "traceback": error_traceback
            }
        )
