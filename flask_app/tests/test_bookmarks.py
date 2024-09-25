import pytest


@pytest.mark.parametrize(('url', 'status'), (
    ('http://localhost:5000/api/like', 200),
    ('http://localhost:5000/api/bookmark', 200),
))
def test_bookmark_insert(client, auth, url, status):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.post(
        '/api/bookmark',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'url': url}
    )
    assert response.status_code == status


def test_bookmark_get(client, auth):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.get(
        '/api/bookmark',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'url': ''}
    )
    assert response.status_code == 200
    assert len(response.json) == 2


@pytest.mark.parametrize(('url', 'status'), (
    ('http://localhost:5000/api/like', 200),
    ('http://localhost:5000/api/bookmark', 200),
))
def test_delete_bookmark_insertions(client, auth, url, status):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.delete(
        '/api/bookmark',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'url': url}
    )
    assert response.status_code == status
