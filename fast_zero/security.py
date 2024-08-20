from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.model import User
from fast_zero.schemas import TokenData

pwd_context = PasswordHash.recommended()
oaut2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = 'sua-chave'
algorithm = 'HS256'
ACESS_TOKEN_EXPIRE_MINUTES = 30


# Sujar a senha
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Verificar se a senha limpa é a mesma do que a senha suja.
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    # Tempo de inspiração 30 minus após a criação do Token
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=ACESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encode_jwt = encode(to_encode, SECRET_KEY, algorithm=algorithm)
    return encode_jwt


# Função só para lguns serem capazes de alterar
def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oaut2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[algorithm])
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if not user:
        raise credentials_exception

    return user
