from crewai.llm import LLM
from crewai import Agent, Crew, Task
from db import update_progress, get_user_progress

# Update with your locally hosted LLM API
# LLM_API_URL = "http://localhost:8000/v1/completions"
LLM_API_URL="http://localhost:11434"

# Agent 1: Study Planner
study_planner = Agent(
    role="Study Planner",
    goal="Create a structured study plan for the given topic: {topic}",
    backstory="You are an expert in creating effective study plans.",
    verbose=True,
    allow_delegation=False,
    llm=LLM(model="ollama/llama3.2", base_url=LLM_API_URL)
)

# Agent 2: Lesson Generator
lesson_generator = Agent(
    role="Lesson Generator",
    goal="Generate lessons and quizzes based on the study plan for topic: {topic}",
    backstory="You are an expert in creating engaging educational content.",
    verbose=True,
    allow_delegation=False,
    llm=LLM(model="ollama/llama3.2", base_url=LLM_API_URL)
)

# Agent 3: Progress Tracker
progress_tracker = Agent(
    role="Progress Tracker",
    goal="Track and store the user's study progress in the database",
    backstory="You are an expert in managing and updating databases.",
    verbose=True,
    allow_delegation=False,
    llm=LLM(model="ollama/llama3.2", base_url=LLM_API_URL)
)

# Task 1: Create Study Plan
create_study_plan_task = Task(
    description="Create a comprehensive study plan for the user's chosen topic: {topic}",
    agent=study_planner,
expected_output = (
        "A comprehensive study plan in the following format:"
        "- Topic"
        "- Detailed Plan"
    )
)

# Task 2: Generate Lesson and Quiz
generate_lesson_task = Task(
    description="Generate an engaging lesson and quiz based on the current step of the study plan for topic: {topic}",
    agent=lesson_generator,
expected_output = (
        "A comprehensive lesson and quiz based on the current step of the study plan in the following format:"
        "- Topic"
        "- Detailed lesson"
        "- Detailed quiz"
    )
)

# Task 3: Track Progress
track_progress_task = Task(
    description="Track the user's progress and update the database accordingly.",
    agent=progress_tracker,
expected_output =""
)

# Create the Crew
crew = Crew(
    agents=[study_planner, lesson_generator, progress_tracker],
    tasks=[create_study_plan_task, generate_lesson_task, track_progress_task],
    verbose=True,
)

# Function to invoke the crew
def invoke_crew(user_id: str, user_topic: str):
    # Check if there's existing progress
    user_progress = get_user_progress(user_id, user_topic)
    if user_progress:
        # If there's progress, resume from the last step
        print(f"Resuming progress for user {user_id} on topic {user_topic}...")
        # You can add logic here to determine the next task based on the progress
        # For simplicity, we'll just generate a new lesson for now
        result = crew.kickoff(inputs={"topic": user_topic})
    else:
        # If no progress, start from the beginning
        print(f"Starting new study plan for user {user_id} on topic {user_topic}...")
        result = crew.kickoff(inputs={"topic": user_topic})

    # Update progress in the database
    update_progress(user_id, user_topic, result.raw)
    return result