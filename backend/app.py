from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta, timezone
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///todoapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

# Handle PostgreSQL URL format for Render
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

# Add fallback for database connection issues
try:
    # Test database connection
    if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI']:
        print("Using PostgreSQL database")
        # Test if psycopg2 is available
        try:
            import psycopg2
            print("psycopg2 is available")
        except ImportError as e:
            print(f"psycopg2 not available: {e}")
            print("Falling back to SQLite")
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todoapp.db'
    else:
        print("Using SQLite database")
except Exception as e:
    print(f"Database configuration warning: {e}")
    # Fallback to SQLite if PostgreSQL fails
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todoapp.db'

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    priority = db.Column(db.String(20), default='Medium')  # High, Medium, Low
    status = db.Column(db.String(20), default='Pending')  # Pending, In Progress, Completed
    category = db.Column(db.String(50), default='General')
    tags = db.Column(db.String(200))  # Comma-separated tags
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

# Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Name, email, and password are required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'User with this email already exists'}), 400
        
        # Hash password
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            password_hash=password_hash
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Task Routes
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        user_id = int(get_jwt_identity())
        
        # Get query parameters for filtering
        status = request.args.get('status')
        category = request.args.get('category')
        priority = request.args.get('priority')
        search = request.args.get('search')
        
        # Build query
        query = Task.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        if category:
            query = query.filter_by(category=category)
        if priority:
            query = query.filter_by(priority=priority)
        if search:
            query = query.filter(
                (Task.title.contains(search)) | 
                (Task.description.contains(search))
            )
        
        tasks = query.order_by(Task.created_at.desc()).all()
        
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'priority': task.priority,
                'status': task.status,
                'category': task.category,
                'tags': task.tags.split(',') if task.tags else [],
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat()
            })
        
        return jsonify({'tasks': tasks_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data.get('title'):
            return jsonify({'error': 'Task title is required'}), 400
        
        # Parse due date if provided
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except:
                return jsonify({'error': 'Invalid due date format'}), 400
        
        # Parse tags
        tags_str = None
        if data.get('tags') and isinstance(data['tags'], list):
            tags_str = ','.join(data['tags'])
        
        task = Task(
            user_id=user_id,
            title=data['title'],
            description=data.get('description', ''),
            due_date=due_date,
            priority=data.get('priority', 'Medium'),
            status=data.get('status', 'Pending'),
            category=data.get('category', 'General'),
            tags=tags_str
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({
            'message': 'Task created successfully',
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'priority': task.priority,
                'status': task.status,
                'category': task.category,
                'tags': task.tags.split(',') if task.tags else [],
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    try:
        user_id = int(get_jwt_identity())
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                except:
                    return jsonify({'error': 'Invalid due date format'}), 400
            else:
                task.due_date = None
        if 'priority' in data:
            task.priority = data['priority']
        if 'status' in data:
            task.status = data['status']
        if 'category' in data:
            task.category = data['category']
        if 'tags' in data:
            if data['tags'] and isinstance(data['tags'], list):
                task.tags = ','.join(data['tags'])
            else:
                task.tags = None
        
        task.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        
        return jsonify({
            'message': 'Task updated successfully',
            'task': {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date.isoformat() if task.due_date else None,
                'priority': task.priority,
                'status': task.status,
                'category': task.category,
                'tags': task.tags.split(',') if task.tags else [],
                'created_at': task.created_at.isoformat(),
                'updated_at': task.updated_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    try:
        user_id = int(get_jwt_identity())
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Statistics Route
@app.route('/api/stats', methods=['GET'])
@jwt_required()
def get_stats():
    try:
        user_id = int(get_jwt_identity())
        
        total_tasks = Task.query.filter_by(user_id=user_id).count()
        completed_tasks = Task.query.filter_by(user_id=user_id, status='Completed').count()
        pending_tasks = Task.query.filter_by(user_id=user_id, status='Pending').count()
        in_progress_tasks = Task.query.filter_by(user_id=user_id, status='In Progress').count()
        
        # Overdue tasks
        overdue_tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.due_date < datetime.now(timezone.utc),
            Task.status != 'Completed'
        ).count()
        
        return jsonify({
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health check route
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'ToDo API is running'}), 200

# Database initialization route (for manual table creation)
@app.route('/api/init-db', methods=['POST'])
def init_database():
    try:
        with app.app_context():
            db.create_all()
            return jsonify({'message': 'Database tables created successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to create database tables: {str(e)}'}), 500

# Initialize database tables
def create_tables():
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating database tables: {e}")

# Create tables when the app starts
create_tables()

if __name__ == '__main__':
    # Get port from environment variable (for Render) or use 5001 for local development
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
