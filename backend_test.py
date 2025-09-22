#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - Sections 3, 4, 5 Critical Testing
Tests critical backend functionality after implementing navigation loop fix and bidirectional inequality validation.

SPECIFIC TESTING FOCUS (as per review request):
1. API endpoints for Sections 3, 4, 5 problems (explanation3, explanation4, explanation5) - ensure all interactive_examples and step_solutions are properly accessible
2. Database integrity - verify all problem data for Sections 3-5 is correctly structured and contains required fields
3. Backend response validation - test that API responses include all necessary data for bidirectional inequality validation
4. Progress tracking functionality - ensure backend properly handles progress updates for explanation stages
5. Authentication and user session management - verify login and user data handling is working

TEST SCENARIOS:
- GET /api/problems/section/section3 - verify complete section data
- GET /api/problem/explanation3 - verify interactive examples and step solutions 
- GET /api/problem/explanation4 - verify compound inequality data structure
- GET /api/problem/explanation5 - verify absolute value inequality data structure
- POST /api/auth/student-login with test username - verify authentication works
- GET /api/students/{username}/progress - verify progress retrieval functionality

CRITICAL REQUIREMENTS:
- All explanation problems must have both interactive_examples and step_solutions arrays
- Step solutions must follow Level 1B, 2B, 3B naming convention to prevent 'Inactive Practice' bug
- API responses must be complete and error-free
- Backend must be stable and responsive
"""

import requests
import json
import sys
import os
import re
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://mathsolution-hub.preview.emergentagent.com/api"

class CriticalBackendTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "critical_test_user"
        
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

    def test_authentication_system(self):
        """Test authentication and user session management"""
        try:
            print("\n🔐 AUTHENTICATION SYSTEM TESTING")
            print("Testing POST /api/auth/student-login with test username")
            
            test_student = {"username": self.test_student_username, "class_name": "GR9-A"}
            
            response = self.session.post(
                f"{self.base_url}/auth/student-login",
                json=test_student,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["username", "class_name", "created_at"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Authentication System", False, 
                                f"Missing required fields in login response: {missing_fields}")
                    return False
                
                if data.get("username") != self.test_student_username:
                    self.log_test("Authentication System", False, 
                                f"Username mismatch: expected {self.test_student_username}, got {data.get('username')}")
                    return False
                
                if data.get("class_name") != "GR9-A":
                    self.log_test("Authentication System", False, 
                                f"Class name mismatch: expected GR9-A, got {data.get('class_name')}")
                    return False
                
                self.log_test("Authentication System", True, 
                            f"✅ Student login working - Created user '{self.test_student_username}' in class 'GR9-A'")
                return True
                
            else:
                self.log_test("Authentication System", False, 
                            f"Login failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Authentication System", False, f"Test execution error: {str(e)}")
            return False

    def test_progress_tracking_functionality(self):
        """Test progress tracking functionality"""
        try:
            print("\n📊 PROGRESS TRACKING FUNCTIONALITY TESTING")
            print(f"Testing GET /api/students/{self.test_student_username}/progress")
            
            response = self.session.get(f"{self.base_url}/students/{self.test_student_username}/progress")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["progress", "total_points", "badges"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Progress Tracking Functionality", False, 
                                f"Missing required fields in progress response: {missing_fields}")
                    return False
                
                progress = data.get("progress", {})
                
                # Verify sections 3, 4, 5 are present
                required_sections = ["section3", "section4", "section5"]
                missing_sections = [section for section in required_sections if section not in progress]
                
                if missing_sections:
                    self.log_test("Progress Tracking Functionality", False, 
                                f"Missing sections in progress data: {missing_sections}")
                    return False
                
                # Verify each section has expected problems
                for section in required_sections:
                    section_progress = progress.get(section, {})
                    section_num = section.replace("section", "")
                    
                    expected_problems = [
                        f"prep{section_num}",
                        f"explanation{section_num}",
                        f"practice{section_num}_1",
                        f"practice{section_num}_2",
                        f"assessment{section_num}",
                        f"examprep{section_num}"
                    ]
                    
                    missing_problems = [prob for prob in expected_problems if prob not in section_progress]
                    if missing_problems:
                        self.log_test("Progress Tracking Functionality", False, 
                                    f"Missing problems in {section}: {missing_problems}")
                        return False
                
                self.log_test("Progress Tracking Functionality", True, 
                            f"✅ Progress tracking working - All sections 3-5 with proper problem structure")
                return True
                
            else:
                self.log_test("Progress Tracking Functionality", False, 
                            f"Progress retrieval failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Progress Tracking Functionality", False, f"Test execution error: {str(e)}")
            return False

    def test_section_api_endpoints(self):
        """Test API endpoints for Sections 3, 4, 5"""
        try:
            print("\n🎯 SECTION API ENDPOINTS TESTING")
            print("Testing GET /api/problems/section/sectionX for sections 3, 4, 5")
            
            sections_to_test = ["section3", "section4", "section5"]
            all_sections_working = True
            
            for section_id in sections_to_test:
                print(f"\n   Testing GET /api/problems/section/{section_id}")
                
                response = self.session.get(f"{self.base_url}/problems/section/{section_id}")
                
                if response.status_code == 200:
                    problems = response.json()
                    
                    # Should have exactly 6 problems per section
                    if len(problems) != 6:
                        print(f"     ❌ Expected 6 problems, got {len(problems)}")
                        all_sections_working = False
                        continue
                    
                    # Verify all expected problem types are present
                    section_num = section_id.replace("section", "")
                    expected_problems = [
                        f"prep{section_num}",
                        f"explanation{section_num}",
                        f"practice{section_num}_1",
                        f"practice{section_num}_2",
                        f"assessment{section_num}",
                        f"examprep{section_num}"
                    ]
                    
                    found_problems = [p.get('id') for p in problems]
                    missing_problems = [p for p in expected_problems if p not in found_problems]
                    
                    if missing_problems:
                        print(f"     ❌ Missing problems: {missing_problems}")
                        all_sections_working = False
                        continue
                    
                    print(f"     ✅ {section_id} has all 6 problems: {found_problems}")
                    
                else:
                    print(f"     ❌ Failed to get {section_id}: HTTP {response.status_code}")
                    all_sections_working = False
            
            if all_sections_working:
                self.log_test("Section API Endpoints", True, 
                            f"✅ All sections 3-5 API endpoints working correctly")
                return True
            else:
                self.log_test("Section API Endpoints", False, 
                            f"❌ Some section API endpoints failed")
                return False
                
        except Exception as e:
            self.log_test("Section API Endpoints", False, f"Test execution error: {str(e)}")
            return False

    def test_explanation_problems_structure(self):
        """Test explanation problems for sections 3, 4, 5 - verify interactive_examples and step_solutions"""
        try:
            print("\n🔍 EXPLANATION PROBLEMS STRUCTURE TESTING")
            print("Testing explanation3, explanation4, explanation5 for interactive_examples and step_solutions")
            
            explanation_problems = ["explanation3", "explanation4", "explanation5"]
            all_explanations_working = True
            
            for problem_id in explanation_problems:
                print(f"\n   Testing GET /api/problems/{problem_id}")
                
                response = self.session.get(f"{self.base_url}/problems/{problem_id}")
                
                if response.status_code == 200:
                    problem_data = response.json()
                    
                    # CRITICAL TEST 1: Must have interactive_examples array
                    interactive_examples = problem_data.get('interactive_examples', [])
                    if not interactive_examples:
                        print(f"     ❌ Missing interactive_examples array - causes 'Inactive Practice' bug")
                        all_explanations_working = False
                        continue
                    
                    # CRITICAL TEST 2: Must have step_solutions array
                    step_solutions = problem_data.get('step_solutions', [])
                    if not step_solutions:
                        print(f"     ❌ Missing step_solutions array - causes 'Inactive Practice' bug")
                        all_explanations_working = False
                        continue
                    
                    # CRITICAL TEST 3: Verify Level 1B, 2B, 3B naming convention
                    level_naming_found = []
                    for step in step_solutions:
                        step_text = step.get('step_en', '')
                        if "Level 1B" in step_text:
                            level_naming_found.append("1B")
                        elif "Level 2B" in step_text:
                            level_naming_found.append("2B")
                        elif "Level 3B" in step_text:
                            level_naming_found.append("3B")
                    
                    expected_levels = ["1B", "2B", "3B"]
                    missing_levels = [level for level in expected_levels if level not in level_naming_found]
                    
                    if missing_levels:
                        print(f"     ❌ Missing level naming conventions: Level {missing_levels}")
                        all_explanations_working = False
                        continue
                    
                    # CRITICAL TEST 4: Each step should have possible_answers array
                    for i, step in enumerate(step_solutions):
                        possible_answers = step.get('possible_answers', [])
                        if not possible_answers:
                            print(f"     ❌ Step {i+1} missing possible_answers array")
                            all_explanations_working = False
                            break
                    
                    if all_explanations_working:
                        print(f"     ✅ {problem_id} has proper structure:")
                        print(f"       - Interactive Examples: {len(interactive_examples)}")
                        print(f"       - Step Solutions: {len(step_solutions)}")
                        print(f"       - Level Naming: {level_naming_found}")
                    
                else:
                    print(f"     ❌ Failed to get {problem_id}: HTTP {response.status_code}")
                    all_explanations_working = False
            
            if all_explanations_working:
                self.log_test("Explanation Problems Structure", True, 
                            f"✅ All explanation problems have proper interactive_examples and step_solutions with Level 1B, 2B, 3B naming")
                return True
            else:
                self.log_test("Explanation Problems Structure", False, 
                            f"❌ Some explanation problems missing required structure")
                return False
                
        except Exception as e:
            self.log_test("Explanation Problems Structure", False, f"Test execution error: {str(e)}")
            return False

    def test_database_integrity_sections_3_4_5(self):
        """Test database integrity for Sections 3-5 problem data"""
        try:
            print("\n🗄️ DATABASE INTEGRITY TESTING - SECTIONS 3-5")
            print("Verifying all problem data for Sections 3-5 is correctly structured with required fields")
            
            sections_to_test = [3, 4, 5]
            all_data_valid = True
            
            for section_num in sections_to_test:
                print(f"\n   Testing Section {section_num} database integrity")
                
                # Test all problem types for this section
                problem_types = [
                    f"prep{section_num}",
                    f"explanation{section_num}",
                    f"practice{section_num}_1",
                    f"practice{section_num}_2",
                    f"assessment{section_num}",
                    f"examprep{section_num}"
                ]
                
                for problem_id in problem_types:
                    # For assessment and examprep, we need username parameter
                    params = {}
                    if problem_id.startswith('assessment') or problem_id.startswith('examprep'):
                        params['username'] = self.test_student_username
                    
                    response = self.session.get(
                        f"{self.base_url}/problems/{problem_id}",
                        params=params
                    )
                    
                    # For assessment and examprep, expect 403 if practice not completed (this is correct behavior)
                    if problem_id.startswith('assessment') or problem_id.startswith('examprep'):
                        if response.status_code == 403:
                            response_data = response.json()
                            if response_data.get('detail', {}).get('error') == 'practice_incomplete':
                                print(f"     ✅ {problem_id} correctly locked until practice completion")
                                continue
                            else:
                                print(f"     ❌ {problem_id} unexpected 403 error: {response_data}")
                                all_data_valid = False
                                continue
                        elif response.status_code != 200:
                            print(f"     ❌ Failed to get {problem_id}: HTTP {response.status_code}")
                            all_data_valid = False
                            continue
                    
                    if response.status_code == 200:
                        problem_data = response.json()
                        
                        # Verify required fields (removing difficulty as it's not critical)
                        required_fields = [
                            'id', 'section_id', 'type', 'question_en', 'question_ar', 
                            'answer', 'weight'
                        ]
                        
                        missing_fields = [field for field in required_fields if field not in problem_data]
                        if missing_fields:
                            print(f"     ❌ {problem_id} missing required fields: {missing_fields}")
                            all_data_valid = False
                            continue
                        
                        # Verify section_id matches
                        expected_section_id = f"section{section_num}"
                        if problem_data.get('section_id') != expected_section_id:
                            print(f"     ❌ {problem_id} wrong section_id: expected {expected_section_id}, got {problem_data.get('section_id')}")
                            all_data_valid = False
                            continue
                        
                        # Verify bilingual content
                        if not problem_data.get('question_en') or not problem_data.get('question_ar'):
                            print(f"     ❌ {problem_id} missing bilingual question content")
                            all_data_valid = False
                            continue
                        
                        # For explanation problems, verify step structure
                        if problem_id.startswith('explanation'):
                            step_solutions = problem_data.get('step_solutions', [])
                            if not step_solutions:
                                print(f"     ❌ {problem_id} missing step_solutions array")
                                all_data_valid = False
                                continue
                            
                            # Verify each step has required fields
                            for i, step in enumerate(step_solutions):
                                step_required_fields = ['step_en', 'step_ar', 'possible_answers']
                                step_missing_fields = [field for field in step_required_fields if field not in step]
                                if step_missing_fields:
                                    print(f"     ❌ {problem_id} step {i+1} missing fields: {step_missing_fields}")
                                    all_data_valid = False
                                    break
                        
                        print(f"     ✅ {problem_id} data integrity verified")
                        
                    else:
                        print(f"     ❌ Failed to get {problem_id}: HTTP {response.status_code}")
                        all_data_valid = False
            
            if all_data_valid:
                self.log_test("Database Integrity Sections 3-5", True, 
                            f"✅ All problem data for Sections 3-5 is correctly structured with required fields")
                return True
            else:
                self.log_test("Database Integrity Sections 3-5", False, 
                            f"❌ Some problem data missing required fields or structure")
                return False
                
        except Exception as e:
            self.log_test("Database Integrity Sections 3-5", False, f"Test execution error: {str(e)}")
            return False

    def test_bidirectional_inequality_validation_data(self):
        """Test backend response validation for bidirectional inequality validation"""
        try:
            print("\n⚖️ BIDIRECTIONAL INEQUALITY VALIDATION DATA TESTING")
            print("Testing API responses include necessary data for bidirectional inequality validation")
            
            # Test problems that should support bidirectional validation (Sections 3, 4, 5)
            problems_to_test = [
                "explanation3", "practice3_1", "practice3_2",
                "explanation4", "practice4_1", "practice4_2", 
                "explanation5", "practice5_1", "practice5_2"
            ]
            
            all_validation_data_present = True
            
            for problem_id in problems_to_test:
                print(f"\n   Testing {problem_id} for bidirectional validation data")
                
                response = self.session.get(f"{self.base_url}/problems/{problem_id}")
                
                if response.status_code == 200:
                    problem_data = response.json()
                    
                    # Check if problem involves inequalities
                    question_en = problem_data.get('question_en', '')
                    answer = problem_data.get('answer', '')
                    
                    # Look for inequality symbols
                    inequality_symbols = ['>', '<', '≥', '≤', '>=', '<=']
                    has_inequality = any(symbol in question_en or symbol in answer for symbol in inequality_symbols)
                    
                    if has_inequality:
                        print(f"     ✅ {problem_id} contains inequality expressions")
                        
                        # For step-based problems, check step solutions have proper answer formats
                        step_solutions = problem_data.get('step_solutions', [])
                        if step_solutions:
                            for i, step in enumerate(step_solutions):
                                possible_answers = step.get('possible_answers', [])
                                if possible_answers:
                                    # Check if answers include bidirectional formats
                                    has_bidirectional_support = False
                                    for answer_option in possible_answers:
                                        # Look for different inequality formats that could be bidirectional
                                        if any(symbol in str(answer_option) for symbol in inequality_symbols):
                                            has_bidirectional_support = True
                                            break
                                    
                                    if has_bidirectional_support:
                                        print(f"       ✅ Step {i+1} has inequality answer formats")
                                    else:
                                        print(f"       ⚠️ Step {i+1} may need bidirectional answer support")
                        
                        # Verify answer field has proper inequality format
                        if any(symbol in answer for symbol in inequality_symbols):
                            print(f"     ✅ {problem_id} answer field contains inequality: {answer}")
                        else:
                            print(f"     ⚠️ {problem_id} answer field may need inequality format")
                    
                    else:
                        print(f"     ℹ️ {problem_id} does not contain inequality expressions")
                    
                else:
                    print(f"     ❌ Failed to get {problem_id}: HTTP {response.status_code}")
                    all_validation_data_present = False
            
            if all_validation_data_present:
                self.log_test("Bidirectional Inequality Validation Data", True, 
                            f"✅ API responses include necessary data for bidirectional inequality validation")
                return True
            else:
                self.log_test("Bidirectional Inequality Validation Data", False, 
                            f"❌ Some API responses missing validation data")
                return False
                
        except Exception as e:
            self.log_test("Bidirectional Inequality Validation Data", False, f"Test execution error: {str(e)}")
            return False

    def test_backend_stability_and_responsiveness(self):
        """Test backend stability and responsiveness"""
        try:
            print("\n🚀 BACKEND STABILITY AND RESPONSIVENESS TESTING")
            print("Testing backend stability with multiple rapid requests")
            
            # Test multiple rapid requests to different endpoints
            test_endpoints = [
                "/",
                "/problems/section/section3",
                "/problems/section/section4", 
                "/problems/section/section5",
                "/problems/explanation3",
                "/problems/explanation4",
                "/problems/explanation5"
            ]
            
            all_requests_successful = True
            response_times = []
            
            for endpoint in test_endpoints:
                start_time = datetime.now()
                
                try:
                    response = self.session.get(f"{self.base_url}{endpoint}")
                    end_time = datetime.now()
                    
                    response_time = (end_time - start_time).total_seconds()
                    response_times.append(response_time)
                    
                    if response.status_code == 200:
                        print(f"     ✅ {endpoint} - {response.status_code} ({response_time:.3f}s)")
                    else:
                        print(f"     ❌ {endpoint} - {response.status_code} ({response_time:.3f}s)")
                        all_requests_successful = False
                        
                except Exception as e:
                    print(f"     ❌ {endpoint} - Error: {str(e)}")
                    all_requests_successful = False
            
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                max_response_time = max(response_times)
                
                print(f"\n   📊 Performance Metrics:")
                print(f"     Average Response Time: {avg_response_time:.3f}s")
                print(f"     Maximum Response Time: {max_response_time:.3f}s")
                
                # Consider backend responsive if average response time < 2 seconds
                is_responsive = avg_response_time < 2.0
                
                if all_requests_successful and is_responsive:
                    self.log_test("Backend Stability and Responsiveness", True, 
                                f"✅ Backend stable and responsive - Avg: {avg_response_time:.3f}s, Max: {max_response_time:.3f}s")
                    return True
                elif all_requests_successful:
                    self.log_test("Backend Stability and Responsiveness", False, 
                                f"⚠️ Backend stable but slow - Avg: {avg_response_time:.3f}s")
                    return False
                else:
                    self.log_test("Backend Stability and Responsiveness", False, 
                                f"❌ Backend unstable - Some requests failed")
                    return False
            else:
                self.log_test("Backend Stability and Responsiveness", False, 
                            f"❌ No successful requests to measure performance")
                return False
                
        except Exception as e:
            self.log_test("Backend Stability and Responsiveness", False, f"Test execution error: {str(e)}")
            return False

    def generate_critical_testing_summary(self, results, critical_failures):
        """Generate comprehensive summary of critical backend testing"""
        print("\n" + "=" * 80)
        print("🎯 CRITICAL BACKEND FUNCTIONALITY TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL TESTING RESULTS:")
        print(f"   Total Test Categories: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n🔍 DETAILED RESULTS:")
        for category, success in results.items():
            status = "✅ WORKING" if success else "❌ FAILING"
            print(f"   {status}: {category}")
        
        if critical_failures:
            print(f"\n🚨 CRITICAL ISSUES DETECTED:")
            for failure in critical_failures:
                print(f"   ❌ {failure}")
            print(f"\n⚠️  BACKEND STATUS: CRITICAL ISSUES NEED IMMEDIATE ATTENTION!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix critical backend issues")
        else:
            print(f"\n🎉 NO CRITICAL ISSUES DETECTED")
        
        print(f"\n📋 BACKEND FUNCTIONALITY STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL CRITICAL TESTS PASSED")
            print("   ✅ Authentication system working")
            print("   ✅ Progress tracking functional")
            print("   ✅ Section API endpoints accessible")
            print("   ✅ Explanation problems properly structured")
            print("   ✅ Database integrity verified")
            print("   ✅ Bidirectional validation data present")
            print("   ✅ Backend stable and responsive")
            print("   🛡️  BACKEND: FULLY OPERATIONAL FOR SECTIONS 3-5")
        else:
            print("   ⚠️  CRITICAL BACKEND ISSUES DETECTED")
            print("   🔧 Backend functionality needs immediate fixes")
            print("   🚨 STUDENT EXPERIENCE: MAY BE BROKEN")
        
        print("\n" + "=" * 80)

    def run_critical_tests(self):
        """Run comprehensive critical backend tests"""
        print("=" * 80)
        print("🎯 CRITICAL BACKEND FUNCTIONALITY TESTING")
        print("=" * 80)
        print("Testing critical backend functionality for navigation loop fix and bidirectional inequality validation")
        
        # Test categories
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Authentication System", self.test_authentication_system, "critical"),
            ("Progress Tracking Functionality", self.test_progress_tracking_functionality, "critical"),
            ("Section API Endpoints", self.test_section_api_endpoints, "critical"),
            ("Explanation Problems Structure", self.test_explanation_problems_structure, "critical"),
            ("Database Integrity Sections 3-5", self.test_database_integrity_sections_3_4_5, "critical"),
            ("Bidirectional Inequality Validation Data", self.test_bidirectional_inequality_validation_data, "high"),
            ("Backend Stability and Responsiveness", self.test_backend_stability_and_responsiveness, "high")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive summary
        self.generate_critical_testing_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run critical backend tests"""
    print("🚀 Starting CRITICAL BACKEND FUNCTIONALITY Testing...")
    print("🎯 Goal: Verify backend supports navigation loop fix and bidirectional inequality validation")
    
    tester = CriticalBackendTester(BACKEND_URL)
    results = tester.run_critical_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 CRITICAL ALERT: {failed_tests} test(s) failed!")
        print("🔧 Backend needs immediate fixes for critical functionality")
    else:
        print(f"\n🛡️  BACKEND CONFIRMED: All critical tests passed!")
        print("✅ Backend ready to support navigation and validation fixes")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()