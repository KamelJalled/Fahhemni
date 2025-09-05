#!/bin/bash

# Math Tutoring App - GitHub Setup Script
# This script helps you push all code files to GitHub

echo "📚 Math Tutoring App - GitHub Repository Setup"
echo "=============================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    
    # Create .gitignore
    cat > .gitignore << EOL
# Dependencies
node_modules/
frontend/node_modules/
backend/__pycache__/
backend/*.pyc
backend/.pytest_cache/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
frontend/.env
backend/.env

# Build outputs
frontend/build/
frontend/dist/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing
coverage/
.nyc_output/

# Temporary files
*.tmp
*.temp

# Python virtual environment
backend/venv/
backend/env/

# Keep important files
!vercel.json
!frontend/package.json
!backend/requirements.txt
!backend/requirements-vercel.txt
EOL
    
    echo "✅ Git repository initialized"
fi

# Check current status
echo ""
echo "📋 Current file structure:"
find . -type f -name "*.js" -o -name "*.py" -o -name "*.json" -o -name "*.md" | head -20

echo ""
echo "🔍 Checking for required files..."

# Required files checklist
required_files=(
    "frontend/src/App.js"
    "frontend/src/components/Dashboard.js"
    "frontend/src/components/ProblemView.js"
    "frontend/src/components/StudentLogin.js"
    "frontend/src/components/TeacherLogin.js"
    "frontend/src/components/TeacherDashboard.js"
    "frontend/package.json"
    "backend/server.py"
    "backend/models.py"
    "backend/database.py"
    "backend/utils.py"
    "backend/requirements.txt"
    "vercel.json"
    "DEPLOYMENT.md"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Some required files are missing. Please ensure all files are present before pushing to GitHub."
    exit 1
fi

echo ""
echo "✅ All required files are present!"

# Add all files to git
echo ""
echo "📁 Adding files to Git..."
git add .

# Check git status
echo ""
echo "📊 Git Status:"
git status --short

# Prompt for commit message
echo ""
read -p "Enter commit message (default: 'Initial commit - Math Tutoring App'): " commit_message
commit_message=${commit_message:-"Initial commit - Math Tutoring App"}

# Commit files
echo ""
echo "💾 Committing files..."
git commit -m "$commit_message"

# Check if remote origin exists
if git remote get-url origin &> /dev/null; then
    echo "✅ Remote origin already configured"
    remote_url=$(git remote get-url origin)
    echo "📍 Remote URL: $remote_url"
else
    echo ""
    echo "🔗 Setting up GitHub remote..."
    echo ""
    echo "Please create a new repository on GitHub first:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: math-tutoring-app"
    echo "3. Description: Interactive Math Tutoring App for Grade 9 Saudi Students"
    echo "4. Make it Public (for easier deployment)"
    echo "5. Don't initialize with README (we already have files)"
    echo "6. Create repository"
    echo ""
    
    read -p "Enter your GitHub repository URL (e.g., https://github.com/username/math-tutoring-app.git): " repo_url
    
    if [ -n "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote origin added: $repo_url"
    else
        echo "⚠️  No repository URL provided. You can add it later with:"
        echo "git remote add origin https://github.com/username/math-tutoring-app.git"
    fi
fi

# Push to GitHub
echo ""
read -p "Push to GitHub now? (y/n): " push_now

if [[ $push_now =~ ^[Yy]$ ]]; then
    echo "🚀 Pushing to GitHub..."
    
    # Get current branch name
    current_branch=$(git branch --show-current)
    
    if [ -z "$current_branch" ]; then
        current_branch="main"
        echo "📝 Creating main branch..."
        git checkout -b main
    fi
    
    # Push to remote
    if git push -u origin "$current_branch"; then
        echo ""
        echo "🎉 Successfully pushed to GitHub!"
        echo ""
        echo "📍 Your repository is now available at:"
        if git remote get-url origin &> /dev/null; then
            repo_url=$(git remote get-url origin)
            # Convert SSH to HTTPS URL for display
            if [[ $repo_url == git@github.com:* ]]; then
                repo_url=$(echo $repo_url | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')
            fi
            echo "🌐 $repo_url"
        fi
        echo ""
        echo "🚀 Next Steps:"
        echo "1. Verify all files are visible on GitHub"
        echo "2. Set up MongoDB Atlas (see DEPLOYMENT.md)"
        echo "3. Deploy to Vercel using the GitHub repository"
        echo "4. Configure environment variables in Vercel"
        echo ""
        echo "📖 Full deployment guide: DEPLOYMENT.md"
    else
        echo "❌ Failed to push to GitHub. Please check:"
        echo "1. Repository URL is correct"
        echo "2. You have push permissions"
        echo "3. Authentication is set up (GitHub token/SSH key)"
    fi
else
    echo ""
    echo "📝 Files are committed locally. To push later, run:"
    echo "git push -u origin main"
fi

echo ""
echo "✅ GitHub setup completed!"
echo ""
echo "📊 Repository Statistics:"
echo "- Total commits: $(git rev-list --count HEAD 2>/dev/null || echo '1')"
echo "- Files tracked: $(git ls-files | wc -l)"
echo "- Current branch: $(git branch --show-current || echo 'main')"
echo ""
echo "Happy coding! 🚀📚✨"