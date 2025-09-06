# 📚 Math Tutoring App - Interactive Algebra Tutor for Grade 9 Saudi Students

A comprehensive, bilingual (Arabic/English) math tutoring application designed specifically for Saudi Grade 9 students learning one-step inequalities. Built with React, FastAPI, and MongoDB.

**🚀 Ready for production deployment on any hosting platform!**

## 🌟 Features

### 📖 **Pedagogical Excellence**
- **Step-by-Step Problem Solving**: Multi-step answer validation with intermediate work acceptance
- **Progressive Hint System**: Hidden hints by default, revealed on-demand to promote independent thinking
- **Socratic Method**: 3-step guided hints that teach without giving away answers
- **Interactive Examples**: Hands-on practice after each explanation

### 🌍 **Bilingual Support**
- **Arabic/English Interface**: Complete RTL support for Arabic
- **Cultural Sensitivity**: Designed for Saudi educational context
- **Dual Numeral Systems**: Accepts both Western (0-9) and Eastern Arabic (٠-٩) numerals
- **Variable Recognition**: Accepts both "x" and "س" as variables

### 🎯 **Student-Centered Design**
- **Flexible Progression**: Students can attempt Assessment after completing just one Practice problem
- **Try Again Functionality**: Reset problems without losing progress
- **Multiple Solution Paths**: Accepts various equivalent intermediate steps
- **Gamification**: Points, badges, and progress tracking

### 👨‍🏫 **Teacher Dashboard**
- **Real-time Analytics**: Track student progress and performance
- **Detailed Insights**: See which path each student took
- **Weighted Scoring**: Comprehensive assessment system
- **Access Code**: Secure teacher access with code `teacher2024`

## 🏗️ **Technical Architecture**

### **Frontend** (React 19)
- Modern React with Hooks and Context
- Tailwind CSS with Shadcn/ui components  
- React Router for navigation
- Responsive design for all devices

### **Backend** (FastAPI + Python)
- RESTful API with automatic documentation
- MongoDB with Motor (async driver)
- Pydantic models for data validation
- CORS enabled for cross-origin requests

### **Database** (MongoDB)
- Student progress tracking
- Problem and section management
- Teacher analytics aggregation
- Scalable cloud deployment ready

## 🚀 **Quick Start**

### Prerequisites
- Node.js 18+
- Python 3.9+
- MongoDB (local or Atlas)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/math-tutoring-app.git
   cd math-tutoring-app
   ```

2. **Set up Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Create .env file
   echo "MONGO_URL=mongodb://localhost:27017" > .env
   echo "DB_NAME=mathtutor" >> .env
   
   # Start backend server
   uvicorn server:app --reload --port 8001
   ```

3. **Set up Frontend**
   ```bash
   cd frontend
   npm install
   
   # Create .env file
   echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env
   
   # Start frontend server
   npm start
   ```

4. **Visit the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - Teacher Dashboard: Use access code `teacher2024`

## 🌐 **Production Deployment**

This application can be deployed to any hosting platform! The frontend is built as static files, and the backend is a standard FastAPI application.

### Quick Deployment Options

**Frontend (Static Hosting):**
- Netlify, GitHub Pages, AWS S3, Firebase Hosting, Surge.sh
- Upload the contents of `frontend/build/` folder

**Backend (API Hosting):**
- Railway, Render, DigitalOcean, AWS, Google Cloud, Heroku
- Deploy the FastAPI application with MongoDB connection

**Complete Setup:**
1. Follow the comprehensive guide in [`DEPLOYMENT.md`](DEPLOYMENT.md)
2. Set up MongoDB database (Atlas recommended)
3. Configure environment variables
4. Deploy frontend and backend separately

### Environment Variables

**Production Required:**
```bash
# Backend
MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/mathtutor

# Frontend (rebuild required after change)
REACT_APP_BACKEND_URL=https://your-api-domain.com
```

## 📚 **Curriculum Structure**

### **Section 1: One-Step Inequalities**

1. **Preparation** (10% weight)
   - Review: x + 8 = 15
   - Multi-step validation
   - Final answer submission

2. **Explanation** (0% weight)
   - Addition/Subtraction: x + 7 > 10
   - Multiplication/Division: 3x ≤ 15
   - Negative Coefficients: -2x > 8
   - Interactive practice after each example

3. **Practice Problems** (15% each)
   - Practice 1: x - 3 ≤ 8
   - Practice 2: 4x < 20
   - Step-by-step validation
   - Hidden hint system

4. **Assessment** (30% weight)
   - 6x ≥ 18
   - No answer revelation
   - Flexible prerequisite (≥1 practice complete)

5. **Exam Preparation** (30% weight)
   - -2x > 8
   - Inequality sign flipping
   - Complete mastery demonstration

## 🎮 **Gamification System**

### **Badges**
- 🏆 **First Steps**: Complete your first problem
- ⭐ **Practice Master**: Complete all practice problems  
- 🏅 **Assessment Ace**: Score 80+ on assessment
- 👑 **Inequality Expert**: Complete entire section

### **Scoring System**
- Base score: 100 points
- Penalty: -20 points per additional attempt
- Penalty: -10 points per hint used
- Minimum score: 40 points (if correct)

## 🔧 **API Documentation**

### **Student Endpoints**
```bash
POST /api/auth/student-login     # Student authentication
GET  /api/students/{username}/progress  # Get progress
POST /api/students/{username}/attempt   # Submit attempt
```

### **Teacher Endpoints**
```bash
POST /api/auth/teacher-login     # Teacher authentication  
GET  /api/teacher/students       # Get all student analytics
```

### **Content Endpoints**
```bash
GET /api/problems/section/{id}   # Get section problems
GET /api/problems/{id}          # Get specific problem
```

## 🧪 **Testing**

### **Manual Testing Checklist**
- [ ] Student login with username
- [ ] Teacher login with access code `teacher2024`
- [ ] Multi-step problem solving in Preparation
- [ ] Hidden hints system in Practice
- [ ] Flexible progression to Assessment
- [ ] Arabic/English language switching
- [ ] Progress tracking and badge earning

### **Automated Testing** (Future Enhancement)
```bash
cd backend && python -m pytest
cd frontend && npm test
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- **Documentation**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub Discussions

## 📊 **Project Status**

✅ **Core Features Complete**
- Multi-step answer validation
- Hidden hints system  
- Bilingual interface
- Teacher dashboard
- Progress tracking
- Gamification

🚀 **Production Ready**
- Deployed on Vercel
- MongoDB Atlas integration
- Environment security
- Performance optimized

## 🎯 **Future Enhancements**

- [ ] Additional math topics (quadratic equations, systems)
- [ ] Student-to-student collaboration features
- [ ] Advanced analytics and reporting
- [ ] Mobile app development
- [ ] AI-powered personalized learning paths

## 🏆 **Acknowledgments**

- Built for Saudi Grade 9 students
- Designed with modern pedagogical principles
- Inspired by interactive learning methodologies
- Arabic language support for cultural relevance

---

**Ready to empower Saudi students in their algebra journey! 🇸🇦📚✨**

## 🔗 **Quick Links**

- [🚀 Deployment Guide](DEPLOYMENT.md)
- [📖 API Documentation](http://localhost:8001/docs)
- [🎯 Live Demo](https://your-app.vercel.app)
- [👨‍🏫 Teacher Dashboard](https://your-app.vercel.app/teacher) (Code: `teacher2024`)

**Happy Learning and Teaching! 🎓**
