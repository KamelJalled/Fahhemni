# Math Tutoring App - Production Deployment Guide

This guide explains how to deploy the Math Tutoring App to any web hosting service.

## Project Structure

```
/app
├── frontend/
│   ├── build/          # Production build files (HTML, CSS, JS)
│   ├── src/            # React source code
│   └── package.json    # Frontend dependencies
├── backend/
│   ├── server.py       # FastAPI backend
│   ├── models.py       # Data models
│   ├── database.py     # MongoDB connection
│   ├── utils.py        # Utility functions
│   └── requirements.txt # Python dependencies
├── README.md
└── DEPLOYMENT.md       # This file
```

## Frontend Deployment (Static Hosting)

The frontend is built as static files in the `frontend/build/` directory. You can deploy these to any static hosting service:

### Popular Static Hosting Options:
- **Netlify**: Upload the `frontend/build` folder
- **GitHub Pages**: Push to repository and enable Pages
- **AWS S3 + CloudFront**: Upload to S3 bucket with static hosting
- **Firebase Hosting**: Use Firebase CLI to deploy
- **Surge.sh**: Simple deployment with `surge` command

### Steps for Static Deployment:
1. The production build is already created in `frontend/build/`
2. Upload the contents of `frontend/build/` to your hosting service
3. Set up custom domain if needed
4. Configure redirects for React Router (SPA routing)

### SPA Routing Configuration:
For single-page applications, you need to redirect all routes to `index.html`:

**Netlify**: Create `frontend/build/_redirects`:
```
/*    /index.html   200
```

**Apache**: Create `frontend/build/.htaccess`:
```
Options -MultiViews
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^ index.html [L]
```

**Nginx**:
```
location / {
  try_files $uri $uri/ /index.html;
}
```

## Backend Deployment (API Service)

The backend is a FastAPI application that can be deployed to various hosting services:

### Popular Backend Hosting Options:
- **Railway**: Simple Python app deployment
- **Render**: Web service deployment
- **DigitalOcean App Platform**: Container deployment
- **AWS Elastic Beanstalk**: Scalable deployment
- **Google Cloud Run**: Serverless container deployment
- **Heroku**: Platform-as-a-Service deployment

### Requirements:
- Python 3.8+
- MongoDB database (MongoDB Atlas recommended for cloud)
- Environment variables configured

### Environment Variables:
Create a `.env` file in the backend directory:
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/mathtutor
```

### Installation Steps:
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables
3. Run the server: `python server.py` or `uvicorn server:app --host 0.0.0.0 --port 8000`

### Docker Deployment (Optional):
Create `Dockerfile` in backend directory:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Database Setup

### MongoDB Atlas (Recommended):
1. Create account at https://mongodb.com/atlas
2. Create a new cluster (free tier available)
3. Create database user and get connection string
4. Replace `MONGO_URL` in backend environment variables

### Local MongoDB:
1. Install MongoDB locally
2. Start MongoDB service
3. Use connection string: `mongodb://localhost:27017/mathtutor`

## Configuration

### Frontend API Configuration:
The frontend is configured to communicate with the backend via the `REACT_APP_BACKEND_URL` environment variable.

For production, create `frontend/.env.production`:
```
REACT_APP_BACKEND_URL=https://your-api-domain.com
```

### Backend CORS Configuration:
The backend is already configured to allow CORS for frontend requests. Update the `origins` list in `server.py` if needed:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Complete Deployment Workflow

### Step 1: Deploy Backend
1. Choose a backend hosting service
2. Set up MongoDB database
3. Configure environment variables
4. Deploy backend code
5. Note the API URL (e.g., https://api.yourdomain.com)

### Step 2: Configure Frontend
1. Update `frontend/.env.production` with your backend URL
2. Rebuild frontend: `cd frontend && yarn build`

### Step 3: Deploy Frontend
1. Upload `frontend/build/` contents to static hosting
2. Configure SPA routing redirects
3. Set up custom domain if needed

### Step 4: Test
1. Visit your frontend URL
2. Test student login functionality
3. Test problem-solving interface
4. Test teacher dashboard
5. Verify backend API responses

## Monitoring and Maintenance

### Backend Monitoring:
- Monitor API response times
- Check database connections
- Monitor error logs
- Set up health checks

### Frontend Monitoring:
- Monitor page load speeds
- Check for JavaScript errors
- Monitor user interactions
- Set up analytics if needed

## Troubleshooting

### Common Issues:

1. **CORS Errors**: Update backend CORS configuration
2. **API Connection Failed**: Check backend URL in frontend config
3. **Database Connection**: Verify MongoDB connection string
4. **Routing Issues**: Ensure SPA redirects are configured
5. **Build Errors**: Check Node.js version and dependencies

### Support:
For technical support, refer to the repository issues or contact the development team.