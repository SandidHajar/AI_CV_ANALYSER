import logging
import io
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import traceback
from pypdf import PdfReader

from app.routes.analyze import router as analyze_router
from app.routes.upload import router as upload_router
from app.routes.auth import router as auth_router
from app.auth.auth_bearer import get_current_user
from app.config.settings import get_settings
from app.models.schemas import TextExtractionResponse
from app.models.database import init_db, User

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Detect if running on Vercel (Vercel sets the VERCEL env var automatically)
IS_VERCEL = os.environ.get("VERCEL") is not None

app = FastAPI(
    title="AI CV Analyzer SaaS",
    description="Production-ready AI CV Analyzer SaaS",
    version="2.0.0",
    root_path="/_/backend" if IS_VERCEL else ""
)

# Initialize Database
@app.on_event("startup")
def on_startup():
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes (root_path will handle the /_/backend prefix automatically)
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(analyze_router, tags=["Analysis"])
app.include_router(upload_router, tags=["Upload"])

@app.get("/debug-routes")
async def debug_routes():
    return [{"path": route.path, "name": route.name} for route in app.routes]

@app.get("/", tags=["Health"])
async def health_check():
    try:
        settings = get_settings()
        app_name = settings.app_name
    except Exception:
        app_name = "AI CV Analyzer"
    return {"status": "ok", "app": app_name, "version": "2.0.0"}

@app.post("/extract-text", response_model=TextExtractionResponse)
async def extract_text(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Extract text from uploaded PDF file (Authenticated)."""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        contents = await file.read()
        pdf_reader = PdfReader(io.BytesIO(contents))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text.strip():
            logger.warning(f"No text extracted from file: {file.filename} by user {current_user.email}")
            raise HTTPException(status_code=400, detail="No text could be extracted from PDF")
        
        return TextExtractionResponse(text=text.strip())
    except Exception as e:
        logger.error(f"Error extracting text from {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")    

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    if isinstance(exc, HTTPException):
        raise exc
    logger.error(f"Global error: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "traceback": traceback.format_exc()}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


