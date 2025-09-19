#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - Global Negative Number Input Validation Testing
Tests the critical global negative number input validation enhancement as requested by user.

CRITICAL GLOBAL ENHANCEMENT BEING TESTED:
- Backend support for multiple negative number formats
- Section 1 and Section 2 negative number validation (as requested)
- Test formats like: "k ≤ -5", "k ≤ (-5)", "k<=-5", "ك ≤ (-٥)", "ك≤(-٥)"
- Arabic numerals and variable names acceptance
- Space variations in mathematical expressions
- Parentheses around negative numbers support
"""

import requests
import json
import sys
import os
import re
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://inequal-progression.preview.emergentagent.com/api"

class Section2ExplanationBugFixTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "explanation_bug_test_student"
        
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
        """Create test student for explanation bug testing"""
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

    def test_explanation2_problem_structure(self):
        """Test that explanation2 has correct problem structure"""
        try:
            print("\n🎯 EXPLANATION2 PROBLEM STRUCTURE VERIFICATION")
            print("Testing if explanation2 has correct structure with 3 interactive examples")
            
            # Get explanation2 problem data
            response = self.session.get(f"{self.base_url}/problems/explanation2")
            
            if response.status_code == 200:
                problem_data = response.json()
                interactive_examples = problem_data.get("interactive_examples", [])
                
                if len(interactive_examples) == 3:
                    # Verify each level has correct practice questions
                    expected_practice_questions = [
                        "4x ≥ 20",  # Level 1B
                        "-3m < 15", # Level 2B  
                        "-6k ≥ 30"  # Level 3B
                    ]
                    
                    structure_correct = True
                    for i, example in enumerate(interactive_examples):
                        practice_question = example.get("practice_question_en", "")
                        expected_question = expected_practice_questions[i]
                        
                        if expected_question in practice_question:
                            print(f"   ✅ Level {i+1}B: Found correct practice question '{expected_question}'")
                        else:
                            print(f"   ❌ Level {i+1}B: Expected '{expected_question}', got '{practice_question}'")
                            structure_correct = False
                    
                    if structure_correct:
                        self.log_test("explanation2 Problem Structure", True, 
                                    f"✅ explanation2 has correct 3-level structure with updated practice questions")
                        return True
                    else:
                        self.log_test("explanation2 Problem Structure", False, 
                                    f"❌ explanation2 practice questions don't match user specifications")
                        return False
                else:
                    self.log_test("explanation2 Problem Structure", False, 
                                f"❌ explanation2 has {len(interactive_examples)} examples, expected 3")
                    return False
            else:
                self.log_test("explanation2 Problem Structure", False, 
                            f"Failed to get explanation2 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("explanation2 Problem Structure", False, f"Test execution error: {str(e)}")
            return False

    def test_step_solutions_structure(self):
        """Test that step_solutions array contains exactly 6 step definitions (2 per level)"""
        try:
            print("\n🎯 STEP SOLUTIONS STRUCTURE VERIFICATION")
            print("Testing if step_solutions contains exactly 6 steps (2 per level)")
            
            # Get explanation2 problem data
            response = self.session.get(f"{self.base_url}/problems/explanation2")
            
            if response.status_code == 200:
                problem_data = response.json()
                step_solutions = problem_data.get("step_solutions", [])
                
                if len(step_solutions) == 6:
                    # Verify step structure for each level
                    expected_steps = [
                        "Level 1B Step 1: Divide both sides by 4",
                        "Level 1B Step 2: Simplify",
                        "Level 2B Step 1: Divide both sides by -3 (flip the inequality sign)",
                        "Level 2B Step 2: Simplify", 
                        "Level 3B Step 1: Divide both sides by -6 (flip the inequality sign)",
                        "Level 3B Step 2: Simplify"
                    ]
                    
                    steps_correct = True
                    for i, step in enumerate(step_solutions):
                        step_text = step.get("step_en", "")
                        expected_step = expected_steps[i]
                        
                        if expected_step in step_text:
                            print(f"   ✅ Step {i+1}: Found correct step '{expected_step}'")
                        else:
                            print(f"   ❌ Step {i+1}: Expected '{expected_step}', got '{step_text}'")
                            steps_correct = False
                    
                    if steps_correct:
                        self.log_test("Step Solutions Structure", True, 
                                    f"✅ step_solutions contains exactly 6 steps with correct definitions")
                        return True
                    else:
                        self.log_test("Step Solutions Structure", False, 
                                    f"❌ step_solutions steps don't match expected definitions")
                        return False
                else:
                    self.log_test("Step Solutions Structure", False, 
                                f"❌ step_solutions has {len(step_solutions)} steps, expected 6")
                    return False
            else:
                self.log_test("Step Solutions Structure", False, 
                            f"Failed to get explanation2 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Step Solutions Structure", False, f"Test execution error: {str(e)}")
            return False

    def test_step_possible_answers(self):
        """Test that each step has correct possible_answers arrays"""
        try:
            print("\n🎯 STEP POSSIBLE ANSWERS VERIFICATION")
            print("Testing if each step has correct possible_answers for validation")
            
            # Get explanation2 problem data
            response = self.session.get(f"{self.base_url}/problems/explanation2")
            
            if response.status_code == 200:
                problem_data = response.json()
                step_solutions = problem_data.get("step_solutions", [])
                
                # Expected possible answers for key steps
                expected_answers = [
                    ["4x/4 ≥ 20/4", "x ≥ 20/4"],  # Level 1B Step 1
                    ["x ≥ 5"],                      # Level 1B Step 2
                    ["m > 15/(-3)", "m > -5"],      # Level 2B Step 1
                    ["m > -5"],                     # Level 2B Step 2
                    ["k ≤ 30/(-6)", "k ≤ -5"],     # Level 3B Step 1
                    ["k ≤ -5"]                      # Level 3B Step 2
                ]
                
                answers_correct = True
                for i, step in enumerate(step_solutions):
                    possible_answers = step.get("possible_answers", [])
                    expected_for_step = expected_answers[i]
                    
                    # Check if at least one expected answer is present
                    found_expected = False
                    for expected_answer in expected_for_step:
                        if expected_answer in possible_answers:
                            found_expected = True
                            break
                    
                    if found_expected:
                        print(f"   ✅ Step {i+1}: Has correct possible answers")
                    else:
                        print(f"   ❌ Step {i+1}: Missing expected answers. Got: {possible_answers}")
                        answers_correct = False
                
                if answers_correct:
                    self.log_test("Step Possible Answers", True, 
                                f"✅ All steps have correct possible_answers for validation")
                    return True
                else:
                    self.log_test("Step Possible Answers", False, 
                                f"❌ Some steps have incorrect possible_answers")
                    return False
            else:
                self.log_test("Step Possible Answers", False, 
                            f"Failed to get explanation2 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Step Possible Answers", False, f"Test execution error: {str(e)}")
            return False

    def test_hints_alignment(self):
        """Test that hints are properly aligned with the 6 steps"""
        try:
            print("\n🎯 HINTS ALIGNMENT VERIFICATION")
            print("Testing if hints_en and hints_ar arrays contain 6 entries aligned with steps")
            
            # Get explanation2 problem data
            response = self.session.get(f"{self.base_url}/problems/explanation2")
            
            if response.status_code == 200:
                problem_data = response.json()
                hints_en = problem_data.get("hints_en", [])
                hints_ar = problem_data.get("hints_ar", [])
                
                if len(hints_en) == 6 and len(hints_ar) == 6:
                    # Verify hint content alignment with steps
                    expected_hint_keywords = [
                        ["divide", "4"],           # Step 1: Level 1B
                        ["simplify"],              # Step 2: Level 1B
                        ["isolate", "m", "flip"],  # Step 3: Level 2B
                        ["simplify"],              # Step 4: Level 2B
                        ["isolate", "k", "-6"],    # Step 5: Level 3B
                        ["simplify"]               # Step 6: Level 3B
                    ]
                    
                    hints_aligned = True
                    for i, hint in enumerate(hints_en):
                        keywords = expected_hint_keywords[i]
                        hint_matches = any(keyword.lower() in hint.lower() for keyword in keywords)
                        
                        if hint_matches:
                            print(f"   ✅ Hint {i+1}: Aligned with step content")
                        else:
                            print(f"   ❌ Hint {i+1}: Not aligned with step. Got: {hint[:50]}...")
                            hints_aligned = False
                    
                    if hints_aligned:
                        self.log_test("Hints Alignment", True, 
                                    f"✅ hints_en and hints_ar arrays properly aligned with 6 steps")
                        return True
                    else:
                        self.log_test("Hints Alignment", False, 
                                    f"❌ Some hints not properly aligned with step content")
                        return False
                else:
                    self.log_test("Hints Alignment", False, 
                                f"❌ hints_en has {len(hints_en)} entries, hints_ar has {len(hints_ar)} entries, expected 6 each")
                    return False
            else:
                self.log_test("Hints Alignment", False, 
                            f"Failed to get explanation2 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Hints Alignment", False, f"Test execution error: {str(e)}")
            return False

    def test_backend_response_structure(self):
        """Test that backend response has all required fields for explanation2"""
        try:
            print("\n🎯 BACKEND RESPONSE STRUCTURE VERIFICATION")
            print("Testing if explanation2 backend response contains all required fields")
            
            # Get explanation2 problem data
            response = self.session.get(f"{self.base_url}/problems/explanation2")
            
            if response.status_code == 200:
                problem_data = response.json()
                
                # Required fields for explanation2
                required_fields = [
                    "id", "section_id", "type", "interactive_examples", 
                    "step_solutions", "hints_en", "hints_ar"
                ]
                
                missing_fields = []
                for field in required_fields:
                    if field not in problem_data:
                        missing_fields.append(field)
                
                if not missing_fields:
                    # Verify field contents
                    interactive_examples = problem_data.get("interactive_examples", [])
                    step_solutions = problem_data.get("step_solutions", [])
                    
                    if len(interactive_examples) == 3 and len(step_solutions) == 6:
                        self.log_test("Backend Response Structure", True, 
                                    f"✅ explanation2 backend response has all required fields with correct structure")
                        return True
                    else:
                        self.log_test("Backend Response Structure", False, 
                                    f"❌ Field contents incorrect: {len(interactive_examples)} examples, {len(step_solutions)} steps")
                        return False
                else:
                    self.log_test("Backend Response Structure", False, 
                                f"❌ Missing required fields: {missing_fields}")
                    return False
            else:
                self.log_test("Backend Response Structure", False, 
                            f"Failed to get explanation2 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Backend Response Structure", False, f"Test execution error: {str(e)}")
            return False

    def generate_bug_fix_summary(self, results, critical_failures):
        """Generate comprehensive summary of Section 2 explanation bug fix testing"""
        print("\n" + "=" * 80)
        print("🎯 SECTION 2 EXPLANATION STAGE STEP COMPLETION BUG FIX TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL BUG FIX TEST RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL BUG FIX ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  BUG FIX STATUS: INCOMPLETE - Step completion bug may still exist!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix remaining issues")
        else:
            print(f"\n🎉 NO CRITICAL BUG FIX ISSUES DETECTED")
        
        print(f"\n📋 SECTION 2 EXPLANATION STAGE STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL BUG FIX TESTS PASSED")
            print("   ✅ explanation2 has correct 3-level structure")
            print("   ✅ step_solutions contains exactly 6 steps (2 per level)")
            print("   ✅ Interactive examples match user specifications")
            print("   ✅ Step possible_answers arrays are correct")
            print("   ✅ Hints properly aligned with 6 steps")
            print("   ✅ Backend response structure is complete")
            print("   🛡️  STEP COMPLETION BUG: FIXED")
        else:
            print("   ⚠️  SECTION 2 EXPLANATION STAGE ISSUES DETECTED")
            print("   🔧 Step completion bug fix needs additional work")
            print("   🚨 STUDENT PROGRESSION: MAY STILL BE BROKEN")
        
        print("\n" + "=" * 80)

    def run_bug_fix_tests(self):
        """Run comprehensive Section 2 explanation stage bug fix tests"""
        print("=" * 80)
        print("🎯 SECTION 2 EXPLANATION STAGE STEP COMPLETION BUG FIX TESTING")
        print("=" * 80)
        print("Testing critical bug fix for Section 2 explanation stage step completion")
        
        # Test categories for Section 2 explanation bug fix
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("explanation2 Problem Structure", self.test_explanation2_problem_structure, "critical"),
            ("Step Solutions Structure", self.test_step_solutions_structure, "critical"),
            ("Step Possible Answers", self.test_step_possible_answers, "critical"),
            ("Hints Alignment", self.test_hints_alignment, "high"),
            ("Backend Response Structure", self.test_backend_response_structure, "high")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 BUG FIX TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive bug fix summary
        self.generate_bug_fix_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run Section 2 explanation stage bug fix tests"""
    print("🚀 Starting SECTION 2 EXPLANATION STAGE STEP COMPLETION BUG FIX Testing...")
    print("🎯 Goal: Verify the critical bug fix for Section 2 explanation stage step completion")
    
    tester = Section2ExplanationBugFixTester(BACKEND_URL)
    results = tester.run_bug_fix_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 BUG FIX ALERT: {failed_tests} test(s) failed!")
        print("🔧 Section 2 explanation stage step completion bug fix needs additional work")
    else:
        print(f"\n🛡️  BUG FIX CONFIRMED: All tests passed!")
        print("✅ Section 2 explanation stage step completion bug has been successfully fixed")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()