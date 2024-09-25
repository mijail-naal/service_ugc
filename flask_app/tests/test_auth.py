def test_methods(client):
    assert client.get('/login').status_code == 405
    response = client.post(
        '/login',
        json={'username': 'username', 'password': 'password'},
    )
    assert response.status_code == 401


def test_login(auth):
    response = auth.login('user', '123')
    assert response.json['msg'] == 'Bad username or password'
    assert auth.login().status_code == 200
