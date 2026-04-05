"""
Alert API Routes
Handles HTTP endpoints for alert operations
"""

from flask import Blueprint, request, jsonify
from controllers.alert_controller import AlertController
from middleware.auth_middleware import token_required

def create_alert_routes(db):
    """Create and configure alert routes"""
    
    alert_bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')
    controller = AlertController(db)
    
    @alert_bp.route('', methods=['GET'])
    @token_required
    def get_alerts(current_user):
        """
        Get alerts with filtering and pagination
        GET /api/alerts?page=1&page_size=100&status=open&severity=high
        """
        try:
            # Get query parameters
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 100))
            sort_by = request.args.get('sort_by', 'timestamp')
            sort_order = request.args.get('sort_order', 'desc')
            
            # Build filters
            filters = {}
            if request.args.get('status'):
                filters['status'] = request.args.get('status')
            if request.args.get('severity'):
                filters['severity'] = request.args.get('severity')
            if request.args.get('ip_address'):
                filters['ip_address'] = request.args.get('ip_address')
            
            result = controller.get_alerts(
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
    
    @alert_bp.route('/stats', methods=['GET'])
    @token_required
    def get_statistics(current_user):
        """
        Get alert statistics
        GET /api/alerts/stats
        """
        try:
            result = controller.get_alert_statistics()
            return jsonify(result), 200
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    @alert_bp.route('/<alert_id>/status', methods=['PATCH'])
    @token_required
    def update_status(current_user, alert_id):
        """
        Update alert status
        PATCH /api/alerts/<id>/status
        Body: {"status": "resolved"}
        """
        try:
            data = request.get_json()
            
            if not data or 'status' not in data:
                return jsonify({
                    'success': False,
                    'message': 'Status not provided'
                }), 400
            
            result = controller.update_alert_status(alert_id, data['status'])
            
            if result['success']:
                return jsonify(result), 200
            else:
                return jsonify(result), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 500
    
    return alert_bp
