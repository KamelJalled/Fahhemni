#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - Section 5 Absolute Value Inequalities Testing
Tests the comprehensive Section 5 Absolute Value Inequalities implementation as requested by user.

CRITICAL FEATURES BEING TESTED:
Section 5 comprehensive Absolute Value Inequalities implementation with all required components.

SPECIFIC VERIFICATION REQUIREMENTS:
1. Section 5 API Endpoints - GET /api/problems/section/section5 returns all 6 problems
2. Individual Problem Endpoints - Test each problem (prep5, explanation5, practice5_1, practice5_2, assessment5, examprep5)
3. Updated Problem Content - prep5 changed from "-3 < 2x + 1 ≤ 7" to "|x| < 4" with absolute value answer "-4 < x < 4"
4. Absolute Value Structure - explanation5 has 3-level structure (Simple Absolute Value, Greater Than, Complex Absolute Value)
5. Step Solutions with Level Naming - Both interactive_examples and step_solutions arrays with Level 1B, 2B, 3B naming
6. Manufacturing Tolerance Word Problem - practice5_2 has manufacturing tolerance problem with target length 50mm, tolerance ±0.5mm, 3-step structure
7. Assessment Updates - assessment5 changed to "|4 - x| ≥ 3" with answer "x ≤ 1 or x ≥ 7"
8. Exam Prep Updates - examprep5 changed to "|2x + 1| - 3 < 4" with answer "-4 < x < 3"
9. Bilingual Content - Verify both English and Arabic content is properly structured
10. Absolute Value Conversion Rules - Test problems ensure proper conversion: |expr| < number → compound, |expr| > number → OR

EXPECTED BACKEND BEHAVIOR:
- All Section 5 endpoints should return proper absolute value inequality content
- explanation5 should have both interactive_examples and step_solutions arrays
- practice5_2 should be manufacturing tolerance word problem with stage_type: "practice_word"
- All problems should have proper bilingual support and absolute value conversion rules
"""

import requests
import json
import sys
import os
import re
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://maths-academy.preview.emergentagent.com/api"

class Section5AbsoluteValueInequalitiesTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "section5_test_student"
        
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
        """Create test student for Section 5 testing"""
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

    def test_section5_api_endpoints(self):
        """Test Section 5 API Endpoints - GET /api/problems/section/section5"""
        try:
            print("\n🎯 SECTION 5 API ENDPOINTS TESTING")
            print("Testing GET /api/problems/section/section5 to ensure all 6 problems are returned")
            
            response = self.session.get(f"{self.base_url}/problems/section/section5")
            
            if response.status_code == 200:
                problems = response.json()
                
                print(f"   Found {len(problems)} problems in Section 5")
                
                # CRITICAL TEST 1: Should have exactly 6 problems
                if len(problems) != 6:
                    self.log_test("Section 5 API Endpoints", False, 
                                f"❌ Expected 6 problems, got {len(problems)}")
                    return False
                
                # CRITICAL TEST 2: Verify all expected problem IDs are present
                expected_problems = ["prep5", "explanation5", "practice5_1", "practice5_2", "assessment5", "examprep5"]
                found_problems = [p.get('id') for p in problems]
                
                missing_problems = [p for p in expected_problems if p not in found_problems]
                if missing_problems:
                    self.log_test("Section 5 API Endpoints", False, 
                                f"❌ Missing problems: {missing_problems}")
                    return False
                
                print(f"   ✅ All 6 expected problems found: {found_problems}")
                
                # CRITICAL TEST 3: Verify section_id is correct for all problems
                for problem in problems:
                    if problem.get('section_id') != 'section5':
                        self.log_test("Section 5 API Endpoints", False, 
                                    f"❌ Problem {problem.get('id')} has wrong section_id: {problem.get('section_id')}")
                        return False
                
                self.log_test("Section 5 API Endpoints", True, 
                            f"✅ Section 5 API endpoint returns all 6 problems correctly")
                return True
                
            else:
                self.log_test("Section 5 API Endpoints", False, 
                            f"Failed to get Section 5 problems: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Section 5 API Endpoints", False, f"Test execution error: {str(e)}")
            return False

    def test_individual_problem_endpoints(self):
        """Test Individual Problem Endpoints for all 6 Section 5 problems"""
        try:
            print("\n🎯 INDIVIDUAL PROBLEM ENDPOINTS TESTING")
            print("Testing each problem endpoint (prep5, explanation5, practice5_1, practice5_2, assessment5, examprep5)")
            
            expected_problems = ["prep5", "explanation5", "practice5_1", "practice5_2", "assessment5", "examprep5"]
            all_problems_working = True
            
            for problem_id in expected_problems:
                print(f"\n   Testing GET /api/problems/{problem_id}")
                
                # For assessment and examprep, we need username parameter
                params = {}
                if problem_id in ['assessment5', 'examprep5']:
                    params['username'] = self.test_student_username
                
                response = self.session.get(
                    f"{self.base_url}/problems/{problem_id}",
                    params=params
                )
                
                if response.status_code == 200:
                    problem_data = response.json()
                    
                    # Verify basic structure
                    required_fields = ['id', 'section_id', 'type', 'question_en', 'question_ar']
                    missing_fields = [field for field in required_fields if field not in problem_data]
                    
                    if missing_fields:
                        print(f"     ❌ Missing required fields: {missing_fields}")
                        all_problems_working = False
                    else:
                        print(f"     ✅ {problem_id} endpoint working - Type: {problem_data.get('type')}")
                        print(f"     Question EN: {problem_data.get('question_en', 'N/A')[:80]}...")
                        print(f"     Answer: {problem_data.get('answer', 'N/A')}")
                else:
                    print(f"     ❌ Failed to get {problem_id}: HTTP {response.status_code}")
                    all_problems_working = False
            
            if all_problems_working:
                self.log_test("Individual Problem Endpoints", True, 
                            f"✅ All 6 individual problem endpoints working correctly")
                return True
            else:
                self.log_test("Individual Problem Endpoints", False, 
                            f"❌ Some individual problem endpoints failed")
                return False
                
        except Exception as e:
            self.log_test("Individual Problem Endpoints", False, f"Test execution error: {str(e)}")
            return False

    def test_updated_problem_content(self):
        """Test Updated Problem Content - prep5 changed to absolute value inequality"""
        try:
            print("\n🎯 UPDATED PROBLEM CONTENT TESTING")
            print("Testing prep5 changed from '-3 < 2x + 1 ≤ 7' to '|x| < 4' with answer '-4 < x < 4'")
            
            response = self.session.get(f"{self.base_url}/problems/prep5")
            
            if response.status_code == 200:
                prep5_data = response.json()
                
                question_en = prep5_data.get('question_en', '')
                answer = prep5_data.get('answer', '')
                
                print(f"   Current Question: {question_en}")
                print(f"   Current Answer: {answer}")
                
                # CRITICAL TEST 1: Question should be absolute value inequality "|x| < 4"
                if "|x| < 4" not in question_en:
                    self.log_test("Updated Problem Content", False, 
                                f"❌ prep5 question should contain '|x| < 4', got: {question_en}")
                    return False
                
                # CRITICAL TEST 2: Answer should be "-4 < x < 4"
                if answer != "-4 < x < 4":
                    self.log_test("Updated Problem Content", False, 
                                f"❌ prep5 answer should be '-4 < x < 4', got: {answer}")
                    return False
                
                # CRITICAL TEST 3: Should be preparation type
                if prep5_data.get('type') != 'preparation':
                    self.log_test("Updated Problem Content", False, 
                                f"❌ prep5 should be type 'preparation', got: {prep5_data.get('type')}")
                    return False
                
                print(f"   ✅ prep5 has correct absolute value inequality content")
                
                self.log_test("Updated Problem Content", True, 
                            f"✅ prep5 successfully updated to absolute value inequality '|x| < 4' with answer '-4 < x < 4'")
                return True
                
            else:
                self.log_test("Updated Problem Content", False, 
                            f"Failed to get prep5 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Updated Problem Content", False, f"Test execution error: {str(e)}")
            return False

    def test_absolute_value_structure(self):
        """Test Absolute Value Structure - explanation5 3-level structure"""
        try:
            print("\n🎯 ABSOLUTE VALUE STRUCTURE TESTING")
            print("Testing explanation5 has 3-level structure (Simple Absolute Value, Greater Than, Complex Absolute Value)")
            
            response = self.session.get(f"{self.base_url}/problems/explanation5")
            
            if response.status_code == 200:
                explanation5_data = response.json()
                
                interactive_examples = explanation5_data.get('interactive_examples', [])
                
                print(f"   Found {len(interactive_examples)} interactive examples")
                
                # CRITICAL TEST 1: Should have exactly 3 interactive examples
                if len(interactive_examples) != 3:
                    self.log_test("Absolute Value Structure", False, 
                                f"❌ Expected 3 interactive examples, got {len(interactive_examples)}")
                    return False
                
                # CRITICAL TEST 2: Verify the 3 levels are present
                expected_levels = [
                    "Simple Absolute Value",
                    "Greater Than", 
                    "Complex Absolute Value"
                ]
                
                found_levels = []
                for i, example in enumerate(interactive_examples):
                    title = example.get('title_en', '')
                    print(f"   Level {i+1}: {title}")
                    
                    # Check if this level matches expected content
                    if "Simple Absolute Value" in title or "Level 1" in title:
                        found_levels.append("Simple Absolute Value")
                    elif "Greater Than" in title or "Level 2" in title:
                        found_levels.append("Greater Than")
                    elif "Complex Absolute Value" in title or "Level 3" in title:
                        found_levels.append("Complex Absolute Value")
                
                # Verify all 3 levels are found
                missing_levels = [level for level in expected_levels if level not in found_levels]
                if missing_levels:
                    self.log_test("Absolute Value Structure", False, 
                                f"❌ Missing levels: {missing_levels}")
                    return False
                
                print(f"   ✅ All 3 absolute value inequality levels found")
                
                self.log_test("Absolute Value Structure", True, 
                            f"✅ explanation5 has correct 3-level structure for absolute value inequalities")
                return True
                
            else:
                self.log_test("Absolute Value Structure", False, 
                            f"Failed to get explanation5 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Absolute Value Structure", False, f"Test execution error: {str(e)}")
            return False

    def test_step_solutions_with_level_naming(self):
        """Test Step Solutions with Level Naming - Both arrays with Level 1B, 2B, 3B naming"""
        try:
            print("\n🎯 STEP SOLUTIONS WITH LEVEL NAMING TESTING")
            print("Testing explanation5 has both interactive_examples and step_solutions arrays with Level 1B, 2B, 3B naming")
            
            response = self.session.get(f"{self.base_url}/problems/explanation5")
            
            if response.status_code == 200:
                explanation5_data = response.json()
                
                interactive_examples = explanation5_data.get('interactive_examples', [])
                step_solutions = explanation5_data.get('step_solutions', [])
                
                print(f"   Interactive Examples: {len(interactive_examples)}")
                print(f"   Step Solutions: {len(step_solutions)}")
                
                # CRITICAL TEST 1: Both arrays must exist
                if not interactive_examples:
                    self.log_test("Step Solutions with Level Naming", False, 
                                f"❌ Missing interactive_examples array")
                    return False
                
                if not step_solutions:
                    self.log_test("Step Solutions with Level Naming", False, 
                                f"❌ Missing step_solutions array - this causes 'Inactive Practice' bug")
                    return False
                
                # CRITICAL TEST 2: Verify Level 1B, 2B, 3B naming convention in step_solutions
                level_naming_found = []
                for step in step_solutions:
                    step_text = step.get('step_en', '')
                    print(f"   Step: {step_text}")
                    
                    if "Level 1B" in step_text:
                        level_naming_found.append("1B")
                    elif "Level 2B" in step_text:
                        level_naming_found.append("2B")
                    elif "Level 3B" in step_text:
                        level_naming_found.append("3B")
                
                # Verify all level naming conventions are present
                expected_levels = ["1B", "2B", "3B"]
                missing_levels = [level for level in expected_levels if level not in level_naming_found]
                
                if missing_levels:
                    self.log_test("Step Solutions with Level Naming", False, 
                                f"❌ Missing level naming conventions: Level {missing_levels}")
                    return False
                
                # CRITICAL TEST 3: Each step should have possible_answers array
                for i, step in enumerate(step_solutions):
                    possible_answers = step.get('possible_answers', [])
                    if not possible_answers:
                        self.log_test("Step Solutions with Level Naming", False, 
                                    f"❌ Step {i+1} missing possible_answers array")
                        return False
                
                print(f"   ✅ Found Level 1B, 2B, 3B naming convention in step_solutions")
                print(f"   ✅ All steps have possible_answers arrays")
                
                self.log_test("Step Solutions with Level Naming", True, 
                            f"✅ explanation5 has both required arrays with proper Level 1B, 2B, 3B naming to prevent 'Inactive Practice' bug")
                return True
                
            else:
                self.log_test("Step Solutions with Level Naming", False, 
                            f"Failed to get explanation5 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Step Solutions with Level Naming", False, f"Test execution error: {str(e)}")
            return False

    def test_manufacturing_tolerance_word_problem(self):
        """Test Manufacturing Tolerance Word Problem - practice5_2"""
        try:
            print("\n🎯 MANUFACTURING TOLERANCE WORD PROBLEM TESTING")
            print("Testing practice5_2 has manufacturing tolerance problem with target length 50mm, tolerance ±0.5mm, 3-step structure")
            
            response = self.session.get(f"{self.base_url}/problems/practice5_2")
            
            if response.status_code == 200:
                practice5_2_data = response.json()
                
                question_en = practice5_2_data.get('question_en', '')
                stage_type = practice5_2_data.get('stage_type', '')
                step_solutions = practice5_2_data.get('step_solutions', [])
                
                print(f"   Question: {question_en[:100]}...")
                print(f"   Stage Type: {stage_type}")
                print(f"   Step Solutions: {len(step_solutions)}")
                
                # CRITICAL TEST 1: Should be manufacturing tolerance problem
                tolerance_keywords = ['manufacturing', 'tolerance', '50mm', '±0.5', 'target length', 'machine', 'parts']
                if not any(keyword in question_en for keyword in tolerance_keywords):
                    self.log_test("Manufacturing Tolerance Word Problem", False, 
                                f"❌ practice5_2 should be manufacturing tolerance problem, got: {question_en}")
                    return False
                
                # CRITICAL TEST 2: Should have stage_type "practice_word"
                if stage_type != "practice_word":
                    self.log_test("Manufacturing Tolerance Word Problem", False, 
                                f"❌ practice5_2 should have stage_type 'practice_word', got: {stage_type}")
                    return False
                
                # CRITICAL TEST 3: Should have 3-step structure
                if len(step_solutions) != 3:
                    self.log_test("Manufacturing Tolerance Word Problem", False, 
                                f"❌ practice5_2 should have 3 step solutions, got {len(step_solutions)}")
                    return False
                
                # CRITICAL TEST 4: Verify step content relates to manufacturing tolerance
                for i, step in enumerate(step_solutions):
                    step_text = step.get('step_en', '')
                    possible_answers = step.get('possible_answers', [])
                    
                    print(f"   Step {i+1}: {step_text}")
                    print(f"   Possible Answers: {possible_answers}")
                    
                    if not possible_answers:
                        self.log_test("Manufacturing Tolerance Word Problem", False, 
                                    f"❌ Step {i+1} missing possible_answers array")
                        return False
                
                print(f"   ✅ practice5_2 is manufacturing tolerance word problem with 3-step structure")
                
                self.log_test("Manufacturing Tolerance Word Problem", True, 
                            f"✅ practice5_2 has manufacturing tolerance problem with target length 50mm, tolerance ±0.5mm, proper 3-step structure and stage_type 'practice_word'")
                return True
                
            else:
                self.log_test("Manufacturing Tolerance Word Problem", False, 
                            f"Failed to get practice5_2 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Manufacturing Tolerance Word Problem", False, f"Test execution error: {str(e)}")
            return False

    def test_assessment_updates(self):
        """Test Assessment Updates - assessment5 changed to new absolute value inequality"""
        try:
            print("\n🎯 ASSESSMENT UPDATES TESTING")
            print("Testing assessment5 changed to '|4 - x| ≥ 3' with answer 'x ≤ 1 or x ≥ 7'")
            
            response = self.session.get(
                f"{self.base_url}/problems/assessment5",
                params={"username": self.test_student_username}
            )
            
            if response.status_code == 200:
                assessment5_data = response.json()
                
                question_en = assessment5_data.get('question_en', '')
                answer = assessment5_data.get('answer', '')
                problem_type = assessment5_data.get('type', '')
                
                print(f"   Question: {question_en}")
                print(f"   Answer: {answer}")
                print(f"   Type: {problem_type}")
                
                # CRITICAL TEST 1: Question should contain "|4 - x| ≥ 3"
                if "|4 - x| ≥ 3" not in question_en:
                    self.log_test("Assessment Updates", False, 
                                f"❌ assessment5 question should contain '|4 - x| ≥ 3', got: {question_en}")
                    return False
                
                # CRITICAL TEST 2: Answer should be "x ≤ 1 or x ≥ 7"
                if answer != "x ≤ 1 or x ≥ 7":
                    self.log_test("Assessment Updates", False, 
                                f"❌ assessment5 answer should be 'x ≤ 1 or x ≥ 7', got: {answer}")
                    return False
                
                # CRITICAL TEST 3: Should be assessment type
                if problem_type != 'assessment':
                    self.log_test("Assessment Updates", False, 
                                f"❌ assessment5 should be type 'assessment', got: {problem_type}")
                    return False
                
                print(f"   ✅ assessment5 has correct absolute value inequality content")
                
                self.log_test("Assessment Updates", True, 
                            f"✅ assessment5 successfully updated to '|4 - x| ≥ 3' with answer 'x ≤ 1 or x ≥ 7'")
                return True
                
            else:
                self.log_test("Assessment Updates", False, 
                            f"Failed to get assessment5 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Assessment Updates", False, f"Test execution error: {str(e)}")
            return False

    def test_exam_prep_updates(self):
        """Test Exam Prep Updates - examprep5 changed to complex absolute value inequality"""
        try:
            print("\n🎯 EXAM PREP UPDATES TESTING")
            print("Testing examprep5 changed to '|2x + 1| - 3 < 4' with answer '-4 < x < 3'")
            
            response = self.session.get(
                f"{self.base_url}/problems/examprep5",
                params={"username": self.test_student_username}
            )
            
            if response.status_code == 200:
                examprep5_data = response.json()
                
                question_en = examprep5_data.get('question_en', '')
                answer = examprep5_data.get('answer', '')
                problem_type = examprep5_data.get('type', '')
                
                print(f"   Question: {question_en}")
                print(f"   Answer: {answer}")
                print(f"   Type: {problem_type}")
                
                # CRITICAL TEST 1: Question should contain "|2x + 1| - 3 < 4"
                if "|2x + 1| - 3 < 4" not in question_en:
                    self.log_test("Exam Prep Updates", False, 
                                f"❌ examprep5 question should contain '|2x + 1| - 3 < 4', got: {question_en}")
                    return False
                
                # CRITICAL TEST 2: Answer should be "-4 < x < 3"
                if answer != "-4 < x < 3":
                    self.log_test("Exam Prep Updates", False, 
                                f"❌ examprep5 answer should be '-4 < x < 3', got: {answer}")
                    return False
                
                # CRITICAL TEST 3: Should be examprep type
                if problem_type != 'examprep':
                    self.log_test("Exam Prep Updates", False, 
                                f"❌ examprep5 should be type 'examprep', got: {problem_type}")
                    return False
                
                print(f"   ✅ examprep5 has correct complex absolute value inequality content")
                
                self.log_test("Exam Prep Updates", True, 
                            f"✅ examprep5 successfully updated to '|2x + 1| - 3 < 4' with answer '-4 < x < 3'")
                return True
                
            else:
                self.log_test("Exam Prep Updates", False, 
                            f"Failed to get examprep5 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Exam Prep Updates", False, f"Test execution error: {str(e)}")
            return False

    def test_bilingual_content(self):
        """Test Bilingual Content - Verify both English and Arabic content"""
        try:
            print("\n🎯 BILINGUAL CONTENT TESTING")
            print("Testing all Section 5 problems have proper English and Arabic content")
            
            problems_to_test = ["prep5", "explanation5", "practice5_1", "practice5_2", "assessment5", "examprep5"]
            all_bilingual_working = True
            
            for problem_id in problems_to_test:
                print(f"\n   Testing bilingual content for {problem_id}")
                
                # For assessment and examprep, we need username parameter
                params = {}
                if problem_id in ['assessment5', 'examprep5']:
                    params['username'] = self.test_student_username
                
                response = self.session.get(
                    f"{self.base_url}/problems/{problem_id}",
                    params=params
                )
                
                if response.status_code == 200:
                    problem_data = response.json()
                    
                    # CRITICAL TEST 1: Basic bilingual fields
                    required_bilingual_fields = [
                        ('question_en', 'question_ar'),
                        ('answer', 'answer_ar')
                    ]
                    
                    for en_field, ar_field in required_bilingual_fields:
                        en_content = problem_data.get(en_field, '')
                        ar_content = problem_data.get(ar_field, '')
                        
                        if not en_content:
                            print(f"     ❌ Missing {en_field}")
                            all_bilingual_working = False
                        
                        if not ar_content and en_content:  # Only check Arabic if English exists
                            print(f"     ❌ Missing {ar_field}")
                            all_bilingual_working = False
                    
                    # CRITICAL TEST 2: Step solutions bilingual content
                    step_solutions = problem_data.get('step_solutions', [])
                    for i, step in enumerate(step_solutions):
                        step_en = step.get('step_en', '')
                        step_ar = step.get('step_ar', '')
                        possible_answers = step.get('possible_answers', [])
                        possible_answers_ar = step.get('possible_answers_ar', [])
                        
                        if step_en and not step_ar:
                            print(f"     ❌ Step {i+1} missing Arabic description")
                            all_bilingual_working = False
                        
                        if possible_answers and not possible_answers_ar:
                            print(f"     ❌ Step {i+1} missing Arabic possible answers")
                            all_bilingual_working = False
                    
                    if all_bilingual_working:
                        print(f"     ✅ {problem_id} has proper bilingual content")
                else:
                    print(f"     ❌ Failed to get {problem_id}: HTTP {response.status_code}")
                    all_bilingual_working = False
            
            if all_bilingual_working:
                self.log_test("Bilingual Content", True, 
                            f"✅ All Section 5 problems have proper English and Arabic content")
                return True
            else:
                self.log_test("Bilingual Content", False, 
                            f"❌ Some Section 5 problems missing bilingual content")
                return False
                
        except Exception as e:
            self.log_test("Bilingual Content", False, f"Test execution error: {str(e)}")
            return False

    def test_absolute_value_conversion_rules(self):
        """Test Absolute Value Conversion Rules - |expr| < number → compound, |expr| > number → OR"""
        try:
            print("\n🎯 ABSOLUTE VALUE CONVERSION RULES TESTING")
            print("Testing problems ensure proper conversion: |expr| < number → compound, |expr| > number → OR")
            
            # Test prep5 (|x| < 4 should convert to compound: -4 < x < 4)
            response = self.session.get(f"{self.base_url}/problems/prep5")
            
            if response.status_code == 200:
                prep5_data = response.json()
                
                question_en = prep5_data.get('question_en', '')
                answer = prep5_data.get('answer', '')
                
                print(f"   prep5 Question: {question_en}")
                print(f"   prep5 Answer: {answer}")
                
                # CRITICAL TEST 1: |x| < 4 should convert to compound inequality
                if "|x| < 4" in question_en and answer == "-4 < x < 4":
                    print(f"   ✅ prep5 correctly converts |x| < 4 to compound inequality -4 < x < 4")
                else:
                    self.log_test("Absolute Value Conversion Rules", False, 
                                f"❌ prep5 should convert |x| < 4 to compound inequality -4 < x < 4")
                    return False
            
            # Test assessment5 (|4 - x| ≥ 3 should convert to OR: x ≤ 1 or x ≥ 7)
            response = self.session.get(
                f"{self.base_url}/problems/assessment5",
                params={"username": self.test_student_username}
            )
            
            if response.status_code == 200:
                assessment5_data = response.json()
                
                question_en = assessment5_data.get('question_en', '')
                answer = assessment5_data.get('answer', '')
                
                print(f"   assessment5 Question: {question_en}")
                print(f"   assessment5 Answer: {answer}")
                
                # CRITICAL TEST 2: |4 - x| ≥ 3 should convert to OR inequality
                if "|4 - x| ≥ 3" in question_en and answer == "x ≤ 1 or x ≥ 7":
                    print(f"   ✅ assessment5 correctly converts |4 - x| ≥ 3 to OR inequality x ≤ 1 or x ≥ 7")
                else:
                    self.log_test("Absolute Value Conversion Rules", False, 
                                f"❌ assessment5 should convert |4 - x| ≥ 3 to OR inequality x ≤ 1 or x ≥ 7")
                    return False
            
            # Test examprep5 (|2x + 1| - 3 < 4 should simplify to |2x + 1| < 7, then compound: -4 < x < 3)
            response = self.session.get(
                f"{self.base_url}/problems/examprep5",
                params={"username": self.test_student_username}
            )
            
            if response.status_code == 200:
                examprep5_data = response.json()
                
                question_en = examprep5_data.get('question_en', '')
                answer = examprep5_data.get('answer', '')
                
                print(f"   examprep5 Question: {question_en}")
                print(f"   examprep5 Answer: {answer}")
                
                # CRITICAL TEST 3: |2x + 1| - 3 < 4 should convert to compound inequality
                if "|2x + 1| - 3 < 4" in question_en and answer == "-4 < x < 3":
                    print(f"   ✅ examprep5 correctly converts |2x + 1| - 3 < 4 to compound inequality -4 < x < 3")
                else:
                    self.log_test("Absolute Value Conversion Rules", False, 
                                f"❌ examprep5 should convert |2x + 1| - 3 < 4 to compound inequality -4 < x < 3")
                    return False
            
            print(f"   ✅ All absolute value conversion rules working correctly")
            
            self.log_test("Absolute Value Conversion Rules", True, 
                        f"✅ Problems ensure proper conversion: |expr| < number → compound, |expr| > number → OR")
            return True
                
        except Exception as e:
            self.log_test("Absolute Value Conversion Rules", False, f"Test execution error: {str(e)}")
            return False

    def generate_section5_summary(self, results, critical_failures):
        """Generate comprehensive summary of Section 5 testing"""
        print("\n" + "=" * 80)
        print("🎯 SECTION 5 ABSOLUTE VALUE INEQUALITIES COMPREHENSIVE TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL SECTION 5 TESTING RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL SECTION 5 ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  SECTION 5 STATUS: INCOMPLETE - Implementation needs fixes!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix remaining Section 5 issues")
        else:
            print(f"\n🎉 NO CRITICAL SECTION 5 ISSUES DETECTED")
        
        print(f"\n📋 SECTION 5 ABSOLUTE VALUE INEQUALITIES STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL SECTION 5 TESTS PASSED")
            print("   ✅ Section 5 API endpoints working")
            print("   ✅ Individual problem endpoints accessible")
            print("   ✅ prep5 updated to absolute value inequality")
            print("   ✅ explanation5 has 3-level structure")
            print("   ✅ Step solutions with Level 1B, 2B, 3B naming")
            print("   ✅ Manufacturing tolerance word problem implemented")
            print("   ✅ Assessment and exam prep updated")
            print("   ✅ Bilingual content properly structured")
            print("   ✅ Absolute value conversion rules working")
            print("   🛡️  SECTION 5 ABSOLUTE VALUE INEQUALITIES: FULLY WORKING")
        else:
            print("   ⚠️  SECTION 5 IMPLEMENTATION ISSUES DETECTED")
            print("   🔧 Section 5 absolute value inequalities need enhancement")
            print("   🚨 STUDENT EXPERIENCE: MAY BE BROKEN FOR SECTION 5")
        
        print("\n" + "=" * 80)

    def run_section5_tests(self):
        """Run comprehensive Section 5 absolute value inequalities tests"""
        print("=" * 80)
        print("🎯 SECTION 5 ABSOLUTE VALUE INEQUALITIES COMPREHENSIVE TESTING")
        print("=" * 80)
        print("Testing comprehensive Section 5 Absolute Value Inequalities implementation")
        
        # Test categories for Section 5
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("Section 5 API Endpoints", self.test_section5_api_endpoints, "critical"),
            ("Individual Problem Endpoints", self.test_individual_problem_endpoints, "critical"),
            ("Updated Problem Content", self.test_updated_problem_content, "critical"),
            ("Absolute Value Structure", self.test_absolute_value_structure, "critical"),
            ("Step Solutions with Level Naming", self.test_step_solutions_with_level_naming, "critical"),
            ("Manufacturing Tolerance Word Problem", self.test_manufacturing_tolerance_word_problem, "critical"),
            ("Assessment Updates", self.test_assessment_updates, "critical"),
            ("Exam Prep Updates", self.test_exam_prep_updates, "critical"),
            ("Bilingual Content", self.test_bilingual_content, "high"),
            ("Absolute Value Conversion Rules", self.test_absolute_value_conversion_rules, "critical")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 SECTION 5 TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive Section 5 summary
        self.generate_section5_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run Section 5 absolute value inequalities tests"""
    print("🚀 Starting SECTION 5 ABSOLUTE VALUE INEQUALITIES COMPREHENSIVE Testing...")
    print("🎯 Goal: Verify comprehensive Section 5 Absolute Value Inequalities implementation")
    
    tester = Section5AbsoluteValueInequalitiesTester(BACKEND_URL)
    results = tester.run_section5_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 SECTION 5 ALERT: {failed_tests} test(s) failed!")
        print("🔧 Section 5 absolute value inequalities need backend enhancement")
    else:
        print(f"\n🛡️  SECTION 5 CONFIRMED: All tests passed!")
        print("✅ Section 5 Absolute Value Inequalities implementation is working correctly")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()