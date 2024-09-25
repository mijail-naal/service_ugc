import pytest


@pytest.mark.parametrize(('film_id', 'created_at', 'user_review'), (
    ('71fdfc7a-49ea-43e7-9755-d7a0ae4ff208', '01/02/2024 00:00:00', 'Some text'),
    ('d1be6e21-7eff-4ac4-af59-0791a3be9e37', '05/06/2024 00:00:00', 'Other text'),
))
def test_review_insert(client, auth, film_id, created_at, user_review):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.post(
        '/api/review',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'film_id': film_id, 'created_at': created_at, 'user_review': user_review}
    )
    assert response.status_code == 200


@pytest.mark.parametrize(('film_id', 'created_at', 'user_review'), (
    ('71fdfc7a-49ea-43e7-9755-d7a0ae4ff208', '01/02/2024 00:00:00', 'Some text and more'),
    ('d1be6e21-7eff-4ac4-af59-0791a3be9e37', '05/06/2024 00:00:00', 'Other text and more'),
))
def test_review_put(client, auth, film_id, created_at, user_review):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.put(
        '/api/review',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'film_id': film_id, 'created_at': created_at, 'user_review': user_review}
    )
    assert response.status_code == 200


def test_review_get(client, auth):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.get(
        '/api/review',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'film_id': 'd1be6e21-7eff-4ac4-af59-0791a3be9e37', 'created_at': '', 'user_review': ''}
    )
    assert response.status_code == 200
    assert len(response.json) == 4


@pytest.mark.parametrize(('film_id', 'created_at', 'user_review'), (
    ('71fdfc7a-49ea-43e7-9755-d7a0ae4ff208', '', ''),
    ('d1be6e21-7eff-4ac4-af59-0791a3be9e37', '', ''),
))
def test_delete_review_insertions(client, auth, film_id, created_at, user_review):
    login_response = auth.login()
    access_token = login_response.json['access_token']
    response = client.delete(
        '/api/review',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'film_id': film_id, 'created_at': created_at, 'user_review': user_review}
    )
    assert response.status_code == 200
