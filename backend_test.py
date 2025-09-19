#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - Section 2 Navigation Bug Testing
Tests the critical navigation bug from practice2_2 to assessment2 where students cannot 
access assessment2 after completing both practice stages.

CRITICAL REQUIREMENTS BEING TESTED:
- Stage Access Control Logic: assessment2 requires both practice2_1 and practice2_2 completion
- Practice Stage Completion Tracking: practice stages are properly marked as completed
- Progress Data Verification: student progress data structure is correct
- Assessment2 Access Bug: assessment2 becomes accessible after completing both practice stages
- Navigation Sequence: prep2 → explanation2 → practice2_1 → practice2_2 → assessment2 → examprep2
"""

import requests
import json
import sys
import os
import re
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://inequality-solver.preview.emergentagent.com/api"

class Section2NavigationTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "section2_nav_test_student"
        
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
        """Create test student for navigation testing"""
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

    def test_practice2_1_completion(self):
        """Test completing practice2_1 with correct answer"""
        try:
            print("\n🎯 PRACTICE2_1 COMPLETION TEST")
            print("Testing completion of practice2_1 with correct answer 'k < -12'")
            
            # Submit correct answer for practice2_1
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
            
            if response.status_code == 200:
                result = response.json()
                if result.get("correct"):
                    progress = result.get("progress", {})
                    if progress.get("completed", False):
                        self.log_test("practice2_1 Completion", True, 
                                    f"✅ practice2_1 completed successfully with answer 'k < -12'")
                        return True
                    else:
                        self.log_test("practice2_1 Completion", False, 
                                    f"❌ Answer correct but problem not marked as completed")
                        return False
                else:
                    self.log_test("practice2_1 Completion", False, 
                                f"❌ Correct answer 'k < -12' was rejected")
                    return False
            else:
                self.log_test("practice2_1 Completion", False, 
                            f"Failed to submit practice2_1: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("practice2_1 Completion", False, f"Test execution error: {str(e)}")
            return False

    def test_practice2_2_completion(self):
        """Test completing practice2_2 with correct 3-step process"""
        try:
            print("\n🎯 PRACTICE2_2 COMPLETION TEST")
            print("Testing completion of practice2_2 with correct answer 't ≥ 50'")
            
            # Submit correct answer for practice2_2
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
            
            if response.status_code == 200:
                result = response.json()
                if result.get("correct"):
                    progress = result.get("progress", {})
                    if progress.get("completed", False):
                        self.log_test("practice2_2 Completion", True, 
                                    f"✅ practice2_2 completed successfully with answer 't ≥ 50'")
                        return True
                    else:
                        self.log_test("practice2_2 Completion", False, 
                                    f"❌ Answer correct but problem not marked as completed")
                        return False
                else:
                    self.log_test("practice2_2 Completion", False, 
                                f"❌ Correct answer 't ≥ 50' was rejected")
                    return False
            else:
                self.log_test("practice2_2 Completion", False, 
                            f"Failed to submit practice2_2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("practice2_2 Completion", False, f"Test execution error: {str(e)}")
            return False

    def test_progress_data_verification(self):
        """Check student progress data structure to ensure practice stage completions are recorded"""
        try:
            print("\n📊 PROGRESS DATA VERIFICATION")
            print("Checking student progress data to verify practice stage completions are recorded")
            
            # Get student progress
            response = self.session.get(f"{self.base_url}/students/{self.test_student_username}/progress")
            
            if response.status_code == 200:
                progress_data = response.json()
                section2_progress = progress_data.get("progress", {}).get("section2", {})
                
                # Check practice2_1 completion
                practice2_1_status = section2_progress.get("practice2_1", {})
                practice2_1_completed = practice2_1_status.get("completed", False)
                
                # Check practice2_2 completion
                practice2_2_status = section2_progress.get("practice2_2", {})
                practice2_2_completed = practice2_2_status.get("completed", False)
                
                if practice2_1_completed and practice2_2_completed:
                    self.log_test("Progress Data Verification", True, 
                                f"✅ Both practice2_1 and practice2_2 marked as completed in progress data")
                    return True
                else:
                    self.log_test("Progress Data Verification", False, 
                                f"❌ Practice stages not properly recorded: practice2_1={practice2_1_completed}, practice2_2={practice2_2_completed}")
                    return False
            else:
                self.log_test("Progress Data Verification", False, 
                            f"Failed to get progress data: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Progress Data Verification", False, f"Test execution error: {str(e)}")
            return False

    def test_assessment2_access_control(self):
        """Test the critical assessment2 access bug - verify it becomes accessible after completing both practice stages"""
        try:
            print("\n🔐 ASSESSMENT2 ACCESS CONTROL TEST")
            print("Testing if assessment2 becomes accessible after completing both practice2_1 and practice2_2")
            
            # Try to access assessment2 problem
            response = self.session.get(f"{self.base_url}/problems/assessment2?username={self.test_student_username}")
            
            if response.status_code == 200:
                assessment2_data = response.json()
                if assessment2_data.get("id") == "assessment2":
                    self.log_test("Assessment2 Access Control", True, 
                                f"✅ assessment2 is accessible after completing both practice stages")
                    return True
                else:
                    self.log_test("Assessment2 Access Control", False, 
                                f"❌ assessment2 data structure incorrect")
                    return False
            elif response.status_code == 403:
                # This is the bug - assessment2 should be accessible but is being blocked
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                self.log_test("Assessment2 Access Control", False, 
                            f"❌ CRITICAL BUG: assessment2 blocked with 403 Forbidden after completing both practice stages", error_data)
                return False
            else:
                self.log_test("Assessment2 Access Control", False, 
                            f"Failed to access assessment2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Assessment2 Access Control", False, f"Test execution error: {str(e)}")
            return False

    def test_assessment2_submission(self):
        """Test submitting correct answer to assessment2 if accessible"""
        try:
            print("\n🎯 ASSESSMENT2 SUBMISSION TEST")
            print("Testing submission of correct answer to assessment2")
            
            # Submit correct answer for assessment2
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
            
            if response.status_code == 200:
                result = response.json()
                if result.get("correct"):
                    progress = result.get("progress", {})
                    if progress.get("completed", False):
                        self.log_test("Assessment2 Submission", True, 
                                    f"✅ assessment2 completed successfully with answer 'y < -12'")
                        return True
                    else:
                        self.log_test("Assessment2 Submission", False, 
                                    f"❌ Answer correct but problem not marked as completed")
                        return False
                else:
                    self.log_test("Assessment2 Submission", False, 
                                f"❌ Correct answer 'y < -12' was rejected")
                    return False
            elif response.status_code == 403:
                # This indicates the access control bug is still present
                error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                self.log_test("Assessment2 Submission", False, 
                            f"❌ CRITICAL BUG: assessment2 submission blocked with 403 Forbidden", error_data)
                return False
            else:
                self.log_test("Assessment2 Submission", False, 
                            f"Failed to submit assessment2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Assessment2 Submission", False, f"Test execution error: {str(e)}")
            return False

    def test_navigation_sequence_verification(self):
        """Verify the complete Section 2 navigation sequence works correctly"""
        try:
            print("\n🗺️ NAVIGATION SEQUENCE VERIFICATION")
            print("Testing complete Section 2 navigation: prep2 → explanation2 → practice2_1 → practice2_2 → assessment2 → examprep2")
            
            # Test access to each stage in sequence
            stages = [
                ("prep2", "Preparation stage"),
                ("explanation2", "Explanation stage"),
                ("practice2_1", "Practice stage 1"),
                ("practice2_2", "Practice stage 2"),
                ("assessment2", "Assessment stage"),
                ("examprep2", "Exam prep stage")
            ]
            
            accessible_stages = []
            blocked_stages = []
            
            for stage_id, stage_name in stages:
                try:
                    response = self.session.get(f"{self.base_url}/problems/{stage_id}?username={self.test_student_username}")
                    
                    if response.status_code == 200:
                        accessible_stages.append(f"{stage_name} ({stage_id})")
                    elif response.status_code == 403:
                        blocked_stages.append(f"{stage_name} ({stage_id})")
                    else:
                        blocked_stages.append(f"{stage_name} ({stage_id}) - HTTP {response.status_code}")
                        
                except Exception as e:
                    blocked_stages.append(f"{stage_name} ({stage_id}) - Error: {str(e)}")
            
            # After completing practice2_1 and practice2_2, assessment2 should be accessible
            if "Assessment stage (assessment2)" in accessible_stages:
                self.log_test("Navigation Sequence Verification", True, 
                            f"✅ Navigation sequence working correctly. Accessible: {', '.join(accessible_stages)}")
                return True
            else:
                self.log_test("Navigation Sequence Verification", False, 
                            f"❌ CRITICAL BUG: assessment2 not accessible after completing practice stages. Blocked: {', '.join(blocked_stages)}")
                return False
                
        except Exception as e:
            self.log_test("Navigation Sequence Verification", False, f"Test execution error: {str(e)}")
            return False

    def test_stage_access_control_logic(self):
        """Test the backend stage access control logic specifically for Section 2"""
        try:
            print("\n🔒 STAGE ACCESS CONTROL LOGIC TEST")
            print("Testing backend stage access control logic for Section 2")
            
            # Create a fresh test student to test access control from scratch
            fresh_student = "fresh_access_test_student"
            test_student = {"username": fresh_student, "class_name": "GR9-A"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Fresh Student Creation", False, "Failed to create fresh test student")
                return False
            
            # Test 1: assessment2 should be blocked initially (no practice stages completed)
            response = self.session.get(f"{self.base_url}/problems/assessment2?username={fresh_student}")
            
            if response.status_code == 403:
                self.log_test("Initial Assessment2 Block", True, 
                            f"✅ assessment2 correctly blocked initially (no practice stages completed)")
            else:
                self.log_test("Initial Assessment2 Block", False, 
                            f"❌ assessment2 should be blocked initially but got HTTP {response.status_code}")
                return False
            
            # Test 2: Complete only practice2_1, assessment2 should still be blocked
            practice2_1_attempt = {
                "problem_id": "practice2_1",
                "answer": "k < -12",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{fresh_student}/attempt",
                json=practice2_1_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200 and response.json().get("correct"):
                # Now test assessment2 access (should still be blocked)
                response = self.session.get(f"{self.base_url}/problems/assessment2?username={fresh_student}")
                
                if response.status_code == 403:
                    self.log_test("Assessment2 Block After practice2_1 Only", True, 
                                f"✅ assessment2 correctly blocked after completing only practice2_1")
                else:
                    self.log_test("Assessment2 Block After practice2_1 Only", False, 
                                f"❌ assessment2 should be blocked after only practice2_1 but got HTTP {response.status_code}")
                    return False
            else:
                self.log_test("practice2_1 Completion for Fresh Student", False, 
                            f"Failed to complete practice2_1 for fresh student")
                return False
            
            # Test 3: Complete practice2_2, assessment2 should now be accessible
            practice2_2_attempt = {
                "problem_id": "practice2_2",
                "answer": "t ≥ 50",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{fresh_student}/attempt",
                json=practice2_2_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200 and response.json().get("correct"):
                # Now test assessment2 access (should be accessible)
                response = self.session.get(f"{self.base_url}/problems/assessment2?username={fresh_student}")
                
                if response.status_code == 200:
                    self.log_test("Assessment2 Access After Both Practice Stages", True, 
                                f"✅ assessment2 correctly accessible after completing both practice2_1 and practice2_2")
                    return True
                else:
                    self.log_test("Assessment2 Access After Both Practice Stages", False, 
                                f"❌ CRITICAL BUG: assessment2 should be accessible after both practice stages but got HTTP {response.status_code}")
                    return False
            else:
                self.log_test("practice2_2 Completion for Fresh Student", False, 
                            f"Failed to complete practice2_2 for fresh student")
                return False
                
        except Exception as e:
            self.log_test("Stage Access Control Logic", False, f"Test execution error: {str(e)}")
            return False

    def test_real_user_scenario_analysis(self):
        """Test the specific scenario that caused the user's bug report"""
        try:
            print("\n🔍 REAL USER SCENARIO ANALYSIS")
            print("Testing the specific scenario that matches the user's bug report")
            
            # Create a test student that mimics the real user "Sami" scenario
            sami_test_student = "sami_scenario_test_student"
            test_student = {"username": sami_test_student, "class_name": "GR9-A"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                self.log_test("Sami Scenario Student Creation", False, "Failed to create Sami scenario test student")
                return False
            
            # Scenario: Complete ONLY practice2_2 (skip practice2_1) - this matches real user "Sami"
            practice2_2_attempt = {
                "problem_id": "practice2_2",
                "answer": "t ≥ 50",
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{sami_test_student}/attempt",
                json=practice2_2_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200 and response.json().get("correct"):
                self.log_test("practice2_2 Only Completion", True, 
                            f"✅ practice2_2 completed successfully (practice2_1 skipped)")
                
                # Now test assessment2 access (should be blocked because practice2_1 is not completed)
                response = self.session.get(f"{self.base_url}/problems/assessment2?username={sami_test_student}")
                
                if response.status_code == 403:
                    error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
                    self.log_test("Assessment2 Block - Sami Scenario", True, 
                                f"✅ assessment2 correctly blocked when only practice2_2 completed (practice2_1 missing). Error: {error_data}")
                    
                    # Verify the progress data shows the incomplete state
                    response = self.session.get(f"{self.base_url}/students/{sami_test_student}/progress")
                    if response.status_code == 200:
                        progress_data = response.json()
                        section2_progress = progress_data.get("progress", {}).get("section2", {})
                        
                        practice2_1_completed = section2_progress.get("practice2_1", {}).get("completed", False)
                        practice2_2_completed = section2_progress.get("practice2_2", {}).get("completed", False)
                        
                        if not practice2_1_completed and practice2_2_completed:
                            self.log_test("Sami Scenario Progress Verification", True, 
                                        f"✅ Progress correctly shows practice2_1=False, practice2_2=True - explains why assessment2 is blocked")
                            return True
                        else:
                            self.log_test("Sami Scenario Progress Verification", False, 
                                        f"❌ Unexpected progress state: practice2_1={practice2_1_completed}, practice2_2={practice2_2_completed}")
                            return False
                    else:
                        self.log_test("Sami Scenario Progress Check", False, 
                                    f"Failed to get progress data: HTTP {response.status_code}")
                        return False
                else:
                    self.log_test("Assessment2 Block - Sami Scenario", False, 
                                f"❌ UNEXPECTED: assessment2 should be blocked when practice2_1 is not completed but got HTTP {response.status_code}")
                    return False
            else:
                self.log_test("practice2_2 Only Completion", False, 
                            f"Failed to complete practice2_2 for Sami scenario test")
                return False
                
        except Exception as e:
            self.log_test("Real User Scenario Analysis", False, f"Test execution error: {str(e)}")
            return False

    def generate_navigation_summary(self, results, critical_failures):
        """Generate comprehensive summary of Section 2 navigation testing"""
        print("\n" + "=" * 80)
        print("🎯 SECTION 2 NAVIGATION BUG TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL SECTION 2 NAVIGATION TEST RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL NAVIGATION ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  NAVIGATION RISK: Students cannot progress from practice2_2 to assessment2!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix stage access control logic")
        else:
            print(f"\n🎉 NO CRITICAL NAVIGATION ISSUES DETECTED")
        
        print(f"\n📋 SECTION 2 NAVIGATION STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL SECTION 2 NAVIGATION TESTS PASSED")
            print("   ✅ practice2_1 completion tracking working")
            print("   ✅ practice2_2 completion tracking working")
            print("   ✅ Progress data structure correct")
            print("   ✅ assessment2 accessible after completing both practice stages")
            print("   ✅ Navigation sequence working correctly")
            print("   🛡️  NAVIGATION INTEGRITY: PROTECTED")
        else:
            print("   ⚠️  SECTION 2 NAVIGATION ISSUES DETECTED")
            print("   🔧 Stage access control logic needs fixes")
            print("   🚨 STUDENT PROGRESSION: BLOCKED")
        
        print("\n" + "=" * 80)

    def run_navigation_tests(self):
        """Run comprehensive Section 2 navigation bug tests"""
        print("=" * 80)
        print("🎯 SECTION 2 NAVIGATION BUG TESTING")
        print("=" * 80)
        print("Testing critical navigation bug: practice2_2 → assessment2 progression blocked")
        
        # Test categories for Section 2 navigation
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("Practice2_1 Completion", self.test_practice2_1_completion, "critical"),
            ("Practice2_2 Completion", self.test_practice2_2_completion, "critical"),
            ("Progress Data Verification", self.test_progress_data_verification, "critical"),
            ("Assessment2 Access Control", self.test_assessment2_access_control, "critical"),
            ("Assessment2 Submission", self.test_assessment2_submission, "high"),
            ("Navigation Sequence Verification", self.test_navigation_sequence_verification, "critical"),
            ("Stage Access Control Logic", self.test_stage_access_control_logic, "critical"),
            ("Real User Scenario Analysis", self.test_real_user_scenario_analysis, "critical")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 SECTION 2 NAVIGATION TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive Section 2 navigation summary
        self.generate_navigation_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run Section 2 navigation tests"""
    print("🚀 Starting SECTION 2 NAVIGATION BUG Testing...")
    print("🎯 Goal: Verify assessment2 becomes accessible after completing both practice stages")
    
    tester = Section2NavigationTester(BACKEND_URL)
    results = tester.run_navigation_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 SECTION 2 NAVIGATION ALERT: {failed_tests} test(s) failed!")
        print("🔧 Stage access control logic needs fixes to allow progression from practice2_2 to assessment2")
    else:
        print(f"\n🛡️  SECTION 2 NAVIGATION CONFIRMED: All navigation tests passed!")
        print("✅ Students can properly progress from practice2_2 to assessment2")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()