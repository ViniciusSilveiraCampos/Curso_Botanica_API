from sqlalchemy import select

from fast_zero.model import User, Plantas


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    v_user = session.scalar(select(User).where(User.username == 'alice'))

    assert v_user.username == 'alice'


def test_create_planta(session):
    todo = Plantas(
        nome='Piúva',
        nome_cientifico="Handroanthus impetiginosus",
        classe='Dicotiledónea',
        ordem='Lamiales',
        familia='Bignoniaceae',
        genero='Handroanthus',
    )

    session.add(todo)
    session.commit()

    v_planta = session.scalar(select(Plantas).where(Plantas.nome == "Piúva"))

    assert v_planta.nome == 'Piúva'


def test_create_flor(session):
    todo = Plantas(
        nome='Piúva',
        nome_cientifico="Handroanthus impetiginosus",
        classe='Dicotiledónea',
        ordem='Lamiales',
        familia='Bignoniaceae',
        genero='Handroanthus',
    )

    session.add(todo)
    session.commit()

    v_planta = session.scalar(select(Plantas).where(Plantas.nome == "Piúva"))

    assert v_planta.nome == 'Piúva'
