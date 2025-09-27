import pymongo
from pymongo import MongoClient
from bson import ObjectId
import sys

# IMPORTANT: Add your MongoDB connection string here
MONGO_URI = "mongodb+srv://@cluster0.dip2jyt.mongodb.net/mathtutor?retryWrites=true&w=majority&appName=Cluster0"

def fix_corrupted_students():
    """Fix students like Somayya whose accounts are corrupted"""
    
    try:
        client = MongoClient(MONGO_URI)
        db = client.mathtutor  # or mathtutor - check your database name
        
        print("Connected to MongoDB!")
        print("-" * 50)
        
        # Find all progress records
        all_progress = list(db.progress.find({}))
        
        print(f"Found {len(all_progress)} progress records")
        
        # Group by student
        students_progress = {}
        for record in all_progress:
            username = record.get('student_username', 'unknown')
            if username not in students_progress:
                students_progress[username] = []
            students_progress[username].append(record)
        
        # Check each student
        for username, progress_records in students_progress.items():
            print(f"\nChecking {username}...")
            
            # Look for corruption patterns
            has_examprep1 = any(p['problem_id'] == 'examprep1' and p.get('completed', False) 
                               for p in progress_records)
            has_prep2 = any(p['problem_id'] == 'prep2' for p in progress_records)
            
            # Count section 1 and section 2 problems
            section1_problems = [p for p in progress_records if p.get('section_id') == 'section1']
            section2_problems = [p for p in progress_records if p.get('section_id') == 'section2']
            
            print(f"  - Has completed examprep1: {has_examprep1}")
            print(f"  - Has prep2: {has_prep2}")
            print(f"  - Section 1 problems: {len(section1_problems)}")
            print(f"  - Section 2 problems: {len(section2_problems)}")
            
            # Fix corruption
            if has_examprep1 and not has_prep2:
                print(f"  ⚠️ {username} completed Section 1 but no Section 2 prep - FIXING...")
                
                # Create prep2 entry
                db.progress.insert_one({
                    "student_username": username,
                    "section_id": "section2",
                    "problem_id": "prep2",
                    "completed": False,
                    "score": 0,
                    "attempts": 0,
                    "hints_used": 0
                })
                print(f"  ✅ Added prep2 for {username}")
            
            # Check for wrong section assignment
            for record in progress_records:
                problem_id = record.get('problem_id', '')
                section_id = record.get('section_id', '')
                
                # Fix prep2 in wrong section
                if problem_id == 'prep2' and section_id == 'section1':
                    print(f"  ⚠️ Found prep2 in section1 - FIXING...")
                    db.progress.update_one(
                        {'_id': record['_id']},
                        {'$set': {'section_id': 'section2'}}
                    )
                    print(f"  ✅ Moved prep2 to section2")
        
        print("\n" + "=" * 50)
        print("✅ FIX COMPLETED!")
        print("=" * 50)
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPlease check:")
        print("1. Your MongoDB connection string")
        print("2. Your database name (mathtutor)")

if __name__ == "__main__":
    print("FAHHEMNI STUDENT DATA FIX")
    print("=" * 50)
    
    response = input("This will fix corrupted student data. Continue? (yes/no): ")
    if response.lower() == 'yes':
        fix_corrupted_students()
    else:
        print("Cancelled.")