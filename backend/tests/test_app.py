import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_register_voter():
    response = client.post('/register', json={'id': '1', 'name': 'Alice', 'eligible': True})
    assert response.status_code == 200
    assert response.json() == {'id': '1', 'name': 'Alice', 'eligible': True}


def test_cast_vote():
    client.post('/register', json={'id': '1', 'name': 'Alice', 'eligible': True})
    response = client.post('/vote', json={'voter_id': '1', 'candidate': 'Bob'})
    assert response.status_code == 200
    assert response.json() == {'voter_id': '1', 'candidate': 'Bob'}


def test_get_results():
    response = client.get('/results')
    assert response.status_code == 200
    assert isinstance(response.json(), list)