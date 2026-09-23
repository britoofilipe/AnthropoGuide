import datetime
import auth


class RespostaFalsa:
    def __init__(self, payload=None, status_code=200):
        self._payload = payload if payload is not None else []
        self.status_code = status_code
        self.text = "ok"

    def json(self):
        return self._payload


def test_gsheets_cadastrar_envia_campos_da_eduzz(monkeypatch):
    enviados = {}

    def post_falso(url, json=None, timeout=None, allow_redirects=None):
        enviados.update(json)
        return RespostaFalsa()

    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth.requests, "post", post_falso)

    ok, _ = auth.gsheets_cadastrar(
        "Ana Souza", "ana@x.com", "scrypt$aa$bb", "Eduzz",
        datetime.date(2026, 9, 23), datetime.date(2027, 1, 21),
        origem="eduzz", eduzz_sale_id=9001, precisa_trocar_senha=1,
    )

    assert ok
    assert enviados["action"] == "cadastrar"
    assert enviados["origem"] == "eduzz"
    assert enviados["eduzz_sale_id"] == 9001
    assert enviados["precisa_trocar_senha"] == 1


def test_gsheets_trocar_senha_e_bloquear(monkeypatch):
    chamadas = []
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(
        auth.requests, "post",
        lambda url, json=None, timeout=None, allow_redirects=None: (chamadas.append(json), RespostaFalsa())[1],
    )

    assert auth.gsheets_trocar_senha("ana@x.com", "scrypt$cc$dd")[0]
    assert auth.gsheets_bloquear(9001)[0]
    assert chamadas[0] == {"action": "trocar_senha", "email": "ana@x.com", "senha_hash": "scrypt$cc$dd"}
    assert chamadas[1] == {"action": "bloquear", "eduzz_sale_id": 9001}


def test_gsheets_listar_devolve_campos_novos(monkeypatch):
    linha = {"nome": "Ana Souza", "email": "ANA@X.com", "senha_hash": "scrypt$aa$bb",
             "turma": "Eduzz", "data_curso": "2026-09-23", "status": "pos_curso",
             "data_expiracao": "2099-01-01", "origem": "eduzz", "eduzz_sale_id": "9001",
             "precisa_trocar_senha": "1"}
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth.requests, "get",
                        lambda url, timeout=None, allow_redirects=None: RespostaFalsa([linha]))

    aluno = auth.gsheets_listar()[0]
    assert aluno["origem"] == "eduzz"
    assert aluno["eduzz_sale_id"] == 9001
    assert aluno["precisa_trocar_senha"] == 1


def test_gsheets_listar_tolera_linha_sem_campos_novos(monkeypatch):
    linha = {"nome": "Bruno Lima", "email": "b@x.com", "senha_hash": "h", "turma": "ISAK N1",
             "data_curso": "2026-01-10", "status": "pos_curso", "data_expiracao": "2099-01-01"}
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth.requests, "get",
                        lambda url, timeout=None, allow_redirects=None: RespostaFalsa([linha]))

    aluno = auth.gsheets_listar()[0]
    assert aluno["origem"] == "manual"
    assert aluno["eduzz_sale_id"] is None
    assert aluno["precisa_trocar_senha"] == 0


def test_gsheets_listar_tolera_eduzz_sale_id_nao_numerico(monkeypatch):
    """Valida que eduzz_sale_id não-numérico não derruba a leitura inteira da lista."""
    linhas = [
        {"nome": "Ana Com Erro", "email": "ana_erro@x.com", "senha_hash": "h1", "turma": "Eduzz",
         "data_curso": "2026-09-23", "status": "pos_curso", "data_expiracao": "2099-01-01",
         "origem": "eduzz", "eduzz_sale_id": "9O01", "precisa_trocar_senha": "1"},
        {"nome": "Bruno OK", "email": "bruno@x.com", "senha_hash": "h2", "turma": "Eduzz",
         "data_curso": "2026-09-23", "status": "pos_curso", "data_expiracao": "2099-01-01",
         "origem": "eduzz", "eduzz_sale_id": "9002", "precisa_trocar_senha": "0"}
    ]
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth.requests, "get",
                        lambda url, timeout=None, allow_redirects=None: RespostaFalsa(linhas))

    # Não deve lançar exceção
    alunos = auth.gsheets_listar()

    # Ambas as linhas devem retornar
    assert len(alunos) == 2

    # A linha com erro deve ter eduzz_sale_id=None
    assert alunos[0]["nome"] == "Ana Com Erro"
    assert alunos[0]["eduzz_sale_id"] is None

    # A linha OK deve ter eduzz_sale_id correto
    assert alunos[1]["nome"] == "Bruno OK"
    assert alunos[1]["eduzz_sale_id"] == 9002
