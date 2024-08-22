from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.model import Plantas, User
from fast_zero.schemas import plantSchema, Message, UserPlantPublic, UserListPlants
from fast_zero.security import get_current_user

router = APIRouter(
    prefix='/plantas',
    tags=['plantas']
)

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


# CRUD
@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPlantPublic)
def create_plant(planta: plantSchema, session: T_Session):
    db_user = session.scalar(
        select(Plantas).where(
            (Plantas.nome == planta.nome)
        )
    )

    if db_user:
        if db_user.nome == planta.nome:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Essa planta já existe. 🍂',
            )

    db_user = Plantas(
        nome=planta.nome,
        nome_cientifico=planta.nome_cientifico,
        classe=planta.classe,
        ordem=planta.ordem,
        familia=planta.familia,
        genero=planta.genero,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserListPlants)
def read_plants(session: T_Session, limit: int = 10, offset: int = 0):
    plan = session.scalars(
        select(Plantas).limit(limit).offset(offset)
    ).all()  # Convertendo para uma lista de objetos
    return {'Plants': plan}  # A chave precisa ser 'Plants' para ser consistente com o esquema


@router.get('/?classe={classe}&ordem={ordem)&familia={familia}&genero={genero}', response_model=UserListPlants)
def read_plants_by(
        session: T_Session,
        classe: str = None,
        ordem: str = None,
        familia: str = None,
        genero: str = None,
        limit: int = 10,
        offset: int = 0
):
    query = select(Plantas)  # pragma: no cover

    if classe:  # pragma: no cover
        query = query.where(Plantas.classe.ilike(f'%{classe}%'))  # pragma: no cover
    if ordem:  # pragma: no cover
        query = query.where(Plantas.ordem.ilike(f'%{ordem}%'))  # pragma: no cover
    if familia:  # pragma: no cover
        query = query.where(Plantas.familia.ilike(f'%{familia}%'))  # pragma: no cover
    if genero:  # pragma: no cover
        query = query.where(Plantas.genero.ilike(f'%{genero}%'))  # pragma: no cover

    plan = session.scalars(query.limit(limit).offset(offset)).all()  # pragma: no cover

    return {'Plants': plan}  # pragma: no cover


@router.get('/{plant_id}', response_model=UserPlantPublic)
def read_plant(session: T_Session, plant_id: int):
    db_plant = session.scalar(
        select(Plantas).where(Plantas.id == plant_id)
    )
    if not db_plant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Planta não encontrada. 🍂"
        )
    session.commit()
    return db_plant


@router.put('/{plant_id}', response_model=UserPlantPublic)
def update_planta(session: T_Session,
                  planta: plantSchema,
                  plant_id: int):
    plant_to_update = session.get(Plantas, plant_id)

    if not plant_to_update:
        raise HTTPException(status_code=404, detail='A planta não existe, ela não foi encontrada. 🍂')

    plant_to_update.nome = planta.nome
    plant_to_update.nome_cientifico = planta.nome_cientifico
    plant_to_update.classe = planta.classe
    plant_to_update.ordem = planta.ordem
    plant_to_update.familia = planta.familia
    plant_to_update.genero = planta.genero

    session.commit()
    session.refresh(plant_to_update)

    return plant_to_update


@router.delete('/{plant_id}', response_model=Message)
def delete_planta(session: T_Session, plant_id: int):
    planta = session.query(Plantas).filter(Plantas.id == plant_id).first()
    if not planta:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Planta não encontrada. 🍂"
        )
    session.delete(planta)
    session.commit()

    return {"message": "A planta foi deletada 🪓🪚"}
