from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.model import Flores, User
from fast_zero.schemas import plantSchema, Message, UserPlantPublic, UserListPlants
from fast_zero.security import get_current_user

router = APIRouter(
    prefix='/flores',
    tags=['flores']
)

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPlantPublic)
def create_flower(planta: plantSchema, session: T_Session):
    db_user = session.scalar(
        select(Flores).where(
            (Flores.nome == planta.nome)
        )
    )

    if db_user:
        if db_user.nome == planta.nome:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Essa flor já existe. 🥀',
            )

    db_user = Flores(
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
def read_flowers(session: T_Session, limit: int = 10, offset: int = 0):
    plan = session.scalars(
        select(Flores).limit(limit).offset(offset)
    ).all()
    return {'Plants': plan}


@router.get('/?classe={classe}&ordem={ordem)&familia={familia}&genero={genero}', response_model=UserListPlants)
def read_flower_by(
        session: T_Session,
        classe: str = None,
        ordem: str = None,
        familia: str = None,
        genero: str = None,
        limit: int = 10,
        offset: int = 0
):
    query = select(Flores)  # pragma: no cover

    if classe:  # pragma: no cover
        query = query.where(Flores.classe.ilike(f'%{classe}%'))  # pragma: no cover
    if ordem:  # pragma: no cover
        query = query.where(Flores.ordem.ilike(f'%{ordem}%'))  # pragma: no cover
    if familia:  # pragma: no cover
        query = query.where(Flores.familia.ilike(f'%{familia}%'))  # pragma: no cover
    if genero:  # pragma: no cover
        query = query.where(Flores.genero.ilike(f'%{genero}%'))  # pragma: no cover

    plan = session.scalars(query.limit(limit).offset(offset)).all()  # pragma: no cover

    return {'Plants': plan}  # pragma: no cover


@router.get('/{plant_id}', response_model=UserPlantPublic)
def read_flower(session: T_Session, plant_id: int):
    db_plant = session.scalar(
        select(Flores).where(Flores.id == plant_id)
    )
    if not db_plant:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Flor não encontrada. 🥀"
        )
    session.commit()
    return db_plant


@router.put('/{plant_id}', response_model=UserPlantPublic, )
def update_flower(session: T_Session,
                  planta: plantSchema,
                  plant_id: int):
    plant_to_update = session.get(Flores, plant_id)

    if not plant_to_update:
        raise HTTPException(status_code=404, detail='A flor não existe, ela não foi encontrada. 🥀')

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
def delete_flower(session: T_Session, plant_id: int):
    planta = session.query(Flores).filter(Flores.id == plant_id).first()
    if not planta:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Flor não encontrada. 🥀"
        )
    session.delete(planta)
    session.commit()

    return {"message": "A flor foi deletada ✂️"}
