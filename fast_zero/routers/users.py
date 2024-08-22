from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.model import User
from fast_zero.schemas import Message, UserSchema, UserPublic, UserList
from fast_zero.security import get_password_hash, get_current_user


router = APIRouter(
    prefix='/usuarios',
    tags=['usuarios']
)
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=UserList)
def read_users(session: T_Session, limit: int = 10, offset: int = 0):
    user = session.scalars(
        select(User).limit(limit).offset(offset)
    )
    return {'users': user}


# Criar um usuario
@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='O nome do usuario já existe!',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='O email do usuario já existe!',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


# Ler os usuarios

@router.get('/{user_id}', response_model=UserPublic)
def read_user(session: T_Session, user_id: int):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado."
        )

    session.commit()
    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(session: T_Session, user_id: int, user: UserSchema, current_user: T_CurrentUser):

    user_to_update = session.get(User, user_id)

    if not user_to_update:
        raise HTTPException(status_code=404, detail='Usuario não encontrado.')

    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail='Sem permissão o suficiente')

    user_to_update.email = user.email
    user_to_update.username = user.username
    user_to_update.password = get_password_hash(user.password)

    session.commit()
    session.refresh(user_to_update)

    return user_to_update


@router.delete('/{user_id}', response_model=Message)
def delete_user(session: T_Session, user_id: int, current_user: T_CurrentUser):
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail='Usuario não encontrado.')

    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail='Sem permissão o suficiente')

    session.delete(user)
    session.commit()

    return {"message": "Usuario deletado"}
