from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from app.models.schemas import CVAnalyzeRequest, CVAnalyzeResponse
from app.models.database import get_db, User, Analysis
from app.auth.auth_bearer import get_current_user
from app.services.analyzer import analyze_cv_service
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def run_analysis_task(job_id: str, cv_text: str, db_session_factory):
    """Background task to run the analysis and update the DB."""
    db = db_session_factory()
    try:
        analysis = db.query(Analysis).filter(Analysis.job_id == job_id).first()
        if not analysis:
            return
            
        analysis.status = "processing"
        db.commit()
        
        # Create a mock request object for the service
        request = CVAnalyzeRequest(cv_text=cv_text)
        result = await analyze_cv_service(request)
        
        analysis.result = result.dict()
        analysis.score = result.score
        analysis.status = "completed"
        db.commit()
    except Exception as e:
        logger.error(f"Background task failed for job {job_id}: {e}")
        analysis.status = "failed"
        db.commit()
    finally:
        db.close()

@router.post("/analyze-cv", status_code=status.HTTP_202_ACCEPTED)
async def start_analysis(
    request: CVAnalyzeRequest, 
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Check Usage Limits (Max 5 per day)
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    analysis_count = db.query(Analysis).filter(
        Analysis.user_id == current_user.id,
        Analysis.created_at >= today
    ).count()
    
    if analysis_count >= 5:
        raise HTTPException(
            status_code=429, 
            detail="Daily limit reached (5 analyses per day). Please upgrade your plan."
        )

    # 2. Create Job Entry
    job_id = str(uuid.uuid4())
    new_analysis = Analysis(
        job_id=job_id,
        user_id=current_user.id,
        status="pending",
        cv_text=request.cv_text[:1000] # store preview
    )
    db.add(new_analysis)
    db.commit()
    
    # 3. Queue Background Task
    from app.models.database import SessionLocal
    background_tasks.add_task(run_analysis_task, job_id, request.cv_text, SessionLocal)
    
    return {"job_id": job_id, "status": "pending", "message": "Analysis started in background"}

@router.get("/analysis-status/{job_id}")
async def get_analysis_status(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analysis = db.query(Analysis).filter(
        Analysis.job_id == job_id,
        Analysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return {
        "job_id": analysis.job_id,
        "status": analysis.status,
        "result": analysis.result,
        "created_at": analysis.created_at
    }

@router.get("/my-analyses")
async def get_my_analyses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc()).all()
    return analyses