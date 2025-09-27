# Database Problem ID Fix Script
# Run this to update practice naming in your database

import pymongo
from pymongo import MongoClient

# Replace with your actual MongoDB connection string
MONGO_URI = "mongodb+srv://kamalaljallad_db_user:K6G2BOpZkiq2qRUE@cluster0.dip2jyt.mongodb.net/mathtutor?retryWrites=true&w=majority&appName=Cluster0"

def fix_problem_naming():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client.mathtutor  # Replace with your database name
        problems_collection = db.problems
        
        print("🔧 Starting problem ID migration...")
        
        # Fix Section 1: practice1 -> practice1_1, practice2 -> practice1_2
        
        # Update practice1 to practice1_1
        result1 = problems_collection.update_one(
            {"id": "practice1", "section_id": "section1"},
            {"$set": {"id": "practice1_1"}}
        )
        print(f"✅ Updated practice1 -> practice1_1: {result1.modified_count} documents")
        
        # Update practice2 to practice1_2  
        result2 = problems_collection.update_one(
            {"id": "practice2", "section_id": "section1"},
            {"$set": {"id": "practice1_2"}}
        )
        print(f"✅ Updated practice2 -> practice1_2: {result2.modified_count} documents")
        
        # Also fix any progress tracking that might reference old IDs
        progress_collection = db.student_progress
        
        # This would need to be done for each student, but for now just log
        print("⚠️  Note: You may also need to update student progress records")
        print("⚠️  that reference 'practice1' and 'practice2' to use new naming")
        
        print("🎉 Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    fix_problem_naming()