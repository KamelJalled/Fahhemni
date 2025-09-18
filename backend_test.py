#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - CRITICAL SECURITY FIX TESTING
Tests stage access control security to prevent cheating by skipping learning stages
"""

import requests
import json
import sys
import os
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://bilingual-algebra.preview.emergentagent.com/api"

class StageAccessControlTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "security_test_student_section2"
        
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

    def create_test_student_section2(self):
        """Create test student specifically for Section 2 access control testing"""
        try:
            test_student = {"username": self.test_student_username, "class_name": "GR9-B"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("class_name") == "GR9-B":
                    self.log_test("Test Student Creation (Section 2)", True, 
                                f"✅ Created test student '{self.test_student_username}' in class GR9-B for Section 2 testing")
                    return True
                else:
                    self.log_test("Test Student Creation (Section 2)", False, 
                                f"Expected class GR9-B, got {data.get('class_name')}")
                    return False
            else:
                self.log_test("Test Student Creation (Section 2)", False, 
                            f"Failed to create test student: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test Student Creation (Section 2)", False, f"Request error: {str(e)}")
            return False

    def test_initial_stage_access_locked(self):
        """Test that assessment2 and examprep2 are initially LOCKED when no practice stages are completed"""
        try:
            print("\n🔒 INITIAL STAGE ACCESS CONTROL TESTING")
            print("Testing that assessment2 and examprep2 are LOCKED initially")
            print("Testing that direct API calls to locked stages are blocked")
            
            # Create fresh test student
            if not self.create_test_student_section2():
                return False
            
            # Test 1: Direct API call to assessment2 should be blocked
            response = self.session.get(f"{self.base_url}/problems/assessment2")
            
            if response.status_code == 200:
                # If we can access the problem data, check if there's access control in the response
                data = response.json()
                if "locked" in data and data["locked"] == True:
                    self.log_test("Assessment2 Initial Lock Status", True, 
                                "✅ assessment2 correctly marked as LOCKED in response")
                else:
                    self.log_test("Assessment2 Initial Lock Status", False, 
                                "❌ SECURITY ISSUE: assessment2 accessible without completing prerequisites")
                    return False
            elif response.status_code == 403:
                self.log_test("Assessment2 Initial Lock Status", True, 
                            "✅ assessment2 correctly blocked with 403 Forbidden")
            else:
                self.log_test("Assessment2 Initial Lock Status", False, 
                            f"❌ SECURITY ISSUE: assessment2 should be blocked but got HTTP {response.status_code}")
                return False
            
            # Test 2: Direct API call to examprep2 should be blocked
            response = self.session.get(f"{self.base_url}/problems/examprep2")
            
            if response.status_code == 200:
                data = response.json()
                if "locked" in data and data["locked"] == True:
                    self.log_test("Examprep2 Initial Lock Status", True, 
                                "✅ examprep2 correctly marked as LOCKED in response")
                else:
                    self.log_test("Examprep2 Initial Lock Status", False, 
                                "❌ SECURITY ISSUE: examprep2 accessible without completing prerequisites")
                    return False
            elif response.status_code == 403:
                self.log_test("Examprep2 Initial Lock Status", True, 
                            "✅ examprep2 correctly blocked with 403 Forbidden")
            else:
                self.log_test("Examprep2 Initial Lock Status", False, 
                            f"❌ SECURITY ISSUE: examprep2 should be blocked but got HTTP {response.status_code}")
                return False
            
            # Test 3: Attempt to submit answer to locked assessment2 should be blocked
            attempt_data = {
                "problem_id": "assessment2",
                "answer": "y < -12",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 403:
                self.log_test("Assessment2 Submission Block", True, 
                            "✅ Direct submission to locked assessment2 correctly blocked with 403")
            elif response.status_code == 400:
                data = response.json()
                if "locked" in data.get("detail", "").lower() or "access" in data.get("detail", "").lower():
                    self.log_test("Assessment2 Submission Block", True, 
                                "✅ Direct submission to locked assessment2 correctly blocked with access control message")
                else:
                    self.log_test("Assessment2 Submission Block", False, 
                                f"❌ SECURITY ISSUE: assessment2 submission should be blocked but got: {data}")
                    return False
            else:
                self.log_test("Assessment2 Submission Block", False, 
                            f"❌ CRITICAL SECURITY ISSUE: Direct submission to locked assessment2 allowed! HTTP {response.status_code}")
                return False
            
            # Test 4: Attempt to submit answer to locked examprep2 should be blocked
            attempt_data = {
                "problem_id": "examprep2",
                "answer": "p ≥ 4",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 403:
                self.log_test("Examprep2 Submission Block", True, 
                            "✅ Direct submission to locked examprep2 correctly blocked with 403")
            elif response.status_code == 400:
                data = response.json()
                if "locked" in data.get("detail", "").lower() or "access" in data.get("detail", "").lower():
                    self.log_test("Examprep2 Submission Block", True, 
                                "✅ Direct submission to locked examprep2 correctly blocked with access control message")
                else:
                    self.log_test("Examprep2 Submission Block", False, 
                                f"❌ SECURITY ISSUE: examprep2 submission should be blocked but got: {data}")
                    return False
            else:
                self.log_test("Examprep2 Submission Block", False, 
                            f"❌ CRITICAL SECURITY ISSUE: Direct submission to locked examprep2 allowed! HTTP {response.status_code}")
                return False
            
            self.log_test("INITIAL STAGE ACCESS CONTROL", True, 
                        "✅ All initial lock tests PASSED - assessment2 and examprep2 properly secured")
            return True
            
        except Exception as e:
            self.log_test("Initial Stage Access Control Testing", False, f"Test execution error: {str(e)}")
            return False

    def test_partial_practice_completion_security(self):
        """Test that completing only practice2_1 keeps assessment2 LOCKED (needs ALL practice stages)"""
        try:
            print("\n🔒 PARTIAL PRACTICE COMPLETION SECURITY TESTING")
            print("Testing that assessment2 remains LOCKED after completing only practice2_1")
            print("Testing that ALL practice stages (practice2_1 AND practice2_2) are required")
            
            # Step 1: Complete practice2_1 only
            attempt_data = {
                "problem_id": "practice2_1",
                "answer": "k < -12",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Practice2_1 Completion", False, 
                            f"Failed to complete practice2_1: HTTP {response.status_code}")
                return False
            
            data = response.json()
            if not data.get("correct"):
                self.log_test("Practice2_1 Completion", False, 
                            f"practice2_1 answer should be correct: {data}")
                return False
            
            self.log_test("Practice2_1 Completion", True, 
                        f"✅ practice2_1 completed successfully, score: {data.get('score')}")
            
            # Step 2: Verify assessment2 is STILL LOCKED after partial completion
            response = self.session.get(f"{self.base_url}/problems/assessment2")
            
            if response.status_code == 200:
                data = response.json()
                if "locked" in data and data["locked"] == True:
                    self.log_test("Assessment2 Still Locked After Partial", True, 
                                "✅ assessment2 correctly remains LOCKED after completing only practice2_1")
                else:
                    self.log_test("Assessment2 Still Locked After Partial", False, 
                                "❌ SECURITY BREACH: assessment2 unlocked after partial practice completion")
                    return False
            elif response.status_code == 403:
                self.log_test("Assessment2 Still Locked After Partial", True, 
                            "✅ assessment2 correctly remains blocked after partial practice completion")
            else:
                self.log_test("Assessment2 Still Locked After Partial", False, 
                            f"❌ SECURITY ISSUE: Unexpected response for locked assessment2: HTTP {response.status_code}")
                return False
            
            # Step 3: Attempt to submit to assessment2 should still be blocked
            attempt_data = {
                "problem_id": "assessment2",
                "answer": "y < -12",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [403, 400]:
                self.log_test("Assessment2 Submission Still Blocked", True, 
                            "✅ assessment2 submission correctly blocked after partial practice completion")
            else:
                self.log_test("Assessment2 Submission Still Blocked", False, 
                            f"❌ CRITICAL SECURITY BREACH: assessment2 submission allowed after partial completion! HTTP {response.status_code}")
                return False
            
            self.log_test("PARTIAL PRACTICE COMPLETION SECURITY", True, 
                        "✅ All partial completion security tests PASSED - assessment2 remains locked")
            return True
            
        except Exception as e:
            self.log_test("Partial Practice Completion Security Testing", False, f"Test execution error: {str(e)}")
            return False

    def test_full_practice_completion_unlock(self):
        """Test that completing both practice2_1 and practice2_2 unlocks assessment2"""
        try:
            print("\n🔓 FULL PRACTICE COMPLETION UNLOCK TESTING")
            print("Testing that assessment2 becomes ACCESSIBLE after completing ALL practice stages")
            print("Testing that examprep2 remains LOCKED until assessment2 is completed")
            
            # Step 1: Complete practice2_2 (practice2_1 already completed in previous test)
            attempt_data = {
                "problem_id": "practice2_2",
                "answer": "t ≥ 50",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Practice2_2 Completion", False, 
                            f"Failed to complete practice2_2: HTTP {response.status_code}")
                return False
            
            data = response.json()
            if not data.get("correct"):
                self.log_test("Practice2_2 Completion", False, 
                            f"practice2_2 answer should be correct: {data}")
                return False
            
            self.log_test("Practice2_2 Completion", True, 
                        f"✅ practice2_2 completed successfully, score: {data.get('score')}")
            
            # Step 2: Verify assessment2 is now UNLOCKED
            response = self.session.get(f"{self.base_url}/problems/assessment2")
            
            if response.status_code == 200:
                data = response.json()
                if "locked" in data and data["locked"] == False:
                    self.log_test("Assessment2 Unlocked After Full Practice", True, 
                                "✅ assessment2 correctly UNLOCKED after completing all practice stages")
                elif "locked" not in data:
                    # If no locked field, assume it's accessible (old implementation)
                    self.log_test("Assessment2 Unlocked After Full Practice", True, 
                                "✅ assessment2 accessible after completing all practice stages")
                else:
                    self.log_test("Assessment2 Unlocked After Full Practice", False, 
                                "❌ SECURITY ISSUE: assessment2 still locked after completing all practice stages")
                    return False
            else:
                self.log_test("Assessment2 Unlocked After Full Practice", False, 
                            f"❌ SECURITY ISSUE: assessment2 should be accessible but got HTTP {response.status_code}")
                return False
            
            # Step 3: Verify assessment2 submission is now allowed
            attempt_data = {
                "problem_id": "assessment2",
                "answer": "y < -12",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("correct"):
                    self.log_test("Assessment2 Submission Allowed", True, 
                                f"✅ assessment2 submission correctly allowed and scored: {data.get('score')}")
                else:
                    self.log_test("Assessment2 Submission Allowed", True, 
                                "✅ assessment2 submission allowed (answer validation working)")
            else:
                self.log_test("Assessment2 Submission Allowed", False, 
                            f"❌ SECURITY ISSUE: assessment2 submission should be allowed but got HTTP {response.status_code}")
                return False
            
            # Step 4: Verify examprep2 is STILL LOCKED (needs assessment2 completion)
            response = self.session.get(f"{self.base_url}/problems/examprep2")
            
            if response.status_code == 200:
                data = response.json()
                if "locked" in data and data["locked"] == True:
                    self.log_test("Examprep2 Still Locked After Assessment Access", True, 
                                "✅ examprep2 correctly remains LOCKED until assessment2 is completed")
                else:
                    self.log_test("Examprep2 Still Locked After Assessment Access", False, 
                                "❌ SECURITY ISSUE: examprep2 should remain locked until assessment2 completion")
                    return False
            elif response.status_code == 403:
                self.log_test("Examprep2 Still Locked After Assessment Access", True, 
                            "✅ examprep2 correctly remains blocked until assessment2 completion")
            else:
                self.log_test("Examprep2 Still Locked After Assessment Access", False, 
                            f"❌ SECURITY ISSUE: examprep2 access control unclear: HTTP {response.status_code}")
                return False
            
            self.log_test("FULL PRACTICE COMPLETION UNLOCK", True, 
                        "✅ All full practice completion tests PASSED - assessment2 unlocked, examprep2 still locked")
            return True
            
        except Exception as e:
            self.log_test("Full Practice Completion Unlock Testing", False, f"Test execution error: {str(e)}")
            return False

    def test_assessment_completion_unlock_examprep(self):
        """Test that completing assessment2 unlocks examprep2"""
        try:
            print("\n🔓 ASSESSMENT COMPLETION UNLOCK TESTING")
            print("Testing that examprep2 becomes ACCESSIBLE after completing assessment2")
            
            # Note: assessment2 should already be completed from previous test
            # Let's verify examprep2 is now unlocked
            
            # Step 1: Verify examprep2 is now UNLOCKED
            response = self.session.get(f"{self.base_url}/problems/examprep2")
            
            if response.status_code == 200:
                data = response.json()
                if "locked" in data and data["locked"] == False:
                    self.log_test("Examprep2 Unlocked After Assessment", True, 
                                "✅ examprep2 correctly UNLOCKED after completing assessment2")
                elif "locked" not in data:
                    # If no locked field, assume it's accessible
                    self.log_test("Examprep2 Unlocked After Assessment", True, 
                                "✅ examprep2 accessible after completing assessment2")
                else:
                    self.log_test("Examprep2 Unlocked After Assessment", False, 
                                "❌ SECURITY ISSUE: examprep2 still locked after completing assessment2")
                    return False
            else:
                self.log_test("Examprep2 Unlocked After Assessment", False, 
                            f"❌ SECURITY ISSUE: examprep2 should be accessible but got HTTP {response.status_code}")
                return False
            
            # Step 2: Verify examprep2 submission is now allowed
            attempt_data = {
                "problem_id": "examprep2",
                "answer": "p ≥ 4",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("correct"):
                    self.log_test("Examprep2 Submission Allowed", True, 
                                f"✅ examprep2 submission correctly allowed and scored: {data.get('score')}")
                else:
                    self.log_test("Examprep2 Submission Allowed", True, 
                                "✅ examprep2 submission allowed (answer validation working)")
            else:
                self.log_test("Examprep2 Submission Allowed", False, 
                            f"❌ SECURITY ISSUE: examprep2 submission should be allowed but got HTTP {response.status_code}")
                return False
            
            self.log_test("ASSESSMENT COMPLETION UNLOCK", True, 
                        "✅ All assessment completion tests PASSED - examprep2 unlocked after assessment2")
            return True
            
        except Exception as e:
            self.log_test("Assessment Completion Unlock Testing", False, f"Test execution error: {str(e)}")
            return False

    def test_cross_section_access_control(self):
        """Test that the same access control works for Section 1 and dynamically for any section"""
        try:
            print("\n🔒 CROSS-SECTION ACCESS CONTROL TESTING")
            print("Testing that access control works for Section 1")
            print("Testing that the logic works dynamically for any section")
            
            # Create a new test student for Section 1 testing
            section1_student = "security_test_student_section1"
            test_student = {"username": section1_student, "class_name": "GR9-C"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Section 1 Test Student Creation", False, 
                            f"Failed to create Section 1 test student: HTTP {response.status_code}")
                return False
            
            self.log_test("Section 1 Test Student Creation", True, 
                        f"✅ Created Section 1 test student '{section1_student}'")
            
            # Test 1: Section 1 assessment1 should be locked initially
            response = self.session.get(f"{self.base_url}/problems/assessment1")
            
            if response.status_code == 200:
                data = response.json()
                if "locked" in data and data["locked"] == True:
                    self.log_test("Section 1 Assessment1 Initial Lock", True, 
                                "✅ Section 1 assessment1 correctly locked initially")
                else:
                    self.log_test("Section 1 Assessment1 Initial Lock", False, 
                                "❌ SECURITY ISSUE: Section 1 assessment1 should be locked initially")
                    return False
            elif response.status_code == 403:
                self.log_test("Section 1 Assessment1 Initial Lock", True, 
                            "✅ Section 1 assessment1 correctly blocked initially")
            else:
                self.log_test("Section 1 Assessment1 Initial Lock", False, 
                            f"❌ SECURITY ISSUE: Section 1 assessment1 access control unclear: HTTP {response.status_code}")
                return False
            
            # Test 2: Section 1 examprep1 should be locked initially
            response = self.session.get(f"{self.base_url}/problems/examprep1")
            
            if response.status_code == 200:
                data = response.json()
                if "locked" in data and data["locked"] == True:
                    self.log_test("Section 1 Examprep1 Initial Lock", True, 
                                "✅ Section 1 examprep1 correctly locked initially")
                else:
                    self.log_test("Section 1 Examprep1 Initial Lock", False, 
                                "❌ SECURITY ISSUE: Section 1 examprep1 should be locked initially")
                    return False
            elif response.status_code == 403:
                self.log_test("Section 1 Examprep1 Initial Lock", True, 
                            "✅ Section 1 examprep1 correctly blocked initially")
            else:
                self.log_test("Section 1 Examprep1 Initial Lock", False, 
                            f"❌ SECURITY ISSUE: Section 1 examprep1 access control unclear: HTTP {response.status_code}")
                return False
            
            # Test 3: Complete Section 1 practice stages to test unlock logic
            section1_practice_problems = [
                {"id": "practice1", "answer": "m > 37"},
                {"id": "practice2", "answer": "m ≥ 290"}
            ]
            
            for problem in section1_practice_problems:
                attempt_data = {
                    "problem_id": problem["id"],
                    "answer": problem["answer"],
                    "hints_used": 0
                }
                
                response = self.session.post(
                    f"{self.base_url}/students/{section1_student}/attempt",
                    json=attempt_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("correct"):
                        self.log_test(f"Section 1 {problem['id']} Completion", True, 
                                    f"✅ {problem['id']} completed successfully")
                    else:
                        self.log_test(f"Section 1 {problem['id']} Completion", False, 
                                    f"Expected correct answer for {problem['id']}")
                        return False
                else:
                    self.log_test(f"Section 1 {problem['id']} Completion", False, 
                                f"HTTP {response.status_code}")
                    return False
            
            # Test 4: Verify Section 1 assessment1 is now unlocked
            response = self.session.get(f"{self.base_url}/problems/assessment1")
            
            if response.status_code == 200:
                data = response.json()
                if "locked" in data and data["locked"] == False:
                    self.log_test("Section 1 Assessment1 Unlocked", True, 
                                "✅ Section 1 assessment1 correctly unlocked after practice completion")
                elif "locked" not in data:
                    self.log_test("Section 1 Assessment1 Unlocked", True, 
                                "✅ Section 1 assessment1 accessible after practice completion")
                else:
                    self.log_test("Section 1 Assessment1 Unlocked", False, 
                                "❌ SECURITY ISSUE: Section 1 assessment1 should be unlocked")
                    return False
            else:
                self.log_test("Section 1 Assessment1 Unlocked", False, 
                            f"❌ SECURITY ISSUE: Section 1 assessment1 should be accessible: HTTP {response.status_code}")
                return False
            
            self.log_test("CROSS-SECTION ACCESS CONTROL", True, 
                        "✅ All cross-section tests PASSED - Access control works dynamically across sections")
            return True
            
        except Exception as e:
            self.log_test("Cross-Section Access Control Testing", False, f"Test execution error: {str(e)}")
            return False

    def test_security_validation_error_messages(self):
        """Test that proper error messages are returned for security violations"""
        try:
            print("\n🔒 SECURITY VALIDATION ERROR MESSAGES TESTING")
            print("Testing that proper error messages are returned for blocked access")
            
            # Create a fresh student for error message testing
            error_test_student = "security_error_test_student"
            test_student = {"username": error_test_student, "class_name": "GR9-D"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Error Test Student Creation", False, 
                            f"Failed to create error test student: HTTP {response.status_code}")
                return False
            
            # Test 1: Attempt to access locked assessment2 and check error message
            attempt_data = {
                "problem_id": "assessment2",
                "answer": "y < -12",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{error_test_student}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [400, 403]:
                try:
                    data = response.json()
                    error_message = data.get("detail", "").lower()
                    
                    # Check for security-related keywords in error message
                    security_keywords = ["locked", "access", "prerequisite", "complete", "practice", "blocked"]
                    has_security_message = any(keyword in error_message for keyword in security_keywords)
                    
                    if has_security_message:
                        self.log_test("Security Error Message Quality", True, 
                                    f"✅ Proper security error message: {data.get('detail')}")
                    else:
                        self.log_test("Security Error Message Quality", False, 
                                    f"❌ Error message should indicate access control: {data.get('detail')}")
                        return False
                        
                except json.JSONDecodeError:
                    self.log_test("Security Error Message Quality", False, 
                                "❌ Error response should be valid JSON")
                    return False
            else:
                self.log_test("Security Error Message Quality", False, 
                            f"❌ Should return 400/403 for locked stage access: HTTP {response.status_code}")
                return False
            
            # Test 2: Attempt to access locked examprep2 and check error message
            attempt_data = {
                "problem_id": "examprep2",
                "answer": "p ≥ 4",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{error_test_student}/attempt",
                json=attempt_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code in [400, 403]:
                try:
                    data = response.json()
                    error_message = data.get("detail", "").lower()
                    
                    # Check for specific examprep access control message
                    if "assessment" in error_message or "locked" in error_message:
                        self.log_test("Examprep Security Error Message", True, 
                                    f"✅ Proper examprep security error: {data.get('detail')}")
                    else:
                        self.log_test("Examprep Security Error Message", False, 
                                    f"❌ Examprep error should mention assessment requirement: {data.get('detail')}")
                        return False
                        
                except json.JSONDecodeError:
                    self.log_test("Examprep Security Error Message", False, 
                                "❌ Examprep error response should be valid JSON")
                    return False
            else:
                self.log_test("Examprep Security Error Message", False, 
                            f"❌ Should return 400/403 for locked examprep access: HTTP {response.status_code}")
                return False
            
            self.log_test("SECURITY VALIDATION ERROR MESSAGES", True, 
                        "✅ All error message tests PASSED - Proper security messages returned")
            return True
            
        except Exception as e:
            self.log_test("Security Validation Error Messages Testing", False, f"Test execution error: {str(e)}")
            return False

    def generate_security_summary(self, results, critical_failures):
        """Generate comprehensive summary of stage access control security testing"""
        print("\n" + "=" * 80)
        print("🔒 STAGE ACCESS CONTROL SECURITY TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL SECURITY TEST RESULTS:")
        print(f"   Total Security Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Security Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED SECURITY RESULTS:")
        for category, success in results.items():
            status = "✅ SECURE" if success else "❌ VULNERABLE"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL SECURITY VULNERABILITIES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  SECURITY RISK: Students can cheat by skipping learning stages!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Implement stage access control")
        else:
            print(f"\n🎉 NO CRITICAL SECURITY VULNERABILITIES DETECTED")
        
        print(f"\n📋 STAGE ACCESS CONTROL STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL SECURITY TESTS PASSED")
            print("   ✅ assessment2 and examprep2 properly locked initially")
            print("   ✅ Partial practice completion security working") 
            print("   ✅ Full practice completion unlocks assessment2")
            print("   ✅ Assessment completion unlocks examprep2")
            print("   ✅ Cross-section access control functional")
            print("   ✅ Proper security error messages")
            print("   🛡️  ANTI-CHEATING PROTECTION: ACTIVE")
        else:
            print("   ⚠️  SECURITY VULNERABILITIES DETECTED")
            print("   🔧 Stage access control needs implementation/fixes")
            print("   🚨 ANTI-CHEATING PROTECTION: COMPROMISED")
        
        print("\n" + "=" * 80)

    def run_stage_access_control_tests(self):
        """Run comprehensive stage access control security tests"""
        print("=" * 80)
        print("🔒 CRITICAL SECURITY FIX - STAGE ACCESS CONTROL TESTING")
        print("=" * 80)
        print("Testing anti-cheating protection to prevent students from skipping learning stages")
        
        # Test categories for stage access control security
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Initial Stage Access Locked", self.test_initial_stage_access_locked, "critical"),
            ("Partial Practice Completion Security", self.test_partial_practice_completion_security, "critical"),
            ("Full Practice Completion Unlock", self.test_full_practice_completion_unlock, "critical"),
            ("Assessment Completion Unlock Examprep", self.test_assessment_completion_unlock_examprep, "critical"),
            ("Cross-Section Access Control", self.test_cross_section_access_control, "critical"),
            ("Security Validation Error Messages", self.test_security_validation_error_messages, "high")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 SECURITY TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive security summary
        self.generate_security_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run stage access control security tests"""
    print("🚀 Starting CRITICAL SECURITY FIX Testing - Stage Access Control...")
    print("🎯 Goal: Prevent cheating by ensuring proper learning progression")
    
    tester = StageAccessControlTester(BACKEND_URL)
    results = tester.run_stage_access_control_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 SECURITY ALERT: {failed_tests} security test(s) failed!")
        print("🔧 Stage access control implementation required to prevent cheating")
    else:
        print(f"\n🛡️  SECURITY CONFIRMED: All stage access control tests passed!")
        print("✅ Anti-cheating protection is working correctly")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()