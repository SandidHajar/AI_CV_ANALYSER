from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.config.settings import get_settings

import os
import ssl

# Use a function to get engine and session to avoid crashing on import if env vars are missing
def get_engine():
    settings = get_settings()
    url = settings.database_url
    
    connect_args = {}
    
    if "sqlite" in url:
        connect_args = {"check_same_thread": False}
    elif "postgresql" in url or "postgres" in url:
        # Use pg8000 (pure Python) instead of psycopg2 (needs C compilation)
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+pg8000://", 1)
        elif url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+pg8000://", 1)
        
        # pg8000 doesn't understand ?sslmode=require — strip it and use ssl_context instead
        if "?" in url:
            # More robust removal: just strip everything after the ? if it contains sslmode
            # or keep other params if you prefer, but Neon usually only needs sslmode
            base_url, query = url.split("?", 1)
            if "sslmode" in query:
                url = base_url
            else:
                url = f"{base_url}?{query}"
        
        # Enable SSL for pg8000 (required by Neon and most cloud PostgreSQL providers)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connect_args["ssl_context"] = ssl_context
    
    return create_engine(url, connect_args=connect_args)

# These will be initialized lazily
_engine = None
_SessionLocal = None

def get_session_local():
    global _engine, _SessionLocal
    if _engine is None:
        _engine = get_engine()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _SessionLocal

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    analyses = relationship("Analysis", back_populates="owner")

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending") # pending, processing, completed, failed
    
    # Analysis results
    filename = Column(String)
    cv_text = Column(Text)
    result = Column(JSON, nullable=True) # Full analysis JSON
    score = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="analyses")

def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
