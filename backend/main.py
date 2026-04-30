import sys
import os
import traceback

# Fix Python path for Vercel: the working directory is /var/task/
# but our app module is in /var/task/backend/app/
# So we need to add /var/task/backend/ to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Create the app immediately so Vercel always finds it
app = FastAPI(title="AI CV Analyzer SaaS")

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
    app = real_app
except Exception as e:
    _load_error = {
        "error": str(e),
        "traceback": traceback.format_exc(),
        "python_version": sys.version,
        "sys_path": sys.path,
        "cwd": os.getcwd(),
        "backend_dir": backend_dir,
        "env_vars": {
            "DATABASE_URL": "SET" if os.environ.get("DATABASE_URL") else "MISSING",
            "JWT_SECRET": "SET" if os.environ.get("JWT_SECRET") else "MISSING",
            "OPENAI_API_KEY": "SET" if os.environ.get("OPENAI_API_KEY") else "MISSING",
        }
    }
    print(f"Failed to load app: {_load_error}")

    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    async def catch_all(path_name: str = ""):
        return JSONResponse(status_code=500, content=_load_error)
