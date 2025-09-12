#!/usr/bin/env python3
"""
Test script for the new DELETE /api/admin/clear-all-data endpoint
As requested in the review request
"""

import requests
import json
import sys
from datetime import datetime

# Use backend URL from frontend/.env
BACKEND_URL = "https://math-tutor-app.preview.emergentagent.com/api"

def test_clear_all_data_endpoint():
    """Test the new DELETE /api/admin/clear-all-data endpoint"""
    print("🔍 TESTING NEW ADMIN CLEAR-ALL-DATA ENDPOINT")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print("Testing DELETE /api/admin/clear-all-data endpoint...")
    print()
    
    session = requests.Session()
    
    try:
        # Step 1: Create some test data first to verify clearing works
        print("Step 1: Creating test data...")
        test_student = {"username": "clear_test_student", "class_name": "GR9-A"}
        
        response = session.post(
            f"{BACKEND_URL}/auth/student-login",
            json=test_student,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Created test student successfully")
        else:
            print(f"❌ Failed to create test student: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        # Step 2: Submit some progress to create progress records
        print("\nStep 2: Creating test progress...")
        attempt_data = {
            "problem_id": "prep1",
            "answer": "7",
            "hints_used": 0
        }
        
        response = session.post(
            f"{BACKEND_URL}/students/clear_test_student/attempt",
            json=attempt_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Created test progress record successfully")
        else:
            print(f"⚠️  Failed to create progress: HTTP {response.status_code}")
            print("Continuing anyway - we still have student data to clear")
        
        # Step 3: Check initial data count
        print("\nStep 3: Checking initial data count...")
        response = session.get(f"{BACKEND_URL}/admin/stats")
        
        if response.status_code == 200:
            stats = response.json()
            initial_students = stats.get("total_students", 0)
            initial_progress = stats.get("total_progress_records", 0)
            print(f"Initial data: {initial_students} students, {initial_progress} progress records")
        else:
            print(f"❌ Failed to get initial stats: HTTP {response.status_code}")
            return False
        
        # Step 4: Test the new DELETE /api/admin/clear-all-data endpoint
        print("\nStep 4: Testing DELETE /api/admin/clear-all-data endpoint...")
        response = session.delete(f"{BACKEND_URL}/admin/clear-all-data")
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response Data: {data}")
                
                # Check for success message
                if "message" in data and "cleared" in data["message"].lower():
                    print("✅ Status 200 response with success message")
                    delete_success = True
                else:
                    print(f"❌ Missing or invalid success message: {data}")
                    delete_success = False
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON response: {response.text}")
                delete_success = False
        else:
            print(f"❌ Expected status 200, got {response.status_code}")
            print(f"Response: {response.text}")
            delete_success = False
        
        # Step 5: Verify data is actually cleared
        print("\nStep 5: Verifying data is cleared...")
        response = session.get(f"{BACKEND_URL}/admin/stats")
        
        if response.status_code == 200:
            stats = response.json()
            final_students = stats.get("total_students", -1)
            final_progress = stats.get("total_progress_records", -1)
            
            print(f"Final data: {final_students} students, {final_progress} progress records")
            
            if final_students == 0 and final_progress == 0:
                print("✅ Database collections emptied successfully")
                verification_success = True
            else:
                print(f"❌ Data not fully cleared - {final_students} students, {final_progress} progress records remain")
                verification_success = False
        else:
            print(f"❌ Failed to verify clearing: HTTP {response.status_code}")
            verification_success = False
        
        # Final result
        overall_success = delete_success and verification_success
        
        print("\n" + "=" * 60)
        print("TEST RESULTS")
        print("=" * 60)
        
        if overall_success:
            print("🎉 SUCCESS: DELETE /api/admin/clear-all-data endpoint working correctly!")
            print("✅ Status 200 response")
            print("✅ Success message confirmed")
            print("✅ Database collections emptied")
        else:
            print("❌ FAILURE: Clear-all-data endpoint has issues")
            if not delete_success:
                print("❌ DELETE request failed or returned invalid response")
            if not verification_success:
                print("❌ Data was not properly cleared from database")
        
        return overall_success
        
    except Exception as e:
        print(f"❌ Test execution error: {str(e)}")
        return False

def main():
    """Main test execution"""
    success = test_clear_all_data_endpoint()
    
    # Save results
    result = {
        "test_name": "Admin Clear All Data Endpoint",
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "backend_url": BACKEND_URL
    }
    
    with open("/app/clear_data_test_result.json", "w") as f:
        json.dump(result, f, indent=2)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()