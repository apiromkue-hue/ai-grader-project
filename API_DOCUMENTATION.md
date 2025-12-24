# REST API Documentation for LMS Integration

## 📚 API Overview

The AI Grader REST API provides endpoints for integrating with Learning Management Systems (LMS) such as Google Classroom, Blackboard, and Canvas.

**Base URL**: `http://localhost:8000` (local) or `https://your-domain.com/api` (production)

---

## 🔧 Endpoints

### 1. Health Check
**GET** `/health`

Check if the API server is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-14T10:50:00.000000"
}
```

---

### 2. Analyze Project
**POST** `/api/v1/analyze`

Analyze a project file using AI.

**Request:**
```json
{
  "username": "student1",
  "file_name": "project_report.pdf",
  "file_content": "base64_encoded_content_here"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "student1",
  "file_name": "project_report.pdf",
  "timestamp": "2025-12-14T10:50:00.000000",
  "result": "## ผลการวิเคราะห์\n...",
  "status": "success"
}
```

---

### 3. Get User History
**GET** `/api/v1/history/{username}`

Get analysis history for a specific user.

**Response:**
```json
[
  {
    "id": 1,
    "file_name": "project.pdf",
    "timestamp": "2025-12-14T10:50:00.000000",
    "result": "## ผลการวิเคราะห์..."
  },
  {
    "id": 2,
    "file_name": "report.docx",
    "timestamp": "2025-12-14T10:45:00.000000",
    "result": "## ผลการวิเคราะห์..."
  }
]
```

---

### 4. Get User Statistics
**GET** `/api/v1/statistics/{username}`

Get statistics for a user.

**Response:**
```json
{
  "total_analyses": 5,
  "last_analysis_date": "2025-12-14T10:50:00.000000",
  "avg_file_size": 4500
}
```

---

### 5. Download Report
**POST** `/api/v1/report/download/{analysis_id}`

Download analysis report in Word or PDF format.

**Query Parameters:**
- `username` (required): User who owns the analysis
- `format` (optional): `docx` (default) or `pdf`

**Response:**
File download (application/vnd.openxmlformats-officedocument.wordprocessingml.document or application/pdf)

---

## 🎓 LMS Integration Endpoints

### Google Classroom Integration
**POST** `/api/v1/lms/google-classroom`

Receive and process submissions from Google Classroom.

**Request:**
```json
{
  "student_id": "123456",
  "student_name": "John Doe",
  "course_id": "course123",
  "assignment_id": "assignment456",
  "file_url": "https://classroom.google.com/files/...",
  "grade": 85.5,
  "feedback": "Good work, but needs improvement in..."
}
```

**Response:**
```json
{
  "status": "processing",
  "message": "Submission received for student John Doe",
  "student_id": "123456",
  "assignment_id": "assignment456"
}
```

---

### Blackboard Integration
**POST** `/api/v1/lms/blackboard`

Receive and process submissions from Blackboard.

**Request:**
```json
{
  "student_id": "987654",
  "student_name": "Jane Smith",
  "course_id": "course789",
  "assignment_id": "assignment101",
  "file_url": "https://blackboard.com/files/...",
  "grade": 92.0,
  "feedback": "Excellent work!"
}
```

---

### Canvas Integration
**POST** `/api/v1/lms/canvas`

Receive and process submissions from Canvas.

**Request:**
```json
{
  "student_id": "canvas123",
  "student_name": "Student Name",
  "course_id": "canvas_course",
  "assignment_id": "canvas_assign",
  "file_url": "https://canvas.instructure.com/files/...",
  "grade": 88.0,
  "feedback": "Good submission"
}
```

---

## 📝 Usage Examples

### Example 1: Analyze a File (Python)
```python
import requests
import base64

# Read file and encode to base64
with open('project.pdf', 'rb') as f:
    file_content = base64.b64encode(f.read()).decode('utf-8')

# Send analysis request
response = requests.post('http://localhost:8000/api/v1/analyze', json={
    "username": "student1",
    "file_name": "project.pdf",
    "file_content": file_content
})

result = response.json()
print(f"Analysis Result ID: {result['id']}")
print(f"Result: {result['result']}")
```

### Example 2: Get User History (JavaScript)
```javascript
fetch('/api/v1/history/student1')
  .then(response => response.json())
  .then(data => {
    console.log('User history:', data);
    data.forEach(item => {
      console.log(`${item.file_name}: ${item.timestamp}`);
    });
  });
```

### Example 3: Google Classroom Webhook
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook/google-classroom', methods=['POST'])
def handle_classroom_submission():
    payload = request.json
    
    # Forward to AI Grader API
    response = requests.post(
        'http://localhost:8000/api/v1/lms/google-classroom',
        json=payload
    )
    
    return response.json()
```

---

## 🔐 Authentication

For production deployment, add API key authentication:

```python
# In api_server.py
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.post("/api/v1/analyze")
async def analyze_project(request: AnalysisRequest, api_key = Depends(verify_api_key)):
    # Protected endpoint
    pass
```

Set in `.env`:
```
API_KEY=your-secret-api-key-here
```

---

## 📊 Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 500 | Internal Server Error |
| 403 | Forbidden (Invalid API Key) |

---

## 🚀 Deployment

### Run Locally
```bash
python api_server.py
```

API will be available at `http://localhost:8000`
Swagger UI documentation at `http://localhost:8000/docs`

### Run with Uvicorn
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Deployment
```bash
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your-key \
  -e API_KEY=your-api-key \
  ai-grader-api
```

---

## 📋 LMS Setup Guides

### Google Classroom
1. Go to Classroom Settings
2. Enable API integration
3. Configure webhook URL: `https://your-domain.com/api/v1/lms/google-classroom`
4. Set the API key in Google Classroom settings

### Blackboard
1. Admin Panel → Integrations
2. Create new REST API integration
3. Set endpoint URL: `https://your-domain.com/api/v1/lms/blackboard`
4. Configure authentication

### Canvas
1. Settings → Integrations
2. Enable webhooks
3. Set URL: `https://your-domain.com/api/v1/lms/canvas`
4. Configure API key

---

## 🐛 Troubleshooting

### API not responding
- Check if server is running: `curl http://localhost:8000/health`
- Check firewall settings
- Check environment variables

### Analysis takes too long
- Check API quota on Google Generative AI
- Reduce file size
- Implement request timeout

### LMS webhook not working
- Verify webhook URL is accessible from LMS
- Check API key configuration
- Review server logs

---

## 📞 Support

For questions or issues:
- Check API documentation at `/docs`
- View server logs: `docker logs container-id`
- Check .env configuration

---

**Version**: 1.0.0
**Last Updated**: December 14, 2025
