import jwt
from functools import wraps
from flask import request, jsonify, current_app
from database.db_connection import get_db
import logging

logger = logging.getLogger(__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check Authorization header (Bearer token)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                
        if not token:
            return jsonify({'success': False, 'message': 'Authentication token is missing!'}), 401
            
        try:
            # Decode the token
            data = jwt.decode(
                token, 
                current_app.config.get('JWT_SECRET_KEY', 'jwt-super-secret-key-production'), 
                algorithms=["HS256"]
            )
            
            # Optionally check if user still exists
            db = get_db()
            if db is not None:
                current_user = db.users.find_one({'username': data['username']})
                if not current_user:
                    return jsonify({'success': False, 'message': 'Invalid token: User no longer exists'}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token!'}), 401
        except Exception as e:
            logger.error(f"JWT Verification Error: {e}")
            return jsonify({'success': False, 'message': 'Token validation failed'}), 500

        # Pass current user payload to the decorated route
        return f(data, *args, **kwargs)
        
    return decorated
