#!/usr/bin/env python3
"""
Backend API Test Suite for Section 3 Explanation Stage Bug Fix
Tests the Section 3 Explanation Stage bug fix as requested by user.

CRITICAL ISSUE BEING TESTED:
Section 3 Explanation Stage showing "Inactive Practice" instead of interactive examples.

SPECIFIC BUG FIX VERIFICATION:
1. Step Solutions Structure - GET /api/problems/explanation3 should have step_solutions array
2. Level-Based Steps - Verify Level 1B, 2B, and 3B steps with correct naming convention
3. Interactive Examples - Confirm both interactive_examples and step_solutions are present
4. Bilingual Support - Check each step has English and Arabic descriptions and possible answers
5. Complete Structure - Verify explanation3 has complete structure for frontend interactive functionality

EXPECTED BACKEND BEHAVIOR:
- explanation3 should have step_solutions array with Level 1B, 2B, 3B steps
- Each level should have 2-3 steps with proper naming (e.g., "Level 1B Step 1")
- Each step should have bilingual content and possible_answers arrays
- Interactive examples should be present alongside step_solutions
- Frontend should be able to render interactive step-by-step interface
"""

import requests
import json
import sys
import os
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://math-bug-fixes.preview.emergentagent.com/api"

class Section3ExplanationTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "section3_explanation_test_student"
        
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
        """Create test student for Section 3 explanation testing"""
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

    def test_explanation3_step_solutions_structure(self):
        """Test Section 3 explanation3 step_solutions array structure"""
        try:
            print("\n🎯 SECTION 3 EXPLANATION STEP SOLUTIONS STRUCTURE TESTING")
            print("Testing explanation3 problem for step_solutions array with Level 1B, 2B, 3B steps")
            
            # Get explanation3 problem to verify structure
            response = self.session.get(f"{self.base_url}/problems/explanation3")
            
            if response.status_code == 200:
                problem_data = response.json()
                
                print(f"   Problem ID: {problem_data.get('id', 'N/A')}")
                print(f"   Problem Type: {problem_data.get('type', 'N/A')}")
                print(f"   Question: {problem_data.get('question_en', 'N/A')}")
                
                # CRITICAL TEST 1: Verify it's an explanation type problem
                if problem_data.get('type') != 'explanation':
                    self.log_test("Explanation3 Step Solutions Structure", False, 
                                f"❌ Expected type 'explanation', got '{problem_data.get('type')}'")
                    return False
                
                # CRITICAL TEST 2: Verify step_solutions array exists
                step_solutions = problem_data.get('step_solutions', [])
                if not step_solutions:
                    self.log_test("Explanation3 Step Solutions Structure", False, 
                                f"❌ Missing step_solutions array for explanation3 - this causes 'Inactive Practice' issue")
                    return False
                
                print(f"   ✅ Found step_solutions array with {len(step_solutions)} steps")
                
                # CRITICAL TEST 3: Verify Level-Based Steps naming convention
                expected_level_patterns = ["Level 1B", "Level 2B", "Level 3B"]
                found_levels = set()
                
                for i, step in enumerate(step_solutions):
                    step_text_en = step.get('step_en', '')
                    step_text_ar = step.get('step_ar', '')
                    possible_answers = step.get('possible_answers', [])
                    
                    print(f"   Step {i+1}: {step_text_en}")
                    print(f"   Arabic: {step_text_ar}")
                    print(f"   Possible Answers: {possible_answers}")
                    
                    # Check for level naming pattern
                    for level_pattern in expected_level_patterns:
                        if level_pattern in step_text_en:
                            found_levels.add(level_pattern)
                    
                    # CRITICAL TEST 4: Each step must have possible_answers
                    if not possible_answers:
                        self.log_test("Explanation3 Step Solutions Structure", False, 
                                    f"❌ Step {i+1} missing possible_answers array")
                        return False
                    
                    # CRITICAL TEST 5: Each step must have bilingual content
                    if not step_text_en or not step_text_ar:
                        self.log_test("Explanation3 Step Solutions Structure", False, 
                                    f"❌ Step {i+1} missing bilingual content (EN: '{step_text_en}', AR: '{step_text_ar}')")
                        return False
                
                # CRITICAL TEST 6: Verify all expected levels are present
                missing_levels = set(expected_level_patterns) - found_levels
                if missing_levels:
                    self.log_test("Explanation3 Step Solutions Structure", False, 
                                f"❌ Missing expected levels: {list(missing_levels)}")
                    return False
                
                print(f"   ✅ Found all expected levels: {list(found_levels)}")
                
                self.log_test("Explanation3 Step Solutions Structure", True, 
                            f"✅ explanation3 has correct step_solutions structure with Level 1B, 2B, 3B steps")
                return True
                
            else:
                self.log_test("Explanation3 Step Solutions Structure", False, 
                            f"Failed to get explanation3 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Explanation3 Step Solutions Structure", False, f"Test execution error: {str(e)}")
            return False

    def test_explanation3_interactive_examples_presence(self):
        """Test that explanation3 has both interactive_examples and step_solutions"""
        try:
            print("\n🎯 SECTION 3 EXPLANATION INTERACTIVE EXAMPLES TESTING")
            print("Testing explanation3 for both interactive_examples and step_solutions presence")
            
            # Get explanation3 problem
            response = self.session.get(f"{self.base_url}/problems/explanation3")
            
            if response.status_code == 200:
                problem_data = response.json()
                
                # CRITICAL TEST 1: Check for interactive_examples
                interactive_examples = problem_data.get('interactive_examples', [])
                step_solutions = problem_data.get('step_solutions', [])
                
                print(f"   Interactive Examples: {len(interactive_examples)} found")
                print(f"   Step Solutions: {len(step_solutions)} found")
                
                if not interactive_examples:
                    self.log_test("Explanation3 Interactive Examples Presence", False, 
                                f"❌ Missing interactive_examples array")
                    return False
                
                if not step_solutions:
                    self.log_test("Explanation3 Interactive Examples Presence", False, 
                                f"❌ Missing step_solutions array")
                    return False
                
                # CRITICAL TEST 2: Verify interactive examples structure
                for i, example in enumerate(interactive_examples):
                    example_en = example.get('example_en', '')
                    example_ar = example.get('example_ar', '')
                    
                    print(f"   Example {i+1}: {example_en}")
                    print(f"   Arabic: {example_ar}")
                    
                    if not example_en or not example_ar:
                        self.log_test("Explanation3 Interactive Examples Presence", False, 
                                    f"❌ Interactive example {i+1} missing bilingual content")
                        return False
                
                self.log_test("Explanation3 Interactive Examples Presence", True, 
                            f"✅ explanation3 has both interactive_examples ({len(interactive_examples)}) and step_solutions ({len(step_solutions)})")
                return True
                
            else:
                self.log_test("Explanation3 Interactive Examples Presence", False, 
                            f"Failed to get explanation3 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Explanation3 Interactive Examples Presence", False, f"Test execution error: {str(e)}")
            return False

    def test_explanation3_level_based_steps_content(self):
        """Test specific content of Level 1B, 2B, 3B steps"""
        try:
            print("\n🎯 SECTION 3 EXPLANATION LEVEL-BASED STEPS CONTENT TESTING")
            print("Testing specific content and structure of Level 1B, 2B, 3B steps")
            
            # Get explanation3 problem
            response = self.session.get(f"{self.base_url}/problems/explanation3")
            
            if response.status_code == 200:
                problem_data = response.json()
                step_solutions = problem_data.get('step_solutions', [])
                
                if not step_solutions:
                    self.log_test("Explanation3 Level-Based Steps Content", False, 
                                f"❌ No step_solutions found")
                    return False
                
                # Expected level content based on the bug fix implementation
                expected_levels = {
                    "Level 1B": {"problem": "2y + 5 ≤ 19", "steps": 2},
                    "Level 2B": {"problem": "15 - 5k ≥ -10", "steps": 2}, 
                    "Level 3B": {"problem": "4(r - 1) > 8", "steps": 3}
                }
                
                level_steps_found = {}
                
                # Group steps by level
                for step in step_solutions:
                    step_text = step.get('step_en', '')
                    
                    for level_name in expected_levels.keys():
                        if level_name in step_text:
                            if level_name not in level_steps_found:
                                level_steps_found[level_name] = []
                            level_steps_found[level_name].append(step)
                
                print(f"   Found levels: {list(level_steps_found.keys())}")
                
                # CRITICAL TEST 1: Verify all expected levels are present
                for level_name, expected_info in expected_levels.items():
                    if level_name not in level_steps_found:
                        self.log_test("Explanation3 Level-Based Steps Content", False, 
                                    f"❌ Missing {level_name} steps")
                        return False
                    
                    level_steps = level_steps_found[level_name]
                    expected_step_count = expected_info["steps"]
                    
                    print(f"   {level_name}: {len(level_steps)} steps (expected {expected_step_count})")
                    
                    # CRITICAL TEST 2: Verify step count for each level
                    if len(level_steps) != expected_step_count:
                        self.log_test("Explanation3 Level-Based Steps Content", False, 
                                    f"❌ {level_name} has {len(level_steps)} steps, expected {expected_step_count}")
                        return False
                    
                    # CRITICAL TEST 3: Verify step content and possible answers
                    for i, step in enumerate(level_steps):
                        step_text = step.get('step_en', '')
                        possible_answers = step.get('possible_answers', [])
                        
                        print(f"     Step {i+1}: {step_text}")
                        print(f"     Possible Answers: {possible_answers}")
                        
                        if not possible_answers:
                            self.log_test("Explanation3 Level-Based Steps Content", False, 
                                        f"❌ {level_name} Step {i+1} missing possible_answers")
                            return False
                
                self.log_test("Explanation3 Level-Based Steps Content", True, 
                            f"✅ All Level 1B, 2B, 3B steps have correct content and structure")
                return True
                
            else:
                self.log_test("Explanation3 Level-Based Steps Content", False, 
                            f"Failed to get explanation3 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Explanation3 Level-Based Steps Content", False, f"Test execution error: {str(e)}")
            return False

    def test_explanation3_bilingual_support(self):
        """Test bilingual support for all step_solutions"""
        try:
            print("\n🎯 SECTION 3 EXPLANATION BILINGUAL SUPPORT TESTING")
            print("Testing bilingual content for all step_solutions in explanation3")
            
            # Get explanation3 problem
            response = self.session.get(f"{self.base_url}/problems/explanation3")
            
            if response.status_code == 200:
                problem_data = response.json()
                step_solutions = problem_data.get('step_solutions', [])
                
                if not step_solutions:
                    self.log_test("Explanation3 Bilingual Support", False, 
                                f"❌ No step_solutions found")
                    return False
                
                bilingual_issues = []
                
                for i, step in enumerate(step_solutions):
                    step_en = step.get('step_en', '')
                    step_ar = step.get('step_ar', '')
                    
                    print(f"   Step {i+1}:")
                    print(f"     English: {step_en}")
                    print(f"     Arabic: {step_ar}")
                    
                    # CRITICAL TEST 1: Both languages must be present
                    if not step_en:
                        bilingual_issues.append(f"Step {i+1} missing English content")
                    
                    if not step_ar:
                        bilingual_issues.append(f"Step {i+1} missing Arabic content")
                    
                    # CRITICAL TEST 2: Content should be meaningful (not just placeholders)
                    if step_en and len(step_en.strip()) < 5:
                        bilingual_issues.append(f"Step {i+1} English content too short: '{step_en}'")
                    
                    if step_ar and len(step_ar.strip()) < 3:
                        bilingual_issues.append(f"Step {i+1} Arabic content too short: '{step_ar}'")
                
                if bilingual_issues:
                    self.log_test("Explanation3 Bilingual Support", False, 
                                f"❌ Bilingual issues found: {'; '.join(bilingual_issues)}")
                    return False
                
                self.log_test("Explanation3 Bilingual Support", True, 
                            f"✅ All {len(step_solutions)} steps have proper bilingual support")
                return True
                
            else:
                self.log_test("Explanation3 Bilingual Support", False, 
                            f"Failed to get explanation3 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Explanation3 Bilingual Support", False, f"Test execution error: {str(e)}")
            return False

    def test_explanation3_complete_structure(self):
        """Test complete structure needed for frontend interactive functionality"""
        try:
            print("\n🎯 SECTION 3 EXPLANATION COMPLETE STRUCTURE TESTING")
            print("Testing complete structure needed for frontend interactive functionality")
            
            # Get explanation3 problem
            response = self.session.get(f"{self.base_url}/problems/explanation3")
            
            if response.status_code == 200:
                problem_data = response.json()
                
                # CRITICAL FIELDS for frontend interactive functionality
                required_fields = [
                    'id', 'type', 'question_en', 'question_ar', 
                    'interactive_examples', 'step_solutions'
                ]
                
                missing_fields = []
                for field in required_fields:
                    if field not in problem_data or not problem_data[field]:
                        missing_fields.append(field)
                
                if missing_fields:
                    self.log_test("Explanation3 Complete Structure", False, 
                                f"❌ Missing required fields: {missing_fields}")
                    return False
                
                # CRITICAL TEST 1: Verify show_full_solution is properly set
                show_full_solution = problem_data.get('show_full_solution', True)
                print(f"   show_full_solution: {show_full_solution}")
                
                # For interactive mode, show_full_solution should be False
                if show_full_solution != False:
                    print(f"   ⚠️  show_full_solution is {show_full_solution}, may affect interactivity")
                
                # CRITICAL TEST 2: Verify step_solutions structure for frontend
                step_solutions = problem_data.get('step_solutions', [])
                interactive_examples = problem_data.get('interactive_examples', [])
                
                print(f"   Interactive Examples: {len(interactive_examples)}")
                print(f"   Step Solutions: {len(step_solutions)}")
                
                # CRITICAL TEST 3: Each step_solution must have required fields for frontend
                step_required_fields = ['step_en', 'step_ar', 'possible_answers']
                
                for i, step in enumerate(step_solutions):
                    step_missing_fields = []
                    for field in step_required_fields:
                        if field not in step or not step[field]:
                            step_missing_fields.append(field)
                    
                    if step_missing_fields:
                        self.log_test("Explanation3 Complete Structure", False, 
                                    f"❌ Step {i+1} missing required fields: {step_missing_fields}")
                        return False
                
                # CRITICAL TEST 4: Verify problem has proper section context
                problem_id = problem_data.get('id', '')
                if not problem_id.startswith('explanation3'):
                    self.log_test("Explanation3 Complete Structure", False, 
                                f"❌ Problem ID '{problem_id}' doesn't match expected 'explanation3'")
                    return False
                
                self.log_test("Explanation3 Complete Structure", True, 
                            f"✅ explanation3 has complete structure for frontend interactive functionality")
                return True
                
            else:
                self.log_test("Explanation3 Complete Structure", False, 
                            f"Failed to get explanation3 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Explanation3 Complete Structure", False, f"Test execution error: {str(e)}")
            return False

    def generate_section3_summary(self, results, critical_failures):
        """Generate comprehensive summary of Section 3 explanation testing"""
        print("\n" + "=" * 80)
        print("🎯 SECTION 3 EXPLANATION STAGE BUG FIX TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL SECTION 3 EXPLANATION TESTING RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL SECTION 3 EXPLANATION ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  SECTION 3 STATUS: 'INACTIVE PRACTICE' ISSUE NOT RESOLVED")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix remaining step_solutions issues")
        else:
            print(f"\n🎉 NO CRITICAL SECTION 3 EXPLANATION ISSUES DETECTED")
        
        print(f"\n📋 SECTION 3 EXPLANATION STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL SECTION 3 EXPLANATION TESTS PASSED")
            print("   ✅ step_solutions array properly added")
            print("   ✅ Level 1B, 2B, 3B steps with correct naming")
            print("   ✅ Interactive examples and step_solutions both present")
            print("   ✅ Bilingual support for all steps")
            print("   ✅ Complete structure for frontend interactive functionality")
            print("   🛡️  SECTION 3 EXPLANATION: 'INACTIVE PRACTICE' ISSUE RESOLVED")
        else:
            print("   ⚠️  SECTION 3 EXPLANATION ISSUES DETECTED")
            print("   🔧 Backend step_solutions structure needs enhancement")
            print("   🚨 STUDENT EXPERIENCE: 'INACTIVE PRACTICE' ISSUE MAY PERSIST")
        
        print("\n" + "=" * 80)

    def run_section3_explanation_tests(self):
        """Run comprehensive Section 3 explanation stage tests"""
        print("=" * 80)
        print("🎯 SECTION 3 EXPLANATION STAGE BUG FIX TESTING")
        print("=" * 80)
        print("Testing Section 3 Explanation Stage 'Inactive Practice' bug fix")
        
        # Test categories for Section 3 explanation
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("Explanation3 Step Solutions Structure", self.test_explanation3_step_solutions_structure, "critical"),
            ("Explanation3 Interactive Examples Presence", self.test_explanation3_interactive_examples_presence, "critical"),
            ("Explanation3 Level-Based Steps Content", self.test_explanation3_level_based_steps_content, "critical"),
            ("Explanation3 Bilingual Support", self.test_explanation3_bilingual_support, "high"),
            ("Explanation3 Complete Structure", self.test_explanation3_complete_structure, "critical")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 SECTION 3 TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive Section 3 summary
        self.generate_section3_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run Section 3 explanation tests"""
    print("🚀 Starting SECTION 3 EXPLANATION STAGE BUG FIX Testing...")
    print("🎯 Goal: Verify 'Inactive Practice' issue is resolved with proper step_solutions structure")
    
    tester = Section3ExplanationTester(BACKEND_URL)
    results = tester.run_section3_explanation_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 SECTION 3 ALERT: {failed_tests} test(s) failed!")
        print("🔧 Section 3 explanation stage needs backend enhancement")
        print("⚠️  'Inactive Practice' issue may not be fully resolved")
    else:
        print(f"\n🛡️  SECTION 3 CONFIRMED: All tests passed!")
        print("✅ Section 3 Explanation Stage 'Inactive Practice' issue is RESOLVED")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()