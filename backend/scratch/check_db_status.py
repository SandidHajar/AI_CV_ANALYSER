import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("DATABASE_URL not found")
    exit(1)

# Fix for pg8000 if needed (but standard sqlalchemy works if driver is installed)
# The project uses pg8000 in database.py
import ssl
connect_args = {}

if "postgresql" in db_url or "postgres" in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+pg8000://", 1)
    db_url = db_url.replace("postgres://", "postgresql+pg8000://", 1)
    
    if "?" in db_url:
        base_url, query = db_url.split("?", 1)
        if "sslmode" in query:
            db_url = base_url
            
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connect_args["ssl_context"] = ssl_context

engine = create_engine(db_url, connect_args=connect_args)

with engine.connect() as conn:
    result = conn.execute(text("SELECT id, job_id, status, created_at, result FROM analyses ORDER BY created_at DESC LIMIT 5"))
    for row in result:
        has_result = "YES" if row[4] else "NO"
        print(f"ID: {row[0]}, JobID: {row[1]}, Status: {row[2]}, Created: {row[3]}, HasResult: {has_result}")

