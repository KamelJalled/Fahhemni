#!/bin/bash

# Math Tutoring App - Quick Deployment Script
# This script prepares your project for Vercel deployment

echo "🚀 Preparing Math Tutoring App for Vercel Deployment..."

# Check if required files exist
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found!"
    exit 1
fi

if [ ! -d "frontend" ]; then
    echo "❌ frontend directory not found!"
    exit 1
fi

if [ ! -d "backend" ]; then
    echo "❌ backend directory not found!"
    exit 1
fi

echo "✅ Project structure verified"

# Install Vercel CLI if not present
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if user is logged in to Vercel
echo "🔐 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "Please log in to Vercel:"
    vercel login
fi

# Set up environment variables
echo "🔧 Setting up environment variables..."
echo ""
echo "Please provide the following information:"
echo ""

read -p "Enter your MongoDB Atlas connection string: " MONGO_URL
read -p "Enter your database name (default: mathtutor): " DB_NAME
DB_NAME=${DB_NAME:-mathtutor}

# Set environment variables in Vercel
echo "📝 Setting environment variables in Vercel..."
vercel env add MONGO_URL production <<< "$MONGO_URL"
vercel env add DB_NAME production <<< "$DB_NAME"

# Get Vercel project URL
echo "🌐 Getting project URL..."
PROJECT_URL=$(vercel inspect --scope=production | grep -o 'https://[^"]*')

if [ -z "$PROJECT_URL" ]; then
    echo "⚠️  Could not auto-detect project URL. You'll need to set REACT_APP_BACKEND_URL manually."
    read -p "Enter your Vercel project URL (e.g., https://your-app.vercel.app): " PROJECT_URL
fi

# Set backend URL for frontend
vercel env add REACT_APP_BACKEND_URL production <<< "$PROJECT_URL"

echo "✅ Environment variables configured"

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "Your Math Tutoring App is now live at:"
echo "🌐 $PROJECT_URL"
echo ""
echo "📊 Teacher Dashboard Access Code: teacher2024"
echo ""
echo "Next steps:"
echo "1. Test your application at the URL above"
echo "2. Check Vercel dashboard for any issues"
echo "3. Monitor MongoDB Atlas for database connections"
echo ""
echo "Happy teaching! 🇸🇦📚✨"