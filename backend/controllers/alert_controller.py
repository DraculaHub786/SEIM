"""
Alert Controller
Handles business logic for alert operations
"""

from datetime import datetime, timedelta
from models.alert_model import AlertModel
import logging

logger = logging.getLogger(__name__)

class AlertController:
    """Controller for alert operations"""
    
    def __init__(self, db):
        self.model = AlertModel(db)
    
    def create_alert(self, alert_data):
        """
        Create a new alert
        
        Args:
            alert_data (dict): Alert data
            
        Returns:
            dict: Result with success status
        """
        try:
            alert_id = self.model.create_alert(alert_data)
            
            return {
                'success': True,
                'message': 'Alert created successfully',
                'alert_id': alert_id,
                'alert': alert_data
            }
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_alerts(self, filters=None, page=1, page_size=100, sort_by='timestamp', sort_order='desc'):
        """
        Retrieve alerts with filtering and pagination
        
        Args:
            filters (dict): Filter criteria
            page (int): Page number (1-indexed)
            page_size (int): Number of alerts per page
            sort_by (str): Field to sort by
            sort_order (str): 'asc' or 'desc'
            
        Returns:
            dict: Paginated alerts with metadata
        """
        try:
            # Build MongoDB query from filters
            query = {}
            
            if filters:
                # Status filter
                if 'status' in filters:
                    query['status'] = filters['status']
                
                # Severity filter
                if 'severity' in filters:
                    query['severity'] = filters['severity']
                
                # IP address filter
                if 'ip_address' in filters:
                    query['ip_address'] = filters['ip_address']
            
            # Calculate pagination
            skip = (page - 1) * page_size
            sort_direction = -1 if sort_order == 'desc' else 1
            
            # Get alerts
            alerts = self.model.get_alerts(
                filters=query,
                skip=skip,
                limit=page_size,
                sort_by=sort_by,
                sort_order=sort_direction
            )
            
            # Get total count
            total_count = self.model.count_alerts(query)
            total_pages = (total_count + page_size - 1) // page_size
            
            return {
                'success': True,
                'alerts': alerts,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages
                }
            }
            
        except Exception as e:
            logger.error(f"Error retrieving alerts: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_alert_statistics(self):
        """
        Get statistics for dashboard
        
        Returns:
            dict: Alert statistics
        """
        try:
            # Total alerts
            total_alerts = self.model.count_alerts()
            
            # Open alerts
            open_alerts = self.model.count_alerts({'status': 'open'})
            
            # Critical alerts
            critical_alerts = self.model.count_alerts({'severity': 'high', 'status': 'open'})
            
            # Alerts today
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            alerts_today = self.model.count_alerts({'timestamp': {'$gte': today_start}})
            
            return {
                'success': True,
                'stats': {
                    'total_alerts': total_alerts,
                    'open_alerts': open_alerts,
                    'critical_alerts': critical_alerts,
                    'alerts_today': alerts_today
                }
            }
            
        except Exception as e:
            logger.error(f"Error retrieving alert statistics: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def update_alert_status(self, alert_id, status):
        """
        Update alert status
        
        Args:
            alert_id (str): Alert ID
            status (str): New status
            
        Returns:
            dict: Result
        """
        try:
            success = self.model.update_alert_status(alert_id, status)
            
            if success:
                return {
                    'success': True,
                    'message': 'Alert status updated'
                }
            else:
                return {
                    'success': False,
                    'message': 'Alert not found or not updated'
                }
                
        except Exception as e:
            logger.error(f"Error updating alert status: {e}")
            return {
                'success': False,
                'message': str(e)
            }
