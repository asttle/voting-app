import pytest
import json
from app import app, get_redis

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    with app.test_client() as client:
        with app.app_context():
            # Ensure Redis is flushed before each test
            get_redis().flushdb()
        yield client

def test_get_home_page(client):
    """Test GET request to home page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Cats' in response.data or b'Dogs' in response.data

def test_post_vote(client):
    """Test POST request to submit a vote."""
    response = client.post('/', data={'vote': 'Cats'})
    assert response.status_code == 200

    # Check if the vote was stored in Redis
    redis = get_redis()
    votes = redis.lrange('votes', 0, -1)
    assert len(votes) == 1

    vote_data = json.loads(votes[0])
    assert vote_data['vote'] == 'Cats'