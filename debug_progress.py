#!/usr/bin/env python3
"""
Debug script to check progress update issue
"""

import requests
import json

BACKEND_URL = "https://inequality-solver.preview.emergentagent.com/api"

def debug_progress():
    # Create student
    student_data = {"username": "debug_test_student", "class_name": "GR9-A"}
    response = requests.post(f"{BACKEND_URL}/auth/student-login", json=student_data)
    print(f"Student creation: {response.status_code}")
    print(f"Student data: {response.json()}")
    
    # Check initial progress
    response = requests.get(f"{BACKEND_URL}/students/debug_test_student/progress")
    print(f"\nInitial progress: {response.status_code}")
    initial_progress = response.json()
    print(f"Initial prep1 status: {initial_progress.get('progress', {}).get('section1', {}).get('prep1', {})}")
    
    # Submit correct answer
    attempt_data = {"problem_id": "prep1", "answer": "7", "hints_used": 0}
    response = requests.post(f"{BACKEND_URL}/students/debug_test_student/attempt", json=attempt_data)
    print(f"\nAnswer submission: {response.status_code}")
    submission_result = response.json()
    print(f"Submission result: {submission_result}")
    
    # Check progress after submission
    response = requests.get(f"{BACKEND_URL}/students/debug_test_student/progress")
    print(f"\nProgress after submission: {response.status_code}")
    final_progress = response.json()
    print(f"Final prep1 status: {final_progress.get('progress', {}).get('section1', {}).get('prep1', {})}")
    
    # Check if there's a difference
    initial_prep1 = initial_progress.get('progress', {}).get('section1', {}).get('prep1', {})
    final_prep1 = final_progress.get('progress', {}).get('section1', {}).get('prep1', {})
    
    print(f"\nComparison:")
    print(f"Initial completed: {initial_prep1.get('completed', False)}")
    print(f"Final completed: {final_prep1.get('completed', False)}")
    print(f"Initial score: {initial_prep1.get('score', 0)}")
    print(f"Final score: {final_prep1.get('score', 0)}")
    print(f"Initial attempts: {initial_prep1.get('attempts', 0)}")
    print(f"Final attempts: {final_prep1.get('attempts', 0)}")

if __name__ == "__main__":
    debug_progress()