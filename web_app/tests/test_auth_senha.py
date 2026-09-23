import hashlib
import sqlite3
import datetime
import pytest
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


def test_verificar_acesso_migra_hash_legado_na_mesma_conexao(tmp_path, monkeypatch):
    """Testa regravação de hash legado dentro de verificar_acesso."""
    db = tmp_path / "teste.db"
    monkeypatch.setattr(auth, "DB_PATH", db)
    auth.init_db()

    email = "teste@example.com"
    senha = "minhaSenha456"
    data_curso = datetime.date(2026, 9, 23)

    # Cadastra aluno (gera hash novo)
    ok, msg = auth.cadastrar_aluno("João", email, senha, "N1", data_curso)
    assert ok, msg

    # Sobrescreve senha_hash com SHA-256 legado
    legado_hash = hashlib.sha256(senha.encode("utf-8")).hexdigest()
    with auth.get_db_connection() as conn:
        conn.execute("UPDATE alunos SET senha_hash = ? WHERE email = ?", (legado_hash, email))
        conn.commit()

    # Verifica que banco tem hash legado antes
    with auth.get_db_connection() as conn:
        cursor = conn.execute("SELECT senha_hash FROM alunos WHERE email = ?", (email,))
        row = cursor.fetchone()
    assert row["senha_hash"] == legado_hash

    # Autentica com a senha — deve autorizar e regravar
    autorizado, msg, aluno = auth.verificar_acesso(email, senha)
    assert autorizado, f"Acesso negado: {msg}"

    # (a) Acesso autorizado ✓ (verificado acima)

    # (b) Hash agora começa com "scrypt$"
    with auth.get_db_connection() as conn:
        cursor = conn.execute("SELECT senha_hash FROM alunos WHERE email = ?", (email,))
        row = cursor.fetchone()
    novo_hash = row["senha_hash"]
    assert novo_hash.startswith("scrypt$"), f"Hash não foi migrado: {novo_hash}"

    # (c) Novo verificar_acesso com mesma senha continua autorizando
    autorizado2, msg2, aluno2 = auth.verificar_acesso(email, senha)
    assert autorizado2, f"Acesso negado após migração: {msg2}"

    # (d) verificar_acesso com senha errada não autoriza
    autorizado3, msg3, aluno3 = auth.verificar_acesso(email, "senhaErrada")
    assert not autorizado3, "Acesso autorizado com senha errada"


def test_conferir_senha_trata_hash_malformado(tmp_path, monkeypatch):
    """Testa que hash malformado não lança exceção, apenas retorna False."""
    db = tmp_path / "teste.db"
    monkeypatch.setattr(auth, "DB_PATH", db)
    auth.init_db()

    email = "teste@example.com"
    senha = "senha123"
    data_curso = datetime.date(2026, 9, 23)

    # Cadastra aluno
    ok, msg = auth.cadastrar_aluno("Maria", email, senha, "N1", data_curso)
    assert ok, msg

    casos_malformados = [
        "scrypt$so2partes",           # split devolve 2 partes (vazio + "so2partes")
        "scrypt$aa$bb$cc",             # split devolve 4 partes
        "scrypt$zz$naohex",            # salt_hex = "zz" (inválido), derivado.hex = "naohex"
        "",                             # string vazia
    ]

    for hash_malformado in casos_malformados:
        # Sobrescreve com hash malformado
        with auth.get_db_connection() as conn:
            conn.execute("UPDATE alunos SET senha_hash = ? WHERE email = ?", (hash_malformado, email))
            conn.commit()

        # verificar_acesso deve retornar acesso negado sem exceção
        autorizado, msg, aluno = auth.verificar_acesso(email, senha)
        assert not autorizado, f"Acesso autorizado com hash malformado '{hash_malformado}'"
        assert msg == "E-mail ou senha incorretos."
