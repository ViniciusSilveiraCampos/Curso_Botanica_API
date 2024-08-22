from http import HTTPStatus

from fast_zero.schemas import UserPlantPublic


# Teste para criar uma planta
def test_create_flores(client):
    response = client.post(
        '/flores/',
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
def test_create_flor_nome_duplicado(client):
    response = client.post(
        '/flores/',
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
        '/flores/',
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
    assert response.json() == {'detail': 'Essa flor já existe. 🥀'}


def teste_leitura_flores(client, flor):
    plant_schema = UserPlantPublic.model_validate(
        flor).model_dump()

    response = client.get('/flores/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Plants': [plant_schema]}


def test_read_flor_nao_existente(client):
    response = client.get('/flores/999999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Flor não encontrada. 🥀'}


def test_read_flor(client):
    user_data = {
        'nome': 'Cactos',
        'nome_cientifico': 'Cactaceae spp.',
        'classe': 'Magnoliopsida',
        'ordem': 'Caryophyllales',
        'familia': 'Cactaceae',
        'genero': 'Cactus',
    }
    create_response = client.post('/flores/', json=user_data)
    assert create_response.status_code == HTTPStatus.CREATED

    user_id = create_response.json().get('id')

    response = client.get(f'/flores/{user_id}')
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


def test_update_flor(client, flor, token):
    response = client.put(
        f'/flores/{flor.id}',
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
        'id': flor.id,
    }


def test_update_flor_nao_existente(client, token):
    response = client.put(
        '/flores/9999',
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
    assert response.json() == {'detail': 'A flor não existe, ela não foi encontrada. 🥀'}


def test_delete_flor(client):
    response = client.post(
        '/flores/',
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

    response = client.delete(f'/flores/{plant_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'A flor foi deletada ✂️'}


def test_delete_flor_nao_existente(client):
    response = client.delete('/flores/9999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Flor não encontrada. 🥀'}


def test_read_flor_by_classe(client, flor):
    response = client.get('/flores/?classe=Magnoliopsida')

    assert response.status_code == HTTPStatus.OK

    expected_response = {
        'Plants': [
            {
                'id': flor.id,
                'nome': flor.nome,
                'nome_cientifico': flor.nome_cientifico,
                'classe': flor.classe,
                'ordem': flor.ordem,
                'familia': flor.familia,
                'genero': flor.genero,
            }
        ]
    }

    assert response.json() == expected_response


def test_read_flor_by_ordem(client, flor):
    response = client.get('/flores/?ordem=Rosales')

    assert response.status_code == HTTPStatus.OK

    expected_response = {
        'Plants': [
            {
                'id': flor.id,
                'nome': flor.nome,
                'nome_cientifico': flor.nome_cientifico,
                'classe': flor.classe,
                'ordem': flor.ordem,
                'familia': flor.familia,
                'genero': flor.genero,
            }
        ]
    }

    assert response.json() == expected_response


def test_read_flor_by_familia(client, flor):
    response = client.get('/flores/?familia=Rosaceae')

    assert response.status_code == HTTPStatus.OK

    expected_response = {
        'Plants': [
            {
                'id': flor.id,
                'nome': flor.nome,
                'nome_cientifico': flor.nome_cientifico,
                'classe': flor.classe,
                'ordem': flor.ordem,
                'familia': flor.familia,
                'genero': flor.genero,
            }
        ]
    }

    assert response.json() == expected_response


def test_read_plants_with_no_matches(client):
    response = client.get('/flores/?classe=NonExistentClass')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Plants': []}
