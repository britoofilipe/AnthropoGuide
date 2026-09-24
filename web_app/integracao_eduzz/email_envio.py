"""E-mail de liberação de acesso, no tom da marca FilipeBrito."""
import smtplib
from email.message import EmailMessage

CORPO = """Olá, {nome}.

Seu acesso ao AnthropoGuide está liberado.

Endereço: {url}
Login: {email}
Senha provisória: {senha}

Ao entrar pela primeira vez, você precisa trocar a senha provisória por uma senha sua.
O acesso é pessoal e intransferível, válido até {validade}.

Uma orientação prática: descreva as dúvidas como você contaria a um colega, com o contexto
do caso, e sempre sem dados que identifiquem o avaliado.

Bom uso.

Prof. Filipe Brito
Instrutor Internacional ISAK Nível 3
"""


def montar(dados: dict, url_plataforma: str, remetente: str = "AnthropoGuide") -> EmailMessage:
    mensagem = EmailMessage()
    mensagem["Subject"] = "Seu acesso ao AnthropoGuide está liberado"
    mensagem["From"] = remetente
    mensagem["To"] = dados["email"]
    nome_bruto = str(dados.get("nome") or "").strip()
    primeiro_nome = nome_bruto.split()[0] if nome_bruto else "Aluno"
    mensagem.set_content(
        CORPO.format(
            nome=primeiro_nome,
            url=url_plataforma,
            email=dados["email"],
            senha=dados["senha"],
            validade=dados["validade"],
        )
    )
    return mensagem


def enviar(mensagem: EmailMessage, host: str, porta: int, usuario: str, senha: str) -> None:
    with smtplib.SMTP(host, porta, timeout=30) as servidor:
        servidor.starttls()
        servidor.login(usuario, senha)
        servidor.send_message(mensagem)
