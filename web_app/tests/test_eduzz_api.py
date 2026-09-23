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

    def get_falso(url, headers=None, params=None, timeout=None):
        chamadas.append(params)
        if params["page"] == 1:
            return RespostaFalsa({"items": [{"id": 1}], "pages": 2, "page": 1})
        return RespostaFalsa({"items": [{"id": 2}], "pages": 2, "page": 2})

    monkeypatch.setattr(eduzz_api.requests, "get", get_falso)
    monkeypatch.setattr(eduzz_api.time, "sleep", lambda s: None)

    vendas = eduzz_api.listar_vendas(
        "tok", 55, datetime.date(2026, 9, 1), datetime.date(2026, 9, 2), "paid"
    )

    assert [v["id"] for v in vendas] == [1, 2]
    assert chamadas[0]["productId"] == 55
    assert chamadas[0]["status"] == "paid"
    assert chamadas[0]["referenceDate"] == "paidAt"
