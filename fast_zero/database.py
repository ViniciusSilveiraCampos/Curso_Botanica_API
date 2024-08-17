from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


# Acessar o sessão do databse do SQL sem muita complicação.
def get_session(): # pragma: no cover
    with Session(engine) as session:
        yield session
