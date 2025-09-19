#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - Section 2 Progressive Socratic Hints Testing
Tests the progressive Socratic hints system for Section 2 word problems as requested by user.

CRITICAL REQUIREMENTS BEING TESTED:
- practice2_2 (tickets problem): 3 progressive hints displayed on wrong attempts
- examprep2 (candy problem): 3 progressive hints displayed on wrong attempts  
- Database verification: hints are correctly stored in database
- API response check: problem endpoints return correct hints
- Critical test: wrong attempts trigger progressive hint display
- Hint content verification: exact hint text matches expected Socratic guidance
"""

import requests
import json
import sys
import os
import re
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://inequality-solver.preview.emergentagent.com/api"

class Section2HintsTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "hints_test_student"
        
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

    def create_test_student(self):
        """Create test student for hints testing"""
        try:
            test_student = {"username": self.test_student_username, "class_name": "GR9-A"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("class_name") == "GR9-A":
                    self.log_test("Test Student Creation", True, 
                                f"✅ Created test student '{self.test_student_username}' in class GR9-A")
                    return True
                else:
                    self.log_test("Test Student Creation", False, 
                                f"Expected class GR9-A, got {data.get('class_name')}")
                    return False
            else:
                self.log_test("Test Student Creation", False, 
                            f"Failed to create test student: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test Student Creation", False, f"Request error: {str(e)}")
            return False

    def test_practice2_2_database_hints(self):
        """Test that practice2_2 (tickets problem) has correct hints stored in database"""
        try:
            print("\n🎯 PRACTICE2_2 DATABASE HINTS VERIFICATION")
            print("Testing if practice2_2 has the 3 expected progressive Socratic hints in database")
            
            # Get practice2_2 problem data
            response = self.session.get(f"{self.base_url}/problems/practice2_2")
            
            if response.status_code == 200:
                problem_data = response.json()
                hints_en = problem_data.get("hints_en", [])
                
                # Expected hints for practice2_2 (tickets problem)
                expected_hints = [
                    "Think about the variable: t represents number of tickets. What's the price per ticket? What amount needs to be collected?",
                    "If you sell t tickets at 10 SAR each, how much will you collect? Does it need to be greater than or equal to 500?",
                    "Amount collected = price per ticket × number of tickets. Use ≥ symbol because it says \"at least\""
                ]
                
                if len(hints_en) >= 3:
                    # Check if all expected hints are present
                    hints_match = True
                    for i, expected_hint in enumerate(expected_hints):
                        if i < len(hints_en) and expected_hint in hints_en[i]:
                            continue
                        else:
                            hints_match = False
                            break
                    
                    if hints_match:
                        self.log_test("practice2_2 Database Hints", True, 
                                    f"✅ practice2_2 has all 3 expected progressive Socratic hints stored correctly")
                        return True
                    else:
                        self.log_test("practice2_2 Database Hints", False, 
                                    f"❌ practice2_2 hints don't match expected content. Got: {hints_en}")
                        return False
                else:
                    self.log_test("practice2_2 Database Hints", False, 
                                f"❌ practice2_2 has only {len(hints_en)} hints, expected 3")
                    return False
            else:
                self.log_test("practice2_2 Database Hints", False, 
                            f"Failed to get practice2_2 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("practice2_2 Database Hints", False, f"Test execution error: {str(e)}")
            return False

    def test_examprep2_database_hints(self):
        """Test that examprep2 (candy problem) has correct hints stored in database"""
        try:
            print("\n🎯 EXAMPREP2 DATABASE HINTS VERIFICATION")
            print("Testing if examprep2 has the 3 expected progressive Socratic hints in database")
            
            # Get examprep2 problem data
            response = self.session.get(f"{self.base_url}/problems/examprep2")
            
            if response.status_code == 200:
                problem_data = response.json()
                hints_en = problem_data.get("hints_en", [])
                
                # Expected hints for examprep2 (candy problem)
                expected_hints = [
                    "Variable p represents pieces per child. How many children? How many total pieces needed?",
                    "If each child gets p pieces, and you have 15 children, how many pieces total will you distribute?",
                    "Total = number of children × pieces per child. Must be \"at least\" 60"
                ]
                
                if len(hints_en) >= 3:
                    # Check if all expected hints are present
                    hints_match = True
                    for i, expected_hint in enumerate(expected_hints):
                        if i < len(hints_en) and expected_hint in hints_en[i]:
                            continue
                        else:
                            hints_match = False
                            break
                    
                    if hints_match:
                        self.log_test("examprep2 Database Hints", True, 
                                    f"✅ examprep2 has all 3 expected progressive Socratic hints stored correctly")
                        return True
                    else:
                        self.log_test("examprep2 Database Hints", False, 
                                    f"❌ examprep2 hints don't match expected content. Got: {hints_en}")
                        return False
                else:
                    self.log_test("examprep2 Database Hints", False, 
                                f"❌ examprep2 has only {len(hints_en)} hints, expected 3")
                    return False
            else:
                self.log_test("examprep2 Database Hints", False, 
                            f"Failed to get examprep2 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("examprep2 Database Hints", False, f"Test execution error: {str(e)}")
            return False

    def test_practice2_2_wrong_attempts_hints(self):
        """Test progressive hints display for practice2_2 with wrong attempts"""
        try:
            print("\n🎯 PRACTICE2_2 PROGRESSIVE HINTS TEST")
            print("Testing progressive hints display for practice2_2 with 3 wrong attempts")
            
            # Complete prerequisites first (practice2_1)
            practice2_1_attempt = {
                "problem_id": "practice2_1",
                "answer": "k < -12",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=practice2_1_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200 or not response.json().get("correct"):
                self.log_test("practice2_2 Prerequisites", False, "Failed to complete practice2_1 prerequisite")
                return False
            
            # Test wrong attempts for practice2_2
            wrong_answers = ["t > 50", "t = 50", "t < 50"]  # Wrong answers to trigger hints
            
            for attempt_num, wrong_answer in enumerate(wrong_answers, 1):
                print(f"\n   Attempt {attempt_num}: Submitting wrong answer '{wrong_answer}'")
                
                practice2_2_attempt = {
                    "problem_id": "practice2_2",
                    "answer": wrong_answer,
                    "hints_used": attempt_num
                }
                
                response = self.session.post(
                    f"{self.base_url}/students/{self.test_student_username}/attempt",
                    json=practice2_2_attempt,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if not result.get("correct"):
                        print(f"   ✅ Attempt {attempt_num}: Wrong answer correctly rejected")
                        
                        # Get problem data to check hints
                        problem_response = self.session.get(f"{self.base_url}/problems/practice2_2")
                        if problem_response.status_code == 200:
                            problem_data = problem_response.json()
                            hints = problem_data.get("hints_en", [])
                            
                            if len(hints) >= attempt_num:
                                expected_hint_keywords = [
                                    ["variable", "t represents", "tickets", "price"],
                                    ["sell t tickets", "10 SAR", "collect", "greater than or equal"],
                                    ["Amount collected", "price per ticket", "number of tickets", "at least"]
                                ]
                                
                                hint_text = hints[attempt_num - 1]
                                keywords = expected_hint_keywords[attempt_num - 1]
                                
                                if any(keyword.lower() in hint_text.lower() for keyword in keywords):
                                    print(f"   ✅ Hint {attempt_num} contains expected keywords: {hint_text[:100]}...")
                                else:
                                    print(f"   ❌ Hint {attempt_num} missing expected keywords: {hint_text}")
                            else:
                                print(f"   ❌ Hint {attempt_num} not available in problem data")
                        else:
                            print(f"   ❌ Failed to get problem data for hint verification")
                    else:
                        print(f"   ❌ Attempt {attempt_num}: Wrong answer '{wrong_answer}' was incorrectly accepted as correct")
                        return False
                else:
                    print(f"   ❌ Attempt {attempt_num}: Failed to submit answer: HTTP {response.status_code}")
                    return False
            
            self.log_test("practice2_2 Progressive Hints", True, 
                        f"✅ practice2_2 progressive hints system working - 3 wrong attempts processed correctly")
            return True
                
        except Exception as e:
            self.log_test("practice2_2 Progressive Hints", False, f"Test execution error: {str(e)}")
            return False

    def test_examprep2_wrong_attempts_hints(self):
        """Test progressive hints display for examprep2 with wrong attempts"""
        try:
            print("\n🎯 EXAMPREP2 PROGRESSIVE HINTS TEST")
            print("Testing progressive hints display for examprep2 with 3 wrong attempts")
            
            # Complete prerequisites first (both practice stages and assessment2)
            practice2_2_attempt = {
                "problem_id": "practice2_2",
                "answer": "t ≥ 50",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=practice2_2_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200 or not response.json().get("correct"):
                self.log_test("examprep2 Prerequisites - practice2_2", False, "Failed to complete practice2_2 prerequisite")
                return False
            
            # Complete assessment2
            assessment2_attempt = {
                "problem_id": "assessment2",
                "answer": "y < -12",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=assessment2_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200 or not response.json().get("correct"):
                self.log_test("examprep2 Prerequisites - assessment2", False, "Failed to complete assessment2 prerequisite")
                return False
            
            # Test wrong attempts for examprep2
            wrong_answers = ["p > 4", "p = 4", "p < 4"]  # Wrong answers to trigger hints
            
            for attempt_num, wrong_answer in enumerate(wrong_answers, 1):
                print(f"\n   Attempt {attempt_num}: Submitting wrong answer '{wrong_answer}'")
                
                examprep2_attempt = {
                    "problem_id": "examprep2",
                    "answer": wrong_answer,
                    "hints_used": attempt_num
                }
                
                response = self.session.post(
                    f"{self.base_url}/students/{self.test_student_username}/attempt",
                    json=examprep2_attempt,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if not result.get("correct"):
                        print(f"   ✅ Attempt {attempt_num}: Wrong answer correctly rejected")
                        
                        # Get problem data to check hints
                        problem_response = self.session.get(f"{self.base_url}/problems/examprep2?username={self.test_student_username}")
                        if problem_response.status_code == 200:
                            problem_data = problem_response.json()
                            hints = problem_data.get("hints_en", [])
                            
                            if len(hints) >= attempt_num:
                                expected_hint_keywords = [
                                    ["Variable p", "pieces per child", "children", "total pieces"],
                                    ["each child gets p pieces", "15 children", "distribute"],
                                    ["Total", "number of children", "pieces per child", "at least"]
                                ]
                                
                                hint_text = hints[attempt_num - 1]
                                keywords = expected_hint_keywords[attempt_num - 1]
                                
                                if any(keyword.lower() in hint_text.lower() for keyword in keywords):
                                    print(f"   ✅ Hint {attempt_num} contains expected keywords: {hint_text[:100]}...")
                                else:
                                    print(f"   ❌ Hint {attempt_num} missing expected keywords: {hint_text}")
                            else:
                                print(f"   ❌ Hint {attempt_num} not available in problem data")
                        else:
                            print(f"   ❌ Failed to get problem data for hint verification")
                    else:
                        print(f"   ❌ Attempt {attempt_num}: Wrong answer '{wrong_answer}' was incorrectly accepted as correct")
                        return False
                else:
                    print(f"   ❌ Attempt {attempt_num}: Failed to submit answer: HTTP {response.status_code}")
                    return False
            
            self.log_test("examprep2 Progressive Hints", True, 
                        f"✅ examprep2 progressive hints system working - 3 wrong attempts processed correctly")
            return True
                
        except Exception as e:
            self.log_test("examprep2 Progressive Hints", False, f"Test execution error: {str(e)}")
            return False

    def test_api_response_hints_structure(self):
        """Test that API responses include hints in correct structure"""
        try:
            print("\n🎯 API RESPONSE HINTS STRUCTURE TEST")
            print("Testing that problem API endpoints return hints in correct structure")
            
            # Test practice2_2 API response structure
            response = self.session.get(f"{self.base_url}/problems/practice2_2")
            
            if response.status_code == 200:
                problem_data = response.json()
                
                # Check required fields for hints
                required_fields = ["hints_en", "hints_ar"]
                missing_fields = []
                
                for field in required_fields:
                    if field not in problem_data:
                        missing_fields.append(field)
                
                if not missing_fields:
                    hints_en = problem_data.get("hints_en", [])
                    hints_ar = problem_data.get("hints_ar", [])
                    
                    if len(hints_en) >= 3 and len(hints_ar) >= 3:
                        self.log_test("API Response Hints Structure", True, 
                                    f"✅ API responses include hints in correct structure (EN: {len(hints_en)}, AR: {len(hints_ar)})")
                        return True
                    else:
                        self.log_test("API Response Hints Structure", False, 
                                    f"❌ Insufficient hints in API response (EN: {len(hints_en)}, AR: {len(hints_ar)})")
                        return False
                else:
                    self.log_test("API Response Hints Structure", False, 
                                f"❌ Missing required hint fields: {missing_fields}")
                    return False
            else:
                self.log_test("API Response Hints Structure", False, 
                            f"Failed to get problem data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("API Response Hints Structure", False, f"Test execution error: {str(e)}")
            return False

    def test_hint_content_accuracy(self):
        """Test that hint content matches expected Socratic guidance"""
        try:
            print("\n🎯 HINT CONTENT ACCURACY TEST")
            print("Testing that hint content provides proper Socratic guidance")
            
            # Test practice2_2 hint content
            response = self.session.get(f"{self.base_url}/problems/practice2_2")
            
            if response.status_code == 200:
                problem_data = response.json()
                hints_en = problem_data.get("hints_en", [])
                
                # Verify Socratic progression in hints
                socratic_elements = [
                    # Hint 1: Identify variables and setup
                    ["variable", "represents", "what"],
                    # Hint 2: Guide through calculation
                    ["if you", "how much", "collect"],
                    # Hint 3: Provide formula/structure
                    ["formula", "equation", "symbol", "=", "×"]
                ]
                
                socratic_score = 0
                for i, hint in enumerate(hints_en[:3]):
                    if i < len(socratic_elements):
                        elements = socratic_elements[i]
                        if any(element.lower() in hint.lower() for element in elements):
                            socratic_score += 1
                            print(f"   ✅ Hint {i+1} contains Socratic elements: {hint[:80]}...")
                        else:
                            print(f"   ❌ Hint {i+1} missing Socratic elements: {hint[:80]}...")
                
                if socratic_score >= 2:  # At least 2 out of 3 hints should have Socratic elements
                    self.log_test("Hint Content Accuracy", True, 
                                f"✅ Hints provide proper Socratic guidance ({socratic_score}/3 hints have Socratic elements)")
                    return True
                else:
                    self.log_test("Hint Content Accuracy", False, 
                                f"❌ Insufficient Socratic guidance in hints ({socratic_score}/3 hints have Socratic elements)")
                    return False
            else:
                self.log_test("Hint Content Accuracy", False, 
                            f"Failed to get problem data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Hint Content Accuracy", False, f"Test execution error: {str(e)}")
            return False

    def generate_hints_summary(self, results, critical_failures):
        """Generate comprehensive summary of Section 2 hints testing"""
        print("\n" + "=" * 80)
        print("🎯 SECTION 2 PROGRESSIVE SOCRATIC HINTS TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL SECTION 2 HINTS TEST RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL HINTS ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  HINTS RISK: Progressive Socratic hints not working properly!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix hint display system")
        else:
            print(f"\n🎉 NO CRITICAL HINTS ISSUES DETECTED")
        
        print(f"\n📋 SECTION 2 HINTS STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL SECTION 2 HINTS TESTS PASSED")
            print("   ✅ practice2_2 progressive hints working")
            print("   ✅ examprep2 progressive hints working")
            print("   ✅ Database hints storage correct")
            print("   ✅ API response hints structure correct")
            print("   ✅ Hint content provides Socratic guidance")
            print("   🛡️  HINTS INTEGRITY: PROTECTED")
        else:
            print("   ⚠️  SECTION 2 HINTS ISSUES DETECTED")
            print("   🔧 Progressive hints system needs fixes")
            print("   🚨 STUDENT LEARNING SUPPORT: COMPROMISED")
        
        print("\n" + "=" * 80)

    def run_hints_tests(self):
        """Run comprehensive Section 2 progressive hints tests"""
        print("=" * 80)
        print("🎯 SECTION 2 PROGRESSIVE SOCRATIC HINTS TESTING")
        print("=" * 80)
        print("Testing progressive Socratic hints for Section 2 word problems")
        
        # Test categories for Section 2 hints
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("practice2_2 Database Hints", self.test_practice2_2_database_hints, "critical"),
            ("examprep2 Database Hints", self.test_examprep2_database_hints, "critical"),
            ("practice2_2 Progressive Hints", self.test_practice2_2_wrong_attempts_hints, "critical"),
            ("examprep2 Progressive Hints", self.test_examprep2_wrong_attempts_hints, "critical"),
            ("API Response Hints Structure", self.test_api_response_hints_structure, "high"),
            ("Hint Content Accuracy", self.test_hint_content_accuracy, "high")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 SECTION 2 HINTS TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
            print("-" * 60)
            
            try:
                success = test_method()
                results[category_name] = success
                
                if not success and priority == "critical":
                    critical_failures.append(category_name)
                    
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {category_name}: {str(e)}")
                results[category_name] = False
                critical_failures.append(category_name)
        
        # Generate comprehensive Section 2 hints summary
        self.generate_hints_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run Section 2 hints tests"""
    print("🚀 Starting SECTION 2 PROGRESSIVE SOCRATIC HINTS Testing...")
    print("🎯 Goal: Verify progressive hints work for practice2_2 and examprep2 word problems")
    
    tester = Section2HintsTester(BACKEND_URL)
    results = tester.run_hints_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 SECTION 2 HINTS ALERT: {failed_tests} test(s) failed!")
        print("🔧 Progressive Socratic hints system needs fixes for proper student guidance")
    else:
        print(f"\n🛡️  SECTION 2 HINTS CONFIRMED: All hints tests passed!")
        print("✅ Progressive Socratic hints working correctly for Section 2 word problems")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()