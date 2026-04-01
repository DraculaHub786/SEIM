"""
Detection Engine
Runs MongoDB aggregation pipelines to detect security threats
"""

from datetime import datetime, timedelta
from models.alert_model import AlertModel
import logging

logger = logging.getLogger(__name__)

class DetectionEngine:
    """Threat detection engine using MongoDB aggregation"""
    
    def __init__(self, db, config, socketio):
        self.db = db
        self.config = config
        self.socketio = socketio
        self.alert_model = AlertModel(db)
        self.logs_collection = db.logs
    
    def run_detection_rules(self):
        """
        Run all detection rules
        Called periodically by scheduler
        """
        logger.info("Running detection engine...")
        
        try:
            # Rule 1: Brute force attack detection (failed login threshold)
            self.detect_brute_force_attacks()
            
            # Rule 2: Multiple event types from same IP (future enhancement)
            # self.detect_suspicious_activity()
            
            # Rule 3: Firewall blocks from external IPs (future enhancement)
            # self.detect_external_threats()
            
            logger.info("Detection engine completed")
            
        except Exception as e:
            logger.error(f"Error in detection engine: {e}")
    
    def detect_brute_force_attacks(self):
        """
        Detect brute force attacks using MongoDB aggregation
        Rule: 10+ failed login attempts from same IP within 2 minutes
        """
        try:
            # Time window
            time_window_start = datetime.utcnow() - timedelta(
                seconds=self.config.FAILED_LOGIN_TIME_WINDOW
            )
            threshold = self.config.FAILED_LOGIN_THRESHOLD
            
            # MongoDB Aggregation Pipeline
            pipeline = [
                # Stage 1: Match failed login events in time window
                {
                    '$match': {
                        'event_type': 'failed_login',
                        'timestamp': {'$gte': time_window_start}
                    }
                },
                # Stage 2: Group by IP address and count
                {
                    '$group': {
                        '_id': {
                            'ip_address': '$ip_address',
                            'username': '$username'
                        },
                        'count': {'$sum': 1},
                        'first_attempt': {'$min': '$timestamp'},
                        'last_attempt': {'$max': '$timestamp'},
                        'source': {'$first': '$source'},
                        'log_ids': {'$push': '$_id'}
                    }
                },
                # Stage 3: Filter groups exceeding threshold
                {
                    '$match': {
                        'count': {'$gte': threshold}
                    }
                },
                # Stage 4: Project final structure
                {
                    '$project': {
                        '_id': 0,
                        'ip_address': '$_id.ip_address',
                        'username': '$_id.username',
                        'attempt_count': '$count',
                        'first_attempt': '$first_attempt',
                        'last_attempt': '$last_attempt',
                        'source': '$source',
                        'log_ids': '$log_ids'
                    }
                }
            ]
            
            # Execute aggregation
            results = list(self.logs_collection.aggregate(pipeline))
            
            # Process results and create alerts
            for result in results:
                # Check if alert already exists for this IP in the last hour
                existing_alert = self.db.alerts.find_one({
                    'ip_address': result['ip_address'],
                    'alert_type': 'brute_force_attack',
                    'status': 'open',
                    'timestamp': {'$gte': datetime.utcnow() - timedelta(hours=1)}
                })
                
                if not existing_alert:
                    # Calculate threat score (0-100)
                    score = min(100, (result['attempt_count'] / threshold) * 50 + 50)
                    
                    # Create alert
                    alert_data = {
                        'timestamp': datetime.utcnow(),
                        'alert_type': 'brute_force_attack',
                        'severity': 'high' if result['attempt_count'] >= threshold * 2 else 'medium',
                        'ip_address': result['ip_address'],
                        'username': result.get('username', 'unknown'),
                        'source': result.get('source', 'unknown'),
                        'description': f"{result['attempt_count']} failed login attempts detected within {self.config.FAILED_LOGIN_TIME_WINDOW // 60} minutes",
                        'event_count': result['attempt_count'],
                        'time_window_start': result['first_attempt'],
                        'time_window_end': result['last_attempt'],
                        'related_logs': [str(log_id) for log_id in result.get('log_ids', [])[:10]],
                        'status': 'open',
                        'score': int(score),
                        'metadata': {
                            'detection_rule': 'failed_login_threshold',
                            'threshold': threshold,
                            'actual_count': result['attempt_count']
                        }
                    }
                    
                    # Save alert
                    alert_id = self.alert_model.create_alert(alert_data)
                    
                    # Broadcast alert via Socket.IO
                    alert_data['_id'] = alert_id
                    self.socketio.emit('new_alert', alert_data, broadcast=True)
                    
                    logger.warning(f"🚨 ALERT: Brute force attack detected from {result['ip_address']} ({result['attempt_count']} attempts)")
            
            if results:
                logger.info(f"Detected {len(results)} potential brute force attacks")
            
        except Exception as e:
            logger.error(f"Error in brute force detection: {e}")
    
    def detect_suspicious_activity(self):
        """
        Detect suspicious activity patterns
        Future enhancement: Multiple different event types from same IP
        """
        # Placeholder for additional detection rules
        pass
