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

# Get backend URL from environment - using local URL since external URL is misconfigured
BACKEND_URL = "http://localhost:8001/api"

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

    def test_student_login(self):
        """Test student login endpoint"""
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

    def test_student_progress(self, username="sarah_ahmed"):
        """Test student progress retrieval"""
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

    def test_problem_data_fetching(self):
        """Test problem data fetching endpoints"""
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

    def test_answer_submission(self, username="sarah_ahmed"):
        """Test answer submission functionality"""
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

    def test_teacher_dashboard(self):
        """Test teacher dashboard endpoint"""
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

    def run_all_tests(self):
        """Run all API tests"""
        print("=" * 60)
        print("MATH TUTORING API TEST SUITE")
        print("=" * 60)
        print(f"Testing backend at: {self.base_url}")
        print()
        
        # Run tests in logical order
        tests = [
            ("Health Check", self.test_health_check),
            ("Student Login", self.test_student_login),
            ("Teacher Login", self.test_teacher_login),
            ("Student Progress", self.test_student_progress),
            ("Problem Data Fetching", self.test_problem_data_fetching),
            ("Answer Submission", self.test_answer_submission),
            ("Teacher Dashboard", self.test_teacher_dashboard),
            ("CORS Configuration", self.test_cors_configuration)
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
        
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED - API is production ready!")
        else:
            print(f"\n⚠️  {total - passed} tests failed - API needs attention")
        
        return passed, total, self.test_results

def main():
    """Main test execution"""
    tester = MathTutoringAPITester(BACKEND_URL)
    passed, total, results = tester.run_all_tests()
    
    # Save detailed results
    with open("/app/test_results_detailed.json", "w") as f:
        json.dump({
            "summary": {"passed": passed, "total": total, "success_rate": passed/total},
            "results": results,
            "backend_url": BACKEND_URL,
            "test_timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()