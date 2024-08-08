from fastapi import FastAPI, HTTPException
from http import HTTPStatus
from fast_zero.schemas import Message, UserSchema, UserPublic, UserDB, UserList

app = FastAPI()

database = []


# Teste da API
@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


# Criar um usuario
@app.post('/usuarios/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


# Ler os usuarios
@app.get('/usuarios/', response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/usuarios/{user_id}', response_model=UserPublic)
def read_user(user_id: int):
    for user in database:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")


# Verificar a existencia e atualizar o usuario existente
@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


# Verificar a existencia e deletar o usuario existente
@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
