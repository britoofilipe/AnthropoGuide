import hashlib
import auth


def test_hash_tem_salt_aleatorio():
    a, b = auth.hash_password("senha123"), auth.hash_password("senha123")
    assert a != b and a.startswith("scrypt$")
    assert auth.conferir_senha("senha123", a)
    assert not auth.conferir_senha("errada", a)


def test_aceita_hash_legado_sha256():
    legado = hashlib.sha256("senha123".encode("utf-8")).hexdigest()
    assert auth.conferir_senha("senha123", legado)
    assert not auth.conferir_senha("errada", legado)
