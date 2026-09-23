import datetime
from integracao_eduzz import eduzz_api


class RespostaFalsa:
    def __init__(self, payload):
        self._payload = payload
        self.status_code = 200

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


def test_listar_vendas_percorre_paginas(monkeypatch):
    chamadas = []
    chamadas_sleep = []

    def get_falso(url, headers=None, params=None, timeout=None):
        chamadas.append(params)
        if params["page"] == 1:
            return RespostaFalsa({"items": [{"id": 1}], "pages": 2, "page": 1})
        return RespostaFalsa({"items": [{"id": 2}], "pages": 2, "page": 2})

    def sleep_falso(s):
        chamadas_sleep.append(s)

    monkeypatch.setattr(eduzz_api.requests, "get", get_falso)
    monkeypatch.setattr(eduzz_api.time, "sleep", sleep_falso)

    vendas = eduzz_api.listar_vendas(
        "tok", 55, datetime.date(2026, 9, 1), datetime.date(2026, 9, 2), "paid"
    )

    assert [v["id"] for v in vendas] == [1, 2]
    assert chamadas[0]["productId"] == 55
    assert chamadas[0]["status"] == "paid"
    assert chamadas[0]["referenceDate"] == "paidAt"
    # Pausa deve ocorrer apenas ENTRE páginas, não depois da última
    assert len(chamadas_sleep) == 1


def test_listar_vendas_pagina_unica_sem_pausa(monkeypatch):
    chamadas_sleep = []

    def get_falso(url, headers=None, params=None, timeout=None):
        # Resposta com uma única página
        return RespostaFalsa({"items": [{"id": 1}], "pages": 1, "page": 1})

    def sleep_falso(s):
        chamadas_sleep.append(s)

    monkeypatch.setattr(eduzz_api.requests, "get", get_falso)
    monkeypatch.setattr(eduzz_api.time, "sleep", sleep_falso)

    vendas = eduzz_api.listar_vendas(
        "tok", 55, datetime.date(2026, 9, 1), datetime.date(2026, 9, 2), "paid"
    )

    assert [v["id"] for v in vendas] == [1]
    # Sem múltiplas páginas, não deve chamar sleep
    assert len(chamadas_sleep) == 0


def test_listar_vendas_resposta_vazia_degradada(monkeypatch):
    """Testa comportamento quando API retorna resposta vazia {}"""

    def get_falso(url, headers=None, params=None, timeout=None):
        # Resposta sem 'items' e sem 'pages'
        return RespostaFalsa({})

    monkeypatch.setattr(eduzz_api.requests, "get", get_falso)
    monkeypatch.setattr(eduzz_api.time, "sleep", lambda s: None)

    vendas = eduzz_api.listar_vendas(
        "tok", 55, datetime.date(2026, 9, 1), datetime.date(2026, 9, 2), "paid"
    )

    # Deve retornar lista vazia, sem exceção e sem laço infinito
    assert vendas == []


def test_listar_vendas_pages_zero_sem_loop(monkeypatch):
    """Testa que pages=0 não causa laço infinito"""
    chamadas_get = []

    def get_falso(url, headers=None, params=None, timeout=None):
        chamadas_get.append(params)
        return RespostaFalsa({"items": [{"id": 1}], "pages": 0})

    monkeypatch.setattr(eduzz_api.requests, "get", get_falso)
    monkeypatch.setattr(eduzz_api.time, "sleep", lambda s: None)

    vendas = eduzz_api.listar_vendas(
        "tok", 55, datetime.date(2026, 9, 1), datetime.date(2026, 9, 2), "paid"
    )

    # Deve retornar itens recebidos e encerrar
    assert [v["id"] for v in vendas] == [1]
    # Deve fazer apenas uma requisição, sem repetir
    assert len(chamadas_get) == 1


def test_listar_vendas_refunded_usa_updated_at(monkeypatch):
    """Testa que status 'refunded' usa referenceDate='updatedAt'"""
    chamadas = []

    def get_falso(url, headers=None, params=None, timeout=None):
        chamadas.append(params)
        return RespostaFalsa({"items": [{"id": 1}], "pages": 1})

    monkeypatch.setattr(eduzz_api.requests, "get", get_falso)
    monkeypatch.setattr(eduzz_api.time, "sleep", lambda s: None)

    vendas = eduzz_api.listar_vendas(
        "tok", 55, datetime.date(2026, 9, 1), datetime.date(2026, 9, 2), "refunded"
    )

    assert [v["id"] for v in vendas] == [1]
    # Para status refunded, deve usar 'updatedAt'
    assert chamadas[0]["referenceDate"] == "updatedAt"
