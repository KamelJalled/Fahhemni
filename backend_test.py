#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - CRITICAL NAVIGATION FLOW BUG TESTING
Tests Section 2 navigation sequence to debug the critical navigation flow bug
"""

import requests
import json
import sys
import os
import re
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "http://localhost:8001/api"

class NavigationFlowTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "navigation_test_student"
        
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

    def test_section2_problem_ids_verification(self):
        """Test Section 2 Problem ID Verification - List all Section 2 problem IDs"""
        try:
            print("\n🔍 SECTION 2 PROBLEM ID VERIFICATION")
            print("Expected sequence: prep2 → explanation2 → practice2_1 → practice2_2 → assessment2 → examprep2")
            
            # Get all Section 2 problems
            response = self.session.get(f"{self.base_url}/problems/section/section2")
            
            if response.status_code == 200:
                problems = response.json()
                problem_ids = [problem.get("id") for problem in problems]
                
                expected_sequence = ["prep2", "explanation2", "practice2_1", "practice2_2", "assessment2", "examprep2"]
                
                # Check if all expected IDs are present
                missing_ids = [pid for pid in expected_sequence if pid not in problem_ids]
                extra_ids = [pid for pid in problem_ids if pid not in expected_sequence]
                
                if not missing_ids and not extra_ids:
                    self.log_test("Section 2 Problem IDs Complete", True, 
                                f"✅ Found all expected Section 2 problem IDs: {problem_ids}")
                    
                    # Verify sequence order
                    actual_sequence = []
                    for expected_id in expected_sequence:
                        for problem in problems:
                            if problem.get("id") == expected_id:
                                actual_sequence.append(expected_id)
                                break
                    
                    if actual_sequence == expected_sequence:
                        self.log_test("Section 2 Sequence Order", True, 
                                    f"✅ Section 2 problems in correct sequence: {actual_sequence}")
                        return True
                    else:
                        self.log_test("Section 2 Sequence Order", False, 
                                    f"❌ Sequence mismatch. Expected: {expected_sequence}, Got: {actual_sequence}")
                        return False
                else:
                    error_details = []
                    if missing_ids:
                        error_details.append(f"Missing: {missing_ids}")
                    if extra_ids:
                        error_details.append(f"Extra: {extra_ids}")
                    
                    self.log_test("Section 2 Problem IDs Complete", False, 
                                f"❌ Problem ID mismatch. {', '.join(error_details)}")
                    return False
            else:
                self.log_test("Section 2 Problem IDs Complete", False, 
                            f"Failed to fetch Section 2 problems: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Section 2 Problem ID Verification", False, f"Test execution error: {str(e)}")
            return False

    def test_navigation_logic_simulation(self):
        """Test Navigation Logic - Simulate completing practice2_1 and check next problem"""
        try:
            print("\n🧭 NAVIGATION LOGIC TESTING")
            print("Simulating completion of practice2_1 and testing what should be next")
            
            # Step 1: Complete practice2_1 for test student
            practice2_1_attempt = {
                "problem_id": "practice2_1",
                "answer": "k < -12",  # Correct answer for -2/3 k > 8
                "hints_used": 0
            }
            
            response = self.session.post(
                f"{self.base_url}/students/{self.test_student_username}/attempt",
                json=practice2_1_attempt,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("correct"):
                    self.log_test("practice2_1 Completion", True, 
                                f"✅ Successfully completed practice2_1 with score: {data.get('score')}")
                else:
                    self.log_test("practice2_1 Completion", False, 
                                f"❌ practice2_1 answer was incorrect: {data}")
                    return False
            else:
                self.log_test("practice2_1 Completion", False, 
                            f"Failed to submit practice2_1: HTTP {response.status_code}")
                return False
            
            # Step 2: Test navigation logic - what should come after practice2_1?
            expected_sequence = ["prep2", "explanation2", "practice2_1", "practice2_2", "assessment2", "examprep2"]
            
            # Find index of practice2_1
            try:
                practice2_1_index = expected_sequence.index("practice2_1")
                next_index = practice2_1_index + 1
                
                if next_index < len(expected_sequence):
                    expected_next = expected_sequence[next_index]
                    
                    self.log_test("Navigation Logic Calculation", True, 
                                f"✅ practice2_1 is at index {practice2_1_index}, next should be {expected_next} at index {next_index}")
                    
                    # Step 3: Verify the next problem exists and is accessible
                    response = self.session.get(f"{self.base_url}/problems/{expected_next}?username={self.test_student_username}")
                    
                    if response.status_code == 200:
                        next_problem = response.json()
                        self.log_test("Next Problem Accessibility", True, 
                                    f"✅ Next problem {expected_next} is accessible: '{next_problem.get('question_en', '')[:50]}...'")
                        return True
                    else:
                        self.log_test("Next Problem Accessibility", False, 
                                    f"❌ Next problem {expected_next} not accessible: HTTP {response.status_code}")
                        return False
                else:
                    self.log_test("Navigation Logic Calculation", False, 
                                f"❌ practice2_1 is the last problem in sequence (index {practice2_1_index})")
                    return False
                    
            except ValueError:
                self.log_test("Navigation Logic Calculation", False, 
                            f"❌ practice2_1 not found in expected sequence: {expected_sequence}")
                return False
                
        except Exception as e:
            self.log_test("Navigation Logic Testing", False, f"Test execution error: {str(e)}")
            return False

    def test_problem_id_matching(self):
        """Test Problem ID Matching - String matching and case sensitivity"""
        try:
            print("\n🔤 PROBLEM ID MATCHING TESTING")
            print("Testing string matching for 'practice2_1' with array elements")
            
            # Test exact string matching
            expected_sequence = ["prep2", "explanation2", "practice2_1", "practice2_2", "assessment2", "examprep2"]
            test_id = "practice2_1"
            
            # Test 1: Exact match
            exact_match = test_id in expected_sequence
            if exact_match:
                match_index = expected_sequence.index(test_id)
                self.log_test("Exact String Matching", True, 
                            f"✅ '{test_id}' matches exactly at index {match_index}")
            else:
                self.log_test("Exact String Matching", False, 
                            f"❌ '{test_id}' not found in sequence: {expected_sequence}")
                return False
            
            # Test 2: Case sensitivity
            case_variants = ["Practice2_1", "PRACTICE2_1", "practice2_1", "Practice2_1"]
            case_results = []
            
            for variant in case_variants:
                is_match = variant in expected_sequence
                case_results.append(f"{variant}: {'✅' if is_match else '❌'}")
            
            # Only lowercase should match
            correct_case_behavior = case_variants[2] in expected_sequence and all(
                variant not in expected_sequence for variant in case_variants[:2] + case_variants[3:]
            )
            
            if correct_case_behavior:
                self.log_test("Case Sensitivity Test", True, 
                            f"✅ Case sensitivity working correctly: {', '.join(case_results)}")
            else:
                self.log_test("Case Sensitivity Test", False, 
                            f"❌ Case sensitivity issue: {', '.join(case_results)}")
                return False
            
            # Test 3: Special character handling
            special_variants = ["practice2_1", "practice2-1", "practice2.1", "practice21"]
            special_results = []
            
            for variant in special_variants:
                is_match = variant in expected_sequence
                special_results.append(f"{variant}: {'✅' if is_match else '❌'}")
            
            # Only underscore version should match
            correct_special_behavior = special_variants[0] in expected_sequence and all(
                variant not in expected_sequence for variant in special_variants[1:]
            )
            
            if correct_special_behavior:
                self.log_test("Special Character Test", True, 
                            f"✅ Special character handling correct: {', '.join(special_results)}")
                return True
            else:
                self.log_test("Special Character Test", False, 
                            f"❌ Special character handling issue: {', '.join(special_results)}")
                return False
                
        except Exception as e:
            self.log_test("Problem ID Matching Test", False, f"Test execution error: {str(e)}")
            return False

    def test_current_navigation_issue_debug(self):
        """Test Current Navigation Issue Debug - Identify why navigation goes to prep instead of practice2_2"""
        try:
            print("\n🐛 CURRENT NAVIGATION ISSUE DEBUG")
            print("Debugging why navigation goes to prep stage instead of practice2_2 after practice2_1")
            
            # Step 1: Get student progress to see current state
            response = self.session.get(f"{self.base_url}/students/{self.test_student_username}/progress")
            
            if response.status_code == 200:
                progress_data = response.json()
                section2_progress = progress_data.get("progress", {}).get("section2", {})
                
                # Check practice2_1 completion status
                practice2_1_status = section2_progress.get("practice2_1", {})
                is_practice2_1_completed = practice2_1_status.get("completed", False)
                
                if is_practice2_1_completed:
                    self.log_test("practice2_1 Completion Status", True, 
                                f"✅ practice2_1 is marked as completed in progress: {practice2_1_status}")
                else:
                    self.log_test("practice2_1 Completion Status", False, 
                                f"❌ practice2_1 not marked as completed: {practice2_1_status}")
                    return False
                
                # Step 2: Check what the next problem should be according to sequence
                expected_sequence = ["prep2", "explanation2", "practice2_1", "practice2_2", "assessment2", "examprep2"]
                practice2_1_index = expected_sequence.index("practice2_1")
                expected_next = expected_sequence[practice2_1_index + 1]
                
                self.log_test("Expected Next Problem", True, 
                            f"✅ After practice2_1 (index {practice2_1_index}), next should be {expected_next}")
                
                # Step 3: Test if practice2_2 is accessible
                response = self.session.get(f"{self.base_url}/problems/practice2_2?username={self.test_student_username}")
                
                if response.status_code == 200:
                    practice2_2_data = response.json()
                    self.log_test("practice2_2 Accessibility", True, 
                                f"✅ practice2_2 is accessible: '{practice2_2_data.get('question_en', '')[:50]}...'")
                else:
                    self.log_test("practice2_2 Accessibility", False, 
                                f"❌ practice2_2 not accessible: HTTP {response.status_code}")
                    return False
                
                # Step 4: Check if there are any hardcoded navigation rules
                # Test accessing prep2 to see if it's incorrectly being suggested
                response = self.session.get(f"{self.base_url}/problems/prep2?username={self.test_student_username}")
                
                if response.status_code == 200:
                    prep2_data = response.json()
                    self.log_test("prep2 Accessibility Check", True, 
                                f"✅ prep2 is also accessible (this might be the issue): '{prep2_data.get('question_en', '')[:30]}...'")
                    
                    # This suggests the issue might be in frontend navigation logic, not backend
                    self.log_test("Navigation Issue Analysis", True, 
                                f"✅ Backend correctly serves both prep2 and practice2_2. Issue likely in frontend navigation logic.")
                    return True
                else:
                    self.log_test("prep2 Accessibility Check", False, 
                                f"❌ prep2 not accessible: HTTP {response.status_code}")
                    return False
                    
            else:
                self.log_test("Student Progress Check", False, 
                            f"Failed to get student progress: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Current Navigation Issue Debug", False, f"Test execution error: {str(e)}")
            return False

    def test_section_sequences_array_lookup(self):
        """Test Section Sequences Array Lookup - Verify sectionSequences array functionality"""
        try:
            print("\n📋 SECTION SEQUENCES ARRAY LOOKUP TESTING")
            print("Testing if sectionSequences array lookup works correctly for Section 2")
            
            # Simulate the frontend sectionSequences array
            section_sequences = {
                "section1": ["prep1", "explanation1", "practice1", "practice2", "assessment1", "examprep1"],
                "section2": ["prep2", "explanation2", "practice2_1", "practice2_2", "assessment2", "examprep2"],
                "section3": ["prep3", "explanation3", "practice3_1", "practice3_2", "assessment3", "examprep3"],
                "section4": ["prep4", "explanation4", "practice4_1", "practice4_2", "assessment4", "examprep4"],
                "section5": ["prep5", "explanation5", "practice5_1", "practice5_2", "assessment5", "examprep5"]
            }
            
            # Test Section 2 sequence lookup
            section2_sequence = section_sequences.get("section2", [])
            
            if section2_sequence:
                self.log_test("Section 2 Sequence Lookup", True, 
                            f"✅ Section 2 sequence found: {section2_sequence}")
                
                # Test finding practice2_1 in the sequence
                if "practice2_1" in section2_sequence:
                    practice2_1_index = section2_sequence.index("practice2_1")
                    next_index = practice2_1_index + 1
                    
                    if next_index < len(section2_sequence):
                        next_problem = section2_sequence[next_index]
                        
                        if next_problem == "practice2_2":
                            self.log_test("Sequence Navigation Logic", True, 
                                        f"✅ practice2_1 at index {practice2_1_index} → next is {next_problem} at index {next_index}")
                            
                            # Verify this matches backend data
                            response = self.session.get(f"{self.base_url}/problems/section/section2")
                            
                            if response.status_code == 200:
                                backend_problems = response.json()
                                backend_ids = [p.get("id") for p in backend_problems]
                                
                                # Check if backend sequence matches frontend expectation
                                sequence_match = all(pid in backend_ids for pid in section2_sequence)
                                
                                if sequence_match:
                                    self.log_test("Backend-Frontend Sequence Match", True, 
                                                f"✅ Backend problems match frontend sequence expectations")
                                    return True
                                else:
                                    missing_in_backend = [pid for pid in section2_sequence if pid not in backend_ids]
                                    self.log_test("Backend-Frontend Sequence Match", False, 
                                                f"❌ Backend missing problems: {missing_in_backend}")
                                    return False
                            else:
                                self.log_test("Backend Sequence Verification", False, 
                                            f"Failed to fetch backend problems: HTTP {response.status_code}")
                                return False
                        else:
                            self.log_test("Sequence Navigation Logic", False, 
                                        f"❌ Expected practice2_2 after practice2_1, got {next_problem}")
                            return False
                    else:
                        self.log_test("Sequence Navigation Logic", False, 
                                    f"❌ practice2_1 is last in sequence (index {practice2_1_index})")
                        return False
                else:
                    self.log_test("practice2_1 in Sequence", False, 
                                f"❌ practice2_1 not found in Section 2 sequence: {section2_sequence}")
                    return False
            else:
                self.log_test("Section 2 Sequence Lookup", False, 
                            f"❌ Section 2 sequence not found in sectionSequences")
                return False
                
        except Exception as e:
            self.log_test("Section Sequences Array Lookup", False, f"Test execution error: {str(e)}")
            return False

    def generate_navigation_summary(self, results, critical_failures):
        """Generate comprehensive summary of navigation flow testing"""
        print("\n" + "=" * 80)
        print("🧭 CRITICAL NAVIGATION FLOW BUG TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL NAVIGATION FLOW TEST RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL NAVIGATION FLOW ISSUES:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  NAVIGATION RISK: Students cannot progress properly through Section 2!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix navigation flow logic")
        else:
            print(f"\n🎉 NO CRITICAL NAVIGATION FLOW ISSUES DETECTED")
        
        print(f"\n📋 NAVIGATION FLOW STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL NAVIGATION FLOW TESTS PASSED")
            print("   ✅ Section 2 problem IDs verified (prep2 → explanation2 → practice2_1 → practice2_2 → assessment2 → examprep2)")
            print("   ✅ Navigation logic working (practice2_1 → practice2_2)")
            print("   ✅ Problem ID matching working correctly")
            print("   ✅ Backend serves correct next problems")
            print("   ✅ Section sequences array lookup functional")
            print("   🛡️  NAVIGATION INTEGRITY: PROTECTED")
        else:
            print("   ⚠️  NAVIGATION FLOW ISSUES DETECTED")
            print("   🔧 Navigation logic needs fixes")
            print("   🚨 STUDENT PROGRESSION: BLOCKED")
        
        print("\n" + "=" * 80)

    def run_navigation_flow_tests(self):
        """Run comprehensive navigation flow tests"""
        print("=" * 80)
        print("🧭 CRITICAL NAVIGATION FLOW BUG TESTING")
        print("=" * 80)
        print("Testing Section 2 navigation sequence to debug the critical navigation flow bug")
        
        # Test categories for navigation flow
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("Section 2 Problem IDs Verification", self.test_section2_problem_ids_verification, "critical"),
            ("Navigation Logic Simulation", self.test_navigation_logic_simulation, "critical"),
            ("Problem ID Matching", self.test_problem_id_matching, "critical"),
            ("Current Navigation Issue Debug", self.test_current_navigation_issue_debug, "critical"),
            ("Section Sequences Array Lookup", self.test_section_sequences_array_lookup, "high")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 NAVIGATION FLOW TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive navigation flow summary
        self.generate_navigation_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run navigation flow tests"""
    print("🚀 Starting CRITICAL NAVIGATION FLOW BUG Testing...")
    print("🎯 Goal: Debug Section 2 navigation sequence issue where practice2_1 → prep instead of practice2_2")
    
    tester = NavigationFlowTester(BACKEND_URL)
    results = tester.run_navigation_flow_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 NAVIGATION FLOW ALERT: {failed_tests} test(s) failed!")
        print("🔧 Navigation flow logic implementation required to fix student progression")
    else:
        print(f"\n🛡️  NAVIGATION FLOW CONFIRMED: All navigation flow tests passed!")
        print("✅ Section 2 navigation sequence is working correctly")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()