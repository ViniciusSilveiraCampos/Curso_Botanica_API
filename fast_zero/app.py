from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select

from fast_zero.database import get_session
from fast_zero.model import User
from fast_zero.schemas import Message, UserSchema, UserPublic, UserList

app = FastAPI()


# Teste da API
@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


# Criar um usuario
@app.post('/usuarios/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    # Verificar se o usuario já existe.
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email))
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='O nome do usuario já existe!'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='O email do usuario já existe!')
    db_user = User(username=user.username, email=user.email, password=user.password)
    # Caso não tenha dado nenhum erro podemos registrar deentro da base de dados

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# Ler os usuarios
@app.get('/usuarios/', response_model=UserList)
def read_users(limit: int = 10, offset: int = 0, session=Depends(get_session)):
    user = session.scalars(
        select(User).limit(limit).offset(offset)
    )
    return {'users': user}


@app.get('/usuarios/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado."
        )

    session.commit()
    return db_user


# Verificar a existencia e atualizar o usuario existente
@app.put('/usuarios/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado."
        )

    db_user.email = user.email
    db_user.username = user.username
    db_user.password = user.password

    session.commit()
    session.refresh(db_user)

    return db_user


# Verificar a existencia e deletar o usuario existente
@app.delete('/usuarios/{user_id}', response_model=Message)
def delete_user(user_id: int, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Usuario não encontrado."

        )
    session.delete(db_user)
    session.commit()
    return {'message': 'Usuario deletado'}
