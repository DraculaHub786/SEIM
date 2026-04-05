import jwt
import bcrypt
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AuthController:
    """Controller for user authentication and management"""

    def __init__(self, db, config):
        self.db = db
        self.users = db.users if db is not None else None
        self.config = config

    def login(self, username, password):
        """Attempt to log in a user and return a JWT token"""
        if self.users is None:
            return {'success': False, 'message': 'Database not connected'}

        user = self.users.find_one({'username': username})
        if not user or not user.get('is_active', False):
            return {'success': False, 'message': 'Invalid username or password'}

        # Check password
        stored_hash = user.get('password_hash', '').encode('utf-8')
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return {'success': False, 'message': 'Invalid username or password'}

        # Generate JWT
        expiration = datetime.utcnow() + timedelta(hours=self.config.get('JWT_EXPIRATION_HOURS', 24))
        payload = {
            'username': user['username'],
            'role': user.get('role', 'user'),
            'exp': expiration,
            'iat': datetime.utcnow()
        }

        try:
            token = jwt.encode(payload, self.config.get('JWT_SECRET_KEY', 'jwt-super-secret-key-production'), algorithm='HS256')
            
            # Update last login
            self.users.update_one({'_id': user['_id']}, {'$set': {'last_login': datetime.utcnow()}})
            
            return {
                'success': True, 
                'token': token,
                'user': {
                    'username': user['username'],
                    'role': user.get('role', 'user'),
                    'email': user.get('email', '')
                }
            }
        except Exception as e:
            logger.error(f"Error generating JWT: {e}")
            return {'success': False, 'message': 'Error generating authentication token'}

    def register(self, username, email, password):
        """Register a new user"""
        if self.users is None:
            return {'success': False, 'message': 'Database not connected'}

        if not username or not email or not password:
            return {'success': False, 'message': 'Missing required fields'}

        # Check existing
        if self.users.find_one({'$or': [{'username': username}, {'email': email}]}):
            return {'success': False, 'message': 'Username or Email already exists'}

        try:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            new_user = {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'role': 'user',  # Default non-admin
                'permissions': ['view_logs', 'view_alerts'],
                'created_at': datetime.utcnow(),
                'last_login': None,
                'is_active': True
            }
            
            self.users.insert_one(new_user)
            logger.info(f"Registered new user: {username}")
            
            return {'success': True, 'message': 'Registration successful'}
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return {'success': False, 'message': 'Error during registration'}
