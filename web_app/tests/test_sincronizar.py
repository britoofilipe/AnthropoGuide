import auth
import pytest
import sincronizar_eduzz
from integracao_eduzz import eduzz_api

CONFIG = {
    "token": "t",
    "product_id": 55,
    "prazo_dias": 120,
    "url_plataforma": "https://x.br",
    "dias_janela": 3,
}
VENDA_PAGA = {
    "id": 9001,
    "status": "paid",
    "paidAt": "2026-09-23T10:00:00-03:00",
    "buyer": {"name": "Ana Souza", "email": "ana@x.com"},
}
VENDA_REEMBOLSADA = {
    "id": 9001,
    "status": "refunded",
    "paidAt": "2026-09-23T10:00:00-03:00",
    "buyer": {"name": "Ana Souza", "email": "ana@x.com"},
}


def test_libera_paga_e_bloqueia_reembolsada(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "s.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    enviados = []
    monkeypatch.setattr(
        eduzz_api,
        "listar_vendas",
        lambda token, product_id, inicio, fim, status: (
            [VENDA_PAGA]
            if status == "paid"
            else ([VENDA_REEMBOLSADA] if status == "refunded" else [])
        ),
    )

    r1 = sincronizar_eduzz.sincronizar(CONFIG, enviados.append)
    assert r1["liberados"] == 1 and r1["bloqueados"] == 1 and r1["erros"] == []
    assert len(enviados) == 1 and enviados[0]["email"] == "ana@x.com"

    r2 = sincronizar_eduzz.sincronizar(CONFIG, enviados.append)
    assert r2["liberados"] == 0 and len(enviados) == 1


def test_erro_em_uma_venda_nao_derruba_as_outras(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "s2.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    ruim = {"id": 9002, "status": "paid", "paidAt": "2026-09-23T10:00:00-03:00", "buyer": {}}
    monkeypatch.setattr(
        eduzz_api,
        "listar_vendas",
        lambda token, product_id, inicio, fim, status: [ruim, VENDA_PAGA] if status == "paid" else [],
    )

    resultado = sincronizar_eduzz.sincronizar(CONFIG, lambda d: None)
    assert resultado["liberados"] == 1 and len(resultado["erros"]) == 1


def test_falha_de_email_vira_erro_da_venda(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "s3.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    monkeypatch.setattr(
        eduzz_api,
        "listar_vendas",
        lambda token, product_id, inicio, fim, status: [VENDA_PAGA] if status == "paid" else [],
    )

    def envio_quebrado(dados):
        raise RuntimeError("smtp fora do ar")

    resultado = sincronizar_eduzz.sincronizar(CONFIG, envio_quebrado)
    assert resultado["liberados"] == 0
    assert len(resultado["erros"]) == 1 and "smtp" in resultado["erros"][0]


def test_falha_na_planilha_aparece_em_erros(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "s4.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_listar", lambda: [])
    monkeypatch.setattr(auth, "gsheets_cadastrar", lambda *a, **k: (False, "planilha offline"))
    auth.init_db()

    monkeypatch.setattr(
        eduzz_api,
        "listar_vendas",
        lambda token, product_id, inicio, fim, status: [VENDA_PAGA] if status == "paid" else [],
    )

    resultado = sincronizar_eduzz.sincronizar(CONFIG, lambda d: None)
    assert resultado["liberados"] == 0
    assert len(resultado["erros"]) == 1
    assert "planilha offline" in resultado["erros"][0]
