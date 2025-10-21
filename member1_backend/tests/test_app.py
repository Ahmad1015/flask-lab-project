import pytest
from app import app

def test_homepage():
    response = app.test_client().get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'app_name' in data
    assert data['app_name'] == 'Flask Lab Project'

def test_health_check():
    response = app.test_client().get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'OK'

def test_post_data():
    test_payload = {'name': 'Test User', 'value': 123}
    response = app.test_client().post('/data', json=test_payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Data submitted successfully'
    assert data['data_received'] == test_payload

def test_get_data():
    response = app.test_client().get('/data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_entries' in data
    assert isinstance(data['data'], list)

def test_get_data_by_id():
    # First, submit data
    test_payload = {'name': 'ID Test', 'value': 456}
    post_response = app.test_client().post('/data', json=test_payload)
    entry_id = post_response.get_json()['entry_id']
    # Now, retrieve by ID
    get_response = app.test_client().get(f'/data/{entry_id}')
    assert get_response.status_code == 200
    entry = get_response.get_json()
    assert entry['id'] == entry_id
    assert entry['data'] == test_payload

def test_404():
    response = app.test_client().get('/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Endpoint not found'

def test_post_data_invalid_content_type():
    response = app.test_client().post('/data', data='not json', content_type='text/plain')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_post_data_no_data():
    response = app.test_client().post('/data', json=None)
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_get_data_by_id_not_found():
    response = app.test_client().get('/data/99999')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Data entry not found'