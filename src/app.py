from fastapi import FastAPI, Depends
from pydantic import BaseModel
from db import SessionLocal, Base, engine
from agent import invoke_crew

app = FastAPI()

# Ensure Database Tables are Created
@app.on_event("startup")
def init_db():
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Model
class StudyRequest(BaseModel):
    user_id: str
    topic: str

# Study API
@app.post("/study")
def study_route(request: StudyRequest):
    result = invoke_crew(request.user_id, request.topic)
    return result