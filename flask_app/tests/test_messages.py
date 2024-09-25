import pytest


def test_api_message_methods(client):
    assert client.get('/api/message').status_code == 405
    response = client.post(
        '/api/message',
        json=''
    )
    assert response.status_code == 401


def test_authorization_required(client):
    response = client.post(
        '/api/message',
        json={'topic': 'test-topic-name', 'value': 'some_message'}
    )
    assert response.status_code == 401
    assert response.json['msg'] == 'Missing Authorization Header'


@pytest.mark.parametrize(('topic', 'value', 'status'), (
    ('test-messages', 'CLICK-description-00:00:00-00:00:00-00:00:00', 200),
    ('no-exists_topic', '', 400),
    ('test_topic', '', 400),
    ('', '', 400),
    ('test-messages', 'VIEW-description-00:00:00-00:00:00-00:00:00', 200),
))
def test_send_message(client, auth, topic, value, status):
    login_response = auth.login()
    client.post('/api/create-topic', json={'name': 'test-messages'})
    access_token = login_response.json['access_token']
    response = client.post(
        '/api/message',
        headers={'Authorization': f'Bearer {access_token}'},
        json={'topic': f'{topic}', 'value': f'{value}'}
    )
    assert response.status_code == status


def test_delete_topic_and_messages(client):
    response = client.delete(
        '/api/create-topic',
        json={'name': 'test-messages'}
    )
    assert response.status_code == 200 and response.json is True
