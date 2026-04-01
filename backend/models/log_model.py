"""
Log Model
Handles log document operations
"""

from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class LogModel:
    """Log document model"""
    
    def __init__(self, db):
        self.collection = db.logs
    
    def create_log(self, log_data):
        """
        Insert a new log document
        
        Args:
            log_data (dict): Log document data
            
        Returns:
            str: Inserted document ID
        """
        try:
            # Ensure timestamp is datetime object
            if 'timestamp' in log_data and isinstance(log_data['timestamp'], str):
                log_data['timestamp'] = datetime.fromisoformat(log_data['timestamp'].replace('Z', '+00:00'))
            elif 'timestamp' not in log_data:
                log_data['timestamp'] = datetime.utcnow()
            
            # Insert document
            result = self.collection.insert_one(log_data)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error creating log: {e}")
            raise
    
    def get_logs(self, filters=None, skip=0, limit=100, sort_by='timestamp', sort_order=-1):
        """
        Retrieve logs with filtering and pagination
        
        Args:
            filters (dict): MongoDB query filters
            skip (int): Number of documents to skip
            limit (int): Maximum number of documents to return
            sort_by (str): Field to sort by
            sort_order (int): 1 for ascending, -1 for descending
            
        Returns:
            list: List of log documents
        """
        try:
            query = filters or {}
            
            cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
            
            logs = []
            for log in cursor:
                log['_id'] = str(log['_id'])
                logs.append(log)
            
            return logs
            
        except Exception as e:
            logger.error(f"Error retrieving logs: {e}")
            raise
    
    def count_logs(self, filters=None):
        """
        Count logs matching filters
        
        Args:
            filters (dict): MongoDB query filters
            
        Returns:
            int: Count of matching documents
        """
        try:
            query = filters or {}
            return self.collection.count_documents(query)
        except Exception as e:
            logger.error(f"Error counting logs: {e}")
            raise
    
    def get_log_by_id(self, log_id):
        """
        Get a single log by ID
        
        Args:
            log_id (str): Log document ID
            
        Returns:
            dict: Log document or None
        """
        try:
            log = self.collection.find_one({'_id': ObjectId(log_id)})
            if log:
                log['_id'] = str(log['_id'])
            return log
        except Exception as e:
            logger.error(f"Error retrieving log by ID: {e}")
            return None
    
    def get_recent_logs(self, limit=10):
        """
        Get most recent logs
        
        Args:
            limit (int): Number of logs to return
            
        Returns:
            list: List of recent log documents
        """
        return self.get_logs(limit=limit, sort_by='timestamp', sort_order=-1)
