#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REST API for LMS Integration
Provides endpoints for Google Classroom, Blackboard, and Canvas integration
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os
import json
from database import AnalysisDatabase
from report_generator import ReportGenerator
import google.generativeai as genai

# Initialize FastAPI app
app = FastAPI(
    title="AI Grader REST API",
    description="API for AI-powered project grading system with LMS integration",
    version="1.0.0"
)

# Add CORS middleware for LMS systems
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (configure as needed for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and utilities
db = AnalysisDatabase()
report_gen = ReportGenerator()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# ========== MODELS ==========
class AnalysisRequest(BaseModel):
    """Request model for analysis"""
    username: str
    file_name: str
    file_content: str  # Base64 encoded file content


class AnalysisResponse(BaseModel):
    """Response model for analysis"""
    id: int
    username: str
    file_name: str
    timestamp: str
    result: str
    status: str = "success"


class HistoryItem(BaseModel):
    """Model for history item"""
    id: int
    file_name: str
    timestamp: str
    result: str


class UserStatistics(BaseModel):
    """Model for user statistics"""
    total_analyses: int
    last_analysis_date: str
    avg_file_size: int


class GradeSubmission(BaseModel):
    """Model for LMS grade submission"""
    student_id: str
    student_name: str
    course_id: str
    assignment_id: str
    file_url: str
    grade: Optional[float] = None
    feedback: Optional[str] = None


# ========== ENDPOINTS ==========

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "AI Grader REST API",
        "version": "1.0.0",
        "description": "API for AI-powered project grading with LMS integration",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/v1/analyze",
            "history": "/api/v1/history/{username}",
            "statistics": "/api/v1/statistics/{username}",
            "lms/google": "/api/v1/lms/google-classroom",
            "lms/blackboard": "/api/v1/lms/blackboard",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/v1/analyze", response_model=AnalysisResponse)
async def analyze_project(request: AnalysisRequest):
    """
    Analyze a project file
    
    Args:
        request: Analysis request with username, file_name, and file_content
    
    Returns:
        AnalysisResponse with analysis results
    """
    try:
        # Prepare prompt for AI
        prompt = f"""
        Role: คุณคือครูที่ปรึกษาโครงงานผู้เชี่ยวชาญ
        Task: วิเคราะห์ "ความสอดคล้อง" ของโครงงาน
        
        Content:
        {request.file_content[:30000]}
        
        Instructions:
        1. หา "วัตถุประสงค์" และ "สรุปผล" จากข้อความ
        2. เปรียบเทียบว่าสอดคล้องกันหรือไม่
        3. ให้คะแนนและข้อแนะนำ
        
        Output Format (ตอบเป็น Markdown ภาษาไทย):
        ## ผลการวิเคราะห์
        [ผลการวิเคราะห์]
        """
        
        # Get AI model and analyze
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            analysis_result = response.text
        except:
            # Fallback model
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            analysis_result = response.text
        
        # Save to database
        db.save_analysis(request.username, request.file_name, analysis_result)
        
        # Get the latest record
        history = db.get_user_history(request.username)
        if history:
            latest = history[0]
            return AnalysisResponse(
                id=latest['id'],
                username=request.username,
                file_name=request.file_name,
                timestamp=latest['timestamp'],
                result=analysis_result,
                status="success"
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/history/{username}", response_model=List[HistoryItem])
async def get_user_history(username: str):
    """
    Get analysis history for a user
    
    Args:
        username: Username to retrieve history for
    
    Returns:
        List of analysis records
    """
    try:
        history = db.get_user_history(username)
        return [
            HistoryItem(
                id=item['id'],
                file_name=item['file_name'],
                timestamp=item['timestamp'],
                result=item['result'][:200]  # Preview first 200 chars
            )
            for item in history
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/statistics/{username}", response_model=UserStatistics)
async def get_user_statistics(username: str):
    """
    Get statistics for a user
    
    Args:
        username: Username to get statistics for
    
    Returns:
        User statistics
    """
    try:
        stats = db.get_statistics(username)
        return UserStatistics(
            total_analyses=stats.get('total_analyses', 0),
            last_analysis_date=stats.get('last_analysis_date', 'N/A'),
            avg_file_size=stats.get('avg_file_size', 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/report/download/{analysis_id}")
async def download_report(analysis_id: int, username: str, format: str = "docx"):
    """
    Download report for an analysis
    
    Args:
        analysis_id: ID of analysis to download
        username: Username
        format: Report format (docx or pdf)
    
    Returns:
        File download
    """
    try:
        record = db.get_analysis_by_id(username, analysis_id)
        if not record:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        if format == "docx":
            doc_buffer = report_gen.generate_word_report(
                username=username,
                file_name=record['file_name'],
                analysis_result=record['result'],
                timestamp=record['timestamp']
            )
            filename = report_gen.get_word_filename(record['file_name'], username)
            return FileResponse(
                doc_buffer,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                filename=filename
            )
        elif format == "pdf":
            pdf_buffer = report_gen.generate_pdf_report(
                username=username,
                file_name=record['file_name'],
                analysis_result=record['result'],
                timestamp=record['timestamp']
            )
            filename = report_gen.get_pdf_filename(record['file_name'], username)
            return FileResponse(
                pdf_buffer,
                media_type="application/pdf",
                filename=filename
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid format")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== LMS INTEGRATION ENDPOINTS ==========

@app.post("/api/v1/lms/google-classroom")
async def google_classroom_webhook(submission: GradeSubmission, background_tasks: BackgroundTasks):
    """
    Google Classroom integration endpoint
    
    Receives submissions from Google Classroom and processes them
    """
    try:
        # Process submission in background
        background_tasks.add_task(
            process_google_classroom_submission,
            submission
        )
        
        return {
            "status": "processing",
            "message": f"Submission received for student {submission.student_name}",
            "student_id": submission.student_id,
            "assignment_id": submission.assignment_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/lms/blackboard")
async def blackboard_webhook(submission: GradeSubmission, background_tasks: BackgroundTasks):
    """
    Blackboard integration endpoint
    
    Receives submissions from Blackboard and processes them
    """
    try:
        # Process submission in background
        background_tasks.add_task(
            process_blackboard_submission,
            submission
        )
        
        return {
            "status": "processing",
            "message": f"Submission received for student {submission.student_name}",
            "student_id": submission.student_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/lms/canvas")
async def canvas_webhook(submission: GradeSubmission, background_tasks: BackgroundTasks):
    """
    Canvas LMS integration endpoint
    
    Receives submissions from Canvas and processes them
    """
    try:
        background_tasks.add_task(
            process_canvas_submission,
            submission
        )
        
        return {
            "status": "processing",
            "message": f"Submission received for student {submission.student_name}",
            "student_id": submission.student_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== BACKGROUND TASKS ==========

async def process_google_classroom_submission(submission: GradeSubmission):
    """Process Google Classroom submission"""
    print(f"Processing Google Classroom submission: {submission.student_id}")
    # Implement Google Classroom API integration
    pass


async def process_blackboard_submission(submission: GradeSubmission):
    """Process Blackboard submission"""
    print(f"Processing Blackboard submission: {submission.student_id}")
    # Implement Blackboard API integration
    pass


async def process_canvas_submission(submission: GradeSubmission):
    """Process Canvas submission"""
    print(f"Processing Canvas submission: {submission.student_id}")
    # Implement Canvas API integration
    pass


# ========== ERROR HANDLERS ==========

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
