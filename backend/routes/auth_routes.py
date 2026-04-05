from flask import Blueprint, request, jsonify, current_app
from controllers.auth_controller import AuthController

def create_auth_routes(db):
    auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.json
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'success': False, 'message': 'Missing username or password'}), 400
            
        auth_controller = AuthController(db, current_app.config)
        result = auth_controller.login(data['username'], data['password'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401

    @auth_bp.route('/register', methods=['POST'])
    def register():
        data = request.json
        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'success': False, 'message': 'Missing required fields (username, email, password)'}), 400
            
        auth_controller = AuthController(db, current_app.config)
        result = auth_controller.register(data['username'], data['email'], data['password'])
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    return auth_bp
