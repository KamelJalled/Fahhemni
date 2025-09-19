#!/usr/bin/env python3
"""
Backend API Test Suite for Math Tutoring App - Section 2 Word Problem Hints Socratic Method Fix
Tests the critical pedagogical bug fix where word problem hints were showing direct inequalities
instead of using progressive Socratic guidance to help students discover solutions.
"""

import requests
import json
import sys
import os
import re
from datetime import datetime

# Use backend URL from frontend/.env as specified in review request
BACKEND_URL = "https://inequality-solver.preview.emergentagent.com/api"

class Section2HintsTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_student_username = "hints_test_student"
        
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
        """Create test student for hints testing"""
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

    def test_practice2_2_database_verification(self):
        """Test practice2_2 (ticket sales problem) database content and hints"""
        try:
            print("\n🎫 PRACTICE2_2 (TICKET SALES PROBLEM) DATABASE VERIFICATION")
            print("Expected: Progressive Socratic hints that DO NOT show '10t ≥ 500' directly")
            
            # Get practice2_2 problem data
            response = self.session.get(f"{self.base_url}/problems/practice2_2?username={self.test_student_username}")
            
            if response.status_code == 200:
                problem_data = response.json()
                
                # Verify problem content integrity
                expected_question = "Tickets must be sold at SAR 10 each to collect at least SAR 500"
                expected_answer = "t ≥ 50"
                
                if expected_question in problem_data.get("question_en", ""):
                    self.log_test("practice2_2 Question Content", True, 
                                f"✅ Question content correct: '{problem_data.get('question_en')[:60]}...'")
                else:
                    self.log_test("practice2_2 Question Content", False, 
                                f"❌ Question content mismatch. Got: '{problem_data.get('question_en')}'")
                    return False
                
                if problem_data.get("answer") == expected_answer:
                    self.log_test("practice2_2 Answer Content", True, 
                                f"✅ Answer correct: {problem_data.get('answer')}")
                else:
                    self.log_test("practice2_2 Answer Content", False, 
                                f"❌ Answer incorrect. Expected: {expected_answer}, Got: {problem_data.get('answer')}")
                    return False
                
                # CRITICAL: Verify hints follow Socratic method and DO NOT show direct inequality
                hints_en = problem_data.get("hints_en", [])
                hints_ar = problem_data.get("hints_ar", [])
                
                if len(hints_en) == 3 and len(hints_ar) == 3:
                    self.log_test("practice2_2 Hint Count", True, 
                                f"✅ Correct number of hints: {len(hints_en)} English, {len(hints_ar)} Arabic")
                else:
                    self.log_test("practice2_2 Hint Count", False, 
                                f"❌ Expected 3 hints each. Got: {len(hints_en)} English, {len(hints_ar)} Arabic")
                    return False
                
                # CRITICAL: Check that hints DO NOT contain direct inequality "10t ≥ 500"
                forbidden_patterns = ["10t ≥ 500", "10t >= 500", "10 * t ≥ 500", "10 * t >= 500"]
                direct_inequality_found = False
                
                for hint in hints_en + hints_ar:
                    for pattern in forbidden_patterns:
                        if pattern in hint:
                            direct_inequality_found = True
                            self.log_test("practice2_2 No Direct Inequality", False, 
                                        f"❌ CRITICAL BUG: Found direct inequality '{pattern}' in hint: '{hint}'")
                            break
                    if direct_inequality_found:
                        break
                
                if not direct_inequality_found:
                    self.log_test("practice2_2 No Direct Inequality", True, 
                                f"✅ CRITICAL FIX VERIFIED: No direct inequalities found in hints")
                else:
                    return False
                
                # Verify progressive Socratic guidance structure
                # Expected progression: Variable identification → Mathematical relationship → Inequality symbol meaning
                hint1_keywords = ["variable", "t represents", "tickets", "price", "amount"]
                hint2_keywords = ["sell", "collect", "greater than or equal", "≥"]
                hint3_keywords = ["Amount collected", "price per ticket", "number of tickets", "at least"]
                
                hint1_valid = any(keyword.lower() in hints_en[0].lower() for keyword in hint1_keywords)
                hint2_valid = any(keyword.lower() in hints_en[1].lower() for keyword in hint2_keywords)
                hint3_valid = any(keyword.lower() in hints_en[2].lower() for keyword in hint3_keywords)
                
                if hint1_valid and hint2_valid and hint3_valid:
                    self.log_test("practice2_2 Socratic Progression", True, 
                                f"✅ Progressive Socratic guidance verified: Variable ID → Math relationship → Symbol meaning")
                else:
                    self.log_test("practice2_2 Socratic Progression", False, 
                                f"❌ Socratic progression incomplete. Hint1: {hint1_valid}, Hint2: {hint2_valid}, Hint3: {hint3_valid}")
                    return False
                
                # Verify bilingual support
                arabic_keywords_present = any("ت" in hint or "تذكرة" in hint or "ريال" in hint for hint in hints_ar)
                if arabic_keywords_present:
                    self.log_test("practice2_2 Bilingual Support", True, 
                                f"✅ Arabic hints properly implemented with mathematical terms")
                else:
                    self.log_test("practice2_2 Bilingual Support", False, 
                                f"❌ Arabic hints missing proper mathematical terminology")
                    return False
                
                return True
                
            else:
                self.log_test("practice2_2 Database Access", False, 
                            f"Failed to fetch practice2_2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("practice2_2 Database Verification", False, f"Test execution error: {str(e)}")
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

    def test_examprep2_database_verification(self):
        """Test examprep2 (candy distribution problem) database content and hints"""
        try:
            print("\n🍬 EXAMPREP2 (CANDY DISTRIBUTION PROBLEM) DATABASE VERIFICATION")
            print("Expected: Progressive Socratic hints that DO NOT show '15p ≥ 60' directly")
            
            # First complete required stages to unlock examprep2
            if not self.complete_required_stages_for_examprep2():
                self.log_test("examprep2 Prerequisites", False, 
                            "❌ Failed to complete required stages (practice2_1, practice2_2, assessment2)")
                return False
            else:
                self.log_test("examprep2 Prerequisites", True, 
                            "✅ Completed required stages to unlock examprep2")
            
            # Get examprep2 problem data
            response = self.session.get(f"{self.base_url}/problems/examprep2?username={self.test_student_username}")
            
            if response.status_code == 200:
                problem_data = response.json()
                
                # Verify problem content integrity
                expected_question = "distribute at least 60 pieces of candy equally among 15 children"
                expected_answer = "p ≥ 4"
                
                if expected_question.lower() in problem_data.get("question_en", "").lower():
                    self.log_test("examprep2 Question Content", True, 
                                f"✅ Question content correct: '{problem_data.get('question_en')[:60]}...'")
                else:
                    self.log_test("examprep2 Question Content", False, 
                                f"❌ Question content mismatch. Got: '{problem_data.get('question_en')}'")
                    return False
                
                if problem_data.get("answer") == expected_answer:
                    self.log_test("examprep2 Answer Content", True, 
                                f"✅ Answer correct: {problem_data.get('answer')}")
                else:
                    self.log_test("examprep2 Answer Content", False, 
                                f"❌ Answer incorrect. Expected: {expected_answer}, Got: {problem_data.get('answer')}")
                    return False
                
                # CRITICAL: Verify hints follow Socratic method and DO NOT show direct inequality
                hints_en = problem_data.get("hints_en", [])
                hints_ar = problem_data.get("hints_ar", [])
                
                if len(hints_en) == 3 and len(hints_ar) == 3:
                    self.log_test("examprep2 Hint Count", True, 
                                f"✅ Correct number of hints: {len(hints_en)} English, {len(hints_ar)} Arabic")
                else:
                    self.log_test("examprep2 Hint Count", False, 
                                f"❌ Expected 3 hints each. Got: {len(hints_en)} English, {len(hints_ar)} Arabic")
                    return False
                
                # CRITICAL: Check that hints DO NOT contain direct inequality "15p ≥ 60"
                forbidden_patterns = ["15p ≥ 60", "15p >= 60", "15 * p ≥ 60", "15 * p >= 60"]
                direct_inequality_found = False
                
                for hint in hints_en + hints_ar:
                    for pattern in forbidden_patterns:
                        if pattern in hint:
                            direct_inequality_found = True
                            self.log_test("examprep2 No Direct Inequality", False, 
                                        f"❌ CRITICAL BUG: Found direct inequality '{pattern}' in hint: '{hint}'")
                            break
                    if direct_inequality_found:
                        break
                
                if not direct_inequality_found:
                    self.log_test("examprep2 No Direct Inequality", True, 
                                f"✅ CRITICAL FIX VERIFIED: No direct inequalities found in hints")
                else:
                    return False
                
                # Verify progressive Socratic guidance structure
                # Expected progression: Variable/children count → Total calculation → "At least" meaning
                hint1_keywords = ["Variable p", "pieces per child", "children", "total pieces"]
                hint2_keywords = ["each child gets", "15 children", "pieces total", "distribute"]
                hint3_keywords = ["Total", "number of children", "pieces per child", "at least"]
                
                hint1_valid = any(keyword.lower() in hints_en[0].lower() for keyword in hint1_keywords)
                hint2_valid = any(keyword.lower() in hints_en[1].lower() for keyword in hint2_keywords)
                hint3_valid = any(keyword.lower() in hints_en[2].lower() for keyword in hint3_keywords)
                
                if hint1_valid and hint2_valid and hint3_valid:
                    self.log_test("examprep2 Socratic Progression", True, 
                                f"✅ Progressive Socratic guidance verified: Variable/children → Total calc → 'At least' meaning")
                else:
                    self.log_test("examprep2 Socratic Progression", False, 
                                f"❌ Socratic progression incomplete. Hint1: {hint1_valid}, Hint2: {hint2_valid}, Hint3: {hint3_valid}")
                    return False
                
                # Verify bilingual support
                arabic_keywords_present = any("ح" in hint or "طفل" in hint or "قطعة" in hint for hint in hints_ar)
                if arabic_keywords_present:
                    self.log_test("examprep2 Bilingual Support", True, 
                                f"✅ Arabic hints properly implemented with mathematical terms")
                else:
                    self.log_test("examprep2 Bilingual Support", False, 
                                f"❌ Arabic hints missing proper mathematical terminology")
                    return False
                
                return True
                
            else:
                self.log_test("examprep2 Database Access", False, 
                            f"Failed to fetch examprep2: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("examprep2 Database Verification", False, f"Test execution error: {str(e)}")
            return False

    def test_hint_content_detailed_analysis(self):
        """Detailed analysis of hint content to ensure pedagogical correctness"""
        try:
            print("\n🔍 DETAILED HINT CONTENT ANALYSIS")
            print("Analyzing hint content for pedagogical correctness and Socratic method compliance")
            
            # Get both problems (examprep2 should be accessible after completing prerequisites)
            practice2_2_response = self.session.get(f"{self.base_url}/problems/practice2_2?username={self.test_student_username}")
            examprep2_response = self.session.get(f"{self.base_url}/problems/examprep2?username={self.test_student_username}")
            
            if practice2_2_response.status_code == 200 and examprep2_response.status_code == 200:
                practice2_2_data = practice2_2_response.json()
                examprep2_data = examprep2_response.json()
                
                # Analyze practice2_2 hints in detail
                practice2_2_hints = practice2_2_data.get("hints_en", [])
                print(f"\n📝 PRACTICE2_2 HINT ANALYSIS:")
                for i, hint in enumerate(practice2_2_hints, 1):
                    print(f"   Hint {i}: {hint}")
                    
                    # Check for pedagogical violations
                    violations = []
                    if "10t ≥ 500" in hint or "10t >= 500" in hint:
                        violations.append("Shows direct inequality")
                    if "t ≥ 50" in hint or "t >= 50" in hint:
                        violations.append("Shows final answer")
                    if "50" in hint and i < 3:  # Final answer shouldn't appear in first 2 hints
                        violations.append("Reveals answer too early")
                    
                    if violations:
                        self.log_test(f"practice2_2 Hint {i} Pedagogical Check", False, 
                                    f"❌ Violations: {', '.join(violations)}")
                        return False
                    else:
                        self.log_test(f"practice2_2 Hint {i} Pedagogical Check", True, 
                                    f"✅ Follows Socratic method")
                
                # Analyze examprep2 hints in detail
                examprep2_hints = examprep2_data.get("hints_en", [])
                print(f"\n📝 EXAMPREP2 HINT ANALYSIS:")
                for i, hint in enumerate(examprep2_hints, 1):
                    print(f"   Hint {i}: {hint}")
                    
                    # Check for pedagogical violations
                    violations = []
                    if "15p ≥ 60" in hint or "15p >= 60" in hint:
                        violations.append("Shows direct inequality")
                    if "p ≥ 4" in hint or "p >= 4" in hint:
                        violations.append("Shows final answer")
                    if "4" in hint and i < 3:  # Final answer shouldn't appear in first 2 hints
                        violations.append("Reveals answer too early")
                    
                    if violations:
                        self.log_test(f"examprep2 Hint {i} Pedagogical Check", False, 
                                    f"❌ Violations: {', '.join(violations)}")
                        return False
                    else:
                        self.log_test(f"examprep2 Hint {i} Pedagogical Check", True, 
                                    f"✅ Follows Socratic method")
                
                return True
                
            else:
                self.log_test("Hint Content Analysis", False, 
                            f"Failed to fetch problems for analysis")
                return False
                
        except Exception as e:
            self.log_test("Hint Content Analysis", False, f"Test execution error: {str(e)}")
            return False

    def test_bilingual_hint_consistency(self):
        """Test bilingual hint consistency between English and Arabic"""
        try:
            print("\n🌐 BILINGUAL HINT CONSISTENCY TESTING")
            print("Verifying English and Arabic hints convey the same pedagogical guidance")
            
            # Get both problems (examprep2 should be accessible after completing prerequisites)
            practice2_2_response = self.session.get(f"{self.base_url}/problems/practice2_2?username={self.test_student_username}")
            examprep2_response = self.session.get(f"{self.base_url}/problems/examprep2?username={self.test_student_username}")
            
            if practice2_2_response.status_code == 200 and examprep2_response.status_code == 200:
                practice2_2_data = practice2_2_response.json()
                examprep2_data = examprep2_response.json()
                
                # Check practice2_2 bilingual consistency
                practice2_2_hints_en = practice2_2_data.get("hints_en", [])
                practice2_2_hints_ar = practice2_2_data.get("hints_ar", [])
                
                if len(practice2_2_hints_en) == len(practice2_2_hints_ar):
                    self.log_test("practice2_2 Bilingual Count Match", True, 
                                f"✅ English and Arabic hint counts match: {len(practice2_2_hints_en)}")
                else:
                    self.log_test("practice2_2 Bilingual Count Match", False, 
                                f"❌ Hint count mismatch: {len(practice2_2_hints_en)} EN vs {len(practice2_2_hints_ar)} AR")
                    return False
                
                # Check examprep2 bilingual consistency
                examprep2_hints_en = examprep2_data.get("hints_en", [])
                examprep2_hints_ar = examprep2_data.get("hints_ar", [])
                
                if len(examprep2_hints_en) == len(examprep2_hints_ar):
                    self.log_test("examprep2 Bilingual Count Match", True, 
                                f"✅ English and Arabic hint counts match: {len(examprep2_hints_en)}")
                else:
                    self.log_test("examprep2 Bilingual Count Match", False, 
                                f"❌ Hint count mismatch: {len(examprep2_hints_en)} EN vs {len(examprep2_hints_ar)} AR")
                    return False
                
                # Verify Arabic hints contain appropriate mathematical terminology
                arabic_math_terms = ["ت", "ح", "ريال", "قطعة", "طفل", "تذكرة", "≥", "على الأقل"]
                
                practice2_2_arabic_valid = any(term in " ".join(practice2_2_hints_ar) for term in arabic_math_terms[:4])
                examprep2_arabic_valid = any(term in " ".join(examprep2_hints_ar) for term in arabic_math_terms[1:])
                
                if practice2_2_arabic_valid and examprep2_arabic_valid:
                    self.log_test("Arabic Mathematical Terminology", True, 
                                f"✅ Arabic hints contain appropriate mathematical terms")
                else:
                    self.log_test("Arabic Mathematical Terminology", False, 
                                f"❌ Arabic hints missing mathematical terminology")
                    return False
                
                return True
                
            else:
                self.log_test("Bilingual Consistency Test", False, 
                            f"Failed to fetch problems for bilingual testing")
                return False
                
        except Exception as e:
            self.log_test("Bilingual Consistency Test", False, f"Test execution error: {str(e)}")
            return False

    def generate_section2_hints_summary(self, results, critical_failures):
        """Generate comprehensive summary of Section 2 hints testing"""
        print("\n" + "=" * 80)
        print("🎯 SECTION 2 WORD PROBLEM HINTS - SOCRATIC METHOD FIX TESTING SUMMARY")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n📈 OVERALL SECTION 2 HINTS TEST RESULTS:")
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
            print(f"\n⚠️  EDUCATIONAL RISK: Students are seeing direct answers instead of guided discovery!")
            print(f"   🔧 IMMEDIATE ACTION REQUIRED: Fix Socratic method implementation")
        else:
            print(f"\n🎉 NO CRITICAL PEDAGOGICAL ISSUES DETECTED")
        
        print(f"\n📋 SECTION 2 HINTS STATUS:")
        if failed_tests == 0:
            print("   🎯 ALL SECTION 2 HINTS TESTS PASSED")
            print("   ✅ practice2_2 (ticket sales) hints follow Socratic method")
            print("   ✅ examprep2 (candy distribution) hints follow Socratic method")
            print("   ✅ No direct inequalities (10t ≥ 500, 15p ≥ 60) shown in hints")
            print("   ✅ Progressive guidance: Variable ID → Math relationship → Symbol meaning")
            print("   ✅ Bilingual support (English/Arabic) properly implemented")
            print("   ✅ Problem content integrity maintained")
            print("   🛡️  PEDAGOGICAL INTEGRITY: PROTECTED")
        else:
            print("   ⚠️  SECTION 2 HINTS ISSUES DETECTED")
            print("   🔧 Socratic method implementation needs fixes")
            print("   🚨 STUDENT LEARNING: COMPROMISED")
        
        print("\n" + "=" * 80)

    def run_section2_hints_tests(self):
        """Run comprehensive Section 2 word problem hints tests"""
        print("=" * 80)
        print("🎯 SECTION 2 WORD PROBLEM HINTS - SOCRATIC METHOD FIX TESTING")
        print("=" * 80)
        print("Testing critical pedagogical bug fix: hints must guide thinking, not show direct answers")
        
        # Test categories for Section 2 hints
        test_categories = [
            ("Health Check", self.test_health_check, "critical"),
            ("Test Student Creation", self.create_test_student, "critical"),
            ("practice2_2 Database Verification", self.test_practice2_2_database_verification, "critical"),
            ("examprep2 Database Verification", self.test_examprep2_database_verification, "critical"),
            ("Hint Content Detailed Analysis", self.test_hint_content_detailed_analysis, "critical"),
            ("Bilingual Hint Consistency", self.test_bilingual_hint_consistency, "high")
        ]
        
        results = {}
        critical_failures = []
        
        for category_name, test_method, priority in test_categories:
            print(f"\n🔍 SECTION 2 HINTS TEST CATEGORY: {category_name} (Priority: {priority.upper()})")
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
        
        # Generate comprehensive Section 2 hints summary
        self.generate_section2_hints_summary(results, critical_failures)
        
        return results

def main():
    """Main function to run Section 2 hints tests"""
    print("🚀 Starting SECTION 2 WORD PROBLEM HINTS - SOCRATIC METHOD FIX Testing...")
    print("🎯 Goal: Verify hints guide thinking process without showing direct inequalities")
    
    tester = Section2HintsTester(BACKEND_URL)
    results = tester.run_section2_hints_tests()
    
    # Exit with appropriate code
    failed_tests = sum(1 for success in results.values() if not success)
    
    if failed_tests > 0:
        print(f"\n🚨 SECTION 2 HINTS ALERT: {failed_tests} test(s) failed!")
        print("🔧 Socratic method implementation needs fixes to prevent showing direct answers")
    else:
        print(f"\n🛡️  SECTION 2 HINTS CONFIRMED: All pedagogical tests passed!")
        print("✅ Word problem hints properly guide student discovery without revealing answers")
    
    sys.exit(failed_tests)

if __name__ == "__main__":
    main()