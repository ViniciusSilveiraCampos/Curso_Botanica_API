from pydantic import BaseModel, EmailStr, ConfigDict, validator


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    message: str


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class plantSchema(BaseModel):
    nome: str
    nome_cientifico: str
    classe: str
    ordem: str
    familia: str
    genero: str

    @validator('*', pre=True)
    def sanitize_fields(cls, v):
        if isinstance(v, str):
            return ' '.join(v.strip().lower().split())
        return v  # pragma: no cover


class UserPlantPublic(BaseModel):
    id: int
    nome: str
    nome_cientifico: str
    classe: str
    ordem: str
    familia: str
    genero: str
    model_config = ConfigDict(from_attributes=True)


class UserListPlants(BaseModel):
    Plants: list[UserPlantPublic]  # Esta chave deve corresponder à chave no retorno do endpoint




class UserFlowerPublic(BaseModel):
    id: int
    nome: str
    nome_cientifico: str
    classe: str
    ordem: str
    familia: str
    genero: str
    model_config = ConfigDict(from_attributes=True)


class UserListFlower(BaseModel):
    Plants: list[UserFlowerPublic]
