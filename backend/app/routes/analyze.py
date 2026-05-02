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

def run_analysis_task(job_id: str, cv_text: str, db_session_factory_func):
    """Background task to run the analysis and update the DB."""
    print(f"DEBUG: run_analysis_task (SYNC) ENTERED for JobID {job_id}")
    
    # db_session_factory_func is get_session_local
    session_maker = db_session_factory_func() 
    db = session_maker() 
    
    try:
        analysis = db.query(Analysis).filter(Analysis.job_id == job_id).first()
        if not analysis:
            print(f"DEBUG: Job {job_id} not found in DB!")
            return
            
        analysis.status = "processing"
        db.commit()
        print(f"DEBUG: Status updated to processing. Starting AI logic...")
        
        # Create a mock request object for the service
        request = CVAnalyzeRequest(cv_text=cv_text)
        
        # Run the async service in a new event loop for this thread
        import asyncio
        try:
            # Check if there's already an event loop (shouldn't be in a new thread, but just in case)
            result = asyncio.run(analyze_cv_service(request))
        except Exception as ai_err:
            print(f"DEBUG: AI Service Execution Error: {ai_err}")
            raise ai_err
            
        print(f"DEBUG: AI logic finished. Saving results...")
        analysis.result = result.dict()
        analysis.score = result.score
        analysis.status = "completed"
        db.commit()
        print(f"DEBUG: Job {job_id} COMPLETED SUCCESSFULLY.")
    except Exception as e:
        print(f"DEBUG ERROR in run_analysis_task: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        try:
            analysis.status = "failed"
            db.commit()
        except:
            pass
    finally:
        db.close()
        print(f"DEBUG: Session closed for Job {job_id}")

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
    import threading
    print(f"API: Starting Thread for JobID {job_id}...")
    from app.models.database import get_session_local
    
    # Use a standard Python thread to ensure it starts immediately
    task_thread = threading.Thread(
        target=run_analysis_task, 
        args=(job_id, request.cv_text, get_session_local)
    )
    task_thread.daemon = True # Ensure thread doesn't block app shutdown
    task_thread.start()
    
    print(f"API: Thread started. Returning 202.")
    
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
        print(f"API STATUS: Job {job_id} NOT FOUND.")
        raise HTTPException(status_code=404, detail="Job not found")
        
    print(f"API STATUS: Job {job_id} status is {analysis.status}")
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