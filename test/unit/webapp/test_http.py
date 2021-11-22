import pytest
import json
from app import create_app

"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.

"""

@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """
    #app.config['TESTING'] = True
    local_app = create_app()
    client = local_app.test_client()

    yield client

def test_root_endpoint(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert 'Hello World!' in html
    assert landing.status_code == 200

def test_get_temperature(client):
    request = client.get("/temperature")
    assert request.status_code == 405

def test_set_temperature(client):
    payload = {'temp': 100}
    rv = client.post('/temperature', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Temperature succesfully recorded"