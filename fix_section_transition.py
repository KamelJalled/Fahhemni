import pymongo
from pymongo import MongoClient
from datetime import datetime

# IMPORTANT: Replace with your MongoDB connection string
MONGO_URI = "your_mongodb_connection_string_here"

def fix_database_issues():
    """Fix the database corruption issues after Section 1 completion"""
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client.mathtutor
        
        print("Connected to MongoDB successfully!")
        print("-" * 50)
        
        # Step 1: Check for corrupted student accounts
        print("Step 1: Checking for corrupted student accounts...")
        
        students = db.students.find({})
        corrupted_count = 0
        
        for student in students:
            username = student.get('username', 'Unknown')
            progress = db.student_progress.find_one({'student_id': student['_id']})
            
            if progress:
                # Check if the progress data has any malformed entries
                progress_data = progress.get('progress', {})
                
                # Look for the specific corruption pattern
                if 'section1' in progress_data:
                    section1_data = progress_data['section1']
                    
                    # Check if examprep1 is completed but prep2 doesn't exist
                    if 'examprep1' in section1_data and section1_data['examprep1'].get('status') == 'complete':
                        if 'prep2' in section1_data or 'section2' not in progress_data:
                            print(f"  ⚠️  Found corrupted account: {username}")
                            corrupted_count += 1
                            
                            # Fix the corruption
                            if 'prep2' in section1_data:
                                # Remove the incorrect prep2 from section1
                                del progress_data['section1']['prep2']
                            
                            # Ensure section2 structure exists
                            if 'section2' not in progress_data:
                                progress_data['section2'] = {
                                    'prep2': {
                                        'status': 'not_started',
                                        'completed': False,
                                        'score': 0,
                                        'attempts': 0,
                                        'last_attempt': None
                                    }
                                }
                            
                            # Update the database
                            db.student_progress.update_one(
                                {'_id': progress['_id']},
                                {'$set': {'progress': progress_data}}
                            )
                            print(f"  ✅ Fixed corruption for: {username}")
        
        print(f"\nTotal corrupted accounts found: {corrupted_count}")
        print(f"All corrupted accounts have been fixed!")
        
        print("-" * 50)
        
        # Step 2: Fix the problem ID naming inconsistencies
        print("\nStep 2: Fixing problem ID naming inconsistencies...")
        
        # Fix duplicate practice2 IDs
        problems_to_fix = [
            {'section_id': 'section1', 'old_id': 'practice2', 'new_id': 'practice1_2'},
            {'section_id': 'section2', 'old_id': 'practice2', 'new_id': 'practice2_2'},
            {'section_id': 'section3', 'old_id': 'practice2', 'new_id': 'practice3_2'},
            {'section_id': 'section4', 'old_id': 'practice2', 'new_id': 'practice4_2'},
            {'section_id': 'section5', 'old_id': 'practice2', 'new_id': 'practice5_2'}
        ]
        
        for fix in problems_to_fix:
            result = db.problems.update_one(
                {'section_id': fix['section_id'], 'id': fix['old_id']},
                {'$set': {'id': fix['new_id']}}
            )
            if result.modified_count > 0:
                print(f"  ✅ Fixed: {fix['section_id']} - {fix['old_id']} → {fix['new_id']}")
        
        print("\nProblem ID naming has been standardized!")
        
        print("-" * 50)
        
        # Step 3: Add transition handler for section completions
        print("\nStep 3: Adding section transition metadata...")
        
        # Add metadata to track section transitions properly
        sections = ['section1', 'section2', 'section3', 'section4', 'section5']
        
        for i, section in enumerate(sections):
            next_section = sections[i + 1] if i < len(sections) - 1 else None
            
            db.sections.update_one(
                {'id': section},
                {
                    '$set': {
                        'next_section': next_section,
                        'completion_stage': f'examprep{i + 1}',
                        'first_stage_next': f'prep{i + 2}' if next_section else None
                    }
                },
                upsert=True
            )
            print(f"  ✅ Updated transition metadata for {section}")
        
        print("\nSection transition metadata has been added!")
        
        print("-" * 50)
        
        # Step 4: Create indexes for better performance
        print("\nStep 4: Creating database indexes for performance...")
        
        # Create indexes
        db.students.create_index('username', unique=True)
        db.student_progress.create_index('student_id')
        db.problems.create_index([('section_id', 1), ('id', 1)])
        db.sections.create_index('id', unique=True)
        
        print("  ✅ Indexes created successfully!")
        
        print("-" * 50)
        print("\n🎉 DATABASE FIX COMPLETED SUCCESSFULLY!")
        print("\nNext steps:")
        print("1. Test with Somayya's account - it should now work")
        print("2. Create a fresh test account to verify the fix")
        print("3. Monitor the transition from Section 1 to Section 2")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        print("\nPlease check:")
        print("1. Your MongoDB connection string is correct")
        print("2. Your database name is 'mathtutor'")
        print("3. You have network connection to MongoDB Atlas")
        return False

def reset_specific_student(username):
    """Reset a specific student's progress - use this if needed"""
    try:
        client = MongoClient(MONGO_URI)
        db = client.mathtutor
        
        student = db.students.find_one({'username': username})
        if student:
            # Delete their progress
            db.student_progress.delete_one({'student_id': student['_id']})
            print(f"✅ Reset progress for student: {username}")
            
            # Create fresh progress entry
            db.student_progress.insert_one({
                'student_id': student['_id'],
                'progress': {},
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            })
            print(f"✅ Created fresh progress entry for: {username}")
        else:
            print(f"❌ Student not found: {username}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error resetting student: {str(e)}")

if __name__ == "__main__":
    print("=" * 50)
    print("FAHHEMNI DATABASE FIX SCRIPT")
    print("=" * 50)
    
    # Run the main fix
    fix_database_issues()
    
    # Uncomment this line if you need to reset a specific student
    # reset_specific_student("Somayya")