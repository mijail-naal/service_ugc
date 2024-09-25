import pytest


def test_api_like_methods(client):
    assert client.get('/api/like').status_code == 401
    response = client.post(
        '/api/like',
        json=''
    )
    assert response.status_code == 401
    assert client.put('/api/like').status_code == 401
    assert client.delete('/api/like').status_code == 401


def test_like_authorization_required(client):
    response = client.post(
        '/api/like',
        json={'film_id': 'c498a816-92f2-4157-a332-885d729f4be2', 'like': 'True'}
    )
    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'


@pytest.mark.parametrize(('film_id', 'like', 'status'), (
    ('c498a816-92f2-4157-a332-885d729f4be2', 'True', 200),
    ('c498a816-92f2-4157-a332-885d729f4be4', True, 200),
))
def test_like_insert(client, auth, film_id, like, status):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.post(
        '/api/like',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'film_id': str(film_id), 'like': like}
    )
    assert response.status_code == status


@pytest.mark.parametrize(('film_id', 'like'), (
    ('c498a816-92f2-4157-a332-885d729f4be2', ''),
    ('c498a816-92f2-4157-a332-885d729f4be4', ''),
))
def test_like_get(client, auth, film_id, like):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.get(
        '/api/like',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'film_id': str(film_id), 'like': like}
    )
    assert response.json is True


@pytest.mark.parametrize(('film_id', 'like', 'status'), (
    ('c498a816-92f2-4157-a332-885d729f4be2', 'True', 200),
    ('c498a816-92f2-4157-a332-885d729f4be4', True, 200),
))
def test_delete_like_insertions(client, auth, film_id, like, status):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.delete(
        '/api/like',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'film_id': str(film_id), 'like': like}
    )
    assert response.status_code == status
