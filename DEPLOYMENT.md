# Deployment Guide

This guide covers different deployment options for the ToDo Application.

## 🚀 Quick Start (Local Development)

### Option 1: Using the Start Script
```bash
./start.sh
```

### Option 2: Manual Setup

1. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp env.example .env
   # Edit .env file with your configuration
   python app.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start
   ```

## 🌐 Production Deployment

### Frontend Deployment (Vercel)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

3. **Configure Environment Variables**
   - `REACT_APP_API_URL`: Your backend API URL

### Backend Deployment (Render)

1. **Connect Repository**
   - Go to [Render](https://render.com)
   - Connect your GitHub repository

2. **Configure Service**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3

3. **Set Environment Variables**
   ```
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   DATABASE_URL=postgresql://username:password@host:port/database
   FLASK_ENV=production
   ```

### Backend Deployment (Heroku)

1. **Install Heroku CLI**
   ```bash
   npm install -g heroku
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set JWT_SECRET_KEY=your-jwt-secret-key-here
   heroku config:set DATABASE_URL=postgresql://username:password@host:port/database
   heroku config:set FLASK_ENV=production
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

## 🐳 Docker Deployment

### Using Docker Compose

1. **Start all services**
   ```bash
   docker-compose up -d
   ```

2. **Access the application**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:5000
   - Database: localhost:5432

### Individual Docker Services

1. **Build and run backend**
   ```bash
   cd backend
   docker build -t todo-backend .
   docker run -p 5000:5000 todo-backend
   ```

2. **Build and run frontend**
   ```bash
   cd frontend
   docker build -t todo-frontend .
   docker run -p 3000:3000 todo-frontend
   ```

## 🗄️ Database Setup

### SQLite (Development)
No additional setup required. The database file will be created automatically.

### PostgreSQL (Production)

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS
   brew install postgresql
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Create Database**
   ```sql
   CREATE DATABASE todoapp;
   CREATE USER todo_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE todoapp TO todo_user;
   ```

3. **Update Environment Variables**
   ```env
   DATABASE_URL=postgresql://todo_user:your_password@localhost:5432/todoapp
   ```

## 🔧 Environment Variables

### Backend (.env)
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///todoapp.db
FLASK_ENV=development
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
```

## 📊 Monitoring and Logs

### Backend Logs
- **Local**: Check console output
- **Render**: Available in dashboard
- **Heroku**: `heroku logs --tail`

### Frontend Logs
- **Local**: Check browser console
- **Vercel**: Available in dashboard

## 🔒 Security Considerations

1. **Environment Variables**
   - Never commit `.env` files
   - Use strong, unique secrets
   - Rotate secrets regularly

2. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

3. **API Security**
   - Enable CORS properly
   - Use HTTPS in production
   - Implement rate limiting

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill process using port 5000
   lsof -ti:5000 | xargs kill -9
   
   # Kill process using port 3000
   lsof -ti:3000 | xargs kill -9
   ```

2. **Database Connection Issues**
   - Check DATABASE_URL format
   - Verify database is running
   - Check firewall settings

3. **CORS Issues**
   - Verify CORS settings in backend
   - Check API URL in frontend

4. **Build Failures**
   - Check Node.js and Python versions
   - Clear node_modules and reinstall
   - Check for syntax errors

### Getting Help

1. Check the logs for error messages
2. Verify all environment variables are set
3. Ensure all dependencies are installed
4. Check network connectivity
5. Review the README.md for setup instructions

## 📈 Performance Optimization

### Backend
- Use a production WSGI server (Gunicorn)
- Enable database connection pooling
- Implement caching (Redis)
- Use a CDN for static files

### Frontend
- Enable code splitting
- Optimize bundle size
- Use lazy loading
- Implement service workers

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy ToDo App

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        # Add your deployment steps here

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        # Add your deployment steps here
```

---

For more detailed information, refer to the main README.md file.
