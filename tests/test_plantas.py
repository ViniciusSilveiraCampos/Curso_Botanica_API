from http import HTTPStatus

from fast_zero.schemas import UserPlantPublic


# Teste para criar uma planta
def test_create_plant(client):
    response = client.post(
        '/plantas/',
        json={
            'nome': 'Rosa',
            'nome_cientifico': 'Rosa spp.',
            'classe': 'Magnoliopsida',
            'ordem': 'rosales',
            'familia': 'Rosaceae',
            'genero': 'Rosa',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'rosa',
        'nome_cientifico': 'rosa spp.',
        'classe': 'magnoliopsida',
        'ordem': 'rosales',
        'familia': 'rosaceae',
        'genero': 'rosa',
    }


# Teste para criar uma planta com nome duplicado
def test_create_plant_nome_duplicado(client):
    response = client.post(
        '/plantas/',
        json={
            'nome': 'Rosa',
            'nome_cientifico': 'Rosa spp.',
            'classe': 'Magnoliopsida',
            'ordem': 'Rosales',
            'familia': 'Rosaceae',
            'genero': 'Rosa',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        '/plantas/',
        json={
            'nome': 'Rosa',
            'nome_cientifico': 'Rosa rubiginosa',
            'classe': 'Magnoliopsida',
            'ordem': 'Rosales',
            'familia': 'Rosaceae',
            'genero': 'Rosa',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Essa planta já existe. 🍂'}


def teste_leitura_plantas(client, planta):
    plant_schema = UserPlantPublic.model_validate(
        planta).model_dump()

    response = client.get('/plantas/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Plants': [plant_schema]}


def test_read_plant_nao_existente(client):
    response = client.get('/plantas/9999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Planta não encontrada. 🍂'}


def test_read_plant(client):
    user_data = {
        'nome': 'Cactos',
        'nome_cientifico': 'Cactaceae spp.',
        'classe': 'Magnoliopsida',
        'ordem': 'Caryophyllales',
        'familia': 'Cactaceae',
        'genero': 'Cactus',
    }
    create_response = client.post('/plantas/', json=user_data)
    assert create_response.status_code == HTTPStatus.CREATED

    user_id = create_response.json().get('id')

    response = client.get(f'/plantas/{user_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'nome': 'cactos',
        'nome_cientifico': 'cactaceae spp.',
        'classe': 'magnoliopsida',
        'ordem': 'caryophyllales',
        'familia': 'cactaceae',
        'genero': 'cactus',
        'id': user_id,
    }


def test_update_plant(client, planta, token):
    response = client.put(
        f'/plantas/{planta.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': 'Cactos',
            'nome_cientifico': 'Cactaceae spp.',
            'classe': 'Magnoliopsida',
            'ordem': 'Caryophyllales',
            'familia': 'Cactaceae',
            'genero': 'Cactus'
        },
    )

    assert response.json() == {
        'nome': 'cactos',
        'nome_cientifico': 'cactaceae spp.',
        'classe': 'magnoliopsida',
        'ordem': 'caryophyllales',
        'familia': 'cactaceae',
        'genero': 'cactus',
        'id': planta.id,
    }


def test_update_plant_nao_existente(client, token):
    response = client.put(
        '/plantas/9999',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'nome': 'Cactus',
            'nome_cientifico': 'Cactaceae spp.',
            'classe': 'Magnoliopsida',
            'ordem': 'Caryophyllales',
            'familia': 'Cactaceae',
            'genero': 'Cactus',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'A planta não existe, ela não foi encontrada. 🍂'}


def test_delete_plant(client):
    response = client.post(
        '/plantas/',
        json={
            'nome': 'Samambaia',
            'nome_cientifico': 'Nephrolepis exaltata',
            'classe': 'Polypodiopsida',
            'ordem': 'Polypodiales',
            'familia': 'Lomariopsidaceae',
            'genero': 'Nephrolepis',
        },
    )
    plant_id = response.json().get('id')

    response = client.delete(f'/plantas/{plant_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'A planta foi deletada 🪓🪚'}


def test_delete_plant_nao_existente(client):
    response = client.delete('/plantas/9999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Planta não encontrada. 🍂'}


def test_read_plants_by_classe(client, planta):
    response = client.get('/plantas/?classe=Magnoliopsida')

    assert response.status_code == HTTPStatus.OK

    expected_response = {
        'Plants': [
            {
                'id': planta.id,
                'nome': planta.nome,
                'nome_cientifico': planta.nome_cientifico,
                'classe': planta.classe,
                'ordem': planta.ordem,
                'familia': planta.familia,
                'genero': planta.genero,
            }
        ]
    }

    assert response.json() == expected_response


def test_read_plants_by_ordem(client, planta):
    response = client.get('/plantas/?ordem=Rosales')

    assert response.status_code == HTTPStatus.OK

    expected_response = {
        'Plants': [
            {
                'id': planta.id,
                'nome': planta.nome,
                'nome_cientifico': planta.nome_cientifico,
                'classe': planta.classe,
                'ordem': planta.ordem,
                'familia': planta.familia,
                'genero': planta.genero,
            }
        ]
    }

    assert response.json() == expected_response


def test_read_plants_by_familia(client, planta):
    response = client.get('/plantas/?familia=Rosaceae')

    assert response.status_code == HTTPStatus.OK

    expected_response = {
        'Plants': [
            {
                'id': planta.id,
                'nome': planta.nome,
                'nome_cientifico': planta.nome_cientifico,
                'classe': planta.classe,
                'ordem': planta.ordem,
                'familia': planta.familia,
                'genero': planta.genero,
            }
        ]
    }

    assert response.json() == expected_response


def test_read_plants_by_genero(client, planta):
    response = client.get('/plantas/?genero=Rosa')

    assert response.status_code == HTTPStatus.OK

    expected_response = {
        'Plants': [
            {
                'id': planta.id,
                'nome': planta.nome,
                'nome_cientifico': planta.nome_cientifico,
                'classe': planta.classe,
                'ordem': planta.ordem,
                'familia': planta.familia,
                'genero': planta.genero,
            }
        ]
    }

    assert response.json() == expected_response


def test_read_plants_no_filters(client, planta):
    response = client.get('/plantas/')

    assert response.status_code == HTTPStatus.OK

    expected_response = {
        'Plants': [
            {
                'id': planta.id,
                'nome': planta.nome,
                'nome_cientifico': planta.nome_cientifico,
                'classe': planta.classe,
                'ordem': planta.ordem,
                'familia': planta.familia,
                'genero': planta.genero,
            }
        ]
    }

    assert response.json() == expected_response


def test_read_plants_with_no_matches(client):
    response = client.get('/plantas/?classe=NonExistentClass')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Plants': []}
