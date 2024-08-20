from jwt import decode
from fast_zero.security import create_access_token, SECRET_KEY, algorithm


def test_jwt():
    data = {'sub': 'teste@teste.com'}
    token = create_access_token(data)

    resultado = decode(token, SECRET_KEY, algorithms=[algorithm])

    assert resultado['sub'] == data['sub']
    assert resultado['exp']
