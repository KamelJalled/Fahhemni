#!/usr/bin/env python3
"""
Section 3 Comprehensive Content Implementation Test Suite
Tests the new Section 3 Multi-Step Inequalities implementation as requested.

TESTING REQUIREMENTS:
1. Section 3 API Endpoints - GET /api/problems/section/section3 for all 6 problems
2. Individual Problem Endpoints - Test each problem (prep3, explanation3, practice3_1, practice3_2, assessment3, examprep3)
3. New Problem Structure - Verify comprehensive explanation3 with 3-level structure
4. Word Problem Implementation - Check practice3_2 car rental word problem with 3-step structure
5. Step Solutions Validation - Test step_solutions arrays contain correct possible_answers
6. Bilingual Content - Verify both English and Arabic content
7. Updated Problem Content - Confirm specific changes to prep3, assessment3, examprep3
8. Database updates and API accessibility

EXPECTED SECTION 3 STRUCTURE:
- prep3: "2x + 5 > 15" with answer "x > 5" (changed from "2(x + 3) > 10")
- explanation3: 3-level structure (Simple, Negative Coefficient, Distributive Property)
- practice3_1: Classic practice problem (2 steps)
- practice3_2: Car rental word problem (3 steps, stage_type: "practice_word")
- assessment3: "(x + 3) / 2 ≤ 5" with answer "x ≤ 7"
- examprep3: "3(1 - k) < 12" with answer "k > -3"
"""

import requests
import json
import sys
import os
from datetime import datetime

# Use backend URL from frontend/.env
BACKEND_URL = "https://math-bug-fixes.preview.emergentagent.com/api"

class Section3Tester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "section3_test_student"
        
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
        """Create test student for Section 3 testing"""
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

    def test_section3_api_endpoint(self):
        """Test GET /api/problems/section/section3 returns all 6 problems"""
        try:
            print("\n🎯 SECTION 3 API ENDPOINT TESTING")
            print("Testing GET /api/problems/section/section3 for all 6 problems")
            
            response = self.session.get(f"{self.base_url}/problems/section/section3")
            
            if response.status_code == 200:
                problems = response.json()
                
                print(f"   Found {len(problems)} problems in Section 3")
                
                # CRITICAL TEST 1: Should have exactly 6 problems
                if len(problems) != 6:
                    self.log_test("Section 3 API Endpoint", False, 
                                f"❌ Expected 6 problems, got {len(problems)}")
                    return False
                
                # CRITICAL TEST 2: Verify all expected problem IDs exist
                expected_problems = ["prep3", "explanation3", "practice3_1", "practice3_2", "assessment3", "examprep3"]
                found_problems = [p.get('id') for p in problems]
                
                print(f"   Expected problems: {expected_problems}")
                print(f"   Found problems: {found_problems}")
                
                missing_problems = [p for p in expected_problems if p not in found_problems]
                if missing_problems:
                    self.log_test("Section 3 API Endpoint", False, 
                                f"❌ Missing problems: {missing_problems}")
                    return False
                
                # CRITICAL TEST 3: Verify problem types are correct
                problem_types = {p.get('id'): p.get('type') for p in problems}
                expected_types = {
                    "prep3": "preparation",
                    "explanation3": "explanation", 
                    "practice3_1": "practice",
                    "practice3_2": "practice",
                    "assessment3": "assessment",
                    "examprep3": "examprep"
                }
                
                for problem_id, expected_type in expected_types.items():
                    actual_type = problem_types.get(problem_id)
                    if actual_type != expected_type:
                        self.log_test("Section 3 API Endpoint", False, 
                                    f"❌ {problem_id} has type '{actual_type}', expected '{expected_type}'")
                        return False
                
                self.log_test("Section 3 API Endpoint", True, 
                            f"✅ Section 3 contains all 6 expected problems with correct types")
                return True
                
            else:
                self.log_test("Section 3 API Endpoint", False, 
                            f"Failed to get Section 3 problems: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Section 3 API Endpoint", False, f"Test execution error: {str(e)}")
            return False

    def test_individual_problem_endpoints(self):
        """Test each individual problem endpoint"""
        try:
            print("\n🎯 INDIVIDUAL PROBLEM ENDPOINTS TESTING")
            print("Testing each Section 3 problem endpoint individually")
            
            problems_to_test = ["prep3", "explanation3", "practice3_1", "practice3_2", "assessment3", "examprep3"]
            all_problems_working = True
            
            for problem_id in problems_to_test:
                print(f"\n   Testing {problem_id} endpoint...")
                
                # For assessment and examprep, need username parameter
                if problem_id in ["assessment3", "examprep3"]:
                    response = self.session.get(
                        f"{self.base_url}/problems/{problem_id}",
                        params={"username": self.test_student_username}
                    )
                else:
                    response = self.session.get(f"{self.base_url}/problems/{problem_id}")
                
                if response.status_code == 200:
                    problem_data = response.json()
                    
                    # Verify basic structure
                    required_fields = ["id", "type", "question_en", "question_ar"]
                    missing_fields = [field for field in required_fields if field not in problem_data]
                    
                    if missing_fields:
                        print(f"     ❌ Missing fields: {missing_fields}")
                        all_problems_working = False
                    else:
                        print(f"     ✅ {problem_id} accessible with all required fields")
                        print(f"     Question EN: {problem_data.get('question_en', 'N/A')[:50]}...")
                        print(f"     Question AR: {problem_data.get('question_ar', 'N/A')[:50]}...")
                        
                else:
                    print(f"     ❌ Failed to access {problem_id}: HTTP {response.status_code}")
                    all_problems_working = False
            
            if all_problems_working:
                self.log_test("Individual Problem Endpoints", True, 
                            f"✅ All 6 Section 3 problem endpoints are accessible")
                return True
            else:
                self.log_test("Individual Problem Endpoints", False, 
                            f"❌ Some Section 3 problem endpoints failed")
                return False
                
        except Exception as e:
            self.log_test("Individual Problem Endpoints", False, f"Test execution error: {str(e)}")
            return False

    def test_updated_problem_content(self):
        """Test updated problem content for prep3, assessment3, examprep3"""
        try:
            print("\n🎯 UPDATED PROBLEM CONTENT TESTING")
            print("Testing specific content changes for prep3, assessment3, examprep3")
            
            # Test prep3: Changed from "2(x + 3) > 10" to "2x + 5 > 15" with answer "x > 5"
            print("\n   Testing prep3 content update...")
            prep3_response = self.session.get(f"{self.base_url}/problems/prep3")
            
            if prep3_response.status_code == 200:
                prep3_data = prep3_response.json()
                
                expected_question = "2x + 5 > 15"
                expected_answer = "x > 5"
                
                actual_question = prep3_data.get('question_en', '')
                actual_answer = prep3_data.get('answer', '')
                
                print(f"     Expected Question: {expected_question}")
                print(f"     Actual Question: {actual_question}")
                print(f"     Expected Answer: {expected_answer}")
                print(f"     Actual Answer: {actual_answer}")
                
                if expected_question not in actual_question:
                    self.log_test("Updated Problem Content", False, 
                                f"❌ prep3 question not updated. Expected '{expected_question}', got '{actual_question}'")
                    return False
                
                if actual_answer != expected_answer:
                    self.log_test("Updated Problem Content", False, 
                                f"❌ prep3 answer not updated. Expected '{expected_answer}', got '{actual_answer}'")
                    return False
                
                print(f"     ✅ prep3 content correctly updated")
            else:
                self.log_test("Updated Problem Content", False, 
                            f"❌ Failed to get prep3: HTTP {prep3_response.status_code}")
                return False
            
            # Test assessment3: Changed to "(x + 3) / 2 ≤ 5" with answer "x ≤ 7"
            print("\n   Testing assessment3 content update...")
            assessment3_response = self.session.get(
                f"{self.base_url}/problems/assessment3",
                params={"username": self.test_student_username}
            )
            
            if assessment3_response.status_code == 200:
                assessment3_data = assessment3_response.json()
                
                expected_question = "(x + 3) / 2 ≤ 5"
                expected_answer = "x ≤ 7"
                
                actual_question = assessment3_data.get('question_en', '')
                actual_answer = assessment3_data.get('answer', '')
                
                print(f"     Expected Question: {expected_question}")
                print(f"     Actual Question: {actual_question}")
                print(f"     Expected Answer: {expected_answer}")
                print(f"     Actual Answer: {actual_answer}")
                
                if expected_question not in actual_question:
                    self.log_test("Updated Problem Content", False, 
                                f"❌ assessment3 question not updated. Expected '{expected_question}', got '{actual_question}'")
                    return False
                
                if actual_answer != expected_answer:
                    self.log_test("Updated Problem Content", False, 
                                f"❌ assessment3 answer not updated. Expected '{expected_answer}', got '{actual_answer}'")
                    return False
                
                print(f"     ✅ assessment3 content correctly updated")
            else:
                self.log_test("Updated Problem Content", False, 
                            f"❌ Failed to get assessment3: HTTP {assessment3_response.status_code}")
                return False
            
            # Test examprep3: Changed to "3(1 - k) < 12" with answer "k > -3"
            print("\n   Testing examprep3 content update...")
            examprep3_response = self.session.get(
                f"{self.base_url}/problems/examprep3",
                params={"username": self.test_student_username}
            )
            
            if examprep3_response.status_code == 200:
                examprep3_data = examprep3_response.json()
                
                expected_question = "3(1 - k) < 12"
                expected_answer = "k > -3"
                
                actual_question = examprep3_data.get('question_en', '')
                actual_answer = examprep3_data.get('answer', '')
                
                print(f"     Expected Question: {expected_question}")
                print(f"     Actual Question: {actual_question}")
                print(f"     Expected Answer: {expected_answer}")
                print(f"     Actual Answer: {actual_answer}")
                
                if expected_question not in actual_question:
                    self.log_test("Updated Problem Content", False, 
                                f"❌ examprep3 question not updated. Expected '{expected_question}', got '{actual_question}'")
                    return False
                
                if actual_answer != expected_answer:
                    self.log_test("Updated Problem Content", False, 
                                f"❌ examprep3 answer not updated. Expected '{expected_answer}', got '{actual_answer}'")
                    return False
                
                print(f"     ✅ examprep3 content correctly updated")
            else:
                self.log_test("Updated Problem Content", False, 
                            f"❌ Failed to get examprep3: HTTP {examprep3_response.status_code}")
                return False
            
            self.log_test("Updated Problem Content", True, 
                        f"✅ All problem content updates verified correctly")
            return True
                
        except Exception as e:
            self.log_test("Updated Problem Content", False, f"Test execution error: {str(e)}")
            return False

    def test_explanation3_structure(self):
        """Test comprehensive explanation3 problem with 3-level structure"""
        try:
            print("\n🎯 EXPLANATION3 STRUCTURE TESTING")
            print("Testing comprehensive explanation3 with 3-level structure")
            
            response = self.session.get(f"{self.base_url}/problems/explanation3")
            
            if response.status_code == 200:
                explanation3_data = response.json()
                
                # CRITICAL TEST 1: Should have interactive_examples
                interactive_examples = explanation3_data.get('interactive_examples', [])
                if not interactive_examples:
                    self.log_test("Explanation3 Structure", False, 
                                f"❌ explanation3 missing interactive_examples")
                    return False
                
                print(f"   Found {len(interactive_examples)} interactive examples")
                
                # CRITICAL TEST 2: Should have 3 levels (Simple, Negative Coefficient, Distributive Property)
                expected_levels = [
                    "Simple",
                    "Negative Coefficient", 
                    "Distributive Property"
                ]
                
                found_levels = []
                for example in interactive_examples:
                    title = example.get('title_en', '')
                    for level in expected_levels:
                        if level.lower() in title.lower():
                            found_levels.append(level)
                            break
                
                print(f"   Expected levels: {expected_levels}")
                print(f"   Found levels: {found_levels}")
                
                missing_levels = [level for level in expected_levels if level not in found_levels]
                if missing_levels:
                    self.log_test("Explanation3 Structure", False, 
                                f"❌ Missing levels: {missing_levels}")
                    return False
                
                # CRITICAL TEST 3: Check for step_solutions in interactive examples
                examples_with_steps = 0
                for example in interactive_examples:
                    if 'step_solutions' in example:
                        examples_with_steps += 1
                        step_solutions = example['step_solutions']
                        print(f"   Example has {len(step_solutions)} step solutions")
                
                if examples_with_steps == 0:
                    self.log_test("Explanation3 Structure", False, 
                                f"❌ No interactive examples have step_solutions")
                    return False
                
                # CRITICAL TEST 4: Verify bilingual content
                bilingual_check = True
                for example in interactive_examples:
                    if not example.get('title_ar') or not example.get('problem_ar'):
                        bilingual_check = False
                        break
                
                if not bilingual_check:
                    self.log_test("Explanation3 Structure", False, 
                                f"❌ Some interactive examples missing Arabic content")
                    return False
                
                self.log_test("Explanation3 Structure", True, 
                            f"✅ explanation3 has correct 3-level structure with bilingual content")
                return True
                
            else:
                self.log_test("Explanation3 Structure", False, 
                            f"Failed to get explanation3: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Explanation3 Structure", False, f"Test execution error: {str(e)}")
            return False

    def test_practice3_2_word_problem(self):
        """Test practice3_2 car rental word problem with 3-step structure"""
        try:
            print("\n🎯 PRACTICE3_2 WORD PROBLEM TESTING")
            print("Testing practice3_2 car rental word problem with 3-step structure")
            
            response = self.session.get(f"{self.base_url}/problems/practice3_2")
            
            if response.status_code == 200:
                practice3_2_data = response.json()
                
                # CRITICAL TEST 1: Should be a word problem about car rental
                question_en = practice3_2_data.get('question_en', '')
                print(f"   Question: {question_en}")
                
                car_rental_keywords = ['car rental', 'rental', 'kilometer', 'budget', 'distance']
                if not any(keyword in question_en.lower() for keyword in car_rental_keywords):
                    self.log_test("Practice3_2 Word Problem", False, 
                                f"❌ practice3_2 doesn't appear to be car rental word problem")
                    return False
                
                # CRITICAL TEST 2: Should have stage_type: "practice_word"
                stage_type = practice3_2_data.get('stage_type')
                if stage_type != "practice_word":
                    self.log_test("Practice3_2 Word Problem", False, 
                                f"❌ practice3_2 stage_type is '{stage_type}', expected 'practice_word'")
                    return False
                
                print(f"   ✅ stage_type correctly set to: {stage_type}")
                
                # CRITICAL TEST 3: Should have 3-step structure
                step_solutions = practice3_2_data.get('step_solutions', [])
                if len(step_solutions) != 3:
                    self.log_test("Practice3_2 Word Problem", False, 
                                f"❌ practice3_2 has {len(step_solutions)} steps, expected 3")
                    return False
                
                print(f"   ✅ Found {len(step_solutions)} step solutions (expected 3)")
                
                # CRITICAL TEST 4: Verify step content
                expected_step_keywords = [
                    ['write', 'inequality'],  # Step 1: Write inequality
                    ['subtract', 'fixed', 'cost'],  # Step 2: Subtract fixed cost
                    ['calculate', 'maximum', 'kilometers']  # Step 3: Calculate maximum
                ]
                
                for i, step in enumerate(step_solutions):
                    step_text = step.get('step_en', '').lower()
                    possible_answers = step.get('possible_answers', [])
                    
                    print(f"   Step {i+1}: {step.get('step_en', 'N/A')}")
                    print(f"   Possible Answers: {possible_answers}")
                    
                    if not possible_answers:
                        self.log_test("Practice3_2 Word Problem", False, 
                                    f"❌ Step {i+1} missing possible_answers")
                        return False
                    
                    # Check if step contains expected keywords
                    expected_keywords = expected_step_keywords[i]
                    if not any(keyword in step_text for keyword in expected_keywords):
                        print(f"   ⚠️  Step {i+1} may not match expected content pattern")
                
                # CRITICAL TEST 5: Verify final answer
                expected_answer = "k ≤ 75"
                actual_answer = practice3_2_data.get('answer', '')
                
                if actual_answer != expected_answer:
                    self.log_test("Practice3_2 Word Problem", False, 
                                f"❌ practice3_2 answer is '{actual_answer}', expected '{expected_answer}'")
                    return False
                
                print(f"   ✅ Final answer correctly set to: {actual_answer}")
                
                self.log_test("Practice3_2 Word Problem", True, 
                            f"✅ practice3_2 car rental word problem correctly implemented with 3-step structure")
                return True
                
            else:
                self.log_test("Practice3_2 Word Problem", False, 
                            f"Failed to get practice3_2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Practice3_2 Word Problem", False, f"Test execution error: {str(e)}")
            return False

    def test_step_solutions_validation(self):
        """Test that step_solutions arrays contain correct possible_answers"""
        try:
            print("\n🎯 STEP SOLUTIONS VALIDATION TESTING")
            print("Testing step_solutions arrays contain correct possible_answers for multi-step problems")
            
            problems_with_steps = ["prep3", "practice3_1", "practice3_2"]
            all_validations_passed = True
            
            for problem_id in problems_with_steps:
                print(f"\n   Testing {problem_id} step solutions...")
                
                response = self.session.get(f"{self.base_url}/problems/{problem_id}")
                
                if response.status_code == 200:
                    problem_data = response.json()
                    step_solutions = problem_data.get('step_solutions', [])
                    
                    if not step_solutions:
                        print(f"     ❌ {problem_id} missing step_solutions")
                        all_validations_passed = False
                        continue
                    
                    print(f"     Found {len(step_solutions)} step solutions")
                    
                    # Validate each step
                    for i, step in enumerate(step_solutions):
                        step_en = step.get('step_en', '')
                        step_ar = step.get('step_ar', '')
                        possible_answers = step.get('possible_answers', [])
                        possible_answers_ar = step.get('possible_answers_ar', [])
                        
                        print(f"     Step {i+1} EN: {step_en}")
                        print(f"     Step {i+1} AR: {step_ar}")
                        print(f"     Possible Answers EN: {possible_answers}")
                        print(f"     Possible Answers AR: {possible_answers_ar}")
                        
                        # CRITICAL VALIDATION 1: Must have possible_answers
                        if not possible_answers:
                            print(f"     ❌ Step {i+1} missing possible_answers")
                            all_validations_passed = False
                        
                        # CRITICAL VALIDATION 2: Must have Arabic possible_answers
                        if not possible_answers_ar:
                            print(f"     ❌ Step {i+1} missing possible_answers_ar")
                            all_validations_passed = False
                        
                        # CRITICAL VALIDATION 3: Answers should be non-empty strings
                        empty_answers = [ans for ans in possible_answers if not ans.strip()]
                        if empty_answers:
                            print(f"     ❌ Step {i+1} has empty possible_answers")
                            all_validations_passed = False
                        
                        if all([possible_answers, possible_answers_ar, not empty_answers]):
                            print(f"     ✅ Step {i+1} validation passed")
                    
                else:
                    print(f"     ❌ Failed to get {problem_id}: HTTP {response.status_code}")
                    all_validations_passed = False
            
            if all_validations_passed:
                self.log_test("Step Solutions Validation", True, 
                            f"✅ All step_solutions arrays contain correct possible_answers")
                return True
            else:
                self.log_test("Step Solutions Validation", False, 
                            f"❌ Some step_solutions validation issues found")
                return False
                
        except Exception as e:
            self.log_test("Step Solutions Validation", False, f"Test execution error: {str(e)}")
            return False

    def test_bilingual_content(self):
        """Test that all Section 3 problems have proper bilingual content"""
        try:
            print("\n🎯 BILINGUAL CONTENT TESTING")
            print("Testing that all Section 3 problems have proper English and Arabic content")
            
            # Get all Section 3 problems
            response = self.session.get(f"{self.base_url}/problems/section/section3")
            
            if response.status_code == 200:
                problems = response.json()
                all_bilingual = True
                
                for problem in problems:
                    problem_id = problem.get('id')
                    print(f"\n   Testing {problem_id} bilingual content...")
                    
                    # CRITICAL TEST 1: Must have both English and Arabic questions
                    question_en = problem.get('question_en', '')
                    question_ar = problem.get('question_ar', '')
                    
                    if not question_en:
                        print(f"     ❌ Missing question_en")
                        all_bilingual = False
                    
                    if not question_ar:
                        print(f"     ❌ Missing question_ar")
                        all_bilingual = False
                    
                    # CRITICAL TEST 2: Must have both English and Arabic answers (if not explanation)
                    if problem.get('type') != 'explanation':
                        answer_en = problem.get('answer', '')
                        answer_ar = problem.get('answer_ar', '')
                        
                        if not answer_en:
                            print(f"     ❌ Missing answer")
                            all_bilingual = False
                        
                        if not answer_ar:
                            print(f"     ❌ Missing answer_ar")
                            all_bilingual = False
                    
                    # CRITICAL TEST 3: Check hints if they exist
                    hints_en = problem.get('hints_en', [])
                    hints_ar = problem.get('hints_ar', [])
                    
                    if hints_en and not hints_ar:
                        print(f"     ❌ Has hints_en but missing hints_ar")
                        all_bilingual = False
                    
                    if hints_ar and not hints_en:
                        print(f"     ❌ Has hints_ar but missing hints_en")
                        all_bilingual = False
                    
                    # CRITICAL TEST 4: Check step_solutions bilingual content
                    step_solutions = problem.get('step_solutions', [])
                    for i, step in enumerate(step_solutions):
                        step_en = step.get('step_en', '')
                        step_ar = step.get('step_ar', '')
                        
                        if not step_en:
                            print(f"     ❌ Step {i+1} missing step_en")
                            all_bilingual = False
                        
                        if not step_ar:
                            print(f"     ❌ Step {i+1} missing step_ar")
                            all_bilingual = False
                    
                    if all([question_en, question_ar]):
                        print(f"     ✅ {problem_id} bilingual content verified")
                
                if all_bilingual:
                    self.log_test("Bilingual Content", True, 
                                f"✅ All Section 3 problems have proper bilingual content")
                    return True
                else:
                    self.log_test("Bilingual Content", False, 
                                f"❌ Some Section 3 problems missing bilingual content")
                    return False
                
            else:
                self.log_test("Bilingual Content", False, 
                            f"Failed to get Section 3 problems: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Bilingual Content", False, f"Test execution error: {str(e)}")
            return False

    def generate_section3_summary(self, results, critical_failures):
        """Generate comprehensive summary of Section 3 testing"""
        print("\n" + "=" * 80)
        print("🎯 SECTION 3 COMPREHENSIVE CONTENT IMPLEMENTATION TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL SECTION 3 TESTING RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL SECTION 3 ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  SECTION 3 STATUS: INCOMPLETE - Implementation needs fixes!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix remaining Section 3 issues")
        else:
            print(f"\n🎉 NO CRITICAL SECTION 3 ISSUES DETECTED")
        
        print(f"\n📋 SECTION 3 IMPLEMENTATION STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL SECTION 3 TESTS PASSED")
            print("   ✅ Section 3 API endpoints working")
            print("   ✅ All 6 problems accessible")
            print("   ✅ Problem content updates verified")
            print("   ✅ 3-level explanation structure implemented")
            print("   ✅ Car rental word problem with 3-step structure")
            print("   ✅ Step solutions validation working")
            print("   ✅ Bilingual content complete")
            print("   🛡️  SECTION 3: FULLY IMPLEMENTED")
        else:
            print("   ⚠️  SECTION 3 IMPLEMENTATION ISSUES DETECTED")
            print("   🔧 Section 3 content needs enhancement")
            print("   🚨 STUDENT EXPERIENCE: MAY BE BROKEN FOR SECTION 3")
        
        print("\n" + "=" * 80)

    def run_section3_tests(self):
        """Run comprehensive Section 3 implementation tests"""
        print("=" * 80)
        print("🎯 SECTION 3 COMPREHENSIVE CONTENT IMPLEMENTATION TESTING")
        print("=" * 80)
        print("Testing new Section 3 Multi-Step Inequalities implementation")
        
        # Test categories for Section 3
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("Section 3 API Endpoint", self.test_section3_api_endpoint, "critical"),
            ("Individual Problem Endpoints", self.test_individual_problem_endpoints, "critical"),
            ("Updated Problem Content", self.test_updated_problem_content, "critical"),
            ("Explanation3 Structure", self.test_explanation3_structure, "critical"),
            ("Practice3_2 Word Problem", self.test_practice3_2_word_problem, "critical"),
            ("Step Solutions Validation", self.test_step_solutions_validation, "critical"),
            ("Bilingual Content", self.test_bilingual_content, "high")
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
    """Main function to run Section 3 tests"""
    print("🚀 Starting SECTION 3 COMPREHENSIVE CONTENT IMPLEMENTATION Testing...")
    print("🎯 Goal: Verify new Section 3 Multi-Step Inequalities implementation")
    
    tester = Section3Tester(BACKEND_URL)
    results = tester.run_section3_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 SECTION 3 ALERT: {failed_tests} test(s) failed!")
        print("🔧 Section 3 implementation needs backend enhancement")
    else:
        print(f"\n🛡️  SECTION 3 CONFIRMED: All tests passed!")
        print("✅ Section 3 comprehensive content implementation is working correctly")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()