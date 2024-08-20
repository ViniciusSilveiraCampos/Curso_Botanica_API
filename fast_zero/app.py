from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy import select

from fast_zero.security import get_password_hash, verify_password, create_access_token, get_current_user
from fast_zero.database import get_session
from fast_zero.model import User
from fast_zero.schemas import Message, UserSchema, UserPublic, UserList, Token

app = FastAPI()


# Teste da API
@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


# Criar um usuario
@app.post('/usuarios/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
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
def update_user(user_id: int, user: UserSchema, session=Depends(get_session), current_user=Depends(get_current_user)):
    # Verifica se o usuário existe na base de dados
    user_to_update = session.get(User, user_id)

    if not user_to_update:
        raise HTTPException(status_code=404, detail='Usuario não encontrado.')

    # Se não for a mesma pessoa, não pode ser alterado.
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail='Sem permissão o suficiente')

    user_to_update.email = user.email
    user_to_update.username = user.username
    user_to_update.password = get_password_hash(user.password)

    session.commit()
    session.refresh(user_to_update)

    return user_to_update


# Verificar a existencia e deletar o usuario existente
@app.delete('/usuarios/{user_id}', response_model=Message)
def delete_user(user_id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail='Usuario não encontrado.')

    # Se não for a mesma pessoa, não pode ser alterado.
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail='Sem permissão o suficiente')

    session.delete(user)
    session.commit()

    return {"message": "Usuario deletado"}


@app.post('/token', response_model=Token)
def login_for_acess_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.email == form_data.username)
    )
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail="Sua senha ou o seu email estão errados."
        )
    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
