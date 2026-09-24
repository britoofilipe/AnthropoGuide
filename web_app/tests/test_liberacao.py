import datetime
import auth
from integracao_eduzz import liberacao

VENDA = {"id": 9001, "status": "paid", "paidAt": "2026-09-23T10:00:00-03:00",
         "buyer": {"name": "Ana Souza", "email": "Ana@X.com"}}


def test_liberar_cria_aluno_uma_unica_vez(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "l.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()

    novo = liberacao.liberar(VENDA, prazo_dias=120)
    assert novo["email"] == "ana@x.com"
    assert novo["validade"] == datetime.date(2026, 9, 23) + datetime.timedelta(days=120)
    ok, _, dados = auth.verificar_acesso("ana@x.com", novo["senha"])
    assert ok and dados["precisa_trocar_senha"] == 1 and dados["origem"] == "eduzz"

    assert liberacao.liberar(VENDA, prazo_dias=120) is None


def test_liberar_consulta_planilha_para_idempotencia(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "l2.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_listar", lambda: [
        {"email": "ana@x.com", "eduzz_sale_id": 9001, "nome": "Ana Souza"}])
    auth.init_db()

    assert liberacao.liberar(VENDA, prazo_dias=120) is None


def test_bloquear_usa_planilha_e_sqlite(tmp_path, monkeypatch):
    bloqueios = []
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "b.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_listar", lambda: [])
    monkeypatch.setattr(auth, "gsheets_cadastrar", lambda *a, **k: (True, "ok"))
    monkeypatch.setattr(auth, "gsheets_bloquear",
                        lambda sale_id: (bloqueios.append(sale_id), (True, "ok"))[1])
    auth.init_db()
    liberacao.liberar(VENDA, prazo_dias=120)

    assert liberacao.bloquear({"id": 9001, "status": "refunded"})
    assert bloqueios == [9001]
    with auth.get_db_connection() as conn:
        linha = conn.execute("SELECT status FROM alunos WHERE eduzz_sale_id = 9001").fetchone()
    assert linha["status"] == "expirado"


def test_senha_provisoria_sem_caracteres_ambiguos():
    senha = liberacao.gerar_senha_provisoria()
    assert len(senha) == 10 and not set(senha) & set("O0Il1")


def test_bloquear_quando_aluno_so_existe_na_planilha(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "b2.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_bloquear", lambda sale_id: (True, "ok"))
    auth.init_db()

    assert liberacao.bloquear({"id": 9001, "status": "refunded"})
    # SQLite vazio: nenhuma linha para atualizar
    with auth.get_db_connection() as conn:
        linha = conn.execute("SELECT status FROM alunos WHERE eduzz_sale_id = 9001").fetchone()
    assert linha is None


def test_bloquear_quando_nao_existe_em_nenhum_lugar(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "b3.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_bloquear", lambda sale_id: (False, "venda nao encontrada"))
    auth.init_db()

    assert not liberacao.bloquear({"id": 9001, "status": "refunded"})


import pytest


def test_liberar_falha_se_gsheets_cadastrar_retorna_false(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "l3.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_listar", lambda: [])
    monkeypatch.setattr(auth, "gsheets_cadastrar", lambda *a, **k: (False, "erro na planilha"))
    auth.init_db()

    with pytest.raises(RuntimeError) as excinfo:
        liberacao.liberar(VENDA, prazo_dias=120)
    assert "erro na planilha" in str(excinfo.value)

    # SQLite deve estar vazio (nenhum aluno foi criado)
    with auth.get_db_connection() as conn:
        linha = conn.execute("SELECT COUNT(*) as cnt FROM alunos").fetchone()
    assert linha["cnt"] == 0

    # ja_processada deve continuar retornando False para tentar novamente
    assert not liberacao.ja_processada(9001)
