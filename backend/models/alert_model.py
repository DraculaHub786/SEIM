"""
Alert Model
Handles alert document operations
"""

from datetime import datetime
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class AlertModel:
    """Alert document model"""
    
    def __init__(self, db):
        self.collection = db.alerts
    
    def create_alert(self, alert_data):
        """
        Insert a new alert document
        
        Args:
            alert_data (dict): Alert document data
            
        Returns:
            str: Inserted document ID
        """
        try:
            # Ensure timestamp
            if 'timestamp' not in alert_data:
                alert_data['timestamp'] = datetime.utcnow()
            
            # Default status
            if 'status' not in alert_data:
                alert_data['status'] = 'open'
            
            result = self.collection.insert_one(alert_data)
            logger.info(f"Alert created: {alert_data.get('alert_type')} - {alert_data.get('ip_address')}")
            
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            raise
    
    def get_alerts(self, filters=None, skip=0, limit=100, sort_by='timestamp', sort_order=-1):
        """
        Retrieve alerts with filtering and pagination
        
        Args:
            filters (dict): MongoDB query filters
            skip (int): Number of documents to skip
            limit (int): Maximum number of documents to return
            sort_by (str): Field to sort by
            sort_order (int): 1 for ascending, -1 for descending
            
        Returns:
            list: List of alert documents
        """
        try:
            query = filters or {}
            
            cursor = self.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
            
            alerts = []
            for alert in cursor:
                alert['_id'] = str(alert['_id'])
                alerts.append(alert)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error retrieving alerts: {e}")
            raise
    
    def count_alerts(self, filters=None):
        """
        Count alerts matching filters
        
        Args:
            filters (dict): MongoDB query filters
            
        Returns:
            int: Count of matching documents
        """
        try:
            query = filters or {}
            return self.collection.count_documents(query)
        except Exception as e:
            logger.error(f"Error counting alerts: {e}")
            raise
    
    def update_alert_status(self, alert_id, status):
        """
        Update alert status
        
        Args:
            alert_id (str): Alert document ID
            status (str): New status
            
        Returns:
            bool: Success status
        """
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(alert_id)},
                {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating alert status: {e}")
            return False
    
    def get_alert_by_id(self, alert_id):
        """
        Get a single alert by ID
        
        Args:
            alert_id (str): Alert document ID
            
        Returns:
            dict: Alert document or None
        """
        try:
            alert = self.collection.find_one({'_id': ObjectId(alert_id)})
            if alert:
                alert['_id'] = str(alert['_id'])
            return alert
        except Exception as e:
            logger.error(f"Error retrieving alert by ID: {e}")
            return None
