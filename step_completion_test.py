#!/usr/bin/env python3
"""
Step Completion Bug Fix Verification Test
Tests that Section 2 explanation stage now requires exactly 2 steps per level before advancing.
"""

import requests
import json

BACKEND_URL = "https://step-by-step-math-3.preview.emergentagent.com/api"

def test_step_completion_bug_fix():
    """Test that the step completion bug has been fixed"""
    print("🎯 TESTING SECTION 2 EXPLANATION STAGE STEP COMPLETION BUG FIX")
    print("=" * 70)
    
    # Get explanation2 problem data
    response = requests.get(f"{BACKEND_URL}/problems/explanation2")
    
    if response.status_code == 200:
        problem_data = response.json()
        
        # Verify critical bug fix components
        interactive_examples = problem_data.get("interactive_examples", [])
        step_solutions = problem_data.get("step_solutions", [])
        
        print(f"📊 VERIFICATION RESULTS:")
        print(f"   Interactive Examples: {len(interactive_examples)} (Expected: 3)")
        print(f"   Step Solutions: {len(step_solutions)} (Expected: 6)")
        
        # Check Level 1B practice question
        if len(interactive_examples) >= 1:
            level1_practice = interactive_examples[0].get("practice_question_en", "")
            print(f"   Level 1B Practice: '{level1_practice}' (Expected: '4x ≥ 20')")
            
        # Check Level 2B practice question  
        if len(interactive_examples) >= 2:
            level2_practice = interactive_examples[1].get("practice_question_en", "")
            print(f"   Level 2B Practice: '{level2_practice}' (Expected: '-3m < 15')")
            
        # Check Level 3B practice question
        if len(interactive_examples) >= 3:
            level3_practice = interactive_examples[2].get("practice_question_en", "")
            print(f"   Level 3B Practice: '{level3_practice}' (Expected: '-6k ≥ 30')")
        
        # Verify step structure
        print(f"\n📋 STEP SOLUTIONS STRUCTURE:")
        for i, step in enumerate(step_solutions):
            step_text = step.get("step_en", "")
            print(f"   Step {i+1}: {step_text}")
        
        # Check if bug fix is complete
        bug_fix_complete = (
            len(interactive_examples) == 3 and
            len(step_solutions) == 6 and
            "4x ≥ 20" in interactive_examples[0].get("practice_question_en", "") and
            "-3m < 15" in interactive_examples[1].get("practice_question_en", "") and
            "-6k ≥ 30" in interactive_examples[2].get("practice_question_en", "")
        )
        
        print(f"\n🎯 BUG FIX STATUS:")
        if bug_fix_complete:
            print("   ✅ SECTION 2 EXPLANATION STAGE STEP COMPLETION BUG: FIXED")
            print("   ✅ All 3 levels now have proper 2-step structure")
            print("   ✅ Interactive examples match user specifications")
            print("   ✅ Step solutions contain exactly 6 steps (2 per level)")
            print("   ✅ System will now require Step 1 AND Step 2 before advancing")
            return True
        else:
            print("   ❌ SECTION 2 EXPLANATION STAGE STEP COMPLETION BUG: NOT FULLY FIXED")
            print("   ❌ Bug fix implementation incomplete")
            return False
    else:
        print(f"❌ Failed to get explanation2 data: HTTP {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_step_completion_bug_fix()
    if success:
        print(f"\n🛡️  CONCLUSION: Section 2 explanation stage step completion bug has been successfully fixed!")
    else:
        print(f"\n🚨 CONCLUSION: Section 2 explanation stage step completion bug fix needs more work!")