from fastapi import FastAPI, Depends
from pydantic import BaseModel
import requests, json
from db import update_progress, UserProgress, SessionLocal, Base, engine

# Update with your locally hosted LLM API
LLM_API_URL = "http://localhost:8000/v1/completions"
app = FastAPI()

# Ensure database and tables are created at startup
@app.on_event("startup")
def init_db():
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)  # Auto-create tables

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class StudyRequest(BaseModel):
    user_id: str
    topic: str


# Study API with persistence
@app.post("/study")
def study_route(request: StudyRequest):
    session = SessionLocal()
    user_progress = session.query(UserProgress).filter_by(user_id=request.user_id, topic=request.topic).first()
    print("user_progress:", user_progress)

    if not user_progress:
        user_progress = UserProgress(user_id=request.user_id, topic=request.topic, progress={})
        session.add(user_progress)
        session.commit()

    prompt = f"Create a study plan for {request.topic}"
    # Generate response using LLM
    payload = {
        "model": "deepseek-r1:8b",  # other model is llama3.2:latest
        "prompt": prompt,
        "temperature": 0
    }
    response = requests.post(LLM_API_URL, json=payload)
    # Print response details for debugging
    print("RAW RESPONSE STATUS CODE:", response.status_code)
    print("RAW RESPONSE TEXT:", response.text)

    try:
        response_json = response.json()
        generated_text = response_json.get("choices", [{}])[0].get("text", "No response generated.")
    except requests.exceptions.JSONDecodeError:
        generated_text = "Error: LLM API did not return valid JSON."

    print("generated_text:", generated_text)
    # Update progress
    update_progress(request.user_id, request.topic, {"study_plan": generated_text})

    return {"study_plan": generated_text}
