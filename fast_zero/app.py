from fastapi import FastAPI

from fast_zero.schemas import Message
from fast_zero.routers import users, auth, plantas, flores

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(plantas.router)
app.include_router(flores.router)


# Teste da API

@app.get('/', response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
