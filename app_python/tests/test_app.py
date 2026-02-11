import pytest
import json
from datetime import datetime, timezone
from app import app, get_system_info, get_uptime, app_start_time


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client



def test_main_endpoint_status_code(client):
    """Test that main endpoint returns 200 OK"""
    response = client.get('/')
    assert response.status_code == 200


def test_main_endpoint_returns_json(client):
    """Test that main endpoint returns JSON"""
    response = client.get('/')
    assert response.content_type == 'application/json'


def test_main_endpoint_fields(client):
    """Test that main endpoint has all required top-level fields"""
    response = client.get('/')
    data = json.loads(response.data)
    
    required_fields = ['service', 'system', 'runtime', 'request', 'endpoints']
    for field in required_fields:
        assert field in data


def test_main_endpoint_service_info(client):
    """Test service metadata fields"""
    response = client.get('/')
    data = json.loads(response.data)
    service = data['service']
    
    assert service['name'] == 'devops-info-service'
    assert service['version'] == '1.0.0'
    assert service['description'] == 'DevOps course info service'
    assert service['framework'] == 'Flask'


def test_main_endpoint_system_info(client):
    """Test system information fields"""
    response = client.get('/')
    data = json.loads(response.data)
    system = data['system']
    
    required_fields = ['hostname', 'platform', 'platform_version', 
                      'architecture', 'cpu_count', 'python_version']
    for field in required_fields:
        assert field in system
        assert system[field] is not None


def test_main_endpoint_runtime(client):
    """Test runtime fields"""
    response = client.get('/')
    data = json.loads(response.data)
    runtime = data['runtime']
    
    assert 'uptime_seconds' in runtime
    assert 'uptime_human' in runtime
    assert 'current_time' in runtime
    assert 'timezone' in runtime
    assert runtime['timezone'] == 'UTC'


def test_main_endpoint_request_info(client):
    """Test request information fields"""
    response = client.get('/')
    data = json.loads(response.data)
    request_info = data['request']
    
    assert 'client_ip' in request_info
    assert 'user_agent' in request_info
    assert 'method' in request_info
    assert 'path' in request_info
    assert request_info['method'] == 'GET'
    assert request_info['path'] == '/'


def test_main_endpoint_endpoints_list(client):
    """Test that endpoints list contains required endpoints"""
    response = client.get('/')
    data = json.loads(response.data)
    endpoints = data['endpoints']
    
    paths = [e['path'] for e in endpoints]
    assert '/' in paths
    assert '/health' in paths


def test_health_endpoint_status_code(client):
    """Test that health endpoint returns 200 OK"""
    response = client.get('/health')
    assert response.status_code == 200


def test_health_endpoint_returns_json(client):
    """Test that health endpoint returns JSON"""
    response = client.get('/health')
    assert response.content_type == 'application/json'


def test_health_endpoint_status(client):
    """Test health endpoint returns healthy status"""
    response = client.get('/health')
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_health_endpoint_timestamp(client):
    """Test health endpoint timestamp is valid ISO format"""
    response = client.get('/health')
    data = json.loads(response.data)
    timestamp = data['timestamp']
    
    # Try to parse it - should not raise exception
    datetime.fromisoformat(timestamp.replace('Z', '+00:00'))


def test_health_endpoint_uptime(client):
    """Test health endpoint has uptime_seconds"""
    response = client.get('/health')
    data = json.loads(response.data)
    assert 'uptime_seconds' in data
    assert isinstance(data['uptime_seconds'], int)


def test_404_error_handler(client):
    """Test 404 error returns JSON with proper message"""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    data = json.loads(response.data)
    
    assert data['error'] == 'Not Found'
    assert 'message' in data
    assert data['path'] == '/nonexistent-endpoint'



def test_get_system_info_fields():
    """Test that get_system_info returns all required fields"""
    info = get_system_info()
    
    required_fields = ['hostname', 'platform', 'platform_version', 
                      'architecture', 'cpu_count', 'python_version']
    for field in required_fields:
        assert field in info


def test_get_uptime_format():
    """Test that uptime human format is string"""
    uptime = get_uptime()
    assert 'seconds' in uptime
    assert 'human' in uptime
    assert isinstance(uptime['human'], str)
    assert isinstance(uptime['seconds'], int)

