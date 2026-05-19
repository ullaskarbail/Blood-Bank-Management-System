import pytest
from app import app, get_db_connection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DB_NAME'] = 'blood_bank'  # using dev db for simple testing
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert b'Blood Bank Management System' in response.data

def test_register_page_loads(client):
    response = client.get('/register')
    assert b'Register' in response.data

def test_request_blood_loads(client):
    response = client.get('/request_blood')
    assert b'Request Blood' in response.data

def test_search_loads(client):
    response = client.get('/search')
    assert b'Search Blood' in response.data

def test_donor_dashboard_auth(client):
    response = client.get('/donor_dashboard', follow_redirects=True)
    assert b'Login' in response.data # should redirect to login if not logged in
