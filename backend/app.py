"""
SIEM Platform - Main Flask Application
Entry point for the SIEM backend server
"""

from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import os
from datetime import datetime

# Import configuration
from config.config import config

# Import database
from database.db_connection import init_db, get_db

# Import routes
from routes.log_routes import create_log_routes
from routes.alert_routes import create_alert_routes
from routes.auth_routes import create_auth_routes

# Import services
from services.detection_engine import DetectionEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Socket.IO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables
db = None
detection_engine = None
scheduler = None

def initialize_app():
    """Initialize application components"""
    global db, detection_engine, scheduler
    
    logger.info("=" * 60)
    logger.info("🔐 SIEM Platform - Starting Server")
    logger.info("=" * 60)
    
    # Connect to MongoDB
    if init_db(config[env]):
        db = get_db()
        logger.info("✓ Database initialized")
    else:
        logger.error("✗ Failed to initialize database")
        return False
    
    # Register routes
    app.register_blueprint(create_log_routes(db, socketio))
    app.register_blueprint(create_alert_routes(db))
    app.register_blueprint(create_auth_routes(db))
    logger.info("✓ Routes registered")
    
    # Initialize detection engine
    detection_engine = DetectionEngine(db, config[env], socketio)
    logger.info("✓ Detection engine initialized")
    
    # Start background scheduler for detection engine
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=detection_engine.run_detection_rules,
        trigger="interval",
        seconds=config[env].DETECTION_INTERVAL,
        id='detection_engine',
        name='Run detection rules',
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"✓ Scheduler started (interval: {config[env].DETECTION_INTERVAL}s)")
    
    logger.info("=" * 60)
    logger.info(f"🚀 Server ready at http://{config[env].HOST}:{config[env].PORT}")
    logger.info(f"📊 Dashboard: http://localhost:{config[env].PORT}/")
    logger.info(f"📝 API Docs: http://localhost:{config[env].PORT}/api/health")
    logger.info("=" * 60)
    
    return True

# Root route - Serve dashboard
@app.route('/')
def index():
    """Serve main dashboard page"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'index.html')

# Frontend page routes
@app.route('/logs')
def logs_page():
    """Serve logs viewer page"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'logs.html')

@app.route('/alerts')
def alerts_page():
    """Serve alerts panel page"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'alerts.html')

@app.route('/live')
def live_page():
    """Serve live monitoring page"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'live.html')

@app.route('/login')
def login_page():
    """Serve login page"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'login.html')

@app.route('/register')
def register_page():
    """Serve registration page"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, 'register.html')

# Serve static files (CSS, JS, images, etc.)
@app.route('/<path:path>')
def serve_static(path):
    """Serve frontend static files"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    return send_from_directory(frontend_path, path)

# Health check endpoint
@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': 'connected' if db is not None else 'disconnected',
        'timestamp': datetime.utcnow().isoformat()
    })

# Socket.IO event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info("Client connected")
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info("Client disconnected")

@socketio.on('ping')
def handle_ping():
    """Handle ping from client"""
    emit('pong', {'timestamp': datetime.utcnow().isoformat()})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize application
    if initialize_app():
        # Run server with Socket.IO
        try:
            socketio.run(
                app,
                host=config[env].HOST,
                port=config[env].PORT,
                debug=config[env].DEBUG,
                use_reloader=False  # Disable reloader to prevent socket issues
            )
        except KeyboardInterrupt:
            logger.info("\n🛑 Server shutting down...")
            try:
                if scheduler:
                    scheduler.shutdown(wait=False)
                logger.info("✓ Scheduler stopped")
            except Exception as e:
                pass  # Ignore cleanup errors
            logger.info("✓ Server stopped")
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            # Clean shutdown
            import sys
            sys.exit(0)
    else:
        logger.error("✗ Failed to initialize application")
