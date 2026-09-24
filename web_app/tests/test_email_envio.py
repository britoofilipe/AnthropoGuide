from integracao_eduzz import email_envio

DADOS = {
    "nome": "Ana Souza",
    "email": "ana@x.com",
    "senha": "Kd7mTq9xAb",
    "validade": "21/01/2027",
    "sale_id": 9001,
}


def test_email_traz_dados_de_acesso():
    msg = email_envio.montar(DADOS, "https://anthropoguide.exemplo.br")
    corpo = msg.get_content()
    assert msg["To"] == "ana@x.com"
    assert "AnthropoGuide" in msg["Subject"]
    assert "Kd7mTq9xAb" in corpo
    assert "https://anthropoguide.exemplo.br" in corpo
    assert "21/01/2027" in corpo
    assert "trocar" in corpo.lower()


def test_email_primeiro_nome_com_espacos_ou_nome_unico():
    dados_nome_simples = {**DADOS, "nome": "  Mariana  "}
    msg = email_envio.montar(dados_nome_simples, "https://anthropoguide.exemplo.br")
    assert "Olá, Mariana." in msg.get_content()


def test_envio_usa_starttls(monkeypatch):
    eventos = []

    class SmtpFalso:
        def __init__(self, host, porta, timeout=None):
            eventos.append(("conectou", host, porta))

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def starttls(self):
            eventos.append(("starttls",))

        def login(self, usuario, senha):
            eventos.append(("login", usuario))

        def send_message(self, mensagem):
            eventos.append(("enviou", mensagem["To"]))

    monkeypatch.setattr(email_envio.smtplib, "SMTP", SmtpFalso)
    email_envio.enviar(email_envio.montar(DADOS, "https://x.br"), "smtp.x", 587, "u@x", "s")

    assert [e[0] for e in eventos] == ["conectou", "starttls", "login", "enviou"]
