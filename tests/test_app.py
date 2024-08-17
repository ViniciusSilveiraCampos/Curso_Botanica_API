from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200


# re
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
    # Primeiro cria o usuário com o username 'alice'
    response = client.post(
        '/usuarios/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    # Tenta criar outro usuário com o mesmo username 'alice'
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
    # Primeiro cria o usuário com o username 'alice'
    response = client.post(
        '/usuarios/',
        json={
            'username': 'Renato',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    # Tenta criar outro usuário com o mesmo email
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
    # Converser o objeto(SQL Alch) do usuario em UserPublic (Pydantic)
    user_schema = UserPublic.validate(user).model_dump()

    response = client.get('/usuarios/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/usuarios/1',
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


def test_delete_user(client, user):
    response = client.delete('/usuarios/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Usuario deletado'}


# Criar testes para os erros 404 (Not Found) nos endpoints de PUT e DELETE.
def test_put_user_not_found(client, user):
    response = client.put(
        '/usuarios/999',  # 999 é um ID que não existe no banco de dados
        json={
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'new_password',
        },
    )
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuario não encontrado.'}


def test_delete_user_not_found(client, user):
    response = client.delete('/usuarios/999')  # 999 é um ID que não existe no banco de dados
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuario não encontrado.'}


#Criar os testes para esse endpoint GET.
def test_read_user_not_found(client, user):
    response = client.get('/usuarios/999')  # 999 é um ID que não existe no banco de dados
    assert response.status_code == 404
    assert response.json() == {'detail': 'Usuario não encontrado.'}


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
