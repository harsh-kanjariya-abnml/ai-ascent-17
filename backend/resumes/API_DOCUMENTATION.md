# Resume API Documentation

## Endpoints

### 1. Process Resume - POST /api/process/

Processes a PDF resume file using AI-powered extraction and calculates frontend/backend scores.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: PDF file with key 'resume'

**Processing Steps:**
1. **PDF Text Extraction**: Converts PDF to plain text using PyPDF2
2. **LLM Analysis**: Uses OpenAI GPT-3.5-turbo to extract structured data
3. **Score Calculation**: Automatically calculates FE/BE scores based on skills and seniority
4. **Data Validation**: Normalizes and validates extracted information

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
    "skills": ["Python", "Django", "React", "JavaScript", "AWS", "Docker"],
    "fe_score": 75,
    "be_score": 85,
    "seniority": "Senior",
    "qualifications": "Bachelors"
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
- `skills` (array of strings): Filter by technical skills
- `seniorityLevel` (string): Filter by seniority level
  - Valid values: "Junior", "Mid", "Senior", "Lead", "Principal"
- `qualifications` (string): Filter by educational qualifications
  - Valid values: "High School", "Bachelors", "Masters", "PhD", "Diploma", "Certification"
- `fe_score` (integer): Minimum frontend score (0-100)
- `be_score` (integer): Minimum backend score (0-100)

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
    "seniorityLevel": "Senior",
    "qualifications": "Bachelors",
    "fe_score": 70,
    "be_score": 80
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
      "seniority": "Senior",
      "qualifications": "Bachelors",
      "created_at": "2023-12-01T10:30:00Z",
      "updated_at": "2023-12-01T10:30:00Z"
    }
  ],
  "total_count": 1,
  "filters_applied": {
    "skills": ["Python", "Django"],
    "seniorityLevel": "Senior",
    "qualifications": "Bachelors",
    "fe_score": 70,
    "be_score": 80
  }
}
```

**Additional Filter Examples:**

**Filter by Frontend Skills and Score:**
```json
{
  "skills": ["React", "JavaScript", "TypeScript"],
  "fe_score": 80
}
```

**Filter by Backend Skills and Seniority:**
```json
{
  "skills": ["Python", "Django", "AWS"],
  "seniorityLevel": "Senior",
  "be_score": 75
}
```

**Filter by Qualifications Only:**
```json
{
  "qualifications": "Masters"
}
```

**Filter by Score Range:**
```json
{
  "fe_score": 60,
  "be_score": 70
}
```

## AI-Powered Processing

### LLM Integration
The system uses **OpenAI GPT-3.5-turbo** to intelligently extract candidate information from resume text with:
- **Structured Prompting**: Guides the AI to extract specific fields
- **JSON Response Parsing**: Ensures consistent data format
- **Fallback Processing**: Uses rule-based extraction if AI fails
- **Data Validation**: Normalizes and validates all extracted information

### PDF Processing
- **Text Extraction**: Uses PyPDF2 to convert PDF content to plain text
- **Multi-page Support**: Processes all pages in the PDF document
- **Error Handling**: Graceful fallback for corrupted or unreadable PDFs

## Models

### CandidateProfile

Fields:
- `id` (UUID): Primary key
- `name` (string): Candidate name (extracted by LLM)
- `skills` (JSON array): List of technical skills (extracted by LLM)
- `fe_score` (integer): Frontend score (0-100) - calculated automatically
- `be_score` (integer): Backend score (0-100) - calculated automatically
- `seniority` (string): Seniority level (extracted by LLM, displayed as "Junior", "Mid", "Senior", "Lead", "Principal")
- `qualifications` (string): Highest qualification (extracted by LLM, displayed as "Bachelors", "Masters", etc.)
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

## Intelligent Scoring System

### Frontend Score (fe_score)
Automatically calculated based on:
- **Frontend Skills**: React (+10), Angular (+10), Vue (+10), JavaScript (+10), TypeScript (+10), HTML (+10), CSS (+10), UI/UX tools (+10 each)
- **Seniority Bonus**: 
  - Junior: +5
  - Mid: +10
  - Senior: +20
  - Lead/Principal: +30
- **Maximum Score**: 100

### Backend Score (be_score)
Automatically calculated based on:
- **Backend Skills**: Python (+10), Django (+10), Node.js (+10), Java (+10), databases (+10), cloud services (+10), APIs (+10 each)
- **Seniority Bonus**:
  - Junior: +5
  - Mid: +10
  - Senior: +20
  - Lead/Principal: +30
- **Maximum Score**: 100

## Filter Behavior

### Skills Filtering
- **Partial Match**: Uses case-insensitive partial matching
- **Multiple Skills**: Filters candidates who have ALL specified skills
- **Example**: `["Python", "React"]` finds candidates with both Python AND React skills

### Score Filtering
- **Minimum Threshold**: `fe_score` and `be_score` filter candidates with scores >= specified value
- **Range Support**: Can combine both scores for candidates strong in both frontend and backend
- **Example**: `{"fe_score": 70, "be_score": 80}` finds full-stack candidates

### Seniority Filtering
- **Exact Match**: Matches exact seniority level
- **Case Sensitive**: Must use exact capitalization: "Junior", "Mid", "Senior", "Lead", "Principal"

### Qualifications Filtering
- **Exact Match**: Matches exact qualification level
- **Case Sensitive**: Must use exact capitalization: "Bachelors", "Masters", "PhD", etc.

## Configuration

### Environment Variables
Set the following environment variable to enable LLM processing:
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### Fallback Behavior
If the OpenAI API is unavailable or fails:
1. The system automatically falls back to rule-based extraction
2. Processing continues without interruption
3. Scores are still calculated using available data
4. Error is logged for debugging

## Error Handling

All endpoints return appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 500: Internal Server Error

Error responses include an `error` field with a descriptive message.

## Performance Notes

- **PDF Processing**: Optimized for documents up to 10MB
- **LLM Processing**: Typical response time 2-5 seconds
- **Caching**: Consider implementing caching for frequently processed resumes
- **Rate Limiting**: OpenAI API has rate limits - consider implementing queuing for high volume 