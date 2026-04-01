"""
Configuration file for SIEM Platform
Contains all environment-specific settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'siem-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'siem_db')
    
    # Redis (Optional - for caching)
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_ENABLED = os.getenv('REDIS_ENABLED', 'False') == 'True'
    
    # Socket.IO
    SOCKETIO_CORS_ALLOWED_ORIGINS = os.getenv('SOCKETIO_CORS_ALLOWED_ORIGINS', '*')
    
    # Detection Engine
    DETECTION_INTERVAL = int(os.getenv('DETECTION_INTERVAL', 30))  # seconds
    FAILED_LOGIN_THRESHOLD = int(os.getenv('FAILED_LOGIN_THRESHOLD', 10))
    FAILED_LOGIN_TIME_WINDOW = int(os.getenv('FAILED_LOGIN_TIME_WINDOW', 120))  # seconds
    
    # Data Retention
    LOG_TTL_DAYS = int(os.getenv('LOG_TTL_DAYS', 90))
    
    # Pagination
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 100))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 1000))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
