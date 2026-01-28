import os
import socket
import platform
import logging
from datetime import datetime, timezone, timedelta
from flask import Flask, jsonify, request

# Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '5000'))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Application Setup
app = Flask(__name__)
app_start_time = datetime.now(timezone.utc)

# Logging Configuration
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Helper Functions
def get_system_info():
    """Collect comprehensive system information."""
    return {
        'hostname': socket.gethostname(),
        'platform': platform.system(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'cpu_count': os.cpu_count() or 0,
        'python_version': platform.python_version()
    }

def get_uptime():
    """Calculate application uptime in seconds and human-readable format."""
    delta = datetime.now(timezone.utc) - app_start_time
    seconds = int(delta.total_seconds())
    
    # Calculate human-readable format
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    human_parts = []
    if days > 0:
        human_parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        human_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        human_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0 or not human_parts:
        human_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return {
        'seconds': seconds,
        'human': ', '.join(human_parts)
    }

# Application Endpoints
@app.route('/')
def main_endpoint():
    """Main endpoint returning service and system information."""
    logger.info(f"Main endpoint accessed by {request.remote_addr}")
    
    return jsonify({
        'service': {
            'name': 'devops-info-service',
            'version': '1.0.0',
            'description': 'DevOps course info service',
            'framework': 'Flask'
        },
        'system': get_system_info(),
        'runtime': {
            'uptime_seconds': get_uptime()['seconds'],
            'uptime_human': get_uptime()['human'],
            'current_time': datetime.now(timezone.utc).isoformat(),
            'timezone': 'UTC'
        },
        'request': {
            'client_ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'Unknown'),
            'method': request.method,
            'path': request.path
        },
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Service information'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'}
        ]
    })

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring and probes."""
    logger.debug(f"Health check from {request.remote_addr}")
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'uptime_seconds': get_uptime()['seconds']
    }), 200

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {request.path}")
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist',
        'path': request.path
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {str(error)}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500

# Application Entry Point
if __name__ == '__main__':
    logger.info(f"Starting DevOps Info Service on {HOST}:{PORT}")
    logger.info(f"Debug mode: {DEBUG}")
    app.run(host=HOST, port=PORT, debug=DEBUG)