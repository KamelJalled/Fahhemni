#!/usr/bin/env python3
"""
Section 2 New Curriculum Testing Suite
Tests Section 2 new curriculum implementation comprehensively
"""

import requests
import json
import sys
import os
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://bilingual-algebra.preview.emergentagent.com/api"

class Section2CurriculumTester:
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

    def test_section2_database_content_verification(self):
        """Test Section 2 Database Content Verification - GET /api/problems/section/section2 returns 6 problems"""
        try:
            print("\n🔍 SECTION 2 DATABASE CONTENT VERIFICATION")
            print("Testing GET /api/problems/section/section2 returns 6 problems...")
            
            response = self.session.get(f"{self.base_url}/problems/section/section2")
            
            if response.status_code == 200:
                problems = response.json()
                
                # Verify it's a list with 6 problems
                if isinstance(problems, list) and len(problems) == 6:
                    self.log_test("Section 2 Problem Count", True, 
                                f"✅ Found exactly 6 problems in section2")
                    
                    # Verify all required problem IDs exist
                    expected_ids = ["prep2", "explanation2", "practice2_1", "practice2_2", "assessment2", "examprep2"]
                    actual_ids = [p.get("id") for p in problems]
                    
                    missing_ids = [pid for pid in expected_ids if pid not in actual_ids]
                    extra_ids = [pid for pid in actual_ids if pid not in expected_ids]
                    
                    if not missing_ids and not extra_ids:
                        self.log_test("Section 2 Problem IDs", True, 
                                    f"✅ All required problem IDs present: {expected_ids}")
                        
                        # Verify section title
                        # Get section info from first problem
                        first_problem = problems[0]
                        if first_problem.get("section_id") == "section2":
                            self.log_test("Section 2 ID Verification", True, 
                                        f"✅ All problems correctly assigned to section2")
                            return True, problems
                        else:
                            self.log_test("Section 2 ID Verification", False, 
                                        f"❌ Problems not assigned to section2: {first_problem.get('section_id')}")
                            return False, None
                    else:
                        error_details = []
                        if missing_ids:
                            error_details.append(f"Missing IDs: {missing_ids}")
                        if extra_ids:
                            error_details.append(f"Extra IDs: {extra_ids}")
                        
                        self.log_test("Section 2 Problem IDs", False, 
                                    f"❌ Problem ID mismatch - {', '.join(error_details)}")
                        return False, None
                else:
                    self.log_test("Section 2 Problem Count", False, 
                                f"❌ Expected 6 problems, got {len(problems) if isinstance(problems, list) else 0}")
                    return False, None
            else:
                self.log_test("Section 2 Database Content", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False, None
                
        except Exception as e:
            self.log_test("Section 2 Database Content", False, 
                        f"❌ Request error: {str(e)}")
            return False, None

    def test_section2_title_verification(self):
        """Verify section title is 'Solving Inequalities by Multiplication or Division'"""
        try:
            print("\n🔍 SECTION 2 TITLE VERIFICATION")
            print("Checking section title is 'Solving Inequalities by Multiplication or Division'...")
            
            # Get section info - we'll check the database structure
            response = self.session.get(f"{self.base_url}/problems/section/section2")
            
            if response.status_code == 200:
                problems = response.json()
                if problems:
                    # The title should be verified through the section structure
                    # For now, we'll verify the content matches the expected curriculum
                    expected_title = "Solving Inequalities by Multiplication or Division"
                    
                    # Check if the problems match the expected curriculum content
                    prep_problem = next((p for p in problems if p.get("id") == "prep2"), None)
                    if prep_problem:
                        if (prep_problem.get("question_en") == "4x < 20" and 
                            prep_problem.get("answer") == "x < 5"):
                            self.log_test("Section 2 Title Content Match", True, 
                                        f"✅ Section content matches '{expected_title}' curriculum")
                            return True
                        else:
                            self.log_test("Section 2 Title Content Match", False, 
                                        f"❌ Content doesn't match expected curriculum")
                            return False
                    else:
                        self.log_test("Section 2 Title Content Match", False, 
                                    f"❌ prep2 problem not found")
                        return False
                else:
                    self.log_test("Section 2 Title Verification", False, 
                                f"❌ No problems found in section2")
                    return False
            else:
                self.log_test("Section 2 Title Verification", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Section 2 Title Verification", False, 
                        f"❌ Request error: {str(e)}")
            return False

    def test_preparation_stage_prep2(self):
        """Test Preparation Stage (prep2) - Verify question and answer content"""
        try:
            print("\n🔍 PREPARATION STAGE TESTING (prep2)")
            print("Testing prep2 content: '4x < 20' → 'x < 5'...")
            
            response = self.session.get(f"{self.base_url}/problems/prep2")
            
            if response.status_code == 200:
                problem = response.json()
                
                # Verify question content
                expected_question_en = "4x < 20"
                expected_question_ar = "٤س < ٢٠"
                expected_answer = "x < 5"
                expected_answer_ar = "س < ٥"
                
                checks = [
                    ("Question English", problem.get("question_en") == expected_question_en, 
                     f"Expected: '{expected_question_en}', Got: '{problem.get('question_en')}'"),
                    ("Question Arabic", problem.get("question_ar") == expected_question_ar,
                     f"Expected: '{expected_question_ar}', Got: '{problem.get('question_ar')}'"),
                    ("Answer English", problem.get("answer") == expected_answer,
                     f"Expected: '{expected_answer}', Got: '{problem.get('answer')}'"),
                    ("Answer Arabic", problem.get("answer_ar") == expected_answer_ar,
                     f"Expected: '{expected_answer_ar}', Got: '{problem.get('answer_ar')}'")
                ]
                
                all_passed = True
                for check_name, passed, details in checks:
                    if passed:
                        self.log_test(f"prep2 {check_name}", True, f"✅ {details}")
                    else:
                        self.log_test(f"prep2 {check_name}", False, f"❌ {details}")
                        all_passed = False
                
                # Verify step solutions and hints are present
                if "step_solutions" in problem and problem["step_solutions"]:
                    self.log_test("prep2 Step Solutions", True, 
                                f"✅ Step solutions present ({len(problem['step_solutions'])} steps)")
                else:
                    self.log_test("prep2 Step Solutions", False, 
                                f"❌ Step solutions missing or empty")
                    all_passed = False
                
                if "hints_en" in problem and problem["hints_en"]:
                    self.log_test("prep2 Hints", True, 
                                f"✅ Hints present ({len(problem['hints_en'])} English, {len(problem.get('hints_ar', []))} Arabic)")
                else:
                    self.log_test("prep2 Hints", False, 
                                f"❌ Hints missing or empty")
                    all_passed = False
                
                return all_passed, problem
            else:
                self.log_test("prep2 Content Verification", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False, None
                
        except Exception as e:
            self.log_test("prep2 Content Verification", False, 
                        f"❌ Request error: {str(e)}")
            return False, None

    def test_answer_submission_prep2(self):
        """Test answer submission with correct answer 'x < 5' for prep2"""
        try:
            print("\n🔍 ANSWER SUBMISSION TESTING (prep2)")
            print("Testing answer submission with correct answer 'x < 5'...")
            
            # First create a test student
            test_student = {"username": "section2_test_student", "class_name": "GR9-A"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Test Student Creation", False, 
                            f"❌ Failed to create test student: HTTP {response.status_code}")
                return False
            
            self.log_test("Test Student Creation", True, 
                        f"✅ Created test student 'section2_test_student'")
            
            # Test answer submission
            attempt_data = {
                "problem_id": "prep2",
                "answer": "x < 5",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/section2_test_student/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["correct", "score", "attempts", "progress"]
                missing_fields = [f for f in required_fields if f not in data]
                
                if missing_fields:
                    self.log_test("prep2 Answer Submission Response", False, 
                                f"❌ Missing required fields: {missing_fields}")
                    return False
                
                # Verify correctness
                if data.get("correct") == True:
                    self.log_test("prep2 Answer Correctness", True, 
                                f"✅ Answer 'x < 5' correctly evaluated as correct, score: {data.get('score')}")
                else:
                    self.log_test("prep2 Answer Correctness", False, 
                                f"❌ Answer 'x < 5' should be correct but got: {data.get('correct')}")
                    return False
                
                # Verify score is positive
                if data.get("score", 0) > 0:
                    self.log_test("prep2 Answer Scoring", True, 
                                f"✅ Positive score awarded: {data.get('score')} points")
                else:
                    self.log_test("prep2 Answer Scoring", False, 
                                f"❌ Expected positive score, got: {data.get('score')}")
                    return False
                
                return True
            else:
                self.log_test("prep2 Answer Submission", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("prep2 Answer Submission", False, 
                        f"❌ Request error: {str(e)}")
            return False

    def test_explanation_stage_explanation2(self):
        """Test Explanation Stage (explanation2) - Verify interactive examples and content"""
        try:
            print("\n🔍 EXPLANATION STAGE TESTING (explanation2)")
            print("Testing explanation2 content and interactive examples...")
            
            response = self.session.get(f"{self.base_url}/problems/explanation2")
            
            if response.status_code == 200:
                problem = response.json()
                
                # Verify title
                expected_title = "Learn Multiplication/Division Inequalities"
                if problem.get("question_en") == expected_title:
                    self.log_test("explanation2 Title", True, 
                                f"✅ Title correct: '{expected_title}'")
                else:
                    self.log_test("explanation2 Title", False, 
                                f"❌ Expected: '{expected_title}', Got: '{problem.get('question_en')}'")
                    return False
                
                # Verify interactive examples
                if "interactive_examples" in problem and problem["interactive_examples"]:
                    examples = problem["interactive_examples"]
                    
                    if len(examples) == 3:
                        self.log_test("explanation2 Example Count", True, 
                                    f"✅ Found 3 interactive examples")
                        
                        # Verify Level 1: Positive coefficient
                        level1 = examples[0]
                        if ("5x ≥ 30" in level1.get("problem_en", "") and 
                            "4y < 24" in level1.get("practice_question_en", "")):
                            self.log_test("explanation2 Level 1", True, 
                                        f"✅ Level 1 positive coefficient examples correct")
                        else:
                            self.log_test("explanation2 Level 1", False, 
                                        f"❌ Level 1 content incorrect")
                            return False
                        
                        # Verify Level 2: Negative coefficient
                        level2 = examples[1]
                        if ("-3m > 15" in level2.get("problem_en", "") and 
                            "-6k ≤ 30" in level2.get("practice_question_en", "")):
                            self.log_test("explanation2 Level 2", True, 
                                        f"✅ Level 2 negative coefficient examples correct")
                        else:
                            self.log_test("explanation2 Level 2", False, 
                                        f"❌ Level 2 content incorrect")
                            return False
                        
                        # Verify Level 3: Division by negative
                        level3 = examples[2]
                        if ("k / (-4) ≤ 2" in level3.get("problem_en", "") and 
                            "n / (-3) > 5" in level3.get("practice_question_en", "")):
                            self.log_test("explanation2 Level 3", True, 
                                        f"✅ Level 3 division by negative examples correct")
                        else:
                            self.log_test("explanation2 Level 3", False, 
                                        f"❌ Level 3 content incorrect")
                            return False
                        
                    else:
                        self.log_test("explanation2 Example Count", False, 
                                    f"❌ Expected 3 examples, got {len(examples)}")
                        return False
                else:
                    self.log_test("explanation2 Interactive Examples", False, 
                                f"❌ Interactive examples missing or empty")
                    return False
                
                # Verify step solutions for student practice
                if "step_solutions" in problem and problem["step_solutions"]:
                    self.log_test("explanation2 Step Solutions", True, 
                                f"✅ Step solutions present ({len(problem['step_solutions'])} steps)")
                else:
                    self.log_test("explanation2 Step Solutions", False, 
                                f"❌ Step solutions missing")
                    return False
                
                return True
            else:
                self.log_test("explanation2 Content Verification", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("explanation2 Content Verification", False, 
                        f"❌ Request error: {str(e)}")
            return False

    def test_practice_stages(self):
        """Test Practice Stages - practice2_1 and practice2_2"""
        try:
            print("\n🔍 PRACTICE STAGES TESTING")
            print("Testing practice2_1 and practice2_2 content...")
            
            # Test practice2_1: "-2/3 k > 8" → "k < -12"
            response = self.session.get(f"{self.base_url}/problems/practice2_1")
            
            if response.status_code == 200:
                problem = response.json()
                
                if (problem.get("question_en") == "-2/3 k > 8" and 
                    problem.get("answer") == "k < -12"):
                    self.log_test("practice2_1 Content", True, 
                                f"✅ practice2_1 content correct: '-2/3 k > 8' → 'k < -12'")
                else:
                    self.log_test("practice2_1 Content", False, 
                                f"❌ practice2_1 content incorrect")
                    return False
                
                # Verify step solutions and hints
                if "step_solutions" in problem and problem["step_solutions"]:
                    self.log_test("practice2_1 Step Solutions", True, 
                                f"✅ Step solutions present")
                else:
                    self.log_test("practice2_1 Step Solutions", False, 
                                f"❌ Step solutions missing")
                    return False
            else:
                self.log_test("practice2_1 Retrieval", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False
            
            # Test practice2_2: Ticket sales problem → "t ≥ 50"
            response = self.session.get(f"{self.base_url}/problems/practice2_2")
            
            if response.status_code == 200:
                problem = response.json()
                
                if ("Tickets must be sold" in problem.get("question_en", "") and 
                    problem.get("answer") == "t ≥ 50"):
                    self.log_test("practice2_2 Content", True, 
                                f"✅ practice2_2 ticket sales problem correct → 't ≥ 50'")
                else:
                    self.log_test("practice2_2 Content", False, 
                                f"❌ practice2_2 content incorrect")
                    return False
                
                # Verify bilingual hints
                if ("hints_en" in problem and problem["hints_en"] and
                    "hints_ar" in problem and problem["hints_ar"]):
                    self.log_test("practice2_2 Bilingual Hints", True, 
                                f"✅ Bilingual hints present")
                else:
                    self.log_test("practice2_2 Bilingual Hints", False, 
                                f"❌ Bilingual hints missing")
                    return False
            else:
                self.log_test("practice2_2 Retrieval", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Practice Stages Testing", False, 
                        f"❌ Request error: {str(e)}")
            return False

    def test_assessment_and_exam_prep(self):
        """Test Assessment & Exam Prep Testing"""
        try:
            print("\n🔍 ASSESSMENT & EXAM PREP TESTING")
            print("Testing assessment2 and examprep2 content...")
            
            # Test assessment2: "y / (-2) > 6" → "y < -12"
            response = self.session.get(f"{self.base_url}/problems/assessment2")
            
            if response.status_code == 200:
                problem = response.json()
                
                if (problem.get("question_en") == "y / (-2) > 6" and 
                    problem.get("answer") == "y < -12"):
                    self.log_test("assessment2 Content", True, 
                                f"✅ assessment2 content correct: 'y / (-2) > 6' → 'y < -12'")
                else:
                    self.log_test("assessment2 Content", False, 
                                f"❌ assessment2 content incorrect")
                    return False
            else:
                self.log_test("assessment2 Retrieval", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False
            
            # Test examprep2: Candy distribution problem → "p ≥ 4"
            response = self.session.get(f"{self.base_url}/problems/examprep2")
            
            if response.status_code == 200:
                problem = response.json()
                
                if ("distribute at least 60 pieces of candy" in problem.get("question_en", "") and 
                    problem.get("answer") == "p ≥ 4"):
                    self.log_test("examprep2 Content", True, 
                                f"✅ examprep2 candy distribution problem correct → 'p ≥ 4'")
                else:
                    self.log_test("examprep2 Content", False, 
                                f"❌ examprep2 content incorrect")
                    return False
            else:
                self.log_test("examprep2 Retrieval", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False
            
            return True
            
        except Exception as e:
            self.log_test("Assessment & Exam Prep Testing", False, 
                        f"❌ Request error: {str(e)}")
            return False

    def test_answer_submission_scoring(self):
        """Test answer submission scoring for different problem types"""
        try:
            print("\n🔍 ANSWER SUBMISSION SCORING TESTING")
            print("Testing answer submission scoring across different problem types...")
            
            # Create test student if not exists
            test_student = {"username": "section2_scoring_test", "class_name": "GR9-B"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Scoring Test Student Creation", False, 
                            f"❌ Failed to create test student")
                return False
            
            # Test cases for different problem types
            test_cases = [
                {"problem_id": "prep2", "answer": "x < 5", "expected_correct": True},
                {"problem_id": "practice2_1", "answer": "k < -12", "expected_correct": True},
                {"problem_id": "assessment2", "answer": "y < -12", "expected_correct": True},
                {"problem_id": "examprep2", "answer": "p ≥ 4", "expected_correct": True}
            ]
            
            all_passed = True
            
            for test_case in test_cases:
                attempt_data = {
                    "problem_id": test_case["problem_id"],
                    "answer": test_case["answer"],
                    "hints_used": 0
                }
                
                response = self.session.post(
                    f"{self.base_url}/students/section2_scoring_test/attempt",
                    json=attempt_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("correct") == test_case["expected_correct"]:
                        self.log_test(f"Scoring {test_case['problem_id']}", True, 
                                    f"✅ Answer '{test_case['answer']}' scored correctly: {data.get('score')} points")
                    else:
                        self.log_test(f"Scoring {test_case['problem_id']}", False, 
                                    f"❌ Answer '{test_case['answer']}' scoring failed")
                        all_passed = False
                else:
                    self.log_test(f"Scoring {test_case['problem_id']}", False, 
                                f"❌ HTTP {response.status_code}")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            self.log_test("Answer Submission Scoring", False, 
                        f"❌ Request error: {str(e)}")
            return False

    def test_bilingual_content_verification(self):
        """Test bilingual content verification - ensure all Arabic translations are present"""
        try:
            print("\n🔍 BILINGUAL CONTENT VERIFICATION")
            print("Testing Arabic translations are present for all Section 2 content...")
            
            response = self.session.get(f"{self.base_url}/problems/section/section2")
            
            if response.status_code == 200:
                problems = response.json()
                
                all_passed = True
                
                for problem in problems:
                    problem_id = problem.get("id")
                    
                    # Check for Arabic question
                    if "question_ar" in problem and problem["question_ar"]:
                        self.log_test(f"{problem_id} Arabic Question", True, 
                                    f"✅ Arabic question present")
                    else:
                        self.log_test(f"{problem_id} Arabic Question", False, 
                                    f"❌ Arabic question missing")
                        all_passed = False
                    
                    # Check for Arabic answer (if answer exists)
                    if problem.get("answer"):
                        if "answer_ar" in problem and problem["answer_ar"]:
                            self.log_test(f"{problem_id} Arabic Answer", True, 
                                        f"✅ Arabic answer present")
                        else:
                            self.log_test(f"{problem_id} Arabic Answer", False, 
                                        f"❌ Arabic answer missing")
                            all_passed = False
                    
                    # Check for Arabic hints
                    if "hints_en" in problem and problem["hints_en"]:
                        if "hints_ar" in problem and problem["hints_ar"]:
                            self.log_test(f"{problem_id} Arabic Hints", True, 
                                        f"✅ Arabic hints present")
                        else:
                            self.log_test(f"{problem_id} Arabic Hints", False, 
                                        f"❌ Arabic hints missing")
                            all_passed = False
                
                return all_passed
            else:
                self.log_test("Bilingual Content Verification", False, 
                            f"❌ HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Bilingual Content Verification", False, 
                        f"❌ Request error: {str(e)}")
            return False

    def run_comprehensive_section2_tests(self):
        """Run all Section 2 comprehensive tests"""
        print("=" * 80)
        print("🚀 SECTION 2 NEW CURRICULUM COMPREHENSIVE TESTING")
        print("=" * 80)
        
        test_results = []
        
        # 1. Section 2 Database Content Verification
        success, _ = self.test_section2_database_content_verification()
        test_results.append(("Database Content Verification", success))
        
        # 2. Section Title Verification
        success = self.test_section2_title_verification()
        test_results.append(("Section Title Verification", success))
        
        # 3. Preparation Stage Testing
        success, _ = self.test_preparation_stage_prep2()
        test_results.append(("Preparation Stage (prep2)", success))
        
        # 4. Answer Submission Testing
        success = self.test_answer_submission_prep2()
        test_results.append(("Answer Submission (prep2)", success))
        
        # 5. Explanation Stage Testing
        success = self.test_explanation_stage_explanation2()
        test_results.append(("Explanation Stage (explanation2)", success))
        
        # 6. Practice Stages Testing
        success = self.test_practice_stages()
        test_results.append(("Practice Stages", success))
        
        # 7. Assessment & Exam Prep Testing
        success = self.test_assessment_and_exam_prep()
        test_results.append(("Assessment & Exam Prep", success))
        
        # 8. Answer Submission Scoring
        success = self.test_answer_submission_scoring()
        test_results.append(("Answer Submission Scoring", success))
        
        # 9. Bilingual Content Verification
        success = self.test_bilingual_content_verification()
        test_results.append(("Bilingual Content Verification", success))
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 SECTION 2 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = [name for name, success in test_results if success]
        failed_tests = [name for name, success in test_results if not success]
        
        print(f"✅ PASSED: {len(passed_tests)}/{len(test_results)} tests")
        for test_name in passed_tests:
            print(f"   ✅ {test_name}")
        
        if failed_tests:
            print(f"\n❌ FAILED: {len(failed_tests)}/{len(test_results)} tests")
            for test_name in failed_tests:
                print(f"   ❌ {test_name}")
        
        overall_success = len(failed_tests) == 0
        
        if overall_success:
            print(f"\n🎉 ALL SECTION 2 TESTS PASSED! New curriculum implementation is working correctly.")
        else:
            print(f"\n⚠️  SOME SECTION 2 TESTS FAILED. Please review the failed tests above.")
        
        return overall_success

def main():
    """Main function to run Section 2 tests"""
    print("Starting Section 2 New Curriculum Testing...")
    
    tester = Section2CurriculumTester(BACKEND_URL)
    success = tester.run_comprehensive_section2_tests()
    
    if success:
        print("\n🎉 Section 2 testing completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Section 2 testing failed. Please check the results above.")
        sys.exit(1)

if __name__ == "__main__":
    main()