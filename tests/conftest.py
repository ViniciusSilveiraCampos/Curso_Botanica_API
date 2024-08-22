import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.model import Plantas, Flores
from fast_zero.model import table_registry, User
from fast_zero.security import get_password_hash


class FlowerFactory(factory.Factory):
    class Meta:
        model = Flores

    nome = factory.Sequence(lambda n: f'Planta{n}')
    nome_cientifico = factory.Sequence(lambda n: f'Nome_cientifico{n}')
    classe = 'Magnoliopsida'
    ordem = 'Caryophyllales'
    familia = 'Cactaceae'
    genero = "Teste"


class PlantFactory(factory.Factory):
    class Meta:
        model = Plantas

    nome = factory.Sequence(lambda n: f'Planta{n}')
    nome_cientifico = factory.Sequence(lambda n: f'Nome_cientifico{n}')
    classe = 'Magnoliopsida'
    ordem = 'Caryophyllales'
    familia = 'Cactaceae'
    genero = "Teste"


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


@pytest.fixture
def client(session):
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
def planta(session):
    planta = PlantFactory()

    session.add(planta)
    session.commit()
    session.refresh(planta)

    return planta


@pytest.fixture
def other_planta(session):
    v_planta = PlantFactory()

    session.add(v_planta)
    session.commit()
    session.refresh(v_planta)

    return v_planta


@pytest.fixture
def other_user(session):
    password = 'testtest'
    v_user = UserFactory(password=get_password_hash(password))

    session.add(v_user)
    session.commit()
    session.refresh(v_user)

    v_user.clean_password = 'testtest'

    return v_user

@pytest.fixture
def flor(session):
    v_flor = FlowerFactory()

    session.add(v_flor)
    session.commit()
    session.refresh(v_flor)

    return v_flor


@pytest.fixture
def other_flor(session):
    v_flor = FlowerFactory()

    session.add(v_flor)
    session.commit()
    session.refresh(v_flor)

    return v_flor


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

    response = client.post('/token', data={
        'username': user_data['username'],
        'password': user_data['password'],
    })
    v_token = response.json().get('access_token')
    return {'Authorization': f'Bearer {v_token}'}
