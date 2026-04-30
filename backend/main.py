import sys
import os

# Step-by-step import diagnostic for Vercel
# This will tell us EXACTLY which import is crashing
_import_results = []

def _test_import(name, import_func):
    try:
        import_func()
        _import_results.append({"step": name, "status": "ok"})
        return True
    except Exception as e:
        import traceback
        _import_results.append({
            "step": name, 
            "status": "FAILED",
            "error": str(e),
            "traceback": traceback.format_exc()
        })
        return False

# Test each critical dependency one by one
_test_import("fastapi", lambda: __import__("fastapi"))
_test_import("sqlalchemy", lambda: __import__("sqlalchemy"))
_test_import("pydantic", lambda: __import__("pydantic"))
_test_import("pydantic_settings", lambda: __import__("pydantic_settings"))
_test_import("bcrypt", lambda: __import__("bcrypt"))
_test_import("passlib", lambda: __import__("passlib"))
_test_import("jose", lambda: __import__("jose"))
_test_import("pg8000", lambda: __import__("pg8000"))
_test_import("pypdf", lambda: __import__("pypdf"))
_test_import("openai", lambda: __import__("openai"))
_test_import("dotenv", lambda: __import__("dotenv"))

# Test our app modules step by step
_test_import("app.config.settings", lambda: __import__("app.config.settings"))
_test_import("app.models.schemas", lambda: __import__("app.models.schemas"))
_test_import("app.models.database", lambda: __import__("app.models.database"))
_test_import("app.services.auth_service", lambda: __import__("app.services.auth_service"))
_test_import("app.auth.auth_bearer", lambda: __import__("app.auth.auth_bearer"))
_test_import("app.routes.auth", lambda: __import__("app.routes.auth"))
_test_import("app.routes.analyze", lambda: __import__("app.routes.analyze"))
_test_import("app.routes.upload", lambda: __import__("app.routes.upload"))
_test_import("app.main", lambda: __import__("app.main"))

# Now try to load the real app
_real_app_loaded = False
try:
    from app.main import app
    _real_app_loaded = True
except Exception:
    pass

if not _real_app_loaded:
    # Create a diagnostic app that shows exactly what failed
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    async def diagnostic(path_name: str = ""):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend failed to initialize",
                "python_version": sys.version,
                "env_vars": {
                    "DATABASE_URL": "SET" if os.environ.get("DATABASE_URL") else "MISSING",
                    "JWT_SECRET": "SET" if os.environ.get("JWT_SECRET") else "MISSING",
                    "OPENAI_API_KEY": "SET" if os.environ.get("OPENAI_API_KEY") else "MISSING",
                    "VERCEL": os.environ.get("VERCEL", "NOT SET"),
                },
                "import_results": _import_results,
            }
        )
