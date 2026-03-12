# Application Endpoints
@app.route('/')
def main_endpoint():
    """Main endpoint returning service and system information."""
    logger.info('Main endpoint accessed')
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
    logger.debug('Health check performed')
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'uptime_seconds': get_uptime()['seconds']
    }), 200

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    logger.warning('404 Not Found', extra={
        'path': request.path,
        'method': request.method
    })
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist',
        'path': request.path
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error('500 Internal Server Error', exc_info=True, extra={
        'path': request.path,
        'method': request.method
    })
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500

# Application Entry Point
if name == 'main':
    logger.info('Application starting', extra={
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })
    app.run(host=HOST, port=PORT, debug=DEBUG)
