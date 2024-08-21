import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.model import table_registry, User

from fast_zero.security import get_password_hash
import factory


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


@pytest.fixture
def client(session):
    # Tudo que depende do banco de dados em produção.
    # Durante o momento de teste será sobreescrito para a utilização da função de teste.
    def fake_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = fake_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:',
                           connect_args={'check_same_thread': False},
                           poolclass=StaticPool)
    # Definindo para que ele não crie uma nova thread ao testar
    # pois enquanto ele roda, ele está testando.
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture
def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user

@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def token_headers(client):
    # Cria um usuário de teste
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'secret',
    }
    client.post('/usuarios', json=user_data)

    # Autentica e obtém o token
    response = client.post('/token', data={
        'username': user_data['username'],
        'password': user_data['password'],
    })
    token = response.json().get('access_token')
    return {'Authorization': f'Bearer {token}'}



