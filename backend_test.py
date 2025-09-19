#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - Section 2 Word Problem 3-Step Enforcement Fix
Tests the critical pedagogical bug fix where word problems were completing at Step 2 instead of 
requiring the complete 3-step mathematical process for proper learning.

CRITICAL REQUIREMENTS BEING TESTED:
- Both word problems must have exactly 3 steps (not 2)
- Step 2 must only accept operation display, not final simplified answer
- Step 3 must be required for completion
- System must not allow progression to next stage until Step 3 is completed
"""

import requests
import json
import sys
import os
import re
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://inequality-solver.preview.emergentagent.com/api"

class Section2StepEnforcementTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "step_enforcement_test_student"
        
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
        """Create test student for step enforcement testing"""
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

    def test_step_count_verification(self):
        """Test that both practice2_2 and examprep2 have exactly 3 step_solutions"""
        try:
            print("\n📊 STEP COUNT VERIFICATION")
            print("Testing that both word problems have exactly 3 steps defined in database")
            
            # Test practice2_2 step count
            response = self.session.get(f"{self.base_url}/problems/practice2_2?username={self.test_student_username}")
            
            if response.status_code == 200:
                practice2_2_data = response.json()
                step_solutions = practice2_2_data.get("step_solutions", [])
                
                if len(step_solutions) == 3:
                    self.log_test("practice2_2 Step Count", True, 
                                f"✅ practice2_2 has exactly 3 steps: {len(step_solutions)}")
                else:
                    self.log_test("practice2_2 Step Count", False, 
                                f"❌ practice2_2 has {len(step_solutions)} steps, expected 3")
                    return False
            else:
                self.log_test("practice2_2 Step Count", False, 
                            f"Failed to fetch practice2_2: HTTP {response.status_code}")
                return False
            
            # Complete prerequisites for examprep2
            if not self.complete_required_stages_for_examprep2():
                self.log_test("examprep2 Prerequisites", False, 
                            "❌ Failed to complete required stages for examprep2 access")
                return False
            
            # Test examprep2 step count
            response = self.session.get(f"{self.base_url}/problems/examprep2?username={self.test_student_username}")
            
            if response.status_code == 200:
                examprep2_data = response.json()
                step_solutions = examprep2_data.get("step_solutions", [])
                
                if len(step_solutions) == 3:
                    self.log_test("examprep2 Step Count", True, 
                                f"✅ examprep2 has exactly 3 steps: {len(step_solutions)}")
                    return True
                else:
                    self.log_test("examprep2 Step Count", False, 
                                f"❌ examprep2 has {len(step_solutions)} steps, expected 3")
                    return False
            else:
                self.log_test("examprep2 Step Count", False, 
                            f"Failed to fetch examprep2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Step Count Verification", False, f"Test execution error: {str(e)}")
            return False

    def test_step_structure_validation(self):
        """Test the 3-step structure for both problems matches expected format"""
        try:
            print("\n🏗️ STEP STRUCTURE VALIDATION")
            print("Verifying the 3-step structure matches expected format for both problems")
            
            # Get practice2_2 data
            response = self.session.get(f"{self.base_url}/problems/practice2_2?username={self.test_student_username}")
            
            if response.status_code == 200:
                practice2_2_data = response.json()
                step_solutions = practice2_2_data.get("step_solutions", [])
                
                # Verify practice2_2 step structure
                expected_practice2_2_steps = [
                    {"step": 1, "description": "Write inequality", "expected_answers": ["10t ≥ 500", "10 * t ≥ 500"]},
                    {"step": 2, "description": "Show operation", "expected_answers": ["10t / 10 ≥ 500 / 10", "t ≥ 500 / 10"]},
                    {"step": 3, "description": "Final answer", "expected_answers": ["t ≥ 50"]}
                ]
                
                practice2_2_valid = True
                for i, expected_step in enumerate(expected_practice2_2_steps):
                    if i < len(step_solutions):
                        step = step_solutions[i]
                        possible_answers = step.get("possible_answers", [])
                        
                        # Check if expected answers are present
                        expected_found = any(exp_ans in possible_answers for exp_ans in expected_step["expected_answers"])
                        
                        if expected_found:
                            self.log_test(f"practice2_2 Step {i+1} Structure", True, 
                                        f"✅ Step {i+1} contains expected answers: {expected_step['expected_answers']}")
                        else:
                            self.log_test(f"practice2_2 Step {i+1} Structure", False, 
                                        f"❌ Step {i+1} missing expected answers. Got: {possible_answers}")
                            practice2_2_valid = False
                    else:
                        self.log_test(f"practice2_2 Step {i+1} Structure", False, 
                                    f"❌ Step {i+1} missing from step_solutions")
                        practice2_2_valid = False
                
                if not practice2_2_valid:
                    return False
            else:
                self.log_test("practice2_2 Step Structure", False, 
                            f"Failed to fetch practice2_2: HTTP {response.status_code}")
                return False
            
            # Get examprep2 data
            response = self.session.get(f"{self.base_url}/problems/examprep2?username={self.test_student_username}")
            
            if response.status_code == 200:
                examprep2_data = response.json()
                step_solutions = examprep2_data.get("step_solutions", [])
                
                # Verify examprep2 step structure
                expected_examprep2_steps = [
                    {"step": 1, "description": "Write inequality", "expected_answers": ["15p ≥ 60", "15 * p ≥ 60"]},
                    {"step": 2, "description": "Show operation", "expected_answers": ["15p / 15 ≥ 60 / 15", "p ≥ 60 / 15"]},
                    {"step": 3, "description": "Final answer", "expected_answers": ["p ≥ 4"]}
                ]
                
                examprep2_valid = True
                for i, expected_step in enumerate(expected_examprep2_steps):
                    if i < len(step_solutions):
                        step = step_solutions[i]
                        possible_answers = step.get("possible_answers", [])
                        
                        # Check if expected answers are present
                        expected_found = any(exp_ans in possible_answers for exp_ans in expected_step["expected_answers"])
                        
                        if expected_found:
                            self.log_test(f"examprep2 Step {i+1} Structure", True, 
                                        f"✅ Step {i+1} contains expected answers: {expected_step['expected_answers']}")
                        else:
                            self.log_test(f"examprep2 Step {i+1} Structure", False, 
                                        f"❌ Step {i+1} missing expected answers. Got: {possible_answers}")
                            examprep2_valid = False
                    else:
                        self.log_test(f"examprep2 Step {i+1} Structure", False, 
                                    f"❌ Step {i+1} missing from step_solutions")
                        examprep2_valid = False
                
                return examprep2_valid
            else:
                self.log_test("examprep2 Step Structure", False, 
                            f"Failed to fetch examprep2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Step Structure Validation", False, f"Test execution error: {str(e)}")
            return False

    def test_premature_completion_prevention(self):
        """Test that Step 2 no longer accepts the final answer to prevent skipping Step 3"""
        try:
            print("\n🚫 PREMATURE COMPLETION PREVENTION")
            print("Testing that Step 2 rejects final answers (t ≥ 50, p ≥ 4) to prevent skipping Step 3")
            
            # Test practice2_2 - Step 2 should NOT accept "t ≥ 50"
            response = self.session.get(f"{self.base_url}/problems/practice2_2?username={self.test_student_username}")
            
            if response.status_code == 200:
                practice2_2_data = response.json()
                step_solutions = practice2_2_data.get("step_solutions", [])
                
                if len(step_solutions) >= 2:
                    step2_answers = step_solutions[1].get("possible_answers", [])
                    
                    # Check that Step 2 does NOT contain the final answer "t ≥ 50"
                    final_answer_in_step2 = "t ≥ 50" in step2_answers
                    
                    if not final_answer_in_step2:
                        self.log_test("practice2_2 Step 2 Final Answer Prevention", True, 
                                    f"✅ Step 2 correctly excludes final answer 't ≥ 50'. Accepts: {step2_answers}")
                    else:
                        self.log_test("practice2_2 Step 2 Final Answer Prevention", False, 
                                    f"❌ CRITICAL BUG: Step 2 still accepts final answer 't ≥ 50'")
                        return False
                else:
                    self.log_test("practice2_2 Step 2 Final Answer Prevention", False, 
                                f"❌ practice2_2 missing Step 2 data")
                    return False
            else:
                self.log_test("practice2_2 Step 2 Final Answer Prevention", False, 
                            f"Failed to fetch practice2_2: HTTP {response.status_code}")
                return False
            
            # Test examprep2 - Step 2 should NOT accept "p ≥ 4"
            response = self.session.get(f"{self.base_url}/problems/examprep2?username={self.test_student_username}")
            
            if response.status_code == 200:
                examprep2_data = response.json()
                step_solutions = examprep2_data.get("step_solutions", [])
                
                if len(step_solutions) >= 2:
                    step2_answers = step_solutions[1].get("possible_answers", [])
                    
                    # Check that Step 2 does NOT contain the final answer "p ≥ 4"
                    final_answer_in_step2 = "p ≥ 4" in step2_answers
                    
                    if not final_answer_in_step2:
                        self.log_test("examprep2 Step 2 Final Answer Prevention", True, 
                                    f"✅ Step 2 correctly excludes final answer 'p ≥ 4'. Accepts: {step2_answers}")
                        return True
                    else:
                        self.log_test("examprep2 Step 2 Final Answer Prevention", False, 
                                    f"❌ CRITICAL BUG: Step 2 still accepts final answer 'p ≥ 4'")
                        return False
                else:
                    self.log_test("examprep2 Step 2 Final Answer Prevention", False, 
                                f"❌ examprep2 missing Step 2 data")
                    return False
            else:
                self.log_test("examprep2 Step 2 Final Answer Prevention", False, 
                            f"Failed to fetch examprep2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Premature Completion Prevention", False, f"Test execution error: {str(e)}")
            return False

    def test_step_progression_logic(self):
        """Test that the system properly requires completion of all 3 steps before marking complete"""
        try:
            print("\n🔄 STEP PROGRESSION LOGIC")
            print("Testing that all 3 steps must be completed before problem is marked as complete")
            
            # Create a fresh test student for step progression testing
            step_test_student = "step_progression_test_student"
            test_student = {"username": step_test_student, "class_name": "GR9-A"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Step Progression Test Student", False, 
                            f"Failed to create step progression test student")
                return False
            
            # Complete prerequisites for practice2_2 testing
            if not self.complete_required_stages_for_practice2_2(step_test_student):
                self.log_test("practice2_2 Step Progression Prerequisites", False, 
                            "❌ Failed to complete prerequisites for practice2_2")
                return False
            
            # Test practice2_2 step progression
            # Step 1: Submit correct answer for Step 1
            step1_attempt = {
                "problem_id": "practice2_2",
                "answer": "10t ≥ 500",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{step_test_student}/attempt",
                json=step1_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("correct"):
                    # Check that problem is NOT marked as completed after Step 1
                    progress = result.get("progress", {})
                    if not progress.get("completed", True):  # Should be False
                        self.log_test("practice2_2 Step 1 Incomplete", True, 
                                    f"✅ Problem correctly remains incomplete after Step 1")
                    else:
                        self.log_test("practice2_2 Step 1 Incomplete", False, 
                                    f"❌ CRITICAL BUG: Problem marked complete after Step 1")
                        return False
                else:
                    self.log_test("practice2_2 Step 1 Answer", False, 
                                f"❌ Step 1 answer '10t ≥ 500' was rejected")
                    return False
            else:
                self.log_test("practice2_2 Step 1 Submission", False, 
                            f"Failed to submit Step 1: HTTP {response.status_code}")
                return False
            
            # Step 2: Submit correct answer for Step 2
            step2_attempt = {
                "problem_id": "practice2_2",
                "answer": "10t / 10 ≥ 500 / 10",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{step_test_student}/attempt",
                json=step2_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("correct"):
                    # Check that problem is STILL NOT marked as completed after Step 2
                    progress = result.get("progress", {})
                    if not progress.get("completed", True):  # Should be False
                        self.log_test("practice2_2 Step 2 Incomplete", True, 
                                    f"✅ Problem correctly remains incomplete after Step 2")
                    else:
                        self.log_test("practice2_2 Step 2 Incomplete", False, 
                                    f"❌ CRITICAL BUG: Problem marked complete after Step 2 (should require Step 3)")
                        return False
                else:
                    self.log_test("practice2_2 Step 2 Answer", False, 
                                f"❌ Step 2 answer '10t / 10 ≥ 500 / 10' was rejected")
                    return False
            else:
                self.log_test("practice2_2 Step 2 Submission", False, 
                            f"Failed to submit Step 2: HTTP {response.status_code}")
                return False
            
            # Step 3: Submit correct answer for Step 3
            step3_attempt = {
                "problem_id": "practice2_2",
                "answer": "t ≥ 50",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{step_test_student}/attempt",
                json=step3_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("correct"):
                    # Check that problem is NOW marked as completed after Step 3
                    progress = result.get("progress", {})
                    if progress.get("completed", False):  # Should be True
                        self.log_test("practice2_2 Step 3 Complete", True, 
                                    f"✅ Problem correctly marked complete after Step 3")
                        return True
                    else:
                        self.log_test("practice2_2 Step 3 Complete", False, 
                                    f"❌ CRITICAL BUG: Problem not marked complete after Step 3")
                        return False
                else:
                    self.log_test("practice2_2 Step 3 Answer", False, 
                                f"❌ Step 3 answer 't ≥ 50' was rejected")
                    return False
            else:
                self.log_test("practice2_2 Step 3 Submission", False, 
                            f"Failed to submit Step 3: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Step Progression Logic", False, f"Test execution error: {str(e)}")
            return False

    def test_database_content_integrity(self):
        """Test that questions, answers, and hints remain correct for both problems"""
        try:
            print("\n🗄️ DATABASE CONTENT INTEGRITY")
            print("Verifying questions, answers, and hints remain correct after 3-step enforcement fix")
            
            # Test practice2_2 content integrity
            response = self.session.get(f"{self.base_url}/problems/practice2_2?username={self.test_student_username}")
            
            if response.status_code == 200:
                practice2_2_data = response.json()
                
                # Verify question content
                expected_question_keywords = ["Tickets", "SAR 10", "at least SAR 500", "minimum number"]
                question_en = practice2_2_data.get("question_en", "")
                
                question_valid = all(keyword in question_en for keyword in expected_question_keywords)
                
                if question_valid:
                    self.log_test("practice2_2 Question Integrity", True, 
                                f"✅ Question contains all expected elements")
                else:
                    self.log_test("practice2_2 Question Integrity", False, 
                                f"❌ Question missing expected elements. Got: {question_en}")
                    return False
                
                # Verify answer
                expected_answer = "t ≥ 50"
                actual_answer = practice2_2_data.get("answer", "")
                
                if actual_answer == expected_answer:
                    self.log_test("practice2_2 Answer Integrity", True, 
                                f"✅ Answer correct: {actual_answer}")
                else:
                    self.log_test("practice2_2 Answer Integrity", False, 
                                f"❌ Answer incorrect. Expected: {expected_answer}, Got: {actual_answer}")
                    return False
                
                # Verify hints are present and follow Socratic method
                hints_en = practice2_2_data.get("hints_en", [])
                
                if len(hints_en) == 3:
                    # Check that hints don't reveal direct inequality
                    hints_text = " ".join(hints_en)
                    if "10t ≥ 500" not in hints_text and "t ≥ 50" not in hints_text:
                        self.log_test("practice2_2 Hints Integrity", True, 
                                    f"✅ Hints follow Socratic method without revealing answers")
                    else:
                        self.log_test("practice2_2 Hints Integrity", False, 
                                    f"❌ Hints reveal direct answers")
                        return False
                else:
                    self.log_test("practice2_2 Hints Integrity", False, 
                                f"❌ Expected 3 hints, got {len(hints_en)}")
                    return False
            else:
                self.log_test("practice2_2 Content Integrity", False, 
                            f"Failed to fetch practice2_2: HTTP {response.status_code}")
                return False
            
            # Test examprep2 content integrity
            response = self.session.get(f"{self.base_url}/problems/examprep2?username={self.test_student_username}")
            
            if response.status_code == 200:
                examprep2_data = response.json()
                
                # Verify question content
                expected_question_keywords = ["distribute", "60 pieces", "15 children", "minimum number"]
                question_en = examprep2_data.get("question_en", "")
                
                question_valid = all(keyword in question_en for keyword in expected_question_keywords)
                
                if question_valid:
                    self.log_test("examprep2 Question Integrity", True, 
                                f"✅ Question contains all expected elements")
                else:
                    self.log_test("examprep2 Question Integrity", False, 
                                f"❌ Question missing expected elements. Got: {question_en}")
                    return False
                
                # Verify answer
                expected_answer = "p ≥ 4"
                actual_answer = examprep2_data.get("answer", "")
                
                if actual_answer == expected_answer:
                    self.log_test("examprep2 Answer Integrity", True, 
                                f"✅ Answer correct: {actual_answer}")
                else:
                    self.log_test("examprep2 Answer Integrity", False, 
                                f"❌ Answer incorrect. Expected: {expected_answer}, Got: {actual_answer}")
                    return False
                
                # Verify hints are present and follow Socratic method
                hints_en = examprep2_data.get("hints_en", [])
                
                if len(hints_en) == 3:
                    # Check that hints don't reveal direct inequality
                    hints_text = " ".join(hints_en)
                    if "15p ≥ 60" not in hints_text and "p ≥ 4" not in hints_text:
                        self.log_test("examprep2 Hints Integrity", True, 
                                    f"✅ Hints follow Socratic method without revealing answers")
                        return True
                    else:
                        self.log_test("examprep2 Hints Integrity", False, 
                                    f"❌ Hints reveal direct answers")
                        return False
                else:
                    self.log_test("examprep2 Hints Integrity", False, 
                                f"❌ Expected 3 hints, got {len(hints_en)}")
                    return False
            else:
                self.log_test("examprep2 Content Integrity", False, 
                            f"Failed to fetch examprep2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Database Content Integrity", False, f"Test execution error: {str(e)}")
            return False

    def complete_required_stages_for_examprep2(self):
        """Complete required stages to unlock examprep2 access"""
        try:
            # Complete practice2_1
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
                return False
            
            # Complete practice2_2
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
                return False
            
            return True
            
        except Exception as e:
            print(f"Error completing required stages: {str(e)}")
            return False

    def complete_required_stages_for_practice2_2(self, username):
        """Complete required stages to unlock practice2_2 access"""
        try:
            # Complete practice2_1
            practice2_1_attempt = {
                "problem_id": "practice2_1",
                "answer": "k < -12",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{username}/attempt",
                json=practice2_1_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200 or not response.json().get("correct"):
                return False
            
            return True
            
        except Exception as e:
            print(f"Error completing required stages for practice2_2: {str(e)}")
            return False

    def generate_step_enforcement_summary(self, results, critical_failures):
        """Generate comprehensive summary of Section 2 step enforcement testing"""
        print("\n" + "=" * 80)
        print("🎯 SECTION 2 WORD PROBLEM 3-STEP ENFORCEMENT FIX TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL SECTION 2 STEP ENFORCEMENT TEST RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL PEDAGOGICAL ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  EDUCATIONAL RISK: Students can skip essential learning steps!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix 3-step enforcement implementation")
        else:
            print(f"\n🎉 NO CRITICAL PEDAGOGICAL ISSUES DETECTED")
        
        print(f"\n📋 SECTION 2 STEP ENFORCEMENT STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL SECTION 2 STEP ENFORCEMENT TESTS PASSED")
            print("   ✅ practice2_2 (tickets) has exactly 3 steps")
            print("   ✅ examprep2 (candy) has exactly 3 steps")
            print("   ✅ Step 2 no longer accepts final answer (prevents skipping Step 3)")
            print("   ✅ All 3 steps required for problem completion")
            print("   ✅ Database content integrity maintained")
            print("   🛡️  PEDAGOGICAL INTEGRITY: PROTECTED")
        else:
            print("   ⚠️  SECTION 2 STEP ENFORCEMENT ISSUES DETECTED")
            print("   🔧 3-step enforcement implementation needs fixes")
            print("   🚨 STUDENT LEARNING: COMPROMISED")
        
        print("\n" + "=" * 80)

    def run_step_enforcement_tests(self):
        """Run comprehensive Section 2 word problem step enforcement tests"""
        print("=" * 80)
        print("🎯 SECTION 2 WORD PROBLEM 3-STEP ENFORCEMENT FIX TESTING")
        print("=" * 80)
        print("Testing critical pedagogical bug fix: word problems must require complete 3-step process")
        
        # Test categories for Section 2 step enforcement
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("Step Count Verification", self.test_step_count_verification, "critical"),
            ("Step Structure Validation", self.test_step_structure_validation, "critical"),
            ("Premature Completion Prevention", self.test_premature_completion_prevention, "critical"),
            ("Step Progression Logic", self.test_step_progression_logic, "critical"),
            ("Database Content Integrity", self.test_database_content_integrity, "high")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 SECTION 2 STEP ENFORCEMENT TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive Section 2 step enforcement summary
        self.generate_step_enforcement_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run Section 2 step enforcement tests"""
    print("🚀 Starting SECTION 2 WORD PROBLEM 3-STEP ENFORCEMENT FIX Testing...")
    print("🎯 Goal: Verify word problems require complete 3-step mathematical process")
    
    tester = Section2StepEnforcementTester(BACKEND_URL)
    results = tester.run_step_enforcement_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 SECTION 2 STEP ENFORCEMENT ALERT: {failed_tests} test(s) failed!")
        print("🔧 3-step enforcement implementation needs fixes to prevent students from skipping steps")
    else:
        print(f"\n🛡️  SECTION 2 STEP ENFORCEMENT CONFIRMED: All pedagogical tests passed!")
        print("✅ Word problems properly enforce complete 3-step mathematical learning process")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()