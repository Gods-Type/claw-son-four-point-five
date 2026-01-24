"""
FastAPI backend for claw-son-four-point-five education platform.

This module provides REST API services for the educational platform,
including user management, content delivery, progress tracking, and assessment.
"""

import logging
import os
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import jwt
from passlib.context import CryptContext

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS2"

# Database setup (placeholder)
def get_db():
    """Get database session."""
    # Placeholder for database session
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting education platform backend...")
    
    # Initialize database
    await initialize_database()
    
    # Load initial content
    await load_content_data()
    
    logger.info("Backend startup complete.")
    yield
    
    logger.info("Shutting down education platform backend...")
    await cleanup_resources()
    logger.info("Backend shutdown complete.")


# Create FastAPI application
app = FastAPI(
    title="Claw Son Education Platform API",
    description="Backend API for AI limitations and solutions educational platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Pydantic models
class User(BaseModel):
    """User model."""
    id: Optional[int] = None
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "student"
    is_active: bool = True
    created_at: Optional[datetime] = None


class UserCreate(BaseModel):
    """User creation model."""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model."""
    username: str
    password: str


class LearningPath(BaseModel):
    """Learning path model."""
    id: Optional[int] = None
    title: str
    description: str
    difficulty: str
    duration: str
    icon: str
    color: str
    modules: List[Dict[str, Any]]
    is_active: bool = True


class Tutorial(BaseModel):
    """Tutorial model."""
    id: Optional[int] = None
    title: str
    description: str
    content: str
    learning_objectives: List[str]
    prerequisites: List[str]
    difficulty: str
    estimated_time: int
    learning_path_id: int
    is_active: bool = True


class Exercise(BaseModel):
    """Exercise model."""
    id: Optional[int] = None
    title: str
    description: str
    problem_statement: str
    starter_code: Optional[str] = None
    solution: str
    hints: List[str]
    difficulty: str
    tutorial_id: int
    learning_objectives: List[str]
    is_active: bool = True


class UserProgress(BaseModel):
    """User progress model."""
    user_id: int
    content_id: int
    content_type: str
    progress_percentage: float
    is_completed: bool
    last_accessed: datetime


class Assessment(BaseModel):
    """Assessment model."""
    id: Optional[int] = None
    title: str
    description: str
    questions: List[Dict[str, Any]]
    time_limit: Optional[int] = None
    passing_score: float
    tutorial_id: Optional[int] = None
    is_active: bool = True


class AssessmentSubmission(BaseModel):
    """Assessment submission model."""
    assessment_id: int
    user_id: int
    answers: List[Dict[str, Any]]
    submitted_at: datetime


# Mock data (in real implementation, this would come from database)
mock_users = []
mock_learning_paths = []
mock_tutorials = []
mock_exercises = []


async def initialize_database():
    """Initialize database connection and tables."""
    try:
        # Placeholder for database initialization
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def load_content_data():
    """Load initial content data."""
    try:
        # Load learning paths
        global mock_learning_paths
        mock_learning_paths = [
            {
                "id": 1,
                "title": "Foundational Path",
                "description": "Learn AI fundamentals and basic limitations",
                "difficulty": "Beginner",
                "duration": "4-6 weeks",
                "icon": "BookOpen",
                "color": "bg-green-500",
                "modules": [
                    {"title": "AI Fundamentals", "completed": True},
                    {"title": "Understanding Limitations", "completed": True},
                    {"title": "Ethical Considerations", "completed": False},
                    {"title": "Basic Hands-on Examples", "completed": False},
                ],
                "is_active": True,
            },
            {
                "id": 2,
                "title": "Technical Path",
                "description": "Deep dive into technical limitations and solutions",
                "difficulty": "Intermediate",
                "duration": "8-10 weeks",
                "icon": "Code2",
                "color": "bg-blue-500",
                "modules": [
                    {"title": "Technical Limitations Overview", "completed": True},
                    {"title": "Common Sense & Reasoning", "completed": False},
                    {"title": "Explainability Methods", "completed": False},
                    {"title": "Implementation Projects", "completed": False},
                    {"title": "Case Study Analysis", "completed": False},
                ],
                "is_active": True,
            },
        ]
        
        logger.info("Content data loaded successfully")
    except Exception as e:
        logger.error(f"Content loading failed: {e}")


async def cleanup_resources():
    """Cleanup resources on shutdown."""
    try:
        # Cleanup database connections
        logger.info("Resources cleaned up successfully")
    except Exception as e:
        logger.error(f"Resource cleanup failed: {e}")


# Authentication utilities
def create_access_token(data: dict, expires_delta: Optional[int] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(username: str = Depends(verify_token)):
    """Get current user from token."""
    # In real implementation, fetch from database
    user = next((user for user in mock_users if user.username == username), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# API Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Claw Son Education Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# Authentication endpoints
@app.post("/auth/register")
async def register(user: UserCreate):
    """Register a new user."""
    # Check if user already exists
    if any(u.username == user.username or u.email == user.email for u in mock_users):
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash password
    hashed_password = pwd_context.hash(user.password)
    
    # Create user
    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role="student"
    )
    
    # Store user (in real implementation, save to database)
    mock_users.append(new_user)
    
    # Create access token
    access_token = create_access_token(data={"sub": new_user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role
        }
    }


@app.post("/auth/login")
async def login(user_credentials: UserLogin):
    """Authenticate user and return token."""
    # Find user (in real implementation, verify with database)
    user = next((u for u in mock_users if u.username == user_credentials.username), None)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password (in real implementation, verify hashed password)
    # if not pwd_context.verify(user_credentials.password, user.hashed_password):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }


# Learning paths endpoints
@app.get("/learning-paths", response_model=List[LearningPath])
async def get_learning_paths():
    """Get all learning paths."""
    return mock_learning_paths


@app.get("/learning-paths/{path_id}", response_model=LearningPath)
async def get_learning_path(path_id: int):
    """Get specific learning path."""
    path = next((p for p in mock_learning_paths if p["id"] == path_id), None)
    if not path:
        raise HTTPException(status_code=404, detail="Learning path not found")
    return path


# Tutorials endpoints
@app.get("/tutorials", response_model=List[Tutorial])
async def get_tutorials(learning_path_id: Optional[int] = None):
    """Get tutorials, optionally filtered by learning path."""
    tutorials = mock_tutorials
    if learning_path_id:
        tutorials = [t for t in tutorials if t["learning_path_id"] == learning_path_id]
    return tutorials


@app.get("/tutorials/{tutorial_id}", response_model=Tutorial)
async def get_tutorial(tutorial_id: int):
    """Get specific tutorial."""
    tutorial = next((t for t in mock_tutorials if t["id"] == tutorial_id), None)
    if not tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return tutorial


# Exercises endpoints
@app.get("/exercises", response_model=List[Exercise])
async def get_exercises(tutorial_id: Optional[int] = None):
    """Get exercises, optionally filtered by tutorial."""
    exercises = mock_exercises
    if tutorial_id:
        exercises = [e for e in exercises if e["tutorial_id"] == tutorial_id]
    return exercises


@app.get("/exercises/{exercise_id}", response_model=Exercise)
async def get_exercise(exercise_id: int):
    """Get specific exercise."""
    exercise = next((e for e in mock_exercises if e["id"] == exercise_id), None)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


# User progress endpoints
@app.post("/progress")
async def update_progress(
    progress: UserProgress, 
    current_user: User = Depends(get_current_user)
):
    """Update user progress."""
    # In real implementation, save to database
    logger.info(f"Updated progress for user {current_user.id}: {progress}")
    return {"status": "success", "message": "Progress updated"}


@app.get("/progress/{user_id}")
async def get_user_progress(
    user_id: int, 
    current_user: User = Depends(get_current_user)
):
    """Get user progress."""
    # In real implementation, fetch from database
    # Ensure user can only access their own progress (unless admin)
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "user_id": user_id,
        "completed_tutorials": 12,
        "total_hours": 156,
        "current_path": "technical",
        "progress_percentage": 45.5,
        "achievements": [
            {"id": 1, "title": "AI Basics", "earned_at": "2024-01-15"},
            {"id": 2, "title": "First Exercise", "earned_at": "2024-01-16"},
        ]
    }


# Assessment endpoints
@app.post("/assessments/{assessment_id}/submit")
async def submit_assessment(
    assessment_id: int,
    submission: AssessmentSubmission,
    current_user: User = Depends(get_current_user)
):
    """Submit assessment for grading."""
    # In real implementation:
    # 1. Save submission to database
    # 2. Run automated grading
    # 3. Calculate score and provide feedback
    # 4. Update user progress
    
    logger.info(f"Assessment {assessment_id} submitted by user {current_user.id}")
    
    # Mock grading result
    score = 85.0
    passed = score >= 70.0
    
    return {
        "submission_id": 1,
        "score": score,
        "passed": passed,
        "feedback": "Good work! Review the questions you missed for improvement.",
        "graded_at": datetime.utcnow().isoformat()
    }


# Analytics endpoints
@app.get("/analytics/learning-stats")
async def get_learning_stats(
    current_user: User = Depends(get_current_user)
):
    """Get learning analytics for current user."""
    return {
        "total_learning_hours": 156,
        "tutorials_completed": 12,
        "exercises_solved": 48,
        "average_score": 82.5,
        "streak_days": 7,
        "weekly_progress": [
            {"week": "2024-W1", "hours": 8},
            {"week": "2024-W2", "hours": 12},
            {"week": "2024-W3", "hours": 15},
            {"week": "2024-W4", "hours": 10},
        ],
        "skill_progress": {
            "ai_fundamentals": 90,
            "technical_limitations": 65,
            "solutions": 40,
            "implementation": 30,
        }
    }


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "detail": str(exc)}
    )


def main():
    """Main function to run the application."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Education Platform API Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes")
    
    args = parser.parse_args()
    
    uvicorn.run(
        "src.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers if not args.reload else 1,
        log_level="info"
    )


if __name__ == "__main__":
    main()