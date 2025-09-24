from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class ProblemType(str, Enum):
    PREPARATION = "preparation"
    EXPLANATION = "explanation"
    PRACTICE = "practice"
    ASSESSMENT = "assessment"
    EXAMPREP = "examprep"

class Student(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    class_name: str = Field(default="GR9-A", pattern="^GR9-[A-D]$")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime = Field(default_factory=datetime.utcnow)
    total_points: int = Field(default=0, ge=0)
    badges: List[str] = Field(default_factory=list)

class StudentCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    class_name: str = Field(default="GR9-A", pattern="^GR9-[A-D]$")

class Progress(BaseModel):
    student_username: str
    section_id: str
    problem_id: str
    completed: bool = False
    score: int = Field(default=0, ge=0, le=100)
    attempts: int = Field(default=0, ge=0)
    hints_used: int = Field(default=0, ge=0)
    last_attempt: Optional[datetime] = None

class ProgressUpdate(BaseModel):
    completed: bool
    score: int = Field(ge=0, le=100)
    attempts: int = Field(ge=0)
    hints_used: int = Field(ge=0)

class ProblemAttempt(BaseModel):
    problem_id: str
    answer: str
    hints_used: int = Field(default=0, ge=0)

class PracticeExample(BaseModel):
    question_en: str
    question_ar: str
    answer: str
    answer_ar: str
    hint_en: str
    hint_ar: str

class InteractiveExample(BaseModel):
    title_en: str
    title_ar: str
    problem_en: str
    problem_ar: str
    solution_en: str
    solution_ar: str
    # Only the next four lines need to be changed
    practice_question_en: str | None = None
    practice_question_ar: str | None = None
    practice_answer: str | None = None
    practice_answer_ar: str | None = None

class StepSolution(BaseModel):
    step_en: str
    step_ar: str
    possible_answers: List[str]
    possible_answers_ar: List[str]

class Problem(BaseModel):
    id: str
    section_id: str
    type: ProblemType
    weight: int = Field(ge=0, le=100)
    question_en: str
    question_ar: str
    answer: str
    answer_ar: str
    hints_en: List[str] = Field(default_factory=list)
    hints_ar: List[str] = Field(default_factory=list)
    explanation_en: Optional[str] = None
    explanation_ar: Optional[str] = None
    show_full_solution: bool = False
    hide_answer: bool = False
    step_solutions: Optional[List[StepSolution]] = None
    practice_problems: Optional[List[PracticeExample]] = None
    interactive_examples: Optional[List[InteractiveExample]] = None
    final_answer_required: Optional[bool] = False
    stage_type: Optional[str] = None

class Section(BaseModel):
    id: str
    title_en: str
    title_ar: str
    problems: List[Problem]

class TeacherAuth(BaseModel):
    access_code: str

class StudentStats(BaseModel):
    username: str
    progress_percentage: float
    completed_problems: int
    total_problems: int
    weighted_score: float
    total_attempts: int
    last_activity: Optional[datetime]
    problems_status: Dict[str, Dict]

class TeacherDashboard(BaseModel):
    total_students: int
    average_progress: float
    completed_problems: int
    average_score: float
    students: List[StudentStats]