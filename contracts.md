# Math Tutoring App - Backend Integration Contracts

## API Contracts

### Authentication Endpoints
- `POST /api/auth/student-login` - Student login with username
- `POST /api/auth/teacher-login` - Teacher login with access code
- `POST /api/auth/logout` - Logout user

### Student Progress Endpoints
- `GET /api/students/{username}/progress` - Get student progress
- `PUT /api/students/{username}/progress` - Update student progress
- `POST /api/students/{username}/attempt` - Record problem attempt

### Problems Endpoints
- `GET /api/problems/section/{sectionId}` - Get problems for a section
- `GET /api/problems/{problemId}` - Get specific problem details

### Teacher Dashboard Endpoints
- `GET /api/teacher/students` - Get all student data and statistics
- `GET /api/teacher/analytics` - Get overall analytics

## Mock Data to Replace

### 1. Student Authentication (mock.js → API)
**Current Mock**: Static username validation in frontend
**Replace With**: Database-backed student records with progress tracking

### 2. Progress Tracking (localStorage → Database)
**Current Mock**: 
```javascript
localStorage.setItem(`mathapp_progress_${username}`, JSON.stringify(progress))
```
**Replace With**: MongoDB collections for student progress

### 3. Problem Data (mock.js → Database)
**Current Mock**: Static problem objects in `mockProblems`
**Replace With**: Database-stored problems with multilingual support

### 4. Teacher Analytics (localStorage → Database)
**Current Mock**: Scanning localStorage for student data
**Replace With**: Aggregated database queries

## Backend Implementation Plan

### 1. Database Models
```python
# Student Model
class Student:
    username: str
    created_at: datetime
    last_login: datetime
    total_points: int
    badges: List[str]

# Progress Model
class Progress:
    student_username: str
    section_id: str
    problem_id: str
    completed: bool
    score: int
    attempts: int
    hints_used: int
    last_attempt: datetime

# Problem Model
class Problem:
    id: str
    section_id: str
    type: str  # preparation, explanation, practice, assessment, examprep
    weight: int
    question_en: str
    question_ar: str
    answer: str
    answer_ar: str
    hints_en: List[str]
    hints_ar: List[str]
    explanation_en: str
    explanation_ar: str
    show_full_solution: bool
    hide_answer: bool
```

### 2. API Endpoints Implementation
- Authentication with session management
- CRUD operations for student progress
- Problem retrieval with language support
- Teacher analytics with aggregation
- Error handling and validation

### 3. Frontend Integration Changes
- Replace mock data imports with API calls
- Update components to use actual endpoints
- Implement loading states and error handling
- Remove localStorage dependency for core data

### 4. Data Migration
- Populate database with Section 1 problems
- Convert mock data structure to database schema
- Ensure Arabic/English content is properly stored

## Integration Testing
- Student login flow
- Problem attempt and progress tracking
- Teacher dashboard data accuracy
- Language switching functionality
- Weighted scoring calculations