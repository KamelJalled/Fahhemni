#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - Expanded Version
Tests all core API endpoints for production readiness with all 5 sections
"""

import requests
import json
import sys
import os
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://bilingual-algebra.preview.emergentagent.com/api"

# Expected sections and their problem counts
EXPECTED_SECTIONS = {
    "section1": {"title": "One-Step Inequalities", "problems": 6},
    "section2": {"title": "Two-Step Inequalities", "problems": 6}, 
    "section3": {"title": "Multi-Step Inequalities", "problems": 6},
    "section4": {"title": "Variables on Both Sides", "problems": 6},
    "section5": {"title": "Compound Inequalities", "problems": 6}
}

class MathTutoringAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, details="", response_data=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        if response_data:
            result["response_data"] = response_data
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    def test_health_check(self):
        """Test basic health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "version" in data:
                    self.log_test("Health Check", True, f"API running version {data.get('version')}")
                    return True
                else:
                    self.log_test("Health Check", False, "Missing required fields in response", data)
                    return False
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False

    def test_infinite_recursion_bug_fix_critical(self):
        """CRITICAL TEST: Verify infinite recursion bug fix in answer validation"""
        try:
            print("\n🔍 CRITICAL BUG TEST: Infinite Recursion Fix in Answer Validation")
            print("Testing answer validation system after fixing the infinite recursion bug...")
            
            # Step 1: Create test student as specified in review request
            test_student = {"username": "validation_test_student", "class_name": "GR9-A"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Student Registration for Validation Test", False, 
                            f"Failed to create test student: HTTP {response.status_code}")
                return False
            
            data = response.json()
            if data.get("class_name") != "GR9-A":
                self.log_test("Student Registration for Validation Test", False, 
                            f"Expected class GR9-A, got {data.get('class_name')}")
                return False
            
            self.log_test("Student Registration for Validation Test", True, 
                        f"✅ Created test student 'validation_test_student' in class GR9-A")
            
            # Step 2: Test answer submission for prep1 (problem: x + 8 = 15)
            # This is the critical test - these submissions should NOT cause stack overflow
            test_cases = [
                {
                    "answer": "7",
                    "expected_correct": True,
                    "description": "Submit answer '7' for prep1 - should be CORRECT"
                },
                {
                    "answer": "x=7", 
                    "expected_correct": True,
                    "description": "Submit answer 'x=7' for prep1 - should also be CORRECT"
                },
                {
                    "answer": "5",
                    "expected_correct": False,
                    "description": "Submit answer '5' for prep1 - should be WRONG"
                }
            ]
            
            all_validation_success = True
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n   Test Case {i}: {test_case['description']}")
                
                attempt_data = {
                    "problem_id": "prep1",
                    "answer": test_case["answer"],
                    "hints_used": 0
                }
                
                try:
                    response = self.session.post(
                        f"{self.base_url}/students/validation_test_student/attempt",
                        json=attempt_data,
                        headers={"Content-Type": "application/json"},
                        timeout=10  # Set timeout to catch infinite recursion
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Check required fields are present
                        required_fields = ["score", "correct", "attempts"]
                        missing_fields = [f for f in required_fields if f not in data]
                        
                        if missing_fields:
                            self.log_test(f"Answer Validation Test Case {i}", False, 
                                        f"Missing required fields: {missing_fields}")
                            all_validation_success = False
                            continue
                        
                        # Verify correctness
                        actual_correct = data.get("correct")
                        expected_correct = test_case["expected_correct"]
                        
                        if actual_correct == expected_correct:
                            self.log_test(f"Answer Validation Test Case {i}", True, 
                                        f"✅ Answer '{test_case['answer']}' correctly evaluated as {actual_correct}, score: {data.get('score')}")
                        else:
                            self.log_test(f"Answer Validation Test Case {i}", False, 
                                        f"❌ Answer '{test_case['answer']}' expected {expected_correct}, got {actual_correct}")
                            all_validation_success = False
                        
                        # Check for feedback field (mentioned in success criteria)
                        if "feedback" not in data:
                            print(f"   Note: 'feedback' field not present in response (may be optional)")
                        
                    else:
                        self.log_test(f"Answer Validation Test Case {i}", False, 
                                    f"HTTP {response.status_code}: {response.text}")
                        all_validation_success = False
                        
                except requests.exceptions.Timeout:
                    self.log_test(f"Answer Validation Test Case {i}", False, 
                                "❌ CRITICAL: Request timed out - possible infinite recursion still present")
                    all_validation_success = False
                    
                except Exception as e:
                    self.log_test(f"Answer Validation Test Case {i}", False, 
                                f"❌ CRITICAL: Request failed with error: {str(e)}")
                    all_validation_success = False
            
            # Step 3: Verify progress update after correct answers
            print(f"\n   Testing Progress Update Verification...")
            
            try:
                response = self.session.get(f"{self.base_url}/students/validation_test_student/progress")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if ("progress" in data and 
                        "section1" in data["progress"] and 
                        "prep1" in data["progress"]["section1"]):
                        
                        prep1_progress = data["progress"]["section1"]["prep1"]
                        
                        if prep1_progress.get("completed") == True:
                            self.log_test("Progress Update Verification", True, 
                                        f"✅ Progress properly updated - prep1 marked as completed")
                        else:
                            self.log_test("Progress Update Verification", False, 
                                        f"❌ Progress not updated - prep1 completed: {prep1_progress.get('completed')}")
                            all_validation_success = False
                    else:
                        self.log_test("Progress Update Verification", False, 
                                    "❌ Progress structure incomplete", data)
                        all_validation_success = False
                else:
                    self.log_test("Progress Update Verification", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    all_validation_success = False
                    
            except Exception as e:
                self.log_test("Progress Update Verification", False, 
                            f"Request error: {str(e)}")
                all_validation_success = False
            
            # Final summary
            if all_validation_success:
                self.log_test("CRITICAL INFINITE RECURSION BUG FIX TEST", True, 
                            "✅ All answer validation tests PASSED - No stack overflow errors, proper responses returned")
            else:
                self.log_test("CRITICAL INFINITE RECURSION BUG FIX TEST", False, 
                            "❌ Answer validation system has issues - Bug may not be fully fixed")
            
            return all_validation_success
            
        except Exception as e:
            self.log_test("CRITICAL INFINITE RECURSION BUG FIX TEST", False, 
                        f"Test execution error: {str(e)}")
            return False

    def test_class_assignment_bug_critical(self):
        """CRITICAL TEST: Verify class assignment bug - students should be saved with correct class"""
        try:
            print("\n🔍 CRITICAL BUG TEST: Class Assignment Verification")
            print("Testing if students are correctly saved with their selected class...")
            
            # Test data for different classes as specified in review request
            test_students = [
                {"username": "mobile_test_a", "class_name": "GR9-A"},
                {"username": "mobile_test_b", "class_name": "GR9-B"}, 
                {"username": "mobile_test_c", "class_name": "GR9-C"},
                {"username": "mobile_test_d", "class_name": "GR9-D"}
            ]
            
            all_success = True
            class_assignment_results = []
            
            # Step 1: Register students with different classes
            for student in test_students:
                response = self.session.post(
                    f"{self.base_url}/auth/student-login",
                    json=student,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    actual_class = data.get("class_name")
                    expected_class = student["class_name"]
                    
                    if actual_class == expected_class:
                        self.log_test(f"Class Assignment - {student['username']}", True, 
                                    f"✅ Correctly saved as {actual_class}")
                        class_assignment_results.append({
                            "username": student["username"],
                            "expected": expected_class,
                            "actual": actual_class,
                            "correct": True
                        })
                    else:
                        self.log_test(f"Class Assignment - {student['username']}", False, 
                                    f"❌ CRITICAL BUG: Expected {expected_class}, but saved as {actual_class}")
                        class_assignment_results.append({
                            "username": student["username"],
                            "expected": expected_class,
                            "actual": actual_class,
                            "correct": False
                        })
                        all_success = False
                else:
                    self.log_test(f"Class Assignment - {student['username']}", False, 
                                f"Failed to register student: HTTP {response.status_code}")
                    all_success = False
            
            # Step 2: Test teacher dashboard filtering for each class
            print("\n🔍 Testing Teacher Dashboard Class Filtering...")
            
            for class_name in ["GR9-A", "GR9-B", "GR9-C", "GR9-D"]:
                response = self.session.get(f"{self.base_url}/teacher/students?class_filter={class_name}")
                
                if response.status_code == 200:
                    data = response.json()
                    students = data.get("students", [])
                    
                    # Check if filtering works correctly
                    expected_students = [s for s in test_students if s["class_name"] == class_name]
                    
                    if students:
                        # Verify all returned students belong to the filtered class
                        correct_class_filter = all(
                            student.get("class_name") == class_name 
                            for student in students 
                            if "class_name" in student
                        )
                        
                        if correct_class_filter:
                            self.log_test(f"Teacher Dashboard Filter - {class_name}", True, 
                                        f"✅ Correctly filtered {len(students)} students from {class_name}")
                        else:
                            self.log_test(f"Teacher Dashboard Filter - {class_name}", False, 
                                        f"❌ Filter returned students from wrong classes")
                            all_success = False
                    else:
                        # Empty result is OK if no students in that class
                        self.log_test(f"Teacher Dashboard Filter - {class_name}", True, 
                                    f"✅ No students in {class_name} (empty state)")
                else:
                    self.log_test(f"Teacher Dashboard Filter - {class_name}", False, 
                                f"HTTP {response.status_code}")
                    all_success = False
            
            # Summary of class assignment test
            if all_success:
                self.log_test("CRITICAL CLASS ASSIGNMENT BUG TEST", True, 
                            "✅ All students correctly saved with their selected classes")
            else:
                failed_assignments = [r for r in class_assignment_results if not r["correct"]]
                self.log_test("CRITICAL CLASS ASSIGNMENT BUG TEST", False, 
                            f"❌ CRITICAL BUG CONFIRMED: {len(failed_assignments)} students saved with wrong class")
                
                # Print detailed failure information
                print("\n❌ DETAILED CLASS ASSIGNMENT FAILURES:")
                for failure in failed_assignments:
                    print(f"   Student: {failure['username']}")
                    print(f"   Expected: {failure['expected']}")
                    print(f"   Actual: {failure['actual']}")
                    print()
            
            return all_success
            
        except Exception as e:
            self.log_test("CRITICAL CLASS ASSIGNMENT BUG TEST", False, f"Test execution error: {str(e)}")
            return False

    def test_student_login_with_class(self):
        """Test student login endpoint with class selection"""
        try:
            # Test with realistic student name and class selection
            test_classes = ["GR9-A", "GR9-B", "GR9-C", "GR9-D"]
            all_success = True
            
            for class_name in test_classes:
                student_data = {"username": f"student_{class_name.lower()}", "class_name": class_name}
                response = self.session.post(
                    f"{self.base_url}/auth/student-login",
                    json=student_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["username", "class_name", "created_at", "last_login", "total_points", "badges"]
                    
                    if all(field in data for field in required_fields):
                        if data["class_name"] == class_name:
                            self.log_test(f"Student Login with Class {class_name}", True, 
                                        f"Student '{data['username']}' logged in to class {class_name}")
                        else:
                            self.log_test(f"Student Login with Class {class_name}", False, 
                                        f"Expected class {class_name}, got {data.get('class_name')}")
                            all_success = False
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_test(f"Student Login with Class {class_name}", False, 
                                    f"Missing fields: {missing}", data)
                        all_success = False
                else:
                    self.log_test(f"Student Login with Class {class_name}", False, 
                                f"HTTP {response.status_code}", response.text)
                    all_success = False
            
            return all_success
                
        except Exception as e:
            self.log_test("Student Login with Class", False, f"Request error: {str(e)}")
            return False

    def test_student_login(self):
        """Test student login endpoint - legacy method"""
        try:
            # Test with realistic student name
            student_data = {"username": "sarah_ahmed"}
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=student_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["username", "created_at", "last_login", "total_points", "badges"]
                
                if all(field in data for field in required_fields):
                    self.log_test("Student Login", True, f"Student '{data['username']}' logged in successfully")
                    return True, data
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Student Login", False, f"Missing fields: {missing}", data)
                    return False, None
            else:
                self.log_test("Student Login", False, f"HTTP {response.status_code}", response.text)
                return False, None
                
        except Exception as e:
            self.log_test("Student Login", False, f"Request error: {str(e)}")
            return False, None

    def test_teacher_login(self):
        """Test teacher login with access code"""
        try:
            # Test with correct access code
            auth_data = {"access_code": "teacher2024"}
            response = self.session.post(
                f"{self.base_url}/auth/teacher-login",
                json=auth_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "role" in data and data["role"] == "teacher":
                    self.log_test("Teacher Login (Valid Code)", True, "Teacher authenticated successfully")
                    teacher_success = True
                else:
                    self.log_test("Teacher Login (Valid Code)", False, "Invalid response format", data)
                    teacher_success = False
            else:
                self.log_test("Teacher Login (Valid Code)", False, f"HTTP {response.status_code}", response.text)
                teacher_success = False
            
            # Test with invalid access code
            auth_data = {"access_code": "wrong_code"}
            response = self.session.post(
                f"{self.base_url}/auth/teacher-login",
                json=auth_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 401:
                self.log_test("Teacher Login (Invalid Code)", True, "Correctly rejected invalid access code")
                invalid_success = True
            else:
                self.log_test("Teacher Login (Invalid Code)", False, f"Should return 401, got {response.status_code}")
                invalid_success = False
                
            return teacher_success and invalid_success
            
        except Exception as e:
            self.log_test("Teacher Login", False, f"Request error: {str(e)}")
            return False

    def test_database_initialization(self):
        """Test that database is initialized with all 5 sections"""
        try:
            all_sections_working = True
            total_problems_found = 0
            
            for section_id, section_info in EXPECTED_SECTIONS.items():
                response = self.session.get(f"{self.base_url}/problems/section/{section_id}")
                
                if response.status_code == 200:
                    problems = response.json()
                    if isinstance(problems, list) and len(problems) == section_info["problems"]:
                        self.log_test(f"Database Init - {section_id}", True, 
                                    f"Found {len(problems)} problems for {section_info['title']}")
                        total_problems_found += len(problems)
                    else:
                        self.log_test(f"Database Init - {section_id}", False, 
                                    f"Expected {section_info['problems']} problems, got {len(problems) if isinstance(problems, list) else 0}")
                        all_sections_working = False
                else:
                    self.log_test(f"Database Init - {section_id}", False, 
                                f"HTTP {response.status_code}", response.text)
                    all_sections_working = False
            
            if all_sections_working:
                self.log_test("Database Initialization", True, 
                            f"All 5 sections initialized with {total_problems_found} total problems")
                return True
            else:
                self.log_test("Database Initialization", False, "Some sections missing or incomplete")
                return False
                
        except Exception as e:
            self.log_test("Database Initialization", False, f"Request error: {str(e)}")
            return False

    def test_student_progress(self, username="sarah_ahmed"):
        """Test student progress retrieval - updated for section1 only initially"""
        try:
            response = self.session.get(f"{self.base_url}/students/{username}/progress")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["progress", "total_points", "badges"]
                
                if all(field in data for field in required_fields):
                    progress = data["progress"]
                    if "section1" in progress:
                        section1 = progress["section1"]
                        expected_problems = ["prep1", "explanation1", "practice1", "practice2", "assessment1", "examprep1"]
                        
                        if all(problem in section1 for problem in expected_problems):
                            self.log_test("Student Progress", True, f"Retrieved progress for {len(section1)} problems")
                            return True, data
                        else:
                            missing = [p for p in expected_problems if p not in section1]
                            self.log_test("Student Progress", False, f"Missing problems: {missing}", data)
                            return False, None
                    else:
                        self.log_test("Student Progress", False, "Missing section1 in progress", data)
                        return False, None
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Student Progress", False, f"Missing fields: {missing}", data)
                    return False, None
            else:
                self.log_test("Student Progress", False, f"HTTP {response.status_code}", response.text)
                return False, None
                
        except Exception as e:
            self.log_test("Student Progress", False, f"Request error: {str(e)}")
            return False, None

    def test_all_sections_problems(self):
        """Test problem data fetching for all sections"""
        try:
            all_sections_success = True
            
            for section_id, section_info in EXPECTED_SECTIONS.items():
                # Test getting section problems
                response = self.session.get(f"{self.base_url}/problems/section/{section_id}")
                
                if response.status_code == 200:
                    problems = response.json()
                    if isinstance(problems, list) and len(problems) == section_info["problems"]:
                        self.log_test(f"Section Problems - {section_id}", True, 
                                    f"Retrieved {len(problems)} problems from {section_info['title']}")
                        
                        # Test getting individual problem from this section
                        if problems:
                            first_problem_id = problems[0]["id"]
                            response = self.session.get(f"{self.base_url}/problems/{first_problem_id}")
                            
                            if response.status_code == 200:
                                problem = response.json()
                                required_fields = ["id", "section_id", "type", "question_en", "answer"]
                                
                                if all(field in problem for field in required_fields):
                                    self.log_test(f"Individual Problem - {section_id}", True, 
                                                f"Retrieved problem '{problem['id']}' from {section_id}")
                                else:
                                    missing = [f for f in required_fields if f not in problem]
                                    self.log_test(f"Individual Problem - {section_id}", False, 
                                                f"Missing fields: {missing}", problem)
                                    all_sections_success = False
                            else:
                                self.log_test(f"Individual Problem - {section_id}", False, 
                                            f"HTTP {response.status_code}", response.text)
                                all_sections_success = False
                    else:
                        expected_count = section_info["problems"]
                        actual_count = len(problems) if isinstance(problems, list) else 0
                        self.log_test(f"Section Problems - {section_id}", False, 
                                    f"Expected {expected_count} problems, got {actual_count}", problems)
                        all_sections_success = False
                else:
                    self.log_test(f"Section Problems - {section_id}", False, 
                                f"HTTP {response.status_code}", response.text)
                    all_sections_success = False
                    
            return all_sections_success
            
        except Exception as e:
            self.log_test("All Sections Problems", False, f"Request error: {str(e)}")
            return False

    def test_problem_data_fetching(self):
        """Test problem data fetching endpoints - legacy method for section1"""
        try:
            # Test getting section problems
            response = self.session.get(f"{self.base_url}/problems/section/section1")
            
            if response.status_code == 200:
                problems = response.json()
                if isinstance(problems, list) and len(problems) > 0:
                    self.log_test("Section Problems", True, f"Retrieved {len(problems)} problems from section1")
                    section_success = True
                    
                    # Test getting individual problem
                    first_problem_id = problems[0]["id"]
                    response = self.session.get(f"{self.base_url}/problems/{first_problem_id}")
                    
                    if response.status_code == 200:
                        problem = response.json()
                        required_fields = ["id", "section_id", "type", "question_en", "answer"]
                        
                        if all(field in problem for field in required_fields):
                            self.log_test("Individual Problem", True, f"Retrieved problem '{problem['id']}'")
                            individual_success = True
                        else:
                            missing = [f for f in required_fields if f not in problem]
                            self.log_test("Individual Problem", False, f"Missing fields: {missing}", problem)
                            individual_success = False
                    else:
                        self.log_test("Individual Problem", False, f"HTTP {response.status_code}", response.text)
                        individual_success = False
                        
                else:
                    self.log_test("Section Problems", False, "Empty or invalid problems list", problems)
                    section_success = False
                    individual_success = False
            else:
                self.log_test("Section Problems", False, f"HTTP {response.status_code}", response.text)
                section_success = False
                individual_success = False
                
            return section_success and individual_success
            
        except Exception as e:
            self.log_test("Problem Data Fetching", False, f"Request error: {str(e)}")
            return False

    def test_answer_submission_all_types(self, username="sarah_ahmed"):
        """Test answer submission for different problem types across sections"""
        try:
            # Test cases for different sections and problem types
            test_cases = [
                # Section 1: One-Step Inequalities
                {"problem_id": "prep1", "correct_answer": "7", "section": "section1"},
                
                # Section 2: Two-Step Inequalities  
                {"problem_id": "prep2", "correct_answer": "x < 3", "section": "section2"},
                
                # Section 3: Multi-Step Inequalities
                {"problem_id": "prep3", "correct_answer": "x > 2", "section": "section3"},
                
                # Section 4: Variables on Both Sides
                {"problem_id": "prep4", "correct_answer": "x < 4", "section": "section4"},
                
                # Section 5: Compound Inequalities
                {"problem_id": "prep5", "correct_answer": "-2 < x ≤ 3", "section": "section5"}
            ]
            
            all_success = True
            
            for test_case in test_cases:
                # Test correct answer
                attempt_data = {
                    "problem_id": test_case["problem_id"],
                    "answer": test_case["correct_answer"],
                    "hints_used": 0
                }
                
                response = self.session.post(
                    f"{self.base_url}/students/{username}/attempt",
                    json=attempt_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["correct", "score", "attempts", "progress"]
                    
                    if all(field in data for field in required_fields):
                        if data["correct"] == True and data["score"] > 0:
                            self.log_test(f"Answer Submission - {test_case['problem_id']}", True, 
                                        f"Correct answer for {test_case['section']} scored {data['score']} points")
                        else:
                            self.log_test(f"Answer Submission - {test_case['problem_id']}", False, 
                                        f"Expected correct=True and score>0, got correct={data['correct']}, score={data['score']}")
                            all_success = False
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_test(f"Answer Submission - {test_case['problem_id']}", False, 
                                    f"Missing fields: {missing}", data)
                        all_success = False
                else:
                    self.log_test(f"Answer Submission - {test_case['problem_id']}", False, 
                                f"HTTP {response.status_code}", response.text)
                    all_success = False
            
            return all_success
            
        except Exception as e:
            self.log_test("Answer Submission All Types", False, f"Request error: {str(e)}")
            return False

    def test_answer_submission(self, username="sarah_ahmed"):
        """Test answer submission functionality - legacy method for section1"""
        try:
            # Test correct answer submission
            attempt_data = {
                "problem_id": "prep1",
                "answer": "7",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["correct", "score", "attempts", "progress"]
                
                if all(field in data for field in required_fields):
                    if data["correct"] == True and data["score"] > 0:
                        self.log_test("Answer Submission (Correct)", True, f"Correct answer scored {data['score']} points")
                        correct_success = True
                    else:
                        self.log_test("Answer Submission (Correct)", False, f"Expected correct=True and score>0, got correct={data['correct']}, score={data['score']}")
                        correct_success = False
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Answer Submission (Correct)", False, f"Missing fields: {missing}", data)
                    correct_success = False
            else:
                self.log_test("Answer Submission (Correct)", False, f"HTTP {response.status_code}", response.text)
                correct_success = False
            
            # Test incorrect answer submission
            attempt_data = {
                "problem_id": "prep1",
                "answer": "wrong_answer",
                "hints_used": 1
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data["correct"] == False:
                    self.log_test("Answer Submission (Incorrect)", True, "Incorrect answer properly handled")
                    incorrect_success = True
                else:
                    self.log_test("Answer Submission (Incorrect)", False, f"Expected correct=False, got {data['correct']}")
                    incorrect_success = False
            else:
                self.log_test("Answer Submission (Incorrect)", False, f"HTTP {response.status_code}", response.text)
                incorrect_success = False
                
            return correct_success and incorrect_success
            
        except Exception as e:
            self.log_test("Answer Submission", False, f"Request error: {str(e)}")
            return False

    def test_teacher_dashboard_class_filtering(self):
        """Test teacher dashboard with class filtering"""
        try:
            # Test without class filter
            response = self.session.get(f"{self.base_url}/teacher/students")
            
            if response.status_code != 200:
                self.log_test("Teacher Dashboard (No Filter)", False, f"HTTP {response.status_code}", response.text)
                return False
            
            all_students_data = response.json()
            
            # Test with specific class filters
            test_classes = ["GR9-A", "GR9-B", "GR9-C", "GR9-D"]
            all_success = True
            
            for class_name in test_classes:
                response = self.session.get(f"{self.base_url}/teacher/students?class_filter={class_name}")
                
                if response.status_code == 200:
                    data = response.json()
                    required_fields = ["total_students", "average_progress", "completed_problems", "average_score", "students"]
                    
                    if all(field in data for field in required_fields):
                        # Check if filtering is working (students should be from specified class only)
                        students = data.get("students", [])
                        
                        if students:
                            # Verify all students belong to the filtered class
                            class_match = all(student.get("class_name") == class_name for student in students if "class_name" in student)
                            if class_match:
                                self.log_test(f"Teacher Dashboard Class Filter {class_name}", True, 
                                            f"Filtered {len(students)} students from class {class_name}")
                            else:
                                self.log_test(f"Teacher Dashboard Class Filter {class_name}", False, 
                                            f"Some students don't belong to class {class_name}")
                                all_success = False
                        else:
                            self.log_test(f"Teacher Dashboard Class Filter {class_name}", True, 
                                        f"No students in class {class_name} (empty state)")
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_test(f"Teacher Dashboard Class Filter {class_name}", False, 
                                    f"Missing fields: {missing}", data)
                        all_success = False
                else:
                    self.log_test(f"Teacher Dashboard Class Filter {class_name}", False, 
                                f"HTTP {response.status_code}", response.text)
                    all_success = False
            
            return all_success
                
        except Exception as e:
            self.log_test("Teacher Dashboard Class Filtering", False, f"Request error: {str(e)}")
            return False

    def test_teacher_dashboard_expanded(self):
        """Test teacher dashboard endpoint with expanded content"""
        try:
            response = self.session.get(f"{self.base_url}/teacher/students")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total_students", "average_progress", "completed_problems", "average_score", "students"]
                
                if all(field in data for field in required_fields):
                    # Test that dashboard can handle students with progress across multiple sections
                    students = data.get("students", [])
                    
                    dashboard_success = True
                    if students:
                        # Check if student data includes proper structure
                        first_student = students[0]
                        student_required_fields = ["username", "progress_percentage", "completed_problems", "problems_status"]
                        
                        if all(field in first_student for field in student_required_fields):
                            self.log_test("Teacher Dashboard Expanded", True, 
                                        f"Dashboard shows {data['total_students']} students with expanded data structure")
                        else:
                            missing = [f for f in student_required_fields if f not in first_student]
                            self.log_test("Teacher Dashboard Expanded", False, 
                                        f"Student data missing fields: {missing}", first_student)
                            dashboard_success = False
                    else:
                        self.log_test("Teacher Dashboard Expanded", True, 
                                    f"Dashboard working with {data['total_students']} students (empty state)")
                    
                    return dashboard_success
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Teacher Dashboard Expanded", False, f"Missing fields: {missing}", data)
                    return False
            else:
                self.log_test("Teacher Dashboard Expanded", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Teacher Dashboard Expanded", False, f"Request error: {str(e)}")
            return False

    def test_teacher_dashboard(self):
        """Test teacher dashboard endpoint - legacy method"""
        try:
            response = self.session.get(f"{self.base_url}/teacher/students")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total_students", "average_progress", "completed_problems", "average_score", "students"]
                
                if all(field in data for field in required_fields):
                    self.log_test("Teacher Dashboard", True, f"Dashboard shows {data['total_students']} students")
                    return True
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Teacher Dashboard", False, f"Missing fields: {missing}", data)
                    return False
            else:
                self.log_test("Teacher Dashboard", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Teacher Dashboard", False, f"Request error: {str(e)}")
            return False

    def test_admin_stats_endpoint(self):
        """Test admin statistics endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/admin/stats")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["total_students", "total_progress_records", "total_problems", "total_sections", "database_status"]
                
                if all(field in data for field in required_fields):
                    # Verify expected data structure
                    if (data["total_sections"] == 5 and 
                        data["total_problems"] == 30 and 
                        data["database_status"] == "connected"):
                        self.log_test("Admin Stats Endpoint", True, 
                                    f"Database stats: {data['total_sections']} sections, {data['total_problems']} problems, {data['total_students']} students")
                        return True
                    else:
                        self.log_test("Admin Stats Endpoint", False, 
                                    f"Unexpected data: sections={data['total_sections']}, problems={data['total_problems']}, status={data['database_status']}")
                        return False
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Admin Stats Endpoint", False, f"Missing fields: {missing}", data)
                    return False
            else:
                self.log_test("Admin Stats Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Stats Endpoint", False, f"Request error: {str(e)}")
            return False

    def test_admin_clear_data_endpoint(self):
        """Test admin clear test data endpoint"""
        try:
            # Test with correct admin key (as query parameter)
            response = self.session.post(f"{self.base_url}/admin/clear-test-data?admin_key=admin123")
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["message", "students_deleted", "progress_deleted"]
                
                if all(field in data for field in required_fields):
                    self.log_test("Admin Clear Data (Valid Key)", True, 
                                f"Cleared {data['students_deleted']} students and {data['progress_deleted']} progress records")
                    valid_success = True
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("Admin Clear Data (Valid Key)", False, f"Missing fields: {missing}", data)
                    valid_success = False
            else:
                self.log_test("Admin Clear Data (Valid Key)", False, f"HTTP {response.status_code}", response.text)
                valid_success = False
            
            # Test with invalid admin key (as query parameter)
            response = self.session.post(f"{self.base_url}/admin/clear-test-data?admin_key=wrong_key")
            
            if response.status_code == 403:
                self.log_test("Admin Clear Data (Invalid Key)", True, "Correctly rejected invalid admin key")
                invalid_success = True
            else:
                self.log_test("Admin Clear Data (Invalid Key)", False, f"Should return 403, got {response.status_code}")
                invalid_success = False
                
            return valid_success and invalid_success
                
        except Exception as e:
            self.log_test("Admin Clear Data Endpoint", False, f"Request error: {str(e)}")
            return False

    def test_section1_preparation_problem_specific(self):
        """SPECIFIC TEST: Section 1 preparation problem as requested in review"""
        try:
            print("\n🎯 SPECIFIC SECTION 1 PREPARATION PROBLEM TEST")
            print("Testing GET /api/problems/section/section1 and verifying prep1 problem data...")
            
            # Step 1: Test GET /api/problems/section/section1
            response = self.session.get(f"{self.base_url}/problems/section/section1")
            
            if response.status_code != 200:
                self.log_test("Section 1 Problems Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            problems = response.json()
            
            if not isinstance(problems, list) or len(problems) == 0:
                self.log_test("Section 1 Problems Endpoint", False, 
                            f"Expected list of problems, got: {type(problems)} with {len(problems) if isinstance(problems, list) else 0} items")
                return False
            
            self.log_test("Section 1 Problems Endpoint", True, 
                        f"✅ Retrieved {len(problems)} problems from section1")
            
            # Step 2: Find and verify the first problem has type 'preparation' and id 'prep1'
            first_problem = problems[0]
            
            if first_problem.get("id") != "prep1":
                self.log_test("First Problem ID Check", False, 
                            f"Expected first problem id 'prep1', got '{first_problem.get('id')}'")
                return False
            
            if first_problem.get("type") != "preparation":
                self.log_test("First Problem Type Check", False, 
                            f"Expected first problem type 'preparation', got '{first_problem.get('type')}'")
                return False
            
            self.log_test("First Problem Verification", True, 
                        f"✅ First problem has id 'prep1' and type 'preparation'")
            
            # Step 3: Verify the preparation problem data
            expected_data = {
                "id": "prep1",
                "type": "preparation",
                "question_en": "x - 5 > 10",
                "answer": "x > 15"
            }
            
            verification_success = True
            for key, expected_value in expected_data.items():
                actual_value = first_problem.get(key)
                if actual_value != expected_value:
                    self.log_test(f"Prep1 Data Verification - {key}", False, 
                                f"Expected '{expected_value}', got '{actual_value}'")
                    verification_success = False
                else:
                    self.log_test(f"Prep1 Data Verification - {key}", True, 
                                f"✅ {key}: '{actual_value}'")
            
            if not verification_success:
                return False
            
            # Step 4: Test accessing specific problem GET /api/problems/prep1
            response = self.session.get(f"{self.base_url}/problems/prep1")
            
            if response.status_code == 200:
                problem = response.json()
                
                # Verify the individual problem endpoint returns same data
                individual_verification_success = True
                for key, expected_value in expected_data.items():
                    actual_value = problem.get(key)
                    if actual_value != expected_value:
                        self.log_test(f"Individual Problem Verification - {key}", False, 
                                    f"Expected '{expected_value}', got '{actual_value}'")
                        individual_verification_success = False
                
                if individual_verification_success:
                    self.log_test("Individual Problem Endpoint", True, 
                                "✅ GET /api/problems/prep1 returns correct data")
                else:
                    self.log_test("Individual Problem Endpoint", False, 
                                "❌ Individual problem data doesn't match expected values")
                    return False
            else:
                self.log_test("Individual Problem Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            # Step 5: Test answer submission for this specific problem
            print("\n   Testing answer submission for prep1...")
            
            # Create test student for this specific test
            test_student = {"username": "section1_prep_test", "class_name": "GR9-A"}
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Test Student Creation for Prep1", False, 
                            f"Failed to create test student: HTTP {response.status_code}")
                return False
            
            # Test correct answer submission
            attempt_data = {
                "problem_id": "prep1",
                "answer": "x > 15",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/section1_prep_test/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("correct") == True and data.get("score", 0) > 0:
                    self.log_test("Prep1 Answer Submission", True, 
                                f"✅ Correct answer 'x > 15' scored {data.get('score')} points")
                else:
                    self.log_test("Prep1 Answer Submission", False, 
                                f"Expected correct=True and score>0, got correct={data.get('correct')}, score={data.get('score')}")
                    return False
            else:
                self.log_test("Prep1 Answer Submission", False, 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            # Final success
            self.log_test("SECTION 1 PREPARATION PROBLEM COMPREHENSIVE TEST", True, 
                        "✅ All Section 1 prep1 tests PASSED - Backend serving correct data")
            
            return True
            
        except Exception as e:
            self.log_test("Section 1 Preparation Problem Test", False, f"Test execution error: {str(e)}")
            return False

    def test_admin_clear_all_data_endpoint(self):
        """Test new admin clear-all-data endpoint as requested in review"""
        try:
            print("\n🔍 TESTING NEW ADMIN CLEAR-ALL-DATA ENDPOINT")
            print("Testing DELETE /api/admin/clear-all-data endpoint...")
            
            # Step 1: Create some test data first to verify clearing works
            test_student = {"username": "clear_test_student", "class_name": "GR9-A"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Admin Clear All Data - Test Data Setup", False, 
                            f"Failed to create test student: HTTP {response.status_code}")
                return False
            
            self.log_test("Admin Clear All Data - Test Data Setup", True, 
                        "✅ Created test student for clearing verification")
            
            # Step 2: Submit some progress to create progress records
            attempt_data = {
                "problem_id": "prep1",
                "answer": "7",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/clear_test_student/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                self.log_test("Admin Clear All Data - Progress Setup", True, 
                            "✅ Created test progress record")
            else:
                self.log_test("Admin Clear All Data - Progress Setup", False, 
                            f"Failed to create progress: HTTP {response.status_code}")
                # Continue anyway - we still have student data to clear
            
            # Step 3: Test the new DELETE /api/admin/clear-all-data endpoint
            response = self.session.delete(f"{self.base_url}/admin/clear-all-data")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for success message
                if "message" in data and "cleared" in data["message"].lower():
                    self.log_test("Admin Clear All Data - DELETE Request", True, 
                                f"✅ Status 200 response with success message: {data['message']}")
                    delete_success = True
                else:
                    self.log_test("Admin Clear All Data - DELETE Request", False, 
                                f"Missing or invalid success message in response: {data}")
                    delete_success = False
            else:
                self.log_test("Admin Clear All Data - DELETE Request", False, 
                            f"Expected status 200, got {response.status_code}: {response.text}")
                delete_success = False
            
            # Step 4: Verify data is actually cleared by checking admin stats
            response = self.session.get(f"{self.base_url}/admin/stats")
            
            if response.status_code == 200:
                stats = response.json()
                
                students_count = stats.get("total_students", -1)
                progress_count = stats.get("total_progress_records", -1)
                
                if students_count == 0 and progress_count == 0:
                    self.log_test("Admin Clear All Data - Verification", True, 
                                "✅ Database collections emptied - 0 students, 0 progress records")
                    verification_success = True
                else:
                    self.log_test("Admin Clear All Data - Verification", False, 
                                f"❌ Data not fully cleared - {students_count} students, {progress_count} progress records remain")
                    verification_success = False
            else:
                self.log_test("Admin Clear All Data - Verification", False, 
                            f"Failed to verify clearing: HTTP {response.status_code}")
                verification_success = False
            
            # Final result
            overall_success = delete_success and verification_success
            
            if overall_success:
                self.log_test("ADMIN CLEAR ALL DATA ENDPOINT TEST", True, 
                            "✅ NEW ENDPOINT WORKING: DELETE /api/admin/clear-all-data successfully clears all student data")
            else:
                self.log_test("ADMIN CLEAR ALL DATA ENDPOINT TEST", False, 
                            "❌ NEW ENDPOINT ISSUES: Clear-all-data endpoint not working properly")
            
            return overall_success
                
        except Exception as e:
            self.log_test("Admin Clear All Data Endpoint", False, f"Request error: {str(e)}")
            return False

    def test_data_persistence(self):
        """Test data persistence across sessions"""
        try:
            # Create a student with progress
            username = "persistence_test_student"
            class_name = "GR9-A"
            
            # Step 1: Login student
            student_data = {"username": username, "class_name": class_name}
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=student_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Data Persistence - Student Creation", False, f"HTTP {response.status_code}")
                return False
            
            # Step 2: Submit an answer to create progress
            attempt_data = {
                "problem_id": "prep1",
                "answer": "7",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Data Persistence - Progress Creation", False, f"HTTP {response.status_code}")
                return False
            
            # Step 3: Retrieve progress to verify it was saved
            response = self.session.get(f"{self.base_url}/students/{username}/progress")
            
            if response.status_code == 200:
                data = response.json()
                if ("progress" in data and 
                    "section1" in data["progress"] and 
                    "prep1" in data["progress"]["section1"] and
                    data["progress"]["section1"]["prep1"]["completed"] == True):
                    self.log_test("Data Persistence", True, 
                                f"Student progress persisted correctly for {username}")
                    return True
                else:
                    self.log_test("Data Persistence", False, 
                                "Progress not found or incomplete", data)
                    return False
            else:
                self.log_test("Data Persistence", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Data Persistence", False, f"Request error: {str(e)}")
            return False

    def test_cors_configuration(self):
        """Test CORS configuration"""
        try:
            # Make a request with Origin header to trigger CORS
            headers = {"Origin": "https://example.com"}
            response = self.session.get(f"{self.base_url}/", headers=headers)
            
            cors_headers = [
                "Access-Control-Allow-Origin",
                "Access-Control-Allow-Credentials"
            ]
            
            present_headers = [h for h in cors_headers if h in response.headers]
            
            if len(present_headers) >= 1:  # At least one CORS header should be present
                origin_header = response.headers.get("Access-Control-Allow-Origin")
                self.log_test("CORS Configuration", True, f"CORS working - Allow-Origin: {origin_header}")
                return True
            else:
                self.log_test("CORS Configuration", False, "No CORS headers found in response")
                return False
                
        except Exception as e:
            self.log_test("CORS Configuration", False, f"Request error: {str(e)}")
            return False

    def run_infinite_recursion_bug_tests(self):
        """Run critical infinite recursion bug fix tests as requested in review"""
        print("=" * 80)
        print("CRITICAL PHASE 1 VERIFICATION: Infinite Recursion Bug Fix Testing")
        print("=" * 80)
        print(f"Testing backend at: {self.base_url}")
        print("Focus: Answer validation system after fixing infinite recursion bug")
        print()
        
        # Critical tests for infinite recursion bug fix
        critical_tests = [
            # PRIORITY 1: Infinite Recursion Bug Fix (CRITICAL)
            ("🚨 CRITICAL: Infinite Recursion Bug Fix Test", self.test_infinite_recursion_bug_fix_critical),
            
            # PRIORITY 2: Supporting Backend Tests
            ("Health Check", self.test_health_check),
            ("Student Login with Class Selection", self.test_student_login_with_class),
            ("Teacher Login", self.test_teacher_login),
        ]
        
        passed = 0
        total = len(critical_tests)
        
        for test_name, test_func in critical_tests:
            try:
                result = test_func()
                if result:
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test execution error: {str(e)}")
        
        print("=" * 80)
        print("INFINITE RECURSION BUG FIX TESTS SUMMARY")
        print("=" * 80)
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 ALL CRITICAL TESTS PASSED!")
            print("✅ Infinite recursion bug is FIXED")
            print("✅ Answer validation system working correctly")
            print("✅ Both '7' and 'x=7' formats work for preparation problems")
            print("✅ Progress tracking works after correct answers")
        else:
            print(f"\n⚠️  {total - passed} critical tests failed")
            print("❌ Infinite recursion bug or answer validation issues detected")
        
        return passed, total, self.test_results

    def run_section1_preparation_tests(self):
        """Run specific Section 1 preparation problem tests as requested in review"""
        print("=" * 80)
        print("SECTION 1 PREPARATION PROBLEM BACKEND TESTING")
        print("=" * 80)
        print(f"Testing backend at: {self.base_url}")
        print("Focus: Section 1 preparation problem (prep1) verification")
        print("Request: Test GET /api/problems/section/section1 and verify prep1 data")
        print()
        
        # Specific tests for Section 1 preparation problem
        section1_tests = [
            # PRIORITY 1: Health check first
            ("Health Check", self.test_health_check),
            
            # PRIORITY 2: Section 1 preparation problem specific test
            ("🎯 Section 1 Preparation Problem Test", self.test_section1_preparation_problem_specific),
            
            # PRIORITY 3: Supporting backend tests
            ("Database Initialization", self.test_database_initialization),
            ("Student Login", self.test_student_login_with_class),
        ]
        
        passed = 0
        total = len(section1_tests)
        
        for test_name, test_func in section1_tests:
            try:
                result = test_func()
                if result:
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test execution error: {str(e)}")
        
        print("=" * 80)
        print("SECTION 1 PREPARATION TESTS SUMMARY")
        print("=" * 80)
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 ALL SECTION 1 PREPARATION TESTS PASSED!")
            print("✅ Backend serving correct Section 1 preparation problem data")
            print("✅ First problem has type 'preparation' and id 'prep1'")
            print("✅ Problem data: id='prep1', type='preparation', question_en='x - 5 > 10', answer='x > 15'")
            print("✅ Individual problem endpoint working")
            print("✅ Answer submission functional")
        else:
            print(f"\n⚠️  {total - passed} Section 1 tests failed")
            print("❌ Backend issues detected with Section 1 preparation problem")
        
        return passed, total, self.test_results

    def run_critical_mobile_tests(self):
        """Run critical mobile optimization tests as requested"""
        print("=" * 80)
        print("CRITICAL MOBILE OPTIMIZATION BACKEND TESTING")
        print("=" * 80)
        print(f"Testing backend at: {self.base_url}")
        print("Focus: Class Assignment Bug and Mobile Backend Features")
        print()
        
        # Critical tests for mobile optimization bugs
        critical_tests = [
            # PRIORITY 1: Class Assignment Bug (CRITICAL)
            ("🚨 CRITICAL: Class Assignment Bug Test", self.test_class_assignment_bug_critical),
            
            # PRIORITY 2: Backend API Endpoints for Mobile Features
            ("Health Check", self.test_health_check),
            ("Database Initialization (5 Sections)", self.test_database_initialization),
            ("Student Login with Class Selection", self.test_student_login_with_class),
            ("Teacher Dashboard Class Filtering", self.test_teacher_dashboard_class_filtering),
            ("Admin Stats Endpoint", self.test_admin_stats_endpoint),
        ]
        
        passed = 0
        total = len(critical_tests)
        
        for test_name, test_func in critical_tests:
            try:
                result = test_func()
                if result:
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test execution error: {str(e)}")
        
        print("=" * 80)
        print("CRITICAL MOBILE TESTS SUMMARY")
        print("=" * 80)
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 ALL CRITICAL MOBILE TESTS PASSED!")
            print("✅ Class assignment bug is FIXED")
        else:
            print(f"\n⚠️  {total - passed} critical tests failed")
            print("❌ Class assignment bug or other critical issues detected")
        
        return passed, total, self.test_results

    def run_all_tests(self):
        """Run all API tests - comprehensive MVP testing"""
        print("=" * 80)
        print("MATH TUTORING API TEST SUITE - COMPREHENSIVE MVP TESTING")
        print("=" * 80)
        print(f"Testing backend at: {self.base_url}")
        print(f"Expected: 5 sections with 30 total problems (6 per section)")
        print(f"Testing: Class management, Admin endpoints, Data persistence")
        print()
        
        # Run tests in logical order - prioritizing comprehensive MVP tests
        tests = [
            # PART 1: Core API Health
            ("Health Check", self.test_health_check),
            ("Database Initialization (5 Sections)", self.test_database_initialization),
            
            # PART 2: Authentication with Class Management
            ("Student Login with Class Selection", self.test_student_login_with_class),
            ("Teacher Login", self.test_teacher_login),
            
            # PART 3: Content and Progress
            ("Student Progress", self.test_student_progress),
            ("All Sections Problems", self.test_all_sections_problems),
            ("Answer Submission All Types", self.test_answer_submission_all_types),
            
            # PART 4: Class Management Features
            ("Teacher Dashboard Class Filtering", self.test_teacher_dashboard_class_filtering),
            ("Teacher Dashboard Expanded", self.test_teacher_dashboard_expanded),
            
            # PART 5: Admin and Data Verification
            ("Admin Stats Endpoint", self.test_admin_stats_endpoint),
            ("Admin Clear Data Endpoint", self.test_admin_clear_data_endpoint),
            ("Data Persistence", self.test_data_persistence),
            
            # PART 6: Infrastructure
            ("CORS Configuration", self.test_cors_configuration),
            
            # Legacy tests for backward compatibility
            ("Student Login (Legacy)", self.test_student_login),
            ("Problem Data Fetching (Legacy)", self.test_problem_data_fetching),
            ("Answer Submission (Legacy)", self.test_answer_submission),
            ("Teacher Dashboard (Legacy)", self.test_teacher_dashboard)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    passed += 1
            except Exception as e:
                self.log_test(test_name, False, f"Test execution error: {str(e)}")
        
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED - Expanded Math Tutoring API is production ready!")
            print("✅ All 5 sections with 30 problems are working correctly")
        else:
            print(f"\n⚠️  {total - passed} tests failed - API needs attention")
            print("❌ Some sections or functionality may not be working properly")
        
        return passed, total, self.test_results

def main():
    """Main test execution - focused on Section 1 preparation problem as requested"""
    print("🚀 MATH TUTORING API BACKEND TESTING")
    print("📋 FOCUS: Section 1 Preparation Problem Verification")
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print()
    
    tester = MathTutoringAPITester(BACKEND_URL)
    
    # Run Section 1 preparation problem tests as requested in review
    passed, total, results = tester.run_section1_preparation_tests()
    
    # Save detailed results
    with open("/app/test_results_section1_prep.json", "w") as f:
        json.dump({
            "summary": {"passed": passed, "total": total, "success_rate": passed/total},
            "results": results,
            "backend_url": BACKEND_URL,
            "test_timestamp": datetime.now().isoformat(),
            "test_focus": "section1_preparation_problem"
        }, f, indent=2)
    
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS")
    print("=" * 80)
    
    if passed == total:
        print("🎉 SUCCESS: All Section 1 preparation problem tests PASSED!")
        print("✅ Backend is serving correct data for Section 1 preparation stage")
        print("✅ Frontend input field issues are likely frontend-specific, not backend")
        return 0
    else:
        print(f"❌ FAILURE: {total - passed}/{total} tests failed")
        print("🔍 Backend issues detected that may be causing frontend problems")
        
        # Print failed tests
        failed_tests = [r for r in results if not r["success"]]
        if failed_tests:
            print("\n📋 FAILED TESTS:")
            for test in failed_tests:
                print(f"   ❌ {test['test']}: {test['details']}")
        
        return 1

if __name__ == "__main__":
    main()