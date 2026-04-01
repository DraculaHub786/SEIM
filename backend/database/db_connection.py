"""
MongoDB Database Connection Manager
Handles connection pooling and database initialization
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages MongoDB connections and operations"""
    
    def __init__(self, config):
        self.config = config
        self.client = None
        self.db = None
        
    def connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(
                self.config.MONGO_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[self.config.MONGO_DB_NAME]
            logger.info(f"✓ Connected to MongoDB: {self.config.MONGO_DB_NAME}")
            
            # Initialize collections and indexes
            self._initialize_collections()
            
            return True
            
        except ConnectionFailure as e:
            logger.error(f"✗ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"✗ Unexpected error connecting to MongoDB: {e}")
            return False
    
    def _initialize_collections(self):
        """Initialize collections with indexes and validation"""
        try:
            # Create logs collection with validation
            if 'logs' not in self.db.list_collection_names():
                self.db.create_collection('logs', validator={
                    '$jsonSchema': {
                        'bsonType': 'object',
                        'required': ['timestamp', 'source', 'event_type', 'ip_address'],
                        'properties': {
                            'timestamp': {'bsonType': 'date'},
                            'source': {'bsonType': 'string'},
                            'event_type': {'bsonType': 'string'},
                            'ip_address': {'bsonType': 'string'}
                        }
                    }
                })
                logger.info("✓ Created 'logs' collection")
            
            # Create indexes for logs
            logs = self.db.logs
            logs.create_index([('timestamp', DESCENDING), ('event_type', ASCENDING)])
            logs.create_index([('ip_address', ASCENDING)])
            logs.create_index([('source', ASCENDING)])
            logs.create_index([('event_type', ASCENDING)])
            
            # TTL index - auto-delete logs after configured days
            ttl_seconds = self.config.LOG_TTL_DAYS * 24 * 60 * 60
            logs.create_index([('timestamp', ASCENDING)], expireAfterSeconds=ttl_seconds)
            logger.info(f"✓ Created indexes for 'logs' (TTL: {self.config.LOG_TTL_DAYS} days)")
            
            # Create alerts collection
            if 'alerts' not in self.db.list_collection_names():
                self.db.create_collection('alerts')
                logger.info("✓ Created 'alerts' collection")
            
            # Create indexes for alerts
            alerts = self.db.alerts
            alerts.create_index([('timestamp', DESCENDING)])
            alerts.create_index([('ip_address', ASCENDING)])
            alerts.create_index([('status', ASCENDING)])
            alerts.create_index([('severity', ASCENDING)])
            alerts.create_index([('status', ASCENDING), ('severity', ASCENDING), ('timestamp', DESCENDING)])
            logger.info("✓ Created indexes for 'alerts'")
            
            # Create users collection
            if 'users' not in self.db.list_collection_names():
                self.db.create_collection('users')
                logger.info("✓ Created 'users' collection")
            
            # Create indexes for users
            users = self.db.users
            users.create_index([('username', ASCENDING)], unique=True)
            users.create_index([('email', ASCENDING)], unique=True)
            users.create_index([('role', ASCENDING)])
            logger.info("✓ Created indexes for 'users'")
            
            # Create default admin user if doesn't exist
            self._create_default_admin()
            
        except OperationFailure as e:
            logger.error(f"✗ Failed to initialize collections: {e}")
        except Exception as e:
            logger.error(f"✗ Unexpected error initializing collections: {e}")
    
    def _create_default_admin(self):
        """Create default admin user"""
        try:
            import bcrypt
            
            if self.db.users.count_documents({'username': 'admin'}) == 0:
                # Password: admin123
                password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
                
                admin_user = {
                    'username': 'admin',
                    'email': 'admin@siem.local',
                    'password_hash': password_hash.decode('utf-8'),
                    'role': 'admin',
                    'permissions': ['view_logs', 'view_alerts', 'export_data', 'manage_users'],
                    'created_at': datetime.utcnow(),
                    'last_login': None,
                    'is_active': True
                }
                
                self.db.users.insert_one(admin_user)
                logger.info("✓ Created default admin user (username: admin, password: admin123)")
        except Exception as e:
            logger.error(f"✗ Failed to create default admin user: {e}")
    
    def get_db(self):
        """Get database instance"""
        return self.db
    
    def get_collection(self, name):
        """Get collection by name"""
        return self.db[name]
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            logger.info("✓ MongoDB connection closed")

# Global database instance
db_manager = None

def init_db(config):
    """Initialize database connection"""
    global db_manager
    db_manager = DatabaseManager(config)
    return db_manager.connect()

def get_db():
    """Get database instance"""
    global db_manager
    if db_manager:
        return db_manager.get_db()
    return None
