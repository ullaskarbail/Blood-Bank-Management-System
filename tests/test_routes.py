def test_public_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Give the gift of' in response.data

def test_login_page_loads(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Admin Login' in response.data

def test_protected_dashboard_redirects(client):
    response = client.get('/dashboard')
    assert response.status_code == 302 # Redirect to login

def test_public_request_page_loads(client, mocker):
    # Mock db connection to return empty hospitals list
    mock_conn = mocker.patch('app.routes.requests.get_db_connection')
    mock_cur = mock_conn.return_value.cursor.return_value
    mock_cur.fetchall.return_value = []
    
    response = client.get('/requests/public')
    assert response.status_code == 200
    assert b'Blood Request Form' in response.data
