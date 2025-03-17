from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:Password%40123@localhost:5433/study_mentor"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Define User Progress model
class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    topic = Column(String)
    progress = Column(JSON)  # Stores lessons completed, quiz scores, etc.


# Create tables
Base.metadata.create_all(bind=engine)


# Function to update progress
def update_progress(user_id, topic, progress):
    session = SessionLocal()
    user = session.query(UserProgress).filter_by(user_id=user_id, topic=topic).first()
    if user:
        user.progress = progress
    else:
        user = UserProgress(user_id=user_id, topic=topic, progress=progress)
        session.add(user)
    session.commit()
    session.close()
