import pytest


def test_api_methods(client):
    assert client.get('/api/create-topic').status_code == 405
    response = client.post(
        '/api/create-topic',
        json=''
    )
    assert response.status_code == 400
    assert response.json['message']['name'] == "Argument 'name' cannot be blank"


@pytest.mark.parametrize(('name', 'status'), (
    ('', 400),
    ('test-topic-name', 201),
    ('test topic name', 400),
))
def test_create_topic(client, name, status):
    response = client.post(
        '/api/create-topic',
        json={'name': name}
    )
    assert status == response.status_code


def test_delete_topic(client):
    response = client.delete(
        '/api/create-topic',
        json={'name': 'test-topic-name'}
    )
    assert response.status_code == 200 and response.json is True
