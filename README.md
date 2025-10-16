# ToDo Web Application

A modern, full-stack ToDo application built with React and Flask. This application provides a clean, intuitive interface for managing tasks with features like authentication, task categorization, priority levels, due dates, and more.

## 🚀 Features

### Core Features
- **User Authentication**: Secure registration and login with JWT tokens
- **Task Management**: Create, edit, delete, and mark tasks as complete
- **Task Organization**: Categorize tasks and assign priority levels
- **Due Dates**: Set and track task deadlines
- **Search & Filter**: Find tasks quickly with search and filtering options
- **Responsive Design**: Works seamlessly across desktop, tablet, and mobile
- **Dark Mode**: Toggle between light and dark themes

### Advanced Features
- **Task Statistics**: View completion rates and task counts
- **Overdue Detection**: Visual indicators for overdue and due-soon tasks
- **Tag System**: Add custom tags to tasks for better organization
- **Real-time Updates**: Instant feedback on task operations
- **Progress Tracking**: Visual progress bars and completion statistics

## 🛠️ Technology Stack

### Frontend
- **React.js** - Modern UI framework
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **React Hot Toast** - Beautiful notifications
- **Lucide React** - Modern icon library
- **Date-fns** - Date manipulation library

### Backend
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - Database ORM
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin resource sharing

### Database
- **SQLite** (Development)
- **PostgreSQL** (Production ready)

## 📁 Project Structure

```
ToDoAppForYoutube/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── env.example           # Environment variables template
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── contexts/         # React contexts (Auth, Theme)
│   │   ├── pages/           # Page components
│   │   ├── App.js           # Main App component
│   │   ├── index.js         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Node.js dependencies
│   ├── tailwind.config.js   # Tailwind configuration
│   └── postcss.config.js    # PostCSS configuration
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)

### Quick Start (Recommended)

**Start the Application:**
```bash
./start-app.sh
```

### Application Management

**Check Status:**
```bash
./status.sh
```

**Stop Application:**
```bash
./stop.sh
```

**Test Application:**
```bash
./test_application.sh
```

### Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `start-app.sh` | Start the complete application | `./start-app.sh` |
| `stop.sh` | Stop all application processes | `./stop.sh` |
| `status.sh` | Check application status | `./status.sh` |
| `test_application.sh` | Run comprehensive tests | `./test_application.sh` |
| `prepare-for-deployment.sh` | Prepare for deployment | `./prepare-for-deployment.sh` |
| `deploy-to-github.sh` | Push code to GitHub | `./deploy-to-github.sh` |
| `check-deployment.sh` | Check deployment status | `./check-deployment.sh` |

For detailed script documentation, see [SCRIPTS_REFERENCE.md](SCRIPTS_REFERENCE.md).

### Manual Installation (Advanced Users)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ToDoAppForYoutube
   ```

2. **Set up the Backend**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp env.example .env
   # Edit .env file with your configuration
   
   # Run the Flask application
   python app.py
   ```

3. **Set up the Frontend**
   ```bash
   cd frontend
   
   # Install dependencies
   npm install
   
   # Start the development server
   npm start
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000 (or dynamically assigned port)
   - Backend API: http://localhost:5001 (or dynamically assigned port)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///todoapp.db
FLASK_ENV=development
```

### Database Configuration

The application uses SQLite by default for development. For production, update the `DATABASE_URL` to use PostgreSQL:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todoapp
```

## 📱 Usage

### User Registration
1. Navigate to the registration page
2. Fill in your name, email, and password
3. Click "Create account"

### Task Management
1. **Create a Task**: Click "Add Task" button and fill in the details
2. **Edit a Task**: Click the edit icon on any task card
3. **Delete a Task**: Click the delete icon on any task card
4. **Change Status**: Use the status dropdown on task cards
5. **Search Tasks**: Use the search bar to find specific tasks
6. **Filter Tasks**: Click the filter button to apply filters

### Features Overview
- **Categories**: Organize tasks by category (Work, Personal, Shopping, etc.)
- **Priorities**: Set task priority (High, Medium, Low)
- **Due Dates**: Set deadlines for tasks
- **Tags**: Add custom tags for better organization
- **Dark Mode**: Toggle theme using the moon/sun icon in the navbar

## 🚀 Deployment

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
   - Set `REACT_APP_API_URL` to your backend URL

### Backend Deployment (Render/Heroku)

1. **Create a Procfile**
   ```bash
   echo "web: gunicorn app:app" > Procfile
   ```

2. **Deploy to Render/Heroku**
   - Connect your GitHub repository
   - Set environment variables
   - Deploy

### Database Setup (Production)

For production, use PostgreSQL:

1. **Create a PostgreSQL database**
2. **Update DATABASE_URL** in environment variables
3. **Run migrations** (database tables will be created automatically)

## 🧪 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Tasks
- `GET /api/tasks` - Get all tasks (with optional filters)
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task

### Statistics
- `GET /api/stats` - Get task statistics

### Health Check
- `GET /api/health` - API health check

## 🎨 Customization

### Styling
- Modify `frontend/src/index.css` for global styles
- Update `frontend/tailwind.config.js` for theme customization
- Component-specific styles are in individual component files

### Adding Features
- Backend: Add new routes in `backend/app.py`
- Frontend: Create new components in `frontend/src/components/`
- Update contexts for state management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Include steps to reproduce the problem

## 🎯 Future Enhancements

- [ ] Task reminders and notifications
- [ ] Recurring tasks
- [ ] File attachments
- [ ] Team collaboration
- [ ] Task templates
- [ ] Export/Import functionality
- [ ] Mobile app (React Native)
- [ ] Advanced analytics and reporting

---

**Happy Task Managing! 🎉**
