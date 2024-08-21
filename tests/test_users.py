from http import HTTPStatus

from fast_zero.schemas import UserPublic


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


def test_create_user_username_duplicado(client):
    response = client.post(
        '/usuarios/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        '/usuarios/',
        json={
            'username': 'alice',
            'email': 'different@example.com',
            'password': 'anothersecret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'O nome do usuario já existe!'}


def test_create_user_email_duplicado(client):
    response = client.post(
        '/usuarios/',
        json={
            'username': 'Renato',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        '/usuarios/',
        json={
            'username': 'fulano',
            'email': 'alice@example.com',
            'password': 'anothersecret',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'O email do usuario já existe!'}


def teste_leitura_de_usarios_com_usuarios(client, user):
    user_schema = UserPublic.validate(user).model_dump()

    response = client.get('/usuarios/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, token):
    user_data = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }
    create_response = client.post('/usuarios/', json=user_data)
    assert create_response.status_code == HTTPStatus.CREATED

    user_id = create_response.json().get('id')

    response = client.get(f'/usuarios/{user_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': user_id,
    }


def test_read_user_not_found(client, token):
    response = client.get(
        '/usuarios/999',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuario não encontrado.'}


def test_update_user(client, user, token):
    response = client.put(
        f'/usuarios/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': user.id,
    }


def test_update_user_not_found(client, token):
    response = client.put(
        '/usuarios/999',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'new_username',
            'email': 'new_email@example.com',
            'password': 'new_password',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuario não encontrado.'}


def test_update_not_user(client, user, token):
    second_user_response = client.post(
        '/usuarios/',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'anothersecret',
        },
    )
    assert second_user_response.status_code == HTTPStatus.CREATED
    second_user_id = second_user_response.json().get('id')
    response = client.put(
        f'/usuarios/{second_user_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'new_bob',
            'email': 'new_bob@example.com',
            'password': 'new_password',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Sem permissão o suficiente'}


# Versão de teste do curso
def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/usuarios/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Sem permissão o suficiente'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/usuarios/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.json() == {'message': 'Usuario deletado'}


def test_delete_user_not_found(client, token):
    response = client.delete(
        '/usuarios/999',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuario não encontrado.'}


def test_delete_not_user(client, user, token):
    second_user_response = client.post(
        '/usuarios/',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'anothersecret',
        },
    )
    assert second_user_response.status_code == HTTPStatus.CREATED
    second_user_id = second_user_response.json().get('id')

    response = client.delete(
        f'/usuarios/{second_user_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Sem permissão o suficiente'}
