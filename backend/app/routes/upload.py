from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.pdf_service import pdf_service
from app.models.schemas import TextExtractionResponse
from app.auth.auth_bearer import get_current_user
from app.models.database import User
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload-cv", response_model=TextExtractionResponse)
async def upload_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        content = await file.read()
        text = pdf_service.extract_text(content)
        if not text:
            logger.warning(f"Failed extraction for user {current_user.email}")
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        return {"text": text}
    except Exception as e:
        logger.error(f"Error for user {current_user.email}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
