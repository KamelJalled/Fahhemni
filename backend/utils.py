import re
from typing import Dict

def convert_to_arabic_numerals(text: str) -> str:
    """Convert Western numerals to Arabic numerals"""
    arabic_numerals = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
    return re.sub(r'[0-9]', lambda x: arabic_numerals[int(x.group())], text)

def convert_to_western_numerals(text: str) -> str:
    """Convert Arabic numerals to Western numerals"""
    arabic_to_western = {'٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', 
                        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'}
    return re.sub(r'[٠-٩]', lambda x: arabic_to_western[x.group()], text)

def basic_normalize_answer(answer: str) -> str:
    """Basic normalization without preparation stage logic"""
    if not answer:
        return ''
    
    # Convert Arabic numerals to Western and س to x
    normalized = convert_to_western_numerals(answer.lower().replace('س', 'x').strip())
    
    # Normalize operators and spaces more carefully
    normalized = re.sub(r'÷', '/', normalized)  # Convert ÷ to /
    normalized = re.sub(r'×', '*', normalized)  # Convert × to *
    normalized = re.sub(r'\s+', ' ', normalized)  # Normalize multiple spaces to single
    normalized = re.sub(r'\s*([+\-*/=])\s*', r'\1', normalized)  # Remove spaces around basic operators
    normalized = re.sub(r'\s*([<>])\s*', r'\1', normalized)  # Remove spaces around inequality signs
    normalized = re.sub(r'\s*([≤≥])\s*', r'\1', normalized)  # Remove spaces around unicode inequalities
    normalized = re.sub(r'\s*([<>]=?)\s*', r'\1', normalized)  # Handle <= >= combinations
    
    return normalized

def normalize_answer(answer: str, problem_type: str = None, expected_answer: str = None) -> str:
    """Enhanced normalize answer for comparison - handles preparation stage logic"""
    if not answer:
        return ''
    
    normalized = basic_normalize_answer(answer)
    
    # ENHANCEMENT: For preparation stage, accept both "x = 7" and "7" formats
    if problem_type == 'preparation' or (expected_answer and 'prep' in str(expected_answer)):
        # If input has "x=" and expected answer is just a number, remove "x=" from input
        if 'x=' in normalized and expected_answer:
            expected_normalized = basic_normalize_answer(expected_answer)
            if re.match(r'^-?\d+(\.\d+)?$', expected_normalized):
                # Remove "x=" from the input to match the expected format
                normalized = re.sub(r'^x=', '', normalized)
        # If input is just a number and expected answer has "x =", add "x ="
        elif re.match(r'^-?\d+(\.\d+)?$', normalized) and expected_answer:
            expected_normalized = basic_normalize_answer(expected_answer)
            if 'x=' in expected_normalized and 'x' not in normalized:
                normalized = 'x=' + normalized
    
    return normalized

def calculate_score(attempts: int, hints_used: int, is_correct: bool) -> int:
    """Calculate score based on attempts and hints used"""
    if not is_correct:
        return 0
    
    # Start with 100 points
    score = 100
    
    # Deduct points for additional attempts (20 points per additional attempt)
    if attempts > 1:
        score -= (attempts - 1) * 20
    
    # Deduct points for hints used (10 points per hint)
    score -= hints_used * 10
    
    # Minimum score is 40 if correct
    return max(40, score)

def calculate_badges(progress_dict: Dict) -> list:
    """Calculate badges earned based on progress"""
    badges = []
    
    # First Steps - complete any problem
    if any(p.get('completed', False) for p in progress_dict.values()):
        badges.append('first_steps')
    
    # Practice Master - complete all practice problems
    practice_completed = (
        progress_dict.get('practice1', {}).get('completed', False) and
        progress_dict.get('practice2', {}).get('completed', False)
    )
    if practice_completed:
        badges.append('practice_master')
    
    # Assessment Ace - score 80+ on assessment
    assessment = progress_dict.get('assessment1', {})
    if assessment.get('completed', False) and assessment.get('score', 0) >= 80:
        badges.append('assessment_ace')
    
    # Inequality Expert - complete entire section
    if all(p.get('completed', False) for p in progress_dict.values()):
        badges.append('inequality_expert')
    
    return badges

def calculate_total_points(progress_dict: Dict, problems_dict: Dict) -> int:
    """Calculate total points based on weighted scoring"""
    total_points = 0
    
    for problem_id, progress in progress_dict.items():
        if progress.get('completed', False):
            problem = problems_dict.get(problem_id, {})
            weight = problem.get('weight', 0)
            score = progress.get('score', 0)
            total_points += (score * weight) / 100
    
    return round(total_points)