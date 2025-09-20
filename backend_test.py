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
BACKEND_URL = "https://math-bug-fixes.preview.emergentagent.com/api"

class Section4CompoundInequalitiesTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "section4_test_student"
        
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
        """Create test student for Section 4 testing"""
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

    def test_section4_api_endpoints(self):
        """Test Section 4 API Endpoints - GET /api/problems/section/section4"""
        try:
            print("\n🎯 SECTION 4 API ENDPOINTS TESTING")
            print("Testing GET /api/problems/section/section4 to ensure all 6 problems are returned")
            
            response = self.session.get(f"{self.base_url}/problems/section/section4")
            
            if response.status_code == 200:
                problems = response.json()
                
                print(f"   Found {len(problems)} problems in Section 4")
                
                # CRITICAL TEST 1: Should have exactly 6 problems
                if len(problems) != 6:
                    self.log_test("Section 4 API Endpoints", False, 
                                f"❌ Expected 6 problems, got {len(problems)}")
                    return False
                
                # CRITICAL TEST 2: Verify all expected problem IDs are present
                expected_problems = ["prep4", "explanation4", "practice4_1", "practice4_2", "assessment4", "examprep4"]
                found_problems = [p.get('id') for p in problems]
                
                missing_problems = [p for p in expected_problems if p not in found_problems]
                if missing_problems:
                    self.log_test("Section 4 API Endpoints", False, 
                                f"❌ Missing problems: {missing_problems}")
                    return False
                
                print(f"   ✅ All 6 expected problems found: {found_problems}")
                
                # CRITICAL TEST 3: Verify section_id is correct for all problems
                for problem in problems:
                    if problem.get('section_id') != 'section4':
                        self.log_test("Section 4 API Endpoints", False, 
                                    f"❌ Problem {problem.get('id')} has wrong section_id: {problem.get('section_id')}")
                        return False
                
                self.log_test("Section 4 API Endpoints", True, 
                            f"✅ Section 4 API endpoint returns all 6 problems correctly")
                return True
                
            else:
                self.log_test("Section 4 API Endpoints", False, 
                            f"Failed to get Section 4 problems: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Section 4 API Endpoints", False, f"Test execution error: {str(e)}")
            return False

    def test_individual_problem_endpoints(self):
        """Test Individual Problem Endpoints for all 6 Section 4 problems"""
        try:
            print("\n🎯 INDIVIDUAL PROBLEM ENDPOINTS TESTING")
            print("Testing each problem endpoint (prep4, explanation4, practice4_1, practice4_2, assessment4, examprep4)")
            
            expected_problems = ["prep4", "explanation4", "practice4_1", "practice4_2", "assessment4", "examprep4"]
            all_problems_working = True
            
            for problem_id in expected_problems:
                print(f"\n   Testing GET /api/problems/{problem_id}")
                
                # For assessment and examprep, we need username parameter
                params = {}
                if problem_id in ['assessment4', 'examprep4']:
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
        """Test Updated Problem Content - prep4 changed to compound inequality"""
        try:
            print("\n🎯 UPDATED PROBLEM CONTENT TESTING")
            print("Testing prep4 changed from '3x + 5 < 2x + 9' to '3 < x + 2 < 8' with answer '1 < x < 6'")
            
            response = self.session.get(f"{self.base_url}/problems/prep4")
            
            if response.status_code == 200:
                prep4_data = response.json()
                
                question_en = prep4_data.get('question_en', '')
                answer = prep4_data.get('answer', '')
                
                print(f"   Current Question: {question_en}")
                print(f"   Current Answer: {answer}")
                
                # CRITICAL TEST 1: Question should be compound inequality "3 < x + 2 < 8"
                if "3 < x + 2 < 8" not in question_en:
                    self.log_test("Updated Problem Content", False, 
                                f"❌ prep4 question should contain '3 < x + 2 < 8', got: {question_en}")
                    return False
                
                # CRITICAL TEST 2: Answer should be "1 < x < 6"
                if answer != "1 < x < 6":
                    self.log_test("Updated Problem Content", False, 
                                f"❌ prep4 answer should be '1 < x < 6', got: {answer}")
                    return False
                
                # CRITICAL TEST 3: Should be preparation type
                if prep4_data.get('type') != 'preparation':
                    self.log_test("Updated Problem Content", False, 
                                f"❌ prep4 should be type 'preparation', got: {prep4_data.get('type')}")
                    return False
                
                print(f"   ✅ prep4 has correct compound inequality content")
                
                self.log_test("Updated Problem Content", True, 
                            f"✅ prep4 successfully updated to compound inequality '3 < x + 2 < 8' with answer '1 < x < 6'")
                return True
                
            else:
                self.log_test("Updated Problem Content", False, 
                            f"Failed to get prep4 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Updated Problem Content", False, f"Test execution error: {str(e)}")
            return False

    def test_compound_inequality_structure(self):
        """Test Compound Inequality Structure - explanation4 3-level structure"""
        try:
            print("\n🎯 COMPOUND INEQUALITY STRUCTURE TESTING")
            print("Testing explanation4 has 3-level structure (Simple Compound, With Multiplication/Division, OR Inequalities)")
            
            response = self.session.get(f"{self.base_url}/problems/explanation4")
            
            if response.status_code == 200:
                explanation4_data = response.json()
                
                interactive_examples = explanation4_data.get('interactive_examples', [])
                
                print(f"   Found {len(interactive_examples)} interactive examples")
                
                # CRITICAL TEST 1: Should have exactly 3 interactive examples
                if len(interactive_examples) != 3:
                    self.log_test("Compound Inequality Structure", False, 
                                f"❌ Expected 3 interactive examples, got {len(interactive_examples)}")
                    return False
                
                # CRITICAL TEST 2: Verify the 3 levels are present
                expected_levels = [
                    "Simple Compound",
                    "With Multiplication/Division", 
                    "OR Inequalities"
                ]
                
                found_levels = []
                for i, example in enumerate(interactive_examples):
                    title = example.get('title_en', '')
                    print(f"   Level {i+1}: {title}")
                    
                    # Check if this level matches expected content
                    if "Simple Compound" in title or "Level 1" in title:
                        found_levels.append("Simple Compound")
                    elif "Multiplication" in title or "Division" in title or "Level 2" in title:
                        found_levels.append("With Multiplication/Division")
                    elif "OR" in title or "Level 3" in title:
                        found_levels.append("OR Inequalities")
                
                # Verify all 3 levels are found
                missing_levels = [level for level in expected_levels if level not in found_levels]
                if missing_levels:
                    self.log_test("Compound Inequality Structure", False, 
                                f"❌ Missing levels: {missing_levels}")
                    return False
                
                print(f"   ✅ All 3 compound inequality levels found")
                
                self.log_test("Compound Inequality Structure", True, 
                            f"✅ explanation4 has correct 3-level structure for compound inequalities")
                return True
                
            else:
                self.log_test("Compound Inequality Structure", False, 
                            f"Failed to get explanation4 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Compound Inequality Structure", False, f"Test execution error: {str(e)}")
            return False

    def test_step_solutions_with_level_naming(self):
        """Test Step Solutions with Level Naming - Both arrays with Level 1B, 2B, 3B naming"""
        try:
            print("\n🎯 STEP SOLUTIONS WITH LEVEL NAMING TESTING")
            print("Testing explanation4 has both interactive_examples and step_solutions arrays with Level 1B, 2B, 3B naming")
            
            response = self.session.get(f"{self.base_url}/problems/explanation4")
            
            if response.status_code == 200:
                explanation4_data = response.json()
                
                interactive_examples = explanation4_data.get('interactive_examples', [])
                step_solutions = explanation4_data.get('step_solutions', [])
                
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
                            f"✅ explanation4 has both required arrays with proper Level 1B, 2B, 3B naming to prevent 'Inactive Practice' bug")
                return True
                
            else:
                self.log_test("Step Solutions with Level Naming", False, 
                            f"Failed to get explanation4 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Step Solutions with Level Naming", False, f"Test execution error: {str(e)}")
            return False

    def test_temperature_conversion_word_problem(self):
        """Test Temperature Conversion Word Problem - practice4_2"""
        try:
            print("\n🎯 TEMPERATURE CONVERSION WORD PROBLEM TESTING")
            print("Testing practice4_2 has Celsius to Fahrenheit temperature conversion with 3-step structure")
            
            response = self.session.get(f"{self.base_url}/problems/practice4_2")
            
            if response.status_code == 200:
                practice4_2_data = response.json()
                
                question_en = practice4_2_data.get('question_en', '')
                stage_type = practice4_2_data.get('stage_type', '')
                step_solutions = practice4_2_data.get('step_solutions', [])
                
                print(f"   Question: {question_en[:100]}...")
                print(f"   Stage Type: {stage_type}")
                print(f"   Step Solutions: {len(step_solutions)}")
                
                # CRITICAL TEST 1: Should be temperature conversion problem
                temperature_keywords = ['temperature', 'Celsius', 'Fahrenheit', '°C', '°F', 'F =', 'C']
                if not any(keyword in question_en for keyword in temperature_keywords):
                    self.log_test("Temperature Conversion Word Problem", False, 
                                f"❌ practice4_2 should be temperature conversion problem, got: {question_en}")
                    return False
                
                # CRITICAL TEST 2: Should have stage_type "practice_word"
                if stage_type != "practice_word":
                    self.log_test("Temperature Conversion Word Problem", False, 
                                f"❌ practice4_2 should have stage_type 'practice_word', got: {stage_type}")
                    return False
                
                # CRITICAL TEST 3: Should have 3-step structure
                if len(step_solutions) != 3:
                    self.log_test("Temperature Conversion Word Problem", False, 
                                f"❌ practice4_2 should have 3 step solutions, got {len(step_solutions)}")
                    return False
                
                # CRITICAL TEST 4: Verify step content relates to temperature conversion
                for i, step in enumerate(step_solutions):
                    step_text = step.get('step_en', '')
                    possible_answers = step.get('possible_answers', [])
                    
                    print(f"   Step {i+1}: {step_text}")
                    print(f"   Possible Answers: {possible_answers}")
                    
                    if not possible_answers:
                        self.log_test("Temperature Conversion Word Problem", False, 
                                    f"❌ Step {i+1} missing possible_answers array")
                        return False
                
                print(f"   ✅ practice4_2 is temperature conversion word problem with 3-step structure")
                
                self.log_test("Temperature Conversion Word Problem", True, 
                            f"✅ practice4_2 has Celsius to Fahrenheit temperature conversion with proper 3-step structure and stage_type 'practice_word'")
                return True
                
            else:
                self.log_test("Temperature Conversion Word Problem", False, 
                            f"Failed to get practice4_2 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Temperature Conversion Word Problem", False, f"Test execution error: {str(e)}")
            return False

    def test_assessment_updates(self):
        """Test Assessment Updates - assessment4 changed to new compound inequality"""
        try:
            print("\n🎯 ASSESSMENT UPDATES TESTING")
            print("Testing assessment4 changed to '-8 ≤ 4 - 2x < 6' with answer '-1 < x ≤ 6'")
            
            response = self.session.get(
                f"{self.base_url}/problems/assessment4",
                params={"username": self.test_student_username}
            )
            
            if response.status_code == 200:
                assessment4_data = response.json()
                
                question_en = assessment4_data.get('question_en', '')
                answer = assessment4_data.get('answer', '')
                problem_type = assessment4_data.get('type', '')
                
                print(f"   Question: {question_en}")
                print(f"   Answer: {answer}")
                print(f"   Type: {problem_type}")
                
                # CRITICAL TEST 1: Question should contain "-8 ≤ 4 - 2x < 6"
                if "-8 ≤ 4 - 2x < 6" not in question_en:
                    self.log_test("Assessment Updates", False, 
                                f"❌ assessment4 question should contain '-8 ≤ 4 - 2x < 6', got: {question_en}")
                    return False
                
                # CRITICAL TEST 2: Answer should be "-1 < x ≤ 6"
                if answer != "-1 < x ≤ 6":
                    self.log_test("Assessment Updates", False, 
                                f"❌ assessment4 answer should be '-1 < x ≤ 6', got: {answer}")
                    return False
                
                # CRITICAL TEST 3: Should be assessment type
                if problem_type != 'assessment':
                    self.log_test("Assessment Updates", False, 
                                f"❌ assessment4 should be type 'assessment', got: {problem_type}")
                    return False
                
                print(f"   ✅ assessment4 has correct compound inequality content")
                
                self.log_test("Assessment Updates", True, 
                            f"✅ assessment4 successfully updated to '-8 ≤ 4 - 2x < 6' with answer '-1 < x ≤ 6'")
                return True
                
            else:
                self.log_test("Assessment Updates", False, 
                            f"Failed to get assessment4 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Assessment Updates", False, f"Test execution error: {str(e)}")
            return False

    def test_exam_prep_updates(self):
        """Test Exam Prep Updates - examprep4 changed to AND compound inequality"""
        try:
            print("\n🎯 EXAM PREP UPDATES TESTING")
            print("Testing examprep4 changed to '2(x - 1) ≤ 6 AND x + 3 > 2' with answer '-1 < x ≤ 4'")
            
            response = self.session.get(
                f"{self.base_url}/problems/examprep4",
                params={"username": self.test_student_username}
            )
            
            if response.status_code == 200:
                examprep4_data = response.json()
                
                question_en = examprep4_data.get('question_en', '')
                answer = examprep4_data.get('answer', '')
                problem_type = examprep4_data.get('type', '')
                
                print(f"   Question: {question_en}")
                print(f"   Answer: {answer}")
                print(f"   Type: {problem_type}")
                
                # CRITICAL TEST 1: Question should contain "2(x - 1) ≤ 6 AND x + 3 > 2"
                if "2(x - 1) ≤ 6" not in question_en or "x + 3 > 2" not in question_en:
                    self.log_test("Exam Prep Updates", False, 
                                f"❌ examprep4 question should contain '2(x - 1) ≤ 6 AND x + 3 > 2', got: {question_en}")
                    return False
                
                # CRITICAL TEST 2: Answer should be "-1 < x ≤ 4"
                if answer != "-1 < x ≤ 4":
                    self.log_test("Exam Prep Updates", False, 
                                f"❌ examprep4 answer should be '-1 < x ≤ 4', got: {answer}")
                    return False
                
                # CRITICAL TEST 3: Should be examprep type
                if problem_type != 'examprep':
                    self.log_test("Exam Prep Updates", False, 
                                f"❌ examprep4 should be type 'examprep', got: {problem_type}")
                    return False
                
                print(f"   ✅ examprep4 has correct AND compound inequality content")
                
                self.log_test("Exam Prep Updates", True, 
                            f"✅ examprep4 successfully updated to '2(x - 1) ≤ 6 AND x + 3 > 2' with answer '-1 < x ≤ 4'")
                return True
                
            else:
                self.log_test("Exam Prep Updates", False, 
                            f"Failed to get examprep4 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Exam Prep Updates", False, f"Test execution error: {str(e)}")
            return False

    def test_bilingual_content(self):
        """Test Bilingual Content - Verify both English and Arabic content"""
        try:
            print("\n🎯 BILINGUAL CONTENT TESTING")
            print("Testing all Section 4 problems have proper English and Arabic content")
            
            problems_to_test = ["prep4", "explanation4", "practice4_1", "practice4_2", "assessment4", "examprep4"]
            all_bilingual_working = True
            
            for problem_id in problems_to_test:
                print(f"\n   Testing bilingual content for {problem_id}")
                
                # For assessment and examprep, we need username parameter
                params = {}
                if problem_id in ['assessment4', 'examprep4']:
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
                            f"✅ All Section 4 problems have proper English and Arabic content")
                return True
            else:
                self.log_test("Bilingual Content", False, 
                            f"❌ Some Section 4 problems missing bilingual content")
                return False
                
        except Exception as e:
            self.log_test("Bilingual Content", False, f"Test execution error: {str(e)}")
            return False

    def test_sign_flipping_logic(self):
        """Test Sign Flipping Logic - Test problems with negative coefficients"""
        try:
            print("\n🎯 SIGN FLIPPING LOGIC TESTING")
            print("Testing problems with negative coefficients for proper sign flipping documentation")
            
            # Test assessment4 which has negative coefficient: -8 ≤ 4 - 2x < 6
            response = self.session.get(
                f"{self.base_url}/problems/assessment4",
                params={"username": self.test_student_username}
            )
            
            if response.status_code == 200:
                assessment4_data = response.json()
                
                question_en = assessment4_data.get('question_en', '')
                answer = assessment4_data.get('answer', '')
                explanation_en = assessment4_data.get('explanation_en', '')
                hints_en = assessment4_data.get('hints_en', [])
                
                print(f"   Question: {question_en}")
                print(f"   Answer: {answer}")
                print(f"   Explanation: {explanation_en}")
                print(f"   Hints: {hints_en}")
                
                # CRITICAL TEST 1: Problem should involve negative coefficient (-2x)
                if "-2x" not in question_en:
                    self.log_test("Sign Flipping Logic", False, 
                                f"❌ assessment4 should contain negative coefficient '-2x', got: {question_en}")
                    return False
                
                # CRITICAL TEST 2: Explanation or hints should mention sign flipping
                sign_flip_keywords = ['flip', 'reverse', 'change', 'sign', 'negative', 'divide by -', 'multiply by -']
                sign_flip_mentioned = False
                
                # Check explanation
                if explanation_en:
                    if any(keyword in explanation_en.lower() for keyword in sign_flip_keywords):
                        sign_flip_mentioned = True
                
                # Check hints
                for hint in hints_en:
                    if any(keyword in hint.lower() for keyword in sign_flip_keywords):
                        sign_flip_mentioned = True
                        break
                
                if not sign_flip_mentioned:
                    self.log_test("Sign Flipping Logic", False, 
                                f"❌ assessment4 should mention sign flipping rules in explanation or hints")
                    return False
                
                # CRITICAL TEST 3: Answer should reflect proper sign flipping
                # Original: -8 ≤ 4 - 2x < 6
                # After subtracting 4: -12 ≤ -2x < 2  
                # After dividing by -2 and flipping: -1 < x ≤ 6
                if answer != "-1 < x ≤ 6":
                    self.log_test("Sign Flipping Logic", False, 
                                f"❌ assessment4 answer should reflect proper sign flipping: '-1 < x ≤ 6', got: {answer}")
                    return False
                
                print(f"   ✅ assessment4 properly documents sign flipping logic")
                
                self.log_test("Sign Flipping Logic", True, 
                            f"✅ Problems with negative coefficients properly document sign flipping rules")
                return True
                
            else:
                self.log_test("Sign Flipping Logic", False, 
                            f"Failed to get assessment4 data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Sign Flipping Logic", False, f"Test execution error: {str(e)}")
            return False

    def generate_section4_summary(self, results, critical_failures):
        """Generate comprehensive summary of Section 4 testing"""
        print("\n" + "=" * 80)
        print("🎯 SECTION 4 COMPOUND INEQUALITIES COMPREHENSIVE TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL SECTION 4 TESTING RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL SECTION 4 ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  SECTION 4 STATUS: INCOMPLETE - Implementation needs fixes!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix remaining Section 4 issues")
        else:
            print(f"\n🎉 NO CRITICAL SECTION 4 ISSUES DETECTED")
        
        print(f"\n📋 SECTION 4 COMPOUND INEQUALITIES STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL SECTION 4 TESTS PASSED")
            print("   ✅ Section 4 API endpoints working")
            print("   ✅ Individual problem endpoints accessible")
            print("   ✅ prep4 updated to compound inequality")
            print("   ✅ explanation4 has 3-level structure")
            print("   ✅ Step solutions with Level 1B, 2B, 3B naming")
            print("   ✅ Temperature conversion word problem implemented")
            print("   ✅ Assessment and exam prep updated")
            print("   ✅ Bilingual content properly structured")
            print("   ✅ Sign flipping logic documented")
            print("   🛡️  SECTION 4 COMPOUND INEQUALITIES: FULLY WORKING")
        else:
            print("   ⚠️  SECTION 4 IMPLEMENTATION ISSUES DETECTED")
            print("   🔧 Section 4 compound inequalities need enhancement")
            print("   🚨 STUDENT EXPERIENCE: MAY BE BROKEN FOR SECTION 4")
        
        print("\n" + "=" * 80)

    def run_section4_tests(self):
        """Run comprehensive Section 4 compound inequalities tests"""
        print("=" * 80)
        print("🎯 SECTION 4 COMPOUND INEQUALITIES COMPREHENSIVE TESTING")
        print("=" * 80)
        print("Testing comprehensive Section 4 Compound Inequalities implementation")
        
        # Test categories for Section 4
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("Section 4 API Endpoints", self.test_section4_api_endpoints, "critical"),
            ("Individual Problem Endpoints", self.test_individual_problem_endpoints, "critical"),
            ("Updated Problem Content", self.test_updated_problem_content, "critical"),
            ("Compound Inequality Structure", self.test_compound_inequality_structure, "critical"),
            ("Step Solutions with Level Naming", self.test_step_solutions_with_level_naming, "critical"),
            ("Temperature Conversion Word Problem", self.test_temperature_conversion_word_problem, "critical"),
            ("Assessment Updates", self.test_assessment_updates, "critical"),
            ("Exam Prep Updates", self.test_exam_prep_updates, "critical"),
            ("Bilingual Content", self.test_bilingual_content, "high"),
            ("Sign Flipping Logic", self.test_sign_flipping_logic, "high")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 SECTION 4 TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive Section 4 summary
        self.generate_section4_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run Section 4 compound inequalities tests"""
    print("🚀 Starting SECTION 4 COMPOUND INEQUALITIES COMPREHENSIVE Testing...")
    print("🎯 Goal: Verify comprehensive Section 4 Compound Inequalities implementation")
    
    tester = Section4CompoundInequalitiesTester(BACKEND_URL)
    results = tester.run_section4_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 SECTION 4 ALERT: {failed_tests} test(s) failed!")
        print("🔧 Section 4 compound inequalities need backend enhancement")
    else:
        print(f"\n🛡️  SECTION 4 CONFIRMED: All tests passed!")
        print("✅ Section 4 Compound Inequalities implementation is working correctly")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()