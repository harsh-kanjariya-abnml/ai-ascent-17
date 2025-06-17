# Resume API Documentation

## Endpoints

### 1. Process Resume - POST /api/process/

Processes a PDF resume file and extracts candidate information.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: PDF file with key 'resume'

**Response:**
- 201 Created: Resume processed successfully
- 400 Bad Request: Invalid input (missing file, wrong format, etc.)
- 500 Internal Server Error: Processing failed

**Example Request:**
```bash
curl -X POST \
  http://localhost:8000/api/process/ \
  -F "resume=@/path/to/resume.pdf"
```

**Example Response (201):**
```json
{
  "message": "Resume processed successfully",
  "candidate_id": "123e4567-e89b-12d3-a456-426614174000",
  "candidate_data": {
    "name": "John Doe",
    "skills": ["Python", "Django", "React", "JavaScript"],
    "fe_score": 75,
    "be_score": 85,
    "seniority": "senior",
    "qualifications": "bachelors"
  }
}
```

### 2. Get Candidates - POST /api/get-candidates/

Retrieves candidates based on filter criteria.

**Request:**
- Method: POST
- Content-Type: application/json
- Body: JSON with filter parameters

**Filter Parameters:**
- `skills` (array of strings): Filter by skills
- `seniority` (string): Filter by seniority level
  - Valid values: "junior", "mid", "senior", "lead", "principal"
- `qualifications` (string): Filter by qualifications
  - Valid values: "high_school", "bachelors", "masters", "phd", "diploma", "certification"
- `fe_score_min` (integer): Minimum frontend score (0-100)
- `be_score_min` (integer): Minimum backend score (0-100)

**Response:**
- 200 OK: Candidates retrieved successfully
- 400 Bad Request: Invalid filter parameters
- 500 Internal Server Error: Server error

**Example Request:**
```bash
curl -X POST \
  http://localhost:8000/api/get-candidates/ \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Python", "Django"],
    "seniority": "senior",
    "qualifications": "bachelors",
    "fe_score_min": 70,
    "be_score_min": 80
  }'
```

**Example Response (200):**
```json
{
  "candidates": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "skills": ["Python", "Django", "React", "JavaScript"],
      "fe_score": 75,
      "be_score": 85,
      "seniority": "senior",
      "qualifications": "bachelors",
      "created_at": "2023-12-01T10:30:00Z",
      "updated_at": "2023-12-01T10:30:00Z"
    }
  ],
  "total_count": 1,
  "filters_applied": {
    "skills": ["Python", "Django"],
    "seniority": "senior",
    "qualifications": "bachelors",
    "fe_score_min": 70,
    "be_score_min": 80
  }
}
```

## Models

### CandidateProfile

Fields:
- `id` (UUID): Primary key
- `name` (string): Candidate name
- `skills` (JSON array): List of skills
- `fe_score` (integer): Frontend score (0-100)
- `be_score` (integer): Backend score (0-100)
- `seniority` (string): Seniority level
- `qualifications` (string): Highest qualification
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

## Scoring System

The system automatically calculates frontend and backend scores based on:

### Frontend Score (fe_score)
- **Skills Detected**: React, Angular, Vue, JavaScript, TypeScript, HTML, CSS, UI/UX tools (+10 each)
- **Experience Level**: 
  - Junior: +5
  - Mid: +10
  - Senior: +20
  - Lead/Principal: +30
- **Maximum Score**: 100

### Backend Score (be_score)
- **Skills Detected**: Python, Django, Node.js, Java, databases, cloud services, APIs (+10 each)
- **Experience Level**: 
  - Junior: +5
  - Mid: +10
  - Senior: +20
  - Lead/Principal: +30
- **Maximum Score**: 100

## Error Handling

All endpoints return appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 500: Internal Server Error

Error responses include an `error` field with a descriptive message. 