from typing import Annotated
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup
from fastapi import Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.model import Flores
from fast_zero.schemas import plantSchema

T_Session = Annotated[Session, Depends(get_session)]


def create_or_update_plant(planta: plantSchema, session: Session):
    db_plant = session.query(Flores).filter_by(nome=planta.nome).first()

    if db_plant:
        db_plant.classe = planta.classe
        db_plant.ordem = planta.ordem
        db_plant.nome_cientifico = planta.nome_cientifico
        db_plant.familia = planta.familia
        db_plant.genero = planta.genero
        session.commit()
        session.refresh(db_plant)
    else:
        db_plant = Flores(
            nome=planta.nome,
            nome_cientifico=planta.nome_cientifico,
            classe=planta.classe,
            ordem=planta.ordem,
            familia=planta.familia,
            genero=planta.genero,
        )
        session.add(db_plant)
        session.commit()
        session.refresh(db_plant)

    return db_plant


flores = open("flores.txt", "r+")


def extrair_informacoes(nome_cientifico, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    info = {"nome": unquote(url.split("/wiki/")[-1].replace("_", " ")), "nome cientifico": nome_cientifico,
            "classe": "null", "ordem": "null", "familia": "null", "genero": "null"}

    for td in soup.find_all("td"):
        if td.find("a") and "Classe" in td.get_text():
            proximo_td = td.find_next_sibling("td")
            if proximo_td and proximo_td.find("a"):
                info["classe"] = proximo_td.get_text(strip=True)

        elif td.find("a") and "Ordem" in td.get_text():
            proximo_td = td.find_next_sibling("td")
            if proximo_td and proximo_td.find("a"):
                info["ordem"] = proximo_td.get_text(strip=True)

        elif td.find("a") and "Família" in td.get_text():
            proximo_td = td.find_next_sibling("td")
            if proximo_td and proximo_td.find("a"):
                info["familia"] = proximo_td.get_text(strip=True)

        elif td.find("a") and "Género" in td.get_text():
            proximo_td = td.find_next_sibling("td")
            if proximo_td and proximo_td.find("a"):
                info["genero"] = proximo_td.get_text(strip=True)

    return info


session = next(get_session())

for linhas in flores:
    print(linhas.strip())
    link = f"https://pt.wikipedia.org/wiki/{linhas.strip()}"
    info = extrair_informacoes(linhas.strip(), link)
    planta_schema = plantSchema(
        nome=info["nome"],
        nome_cientifico=info["nome cientifico"],
        classe=info["classe"],
        ordem=info["ordem"],
        familia=info["familia"],
        genero=info["genero"]
    )

    create_or_update_plant(planta_schema, session)
