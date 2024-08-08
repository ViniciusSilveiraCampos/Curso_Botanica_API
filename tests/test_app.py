from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200


def test_create_user(client):
    response = client.post(
        '/usuarios/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/usuarios/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'id': 1, }]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# Criar testes para os erros 404 (Not Found) nos endpoints de PUT e DELETE.
def test_put_user_not_found(client):
    response = client.put(
        '/usuarios/999',  # 999 é um ID que não existe no banco de dados
        json={
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'new_password',
        },
    )
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}


def test_delete_user_not_found(client):
    response = client.delete('/usuarios/999')  # 999 é um ID que não existe no banco de dados
    assert response.status_code == 405
    assert response.json() == {'detail': 'Method Not Allowed'}


#Criar os testes para esse endpoint GET.
def test_read_user_not_found(client):
    response = client.get('/usuarios/999')  # 999 é um ID que não existe no banco de dados
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user(client):
    # Primeiro cria um usuário para garantir que ele exista no banco de dados
    client.post(
        '/usuarios',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    # Pega o usuário criado
    response = client.get('/usuarios/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }
