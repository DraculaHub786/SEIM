"""
Log API Routes
Handles HTTP endpoints for log operations
"""

from flask import Blueprint, request, jsonify
from controllers.log_controller import LogController
from middleware.auth_middleware import token_required

def create_log_routes(db, socketio):
    """Create and configure log routes"""
    
    log_bp = Blueprint('logs', __name__, url_prefix='/api/logs')
    controller = LogController(db)
    
    @log_bp.route('', methods=['POST'])
    def ingest_log():
        """
        Ingest a new log
        POST /api/logs
        Body: JSON log data
        """
        try:
            log_data = request.get_json()
            
            if not log_data:
                return jsonify({
                    'success': False,
                    'message': 'No data provided'
                }), 400
            
            result = controller.ingest_log(log_data)
            
            if result['success']:
                # Emit real-time event to all connected clients
                try:
                    socketio.emit('new_log', log_data, broadcast=True, skip_sid=None)
                except Exception as emit_error:
                    # Log emission failed, but data was stored successfully
                    pass
                return jsonify(result), 201
            else:
                return jsonify(result), 400
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @log_bp.route('', methods=['GET'])
    @token_required
    def get_logs(current_user):
        """
        Get logs with filtering and pagination
        GET /api/logs?page=1&page_size=100&ip_address=...&event_type=...
        """
        try:
            # Get query parameters
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 100))
            sort_by = request.args.get('sort_by', 'timestamp')
            sort_order = request.args.get('sort_order', 'desc')
            
            # Build filters
            filters = {}
            if request.args.get('ip_address'):
                filters['ip_address'] = request.args.get('ip_address')
            if request.args.get('event_type'):
                filters['event_type'] = request.args.get('event_type')
            if request.args.get('source'):
                filters['source'] = request.args.get('source')
            if request.args.get('start_time'):
                filters['start_time'] = request.args.get('start_time')
            if request.args.get('end_time'):
                filters['end_time'] = request.args.get('end_time')
            
            result = controller.get_logs(
                filters=filters,
                page=page,
                page_size=page_size,
                sort_by=sort_by,
                sort_order=sort_order
            )
            
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @log_bp.route('/stats', methods=['GET'])
    @token_required
    def get_statistics(current_user):
        """
        Get log statistics
        GET /api/logs/stats
        """
        try:
            result = controller.get_log_statistics()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @log_bp.route('/chart/over-time', methods=['GET'])
    @token_required
    def get_logs_over_time(current_user):
        """
        Get logs over time for chart
        GET /api/logs/chart/over-time?hours=24
        """
        try:
            hours = int(request.args.get('hours', 24))
            result = controller.get_logs_over_time(hours)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @log_bp.route('/chart/by-type', methods=['GET'])
    @token_required
    def get_events_by_type(current_user):
        """
        Get events grouped by type for chart
        GET /api/logs/chart/by-type
        """
        try:
            result = controller.get_events_by_type()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    return log_bp
