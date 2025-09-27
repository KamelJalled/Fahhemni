import subprocess
import sys

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "motor", "pymongo", "python-dotenv"])

# Download and run the migration script from Emergent
import requests

# Get the migration script content
migration_url = "https://raw.githubusercontent.com/your-repo/complete_database_migration.py"  

# For now, let's check if problems exist
from pymongo import MongoClient

MONGO_URI = "your_mongodb_connection_string"  # Add your connection string

client = MongoClient(MONGO_URI)
db = client.mathtutor

# Check if problems exist
problems_count = db.problems.count_documents({})
sections_count = db.sections.count_documents({})

print(f"Problems in database: {problems_count}")
print(f"Sections in database: {sections_count}")

if problems_count == 0:
    print("\n⚠️ NO PROBLEMS IN DATABASE!")
    print("You need to run the complete_database_migration.py script from Emergent")
    print("This script will populate all problems and sections")
else:
    # List all problems
    problems = list(db.problems.find({}, {"id": 1, "section_id": 1}))
    for p in problems:
        print(f"  - {p['section_id']}: {p['id']}")

client.close()