"""
Log Controller
Handles business logic for log operations
"""

from datetime import datetime, timedelta
from models.log_model import LogModel
import logging

logger = logging.getLogger(__name__)

class LogController:
    """Controller for log operations"""
    
    def __init__(self, db):
        self.model = LogModel(db)
    
    def ingest_log(self, log_data):
        """
        Validate and ingest a new log
        
        Args:
            log_data (dict): Raw log data
            
        Returns:
            dict: Result with success status and message
        """
        try:
            # Validate required fields
            required_fields = ['source', 'event_type', 'ip_address']
            for field in required_fields:
                if field not in log_data:
                    return {
                        'success': False,
                        'message': f'Missing required field: {field}'
                    }
            
            # Normalize timestamp
            if 'timestamp' not in log_data:
                log_data['timestamp'] = datetime.utcnow()
            elif isinstance(log_data['timestamp'], str):
                try:
                    log_data['timestamp'] = datetime.fromisoformat(log_data['timestamp'].replace('Z', '+00:00'))
                except ValueError:
                    log_data['timestamp'] = datetime.utcnow()
            
            # Insert log
            log_id = self.model.create_log(log_data)
            
            return {
                'success': True,
                'message': 'Log ingested successfully',
                'log_id': log_id
            }
            
        except Exception as e:
            logger.error(f"Error ingesting log: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_logs(self, filters=None, page=1, page_size=100, sort_by='timestamp', sort_order='desc'):
        """
        Retrieve logs with filtering and pagination
        
        Args:
            filters (dict): Filter criteria
            page (int): Page number (1-indexed)
            page_size (int): Number of logs per page
            sort_by (str): Field to sort by
            sort_order (str): 'asc' or 'desc'
            
        Returns:
            dict: Paginated logs with metadata
        """
        try:
            # Build MongoDB query from filters
            query = {}
            
            if filters:
                # IP address filter
                if 'ip_address' in filters:
                    query['ip_address'] = filters['ip_address']
                
                # Event type filter
                if 'event_type' in filters:
                    query['event_type'] = filters['event_type']
                
                # Source filter
                if 'source' in filters:
                    query['source'] = filters['source']
                
                # Time range filter
                if 'start_time' in filters or 'end_time' in filters:
                    query['timestamp'] = {}
                    if 'start_time' in filters:
                        query['timestamp']['$gte'] = datetime.fromisoformat(filters['start_time'].replace('Z', '+00:00'))
                    if 'end_time' in filters:
                        query['timestamp']['$lte'] = datetime.fromisoformat(filters['end_time'].replace('Z', '+00:00'))
            
            # Calculate pagination
            skip = (page - 1) * page_size
            sort_direction = -1 if sort_order == 'desc' else 1
            
            # Get logs
            logs = self.model.get_logs(
                filters=query,
                skip=skip,
                limit=page_size,
                sort_by=sort_by,
                sort_order=sort_direction
            )
            
            # Get total count
            total_count = self.model.count_logs(query)
            total_pages = (total_count + page_size - 1) // page_size
            
            return {
                'success': True,
                'logs': logs,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages
                }
            }
            
        except Exception as e:
            logger.error(f"Error retrieving logs: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_log_statistics(self):
        """
        Get statistics for dashboard
        
        Returns:
            dict: Log statistics
        """
        try:
            # Total logs
            total_logs = self.model.count_logs()
            
            # Logs today
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            logs_today = self.model.count_logs({'timestamp': {'$gte': today_start}})
            
            # Logs by event type (last 24 hours)
            last_24h = datetime.utcnow() - timedelta(hours=24)
            
            return {
                'success': True,
                'stats': {
                    'total_logs': total_logs,
                    'logs_today': logs_today,
                    'last_24_hours': self.model.count_logs({'timestamp': {'$gte': last_24h}})
                }
            }
            
        except Exception as e:
            logger.error(f"Error retrieving log statistics: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_logs_over_time(self, hours=24):
        """
        Get logs grouped by time for chart
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            dict: Time-series data
        """
        try:
            # Calculate time range
            now = datetime.utcnow()
            start_time = now - timedelta(hours=hours)
            
            # Aggregate logs by hour
            pipeline = [
                {
                    '$match': {
                        'timestamp': {'$gte': start_time}
                    }
                },
                {
                    '$group': {
                        '_id': {
                            'year': {'$year': '$timestamp'},
                            'month': {'$month': '$timestamp'},
                            'day': {'$dayOfMonth': '$timestamp'},
                            'hour': {'$hour': '$timestamp'}
                        },
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'_id': 1}
                }
            ]
            
            result = list(self.model.collection.aggregate(pipeline))
            
            # Create time labels and data
            labels = []
            data = []
            
            for i in range(hours, -1, -1):
                time_point = now - timedelta(hours=i)
                label = time_point.strftime('%H:00')
                labels.append(label)
                
                # Find count for this hour
                count = 0
                for item in result:
                    item_time = datetime(
                        item['_id']['year'],
                        item['_id']['month'],
                        item['_id']['day'],
                        item['_id']['hour']
                    )
                    if item_time.hour == time_point.hour and item_time.day == time_point.day:
                        count = item['count']
                        break
                
                data.append(count)
            
            return {
                'success': True,
                'labels': labels,
                'data': data
            }
            
        except Exception as e:
            logger.error(f"Error retrieving logs over time: {e}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def get_events_by_type(self):
        """
        Get logs grouped by event type
        
        Returns:
            dict: Event type distribution
        """
        try:
            # Aggregate by event type
            pipeline = [
                {
                    '$group': {
                        '_id': '$event_type',
                        'count': {'$sum': 1}
                    }
                },
                {
                    '$sort': {'count': -1}
                },
                {
                    '$limit': 10
                }
            ]
            
            result = list(self.model.collection.aggregate(pipeline))
            
            labels = []
            data = []
            
            for item in result:
                event_type = item['_id'] if item['_id'] else 'unknown'
                # Format event type (remove underscores, capitalize)
                formatted = event_type.replace('_', ' ').title()
                labels.append(formatted)
                data.append(item['count'])
            
            return {
                'success': True,
                'labels': labels,
                'data': data
            }
            
        except Exception as e:
            logger.error(f"Error retrieving events by type: {e}")
            return {
                'success': False,
                'message': str(e)
            }
