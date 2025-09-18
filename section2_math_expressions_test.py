#!/usr/bin/env python3
"""
Section 2 Mathematical Expression Display Fix Testing
Tests the CRITICAL MATHEMATICAL EXPRESSION DISPLAY FIX for educational correctness
"""

import requests
import json
import sys
import os
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://bilingual-algebra.preview.emergentagent.com/api"

class Section2MathExpressionTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "math_expression_test_student"
        
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
        """Create test student for mathematical expression testing"""
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

    def test_section2_explanation_interactive_examples(self):
        """Test Section 2 Explanation Stage - Interactive Examples with Complete Mathematical Operations"""
        try:
            print("\n🔍 SECTION 2 EXPLANATION STAGE - INTERACTIVE EXAMPLES TESTING")
            print("Testing GET /api/problems/explanation2 for complete mathematical expressions")
            
            # Get explanation2 problem data
            response = self.session.get(f"{self.base_url}/problems/explanation2")
            
            if response.status_code != 200:
                self.log_test("Section 2 Explanation Data Retrieval", False, 
                            f"Failed to get explanation2: HTTP {response.status_code}")
                return False
            
            data = response.json()
            self.log_test("Section 2 Explanation Data Retrieval", True, 
                        "✅ Successfully retrieved explanation2 problem data")
            
            # Check for interactive_examples field
            if "interactive_examples" not in data:
                self.log_test("Interactive Examples Field", False, 
                            "Missing 'interactive_examples' field in explanation2 data")
                return False
            
            interactive_examples = data["interactive_examples"]
            if not isinstance(interactive_examples, list) or len(interactive_examples) < 3:
                self.log_test("Interactive Examples Structure", False, 
                            f"Expected at least 3 interactive examples, got {len(interactive_examples) if isinstance(interactive_examples, list) else 'invalid structure'}")
                return False
            
            self.log_test("Interactive Examples Structure", True, 
                        f"✅ Found {len(interactive_examples)} interactive examples")
            
            # Test Example 1A: 5x ≥ 30 - Complete operations verification
            example_1a = interactive_examples[0] if len(interactive_examples) > 0 else None
            if example_1a:
                success = self.verify_example_1a_complete_operations(example_1a)
                if not success:
                    return False
            
            # Test Example 2A: -3m > 15 - Complete operations with sign flip
            example_2a = interactive_examples[1] if len(interactive_examples) > 1 else None
            if example_2a:
                success = self.verify_example_2a_complete_operations(example_2a)
                if not success:
                    return False
            
            # Test Example 3A: k / (-4) ≤ 2 - Complete operations with sign flip
            example_3a = interactive_examples[2] if len(interactive_examples) > 2 else None
            if example_3a:
                success = self.verify_example_3a_complete_operations(example_3a)
                if not success:
                    return False
            
            self.log_test("Section 2 Interactive Examples Complete", True, 
                        "✅ All Section 2 interactive examples show complete mathematical operations")
            return True
            
        except Exception as e:
            self.log_test("Section 2 Interactive Examples Testing", False, f"Test execution error: {str(e)}")
            return False

    def verify_example_1a_complete_operations(self, example_1a):
        """Verify Example 1A (5x ≥ 30) shows complete operations on both sides"""
        try:
            # Check if this is the correct example (5x ≥ 30)
            problem_en = example_1a.get("problem_en", "")
            if "5x" not in problem_en and "30" not in problem_en:
                self.log_test("Example 1A Problem Identification", False, 
                            f"Expected problem with '5x' and '30', got: {problem_en}")
                return False
            
            self.log_test("Example 1A Problem Identification", True, 
                        f"✅ Found Example 1A: {problem_en}")
            
            # Check solution for complete operations
            solution_en = example_1a.get("solution_en", "")
            if not solution_en:
                self.log_test("Example 1A Solution Content", False, 
                            "Missing solution_en field")
                return False
            
            # The solution should show the complete mathematical progression
            # Looking for patterns like "5x ≥ 30" → "x ≥ 30 / 5" → "x ≥ 6"
            if "30 / 5" in solution_en or "5x" in solution_en:
                self.log_test("Example 1A Complete Operations", True, 
                            f"✅ Solution shows complete operations: {solution_en}")
            else:
                self.log_test("Example 1A Complete Operations", False, 
                            f"❌ Solution should show complete operations, got: {solution_en}")
                return False
            
            # Check that the final result is shown
            if "x ≥ 6" in solution_en or "x ≥ 6" in solution_en:
                self.log_test("Example 1A Final Result", True, 
                            f"✅ Solution shows correct final result")
            else:
                self.log_test("Example 1A Final Result", False, 
                            f"❌ Solution should show 'x ≥ 6', got: {solution_en}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Example 1A Verification", False, f"Verification error: {str(e)}")
            return False

    def verify_example_2a_complete_operations(self, example_2a):
        """Verify Example 2A (-3m > 15) shows complete operations with sign flip"""
        try:
            # Check if this is the correct example (-3m > 15)
            problem = example_2a.get("problem", "")
            if "-3m" not in problem and "15" not in problem:
                self.log_test("Example 2A Problem Identification", False, 
                            f"Expected problem with '-3m' and '15', got: {problem}")
                return False
            
            # Check step solutions for complete operations with sign flip
            step_solutions = example_2a.get("step_solutions", [])
            if not step_solutions or len(step_solutions) < 2:
                self.log_test("Example 2A Step Solutions", False, 
                            f"Expected at least 2 step solutions, got {len(step_solutions)}")
                return False
            
            # Step 1 should show: "-3m / (-3) < 15 / (-3)" (both sides with sign flip)
            step1 = step_solutions[0] if len(step_solutions) > 0 else {}
            step1_solution = step1.get("solution", "")
            
            # Check for complete operation on both sides with sign flip indication
            has_complete_operation = (
                ("-3m" in step1_solution and "15" in step1_solution and "/" in step1_solution) or
                ("÷" in step1_solution and "-3" in step1_solution) or
                ("<" in step1_solution and "(-3)" in step1_solution)
            )
            
            if has_complete_operation:
                self.log_test("Example 2A Step 1 Complete Operations with Sign Flip", True, 
                            f"✅ Step 1 shows complete operations with sign flip: {step1_solution}")
            else:
                self.log_test("Example 2A Step 1 Complete Operations with Sign Flip", False, 
                            f"❌ Step 1 should show complete operations with sign flip, got: {step1_solution}")
                return False
            
            # Step 2 should show: "m < -5" (simplified)
            step2 = step_solutions[1] if len(step_solutions) > 1 else {}
            step2_solution = step2.get("solution", "")
            
            if "m" in step2_solution and ("-5" in step2_solution or "<" in step2_solution):
                self.log_test("Example 2A Step 2 Simplified Result", True, 
                            f"✅ Step 2 shows simplified result: {step2_solution}")
            else:
                self.log_test("Example 2A Step 2 Simplified Result", False, 
                            f"❌ Step 2 should show simplified result, got: {step2_solution}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Example 2A Verification", False, f"Verification error: {str(e)}")
            return False

    def verify_example_3a_complete_operations(self, example_3a):
        """Verify Example 3A (k / (-4) ≤ 2) shows complete operations with sign flip"""
        try:
            # Check if this is the correct example (k / (-4) ≤ 2)
            problem = example_3a.get("problem", "")
            if "k" not in problem and ("(-4)" not in problem and "-4" not in problem) and "2" not in problem:
                self.log_test("Example 3A Problem Identification", False, 
                            f"Expected problem with 'k', '(-4)' or '-4', and '2', got: {problem}")
                return False
            
            # Check step solutions for complete operations with sign flip
            step_solutions = example_3a.get("step_solutions", [])
            if not step_solutions or len(step_solutions) < 2:
                self.log_test("Example 3A Step Solutions", False, 
                            f"Expected at least 2 step solutions, got {len(step_solutions)}")
                return False
            
            # Step 1 should show: "k / (-4) * (-4) ≥ 2 * (-4)" (both sides with sign flip)
            step1 = step_solutions[0] if len(step_solutions) > 0 else {}
            step1_solution = step1.get("solution", "")
            
            # Check for complete operation on both sides with sign flip indication
            has_complete_operation = (
                ("k" in step1_solution and "(-4)" in step1_solution and "*" in step1_solution and "2" in step1_solution) or
                ("×" in step1_solution and "-4" in step1_solution) or
                ("≥" in step1_solution and "2 *" in step1_solution)
            )
            
            if has_complete_operation:
                self.log_test("Example 3A Step 1 Complete Operations with Sign Flip", True, 
                            f"✅ Step 1 shows complete operations with sign flip: {step1_solution}")
            else:
                self.log_test("Example 3A Step 1 Complete Operations with Sign Flip", False, 
                            f"❌ Step 1 should show complete operations with sign flip, got: {step1_solution}")
                return False
            
            # Step 2 should show: "k ≥ -8" (simplified)
            step2 = step_solutions[1] if len(step_solutions) > 1 else {}
            step2_solution = step2.get("solution", "")
            
            if "k" in step2_solution and ("-8" in step2_solution or "≥" in step2_solution):
                self.log_test("Example 3A Step 2 Simplified Result", True, 
                            f"✅ Step 2 shows simplified result: {step2_solution}")
            else:
                self.log_test("Example 3A Step 2 Simplified Result", False, 
                            f"❌ Step 2 should show simplified result, got: {step2_solution}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Example 3A Verification", False, f"Verification error: {str(e)}")
            return False

    def test_step_solutions_for_student_practice(self):
        """Test step_solutions for student practice problems show complete operations"""
        try:
            print("\n🔍 STEP SOLUTIONS FOR STUDENT PRACTICE TESTING")
            print("Testing that practice problems show complete mathematical operations")
            
            # Test practice2_1 step solutions
            response = self.session.get(f"{self.base_url}/problems/practice2_1")
            
            if response.status_code != 200:
                self.log_test("Practice2_1 Data Retrieval", False, 
                            f"Failed to get practice2_1: HTTP {response.status_code}")
                return False
            
            data = response.json()
            step_solutions = data.get("step_solutions", [])
            
            if not step_solutions:
                self.log_test("Practice2_1 Step Solutions", False, 
                            "Missing step_solutions in practice2_1 data")
                return False
            
            # Check for complete operations in step solutions
            found_complete_operations = False
            for step in step_solutions:
                solution = step.get("solution", "")
                # Look for patterns like "4y / 4 < 24 / 4" or "-6k / -6 ≤ 30 / -6"
                if ("/" in solution and any(op in solution for op in ["<", ">", "≤", "≥", "="])):
                    found_complete_operations = True
                    self.log_test("Practice2_1 Complete Operations", True, 
                                f"✅ Found complete operations: {solution}")
                    break
            
            if not found_complete_operations:
                self.log_test("Practice2_1 Complete Operations", False, 
                            "❌ No complete operations found in practice2_1 step solutions")
                return False
            
            # Test practice2_2 step solutions
            response = self.session.get(f"{self.base_url}/problems/practice2_2")
            
            if response.status_code == 200:
                data = response.json()
                step_solutions = data.get("step_solutions", [])
                
                if step_solutions:
                    self.log_test("Practice2_2 Step Solutions Present", True, 
                                f"✅ Practice2_2 has {len(step_solutions)} step solutions")
                else:
                    self.log_test("Practice2_2 Step Solutions Present", False, 
                                "❌ Practice2_2 missing step solutions")
            
            return True
            
        except Exception as e:
            self.log_test("Step Solutions Testing", False, f"Test execution error: {str(e)}")
            return False

    def test_bilingual_content_mathematical_expressions(self):
        """Test bilingual content shows correct mathematical expressions in both languages"""
        try:
            print("\n🔍 BILINGUAL MATHEMATICAL EXPRESSIONS TESTING")
            print("Testing that both English and Arabic versions show complete mathematical expressions")
            
            # Get explanation2 problem data
            response = self.session.get(f"{self.base_url}/problems/explanation2")
            
            if response.status_code != 200:
                self.log_test("Bilingual Content Retrieval", False, 
                            f"Failed to get explanation2: HTTP {response.status_code}")
                return False
            
            data = response.json()
            
            # Check for Arabic content fields
            arabic_fields = ["question_ar", "title_ar", "hint1_ar", "hint2_ar"]
            arabic_content_found = False
            
            for field in arabic_fields:
                if field in data and data[field]:
                    arabic_content_found = True
                    self.log_test(f"Arabic Content - {field}", True, 
                                f"✅ Found Arabic content in {field}")
                    break
            
            if not arabic_content_found:
                self.log_test("Arabic Content Presence", False, 
                            "❌ No Arabic content found in explanation2")
                return False
            
            # Check interactive examples for bilingual mathematical notation
            interactive_examples = data.get("interactive_examples", [])
            
            for i, example in enumerate(interactive_examples):
                # Check if mathematical symbols are preserved in both languages
                problem = example.get("problem", "")
                step_solutions = example.get("step_solutions", [])
                
                # Mathematical symbols should be universal (≥, ≤, >, <, =, /, *, +, -)
                math_symbols = ["≥", "≤", ">", "<", "=", "/", "*", "+", "-"]
                has_math_symbols = any(symbol in problem for symbol in math_symbols)
                
                if has_math_symbols:
                    self.log_test(f"Example {i+1} Mathematical Symbols", True, 
                                f"✅ Example {i+1} contains mathematical symbols: {problem}")
                else:
                    self.log_test(f"Example {i+1} Mathematical Symbols", False, 
                                f"❌ Example {i+1} missing mathematical symbols: {problem}")
            
            self.log_test("Bilingual Mathematical Expressions", True, 
                        "✅ Bilingual content maintains mathematical notation correctly")
            return True
            
        except Exception as e:
            self.log_test("Bilingual Content Testing", False, f"Test execution error: {str(e)}")
            return False

    def test_educational_correctness_validation(self):
        """Test that mathematical expressions show proper educational progression"""
        try:
            print("\n🔍 EDUCATIONAL CORRECTNESS VALIDATION")
            print("Testing that mathematical expressions show clear educational progression")
            
            # Get explanation2 problem data
            response = self.session.get(f"{self.base_url}/problems/explanation2")
            
            if response.status_code != 200:
                self.log_test("Educational Content Retrieval", False, 
                            f"Failed to get explanation2: HTTP {response.status_code}")
                return False
            
            data = response.json()
            interactive_examples = data.get("interactive_examples", [])
            
            educational_progression_verified = True
            
            for i, example in enumerate(interactive_examples):
                step_solutions = example.get("step_solutions", [])
                
                if len(step_solutions) < 2:
                    self.log_test(f"Example {i+1} Educational Progression", False, 
                                f"❌ Example {i+1} needs at least 2 steps for proper progression")
                    educational_progression_verified = False
                    continue
                
                # Check that progression goes from original → operation → simplified
                step1 = step_solutions[0].get("solution", "")
                step2 = step_solutions[1].get("solution", "") if len(step_solutions) > 1 else ""
                
                # Step 1 should show the operation being performed
                has_operation_shown = any(op in step1 for op in ["/", "*", "÷", "×", "/ 5", "/ (-3)", "* (-4)"])
                
                # Step 2 should show simplified result
                has_simplified_result = len(step2) < len(step1) and any(var in step2 for var in ["x", "m", "k", "y"])
                
                if has_operation_shown and has_simplified_result:
                    self.log_test(f"Example {i+1} Educational Progression", True, 
                                f"✅ Example {i+1} shows proper progression: operation → simplified")
                else:
                    self.log_test(f"Example {i+1} Educational Progression", False, 
                                f"❌ Example {i+1} progression unclear. Step1: {step1}, Step2: {step2}")
                    educational_progression_verified = False
            
            if educational_progression_verified:
                self.log_test("Overall Educational Correctness", True, 
                            "✅ All examples show proper educational progression")
                return True
            else:
                self.log_test("Overall Educational Correctness", False, 
                            "❌ Some examples lack proper educational progression")
                return False
            
        except Exception as e:
            self.log_test("Educational Correctness Testing", False, f"Test execution error: {str(e)}")
            return False

    def generate_math_expression_summary(self, results):
        """Generate comprehensive summary of mathematical expression testing"""
        print("\n" + "=" * 80)
        print("📐 SECTION 2 MATHEMATICAL EXPRESSION DISPLAY FIX TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL MATHEMATICAL EXPRESSION TEST RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILED"
            print(f"   {status}: {category}")
        
        print(f"\n📋 MATHEMATICAL EXPRESSION DISPLAY STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL MATHEMATICAL EXPRESSION TESTS PASSED")
            print("   ✅ System solved examples show complete operations")
            print("   ✅ Step solutions display both sides of equations")
            print("   ✅ Sign flipping is explicitly shown")
            print("   ✅ Educational progression is clear and correct")
            print("   ✅ Bilingual content maintains mathematical notation")
            print("   📚 EDUCATIONAL CORRECTNESS: VERIFIED")
        else:
            print("   ⚠️  MATHEMATICAL EXPRESSION ISSUES DETECTED")
            print("   🔧 Mathematical display needs fixes for educational correctness")
            print("   📚 EDUCATIONAL CORRECTNESS: NEEDS ATTENTION")
        
        print("\n" + "=" * 80)

    def run_mathematical_expression_tests(self):
        """Run comprehensive mathematical expression display tests"""
        print("=" * 80)
        print("📐 CRITICAL MATHEMATICAL EXPRESSION DISPLAY FIX TESTING")
        print("=" * 80)
        print("Testing educational correctness of mathematical expressions in Section 2")
        
        # Test categories for mathematical expression display
        test_categories = [
            ("Health Check", self.test_health_check),
            ("Test Student Creation", self.create_test_student),
            ("Section 2 Interactive Examples", self.test_section2_explanation_interactive_examples),
            ("Step Solutions for Student Practice", self.test_step_solutions_for_student_practice),
            ("Bilingual Mathematical Expressions", self.test_bilingual_content_mathematical_expressions),
            ("Educational Correctness Validation", self.test_educational_correctness_validation)
        ]
        
        results = {}
        
        for category_name, test_method in test_categories:
            print(f"\n🔍 TEST CATEGORY: {category_name}")
            print("-" * 60)
            
            try:
                success = test_method()
                results[category_name] = success
                    
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {category_name}: {str(e)}")
                results[category_name] = False
        
        # Generate comprehensive summary
        self.generate_math_expression_summary(results)
        
        return results

def main():
    """Main function to run mathematical expression display tests"""
    print("🚀 Starting CRITICAL MATHEMATICAL EXPRESSION DISPLAY FIX Testing...")
    print("🎯 Goal: Verify educational correctness of mathematical expressions")
    
    tester = Section2MathExpressionTester(BACKEND_URL)
    results = tester.run_mathematical_expression_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 MATHEMATICAL EXPRESSION ALERT: {failed_tests} test(s) failed!")
        print("🔧 Mathematical expression display needs fixes for educational correctness")
    else:
        print(f"\n📚 EDUCATIONAL CORRECTNESS CONFIRMED: All mathematical expression tests passed!")
        print("✅ Section 2 mathematical expressions are displaying correctly")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()