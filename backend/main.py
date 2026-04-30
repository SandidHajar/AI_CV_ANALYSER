import sys
import os
import traceback

# IMPORTANT: Vercel requires a top-level `app` variable.
# We MUST define it unconditionally at module level.

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Create the app immediately so Vercel always finds it
app = FastAPI(title="AI CV Analyzer SaaS")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Now try to load the real application
_load_error = None
try:
    from app.main import app as real_app
    # If import succeeds, replace app with the real one
    app = real_app
except Exception as e:
    _load_error = {
        "error": str(e),
        "traceback": traceback.format_exc(),
        "python_version": sys.version,
        "env_vars": {
            "DATABASE_URL": "SET" if os.environ.get("DATABASE_URL") else "MISSING",
            "JWT_SECRET": "SET" if os.environ.get("JWT_SECRET") else "MISSING", 
            "OPENAI_API_KEY": "SET" if os.environ.get("OPENAI_API_KEY") else "MISSING",
        }
    }
    print(f"Failed to load app: {_load_error}")

    # Add a catch-all route to the fallback app to show the error
    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    async def catch_all(path_name: str = ""):
        return JSONResponse(
            status_code=500,
            content=_load_error
        )
