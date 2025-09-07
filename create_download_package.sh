#!/bin/bash

# Math Tutoring App - Create Download Package
echo "📦 Creating complete Math Tutoring App package..."

# Create temporary directory
mkdir -p /tmp/math-tutoring-app-export

# Copy essential files
echo "📋 Copying project files..."

# Frontend files
cp -r frontend/src /tmp/math-tutoring-app-export/frontend/
cp -r frontend/public /tmp/math-tutoring-app-export/frontend/
cp -r frontend/build /tmp/math-tutoring-app-export/frontend/
cp frontend/package.json /tmp/math-tutoring-app-export/frontend/
cp frontend/tailwind.config.js /tmp/math-tutoring-app-export/frontend/
cp frontend/.env.example /tmp/math-tutoring-app-export/frontend/

# Backend files  
mkdir -p /tmp/math-tutoring-app-export/backend
cp backend/*.py /tmp/math-tutoring-app-export/backend/
cp backend/requirements.txt /tmp/math-tutoring-app-export/backend/
cp backend/.env.example /tmp/math-tutoring-app-export/backend/

# Documentation
cp *.md /tmp/math-tutoring-app-export/
cp .gitignore /tmp/math-tutoring-app-export/

# Root files
cp package.json /tmp/math-tutoring-app-export/ 2>/dev/null || echo "No root package.json"

echo "✅ Files copied to: /tmp/math-tutoring-app-export"
echo "📊 Package contents:"
find /tmp/math-tutoring-app-export -type f | wc -l
echo " files ready for download"

echo ""
echo "🎯 To get your files:"
echo "1. The complete project is in: /tmp/math-tutoring-app-export"
echo "2. You can zip it: cd /tmp && zip -r math-tutoring-app.zip math-tutoring-app-export"
echo "3. Or copy files individually using the paths in FILE_LIST_COMPLETE.md"
echo ""
echo "🚀 Ready for GitHub push!"