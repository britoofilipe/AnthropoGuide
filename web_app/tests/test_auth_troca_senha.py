import datetime
import auth


def test_troca_senha_atualiza_sqlite_e_limpa_flag(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "t.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    auth.cadastrar_aluno("Ana Souza", "ana@x.com", "provisoria", "Eduzz",
                         datetime.date.today(), precisa_trocar_senha=1)

    ok, _, dados = auth.verificar_acesso("ana@x.com", "provisoria")
    assert ok and dados["precisa_trocar_senha"] == 1

    assert auth.trocar_senha("ana@x.com", "novaSenhaForte")[0]
    ok, _, dados = auth.verificar_acesso("ana@x.com", "novaSenhaForte")
    assert ok and dados["precisa_trocar_senha"] == 0
    assert not auth.verificar_acesso("ana@x.com", "provisoria")[0]


def test_troca_senha_grava_na_planilha_quando_configurada(tmp_path, monkeypatch):
    chamadas = []
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "t2.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_trocar_senha",
                        lambda email, senha_hash: (chamadas.append((email, senha_hash)), (True, "ok"))[1])
    auth.init_db()
    auth.cadastrar_aluno("Ana Souza", "ana@x.com", "provisoria", "Eduzz", datetime.date.today())

    assert auth.trocar_senha("ana@x.com", "novaSenhaForte")[0]
    assert chamadas[0][0] == "ana@x.com"
    assert chamadas[0][1].startswith("scrypt$")


def test_troca_senha_exige_oito_caracteres(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "t3.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    auth.cadastrar_aluno("Ana Souza", "ana@x.com", "provisoria", "Eduzz", datetime.date.today())
    ok, msg = auth.trocar_senha("ana@x.com", "curta")
    assert not ok and "8" in msg


def test_troca_senha_planilha_falha_nao_atualiza_sqlite(tmp_path, monkeypatch):
    """Planilha retorna False: não atualiza SQLite, mantém sincronismo."""
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "t4.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_trocar_senha", lambda email, senha_hash: (False, "erro na planilha"))
    auth.init_db()
    auth.cadastrar_aluno("Ana Souza", "ana@x.com", "provisoria", "Eduzz", datetime.date.today())

    # Tenta trocar
    ok, msg = auth.trocar_senha("ana@x.com", "novaSenhaForte")

    # Retorna erro
    assert not ok
    assert "Senha alterada" not in msg

    # SQLite não foi atualizado: senha provisória continua funcionando
    ok, _, _ = auth.verificar_acesso("ana@x.com", "provisoria")
    assert ok

    # Nova senha não funciona
    ok, _, _ = auth.verificar_acesso("ana@x.com", "novaSenhaForte")
    assert not ok


def test_troca_senha_planilha_excecao_nao_atualiza_sqlite(tmp_path, monkeypatch):
    """Planilha lança exceção: não atualiza SQLite, mantém sincronismo, nenhuma exceção escapa."""
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "t5.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_trocar_senha", lambda email, senha_hash: (_ for _ in ()).throw(RuntimeError("conexao perdida")))
    auth.init_db()
    auth.cadastrar_aluno("Ana Souza", "ana@x.com", "provisoria", "Eduzz", datetime.date.today())

    # Tenta trocar — nenhuma exceção deve escapar
    ok, msg = auth.trocar_senha("ana@x.com", "novaSenhaForte")

    # Retorna erro
    assert not ok
    assert "Senha alterada" not in msg

    # SQLite não foi atualizado: senha provisória continua funcionando
    ok, _, _ = auth.verificar_acesso("ana@x.com", "provisoria")
    assert ok

    # Nova senha não funciona
    ok, _, _ = auth.verificar_acesso("ana@x.com", "novaSenhaForte")
    assert not ok
