#!/usr/bin/env python3
"""
Priority Backend Tests - Final Verification Post-Bug Fixes
Focus on the specific tests requested in the review
"""

import requests
import json
import sys
from datetime import datetime

BACKEND_URL = "https://fahhemni-backend.onrender.com/api"

class PriorityTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def log_result(self, test_name, success, details=""):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   {details}")
        print()

    def test_student_registration_gr9c(self):
        """Priority Test 1: Student registration with class GR9-C"""
        try:
            print("🔍 PRIORITY TEST 1: Student Registration with Class GR9-C")
            
            student_data = {"username": "final_verify_student", "class_name": "GR9-C"}
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=student_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                actual_class = data.get("class_name")
                
                if actual_class == "GR9-C":
                    self.log_result("Student Registration GR9-C", True, 
                                  f"✅ Student correctly saved with class GR9-C (not defaulting to GR9-A)")
                    return True
                else:
                    self.log_result("Student Registration GR9-C", False, 
                                  f"❌ CRITICAL BUG: Expected GR9-C, but saved as {actual_class}")
                    return False
            else:
                self.log_result("Student Registration GR9-C", False, 
                              f"Registration failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Student Registration GR9-C", False, f"Error: {str(e)}")
            return False

    def test_problem_retrieval_section1(self):
        """Priority Test 2: Problem retrieval for section 1"""
        try:
            print("🔍 PRIORITY TEST 2: Problem Retrieval for Section 1")
            
            response = self.session.get(f"{self.base_url}/problems/section/section1")
            
            if response.status_code == 200:
                problems = response.json()
                if isinstance(problems, list) and len(problems) > 0:
                    self.log_result("Problem Retrieval Section 1", True, 
                                  f"✅ Retrieved {len(problems)} problems from section 1")
                    return True
                else:
                    self.log_result("Problem Retrieval Section 1", False, 
                                  f"❌ No problems found or invalid response")
                    return False
            else:
                self.log_result("Problem Retrieval Section 1", False, 
                              f"❌ HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Problem Retrieval Section 1", False, f"Error: {str(e)}")
            return False

    def test_answer_submission(self):
        """Priority Test 3: Answer submission"""
        try:
            print("🔍 PRIORITY TEST 3: Answer Submission")
            
            # Use the student we just created
            username = "final_verify_student"
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
                if data.get("correct") == True and data.get("score", 0) > 0:
                    self.log_result("Answer Submission", True, 
                                  f"✅ Correct answer scored {data['score']} points")
                    return True
                else:
                    self.log_result("Answer Submission", False, 
                                  f"❌ Expected correct=True and score>0, got correct={data.get('correct')}, score={data.get('score')}")
                    return False
            else:
                self.log_result("Answer Submission", False, 
                              f"❌ HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Answer Submission", False, f"Error: {str(e)}")
            return False

    def test_teacher_login(self):
        """Priority Test 4: Teacher login verification"""
        try:
            print("🔍 PRIORITY TEST 4: Teacher Login Verification")
            
            auth_data = {"access_code": "teacher2024"}
            response = self.session.post(
                f"{self.base_url}/auth/teacher-login",
                json=auth_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("role") == "teacher":
                    self.log_result("Teacher Login", True, 
                                  "✅ Teacher login with 'teacher2024' working correctly")
                    return True
                else:
                    self.log_result("Teacher Login", False, 
                                  f"❌ Invalid response: {data}")
                    return False
            else:
                self.log_result("Teacher Login", False, 
                              f"❌ HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Teacher Login", False, f"Error: {str(e)}")
            return False

    def test_database_integrity(self):
        """Priority Test 5: Database integrity - sections and problems count"""
        try:
            print("🔍 PRIORITY TEST 5: Database Integrity Check")
            
            response = self.session.get(f"{self.base_url}/admin/stats")
            
            if response.status_code == 200:
                data = response.json()
                sections = data.get("total_sections", 0)
                problems = data.get("total_problems", 0)
                
                # Check if we have the expected structure
                if sections >= 5 and problems >= 30:
                    self.log_result("Database Integrity", True, 
                                  f"✅ Database has {sections} sections and {problems} problems (≥5 sections, ≥30 problems)")
                    return True
                else:
                    self.log_result("Database Integrity", False, 
                                  f"❌ Expected ≥5 sections and ≥30 problems, got {sections} sections and {problems} problems")
                    return False
            else:
                self.log_result("Database Integrity", False, 
                              f"❌ Admin stats endpoint failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Database Integrity", False, f"Error: {str(e)}")
            return False

    def run_priority_tests(self):
        """Run all priority tests as requested in review"""
        print("=" * 80)
        print("FINAL VERIFICATION - PRIORITY BACKEND TESTS POST-BUG FIXES")
        print("=" * 80)
        print(f"Backend URL: {self.base_url}")
        print("Focus: Ensure critical bug fixes didn't break backend functionality")
        print()
        
        tests = [
            ("Student Registration with GR9-C", self.test_student_registration_gr9c),
            ("Problem Retrieval Section 1", self.test_problem_retrieval_section1),
            ("Answer Submission", self.test_answer_submission),
            ("Teacher Login Verification", self.test_teacher_login),
            ("Database Integrity Check", self.test_database_integrity),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    passed += 1
            except Exception as e:
                self.log_result(test_name, False, f"Test execution error: {str(e)}")
        
        print("=" * 80)
        print("PRIORITY TESTS SUMMARY")
        print("=" * 80)
        print(f"Passed: {passed}/{total}")
        print(f"Failed: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 ALL PRIORITY TESTS PASSED!")
            print("✅ Critical bug fixes didn't break backend functionality")
        else:
            print(f"\n⚠️  {total - passed} priority tests failed")
            print("❌ Some backend functionality may be broken")
        
        return passed, total, self.results

def main():
    tester = PriorityTester(BACKEND_URL)
    passed, total, results = tester.run_priority_tests()
    
    # Save results
    with open("/app/priority_test_results.json", "w") as f:
        json.dump({
            "summary": {"passed": passed, "total": total, "success_rate": passed/total},
            "results": results,
            "backend_url": BACKEND_URL,
            "test_timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()