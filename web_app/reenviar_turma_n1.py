"""Script para atualizar senhas e reenviar e-mails de acesso com o novo link ia.filipebrito.com.br."""
import datetime
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import auth
from integracao_eduzz import email_envio, liberacao

BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

ALUNOS = [
    {"nome": "Ana Grasiele Ferreira dias de Brito", "email": "grasibrito@yahoo.com"},
    {"nome": "Camilla da Silva Ribeiro", "email": "cahsribeironutricao@gmail.com"},
    {"nome": "Daniel Nogueira de Oliveira", "email": "nogueiradanoliver@gmail.com"},
    {"nome": "Débora de Souza Vieira", "email": "deboravieirasouza418@gmail.com"},
    {"nome": "Emanuela Sarmento Farias Coelho", "email": "emanuelasarmento@hotmail.com"},
    {"nome": "Francimaria Moreira Maia", "email": "marammaia@hotmail.com"},
    {"nome": "Gabriel Guttierrez Tolomelli", "email": "gabrieltolomellinutri@gmail.com"},
    {"nome": "Ítalo Andrade Gomes", "email": "italoandrade1515@gmail.com"},
    {"nome": "Leticia de Assunção Lima Rodrigues", "email": "leticia.aslimarodrigues@gmail.com"},
    {"nome": "Luiza Cavalcante Amora", "email": "lcamora2@gmail.com"},
    {"nome": "Mario Quesado Miranda Bezerra", "email": "mquesado@unifor.br"},
    {"nome": "Pablo Bastos Pontes", "email": "pablobastospontes1@edu.unifor.br"},
    {"nome": "Vivian Maria Ferreira de Freitas", "email": "vivianfreitasff@gmail.com"},
]

JA_ENVIADOS = {
    "cahsribeironutricao@gmail.com",
    "nogueiradanoliver@gmail.com",
}

VALIDADE = datetime.date(2027, 9, 28)


def executar():
    url_plataforma = os.environ.get("URL_PLATAFORMA", "https://ia.filipebrito.com.br")
    email_remetente = os.environ.get("EMAIL_REMETENTE", "AnthropoGuide <sizelab.academy@gmail.com>")
    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ["SMTP_PORT"])
    smtp_usuario = os.environ["SMTP_USUARIO"]
    smtp_senha = os.environ["SMTP_SENHA"]

    sucessos = []
    erros = []

    print(f"Iniciando atualização de credenciais e reenvio para {len(ALUNOS)} alunos...")
    print(f"Endereço oficial: {url_plataforma}")
    print("=" * 60)

    for i, a in enumerate(ALUNOS, 1):
        nome = a["nome"].strip()
        email = a["email"].strip().lower()

        if email in JA_ENVIADOS:
            print(f"[{i}/{len(ALUNOS)}] {nome} <{email}>: Ja enviado na rodada anterior. Pulando.")
            sucessos.append({"aluno": nome, "email": email, "status": "ja_enviado"})
            continue

        nova_senha = liberacao.gerar_senha_provisoria()
        print(f"[{i}/{len(ALUNOS)}] Atualizando e reenviando: {nome} <{email}>...")

        # 1. Atualiza senha com até 2 tentativas
        ok = False
        msg = ""
        for tentativa in range(1, 3):
            ok, msg = auth.trocar_senha(email, nova_senha)
            if ok:
                break
            print(f"   [RETRY] Tentativa {tentativa} falhou ({msg}). Aguardando 3s...")
            time.sleep(3)

        if not ok:
            print(f"   [ERRO] Falha definitiva ao atualizar senha: {msg}")
            erros.append({"aluno": nome, "email": email, "motivo": f"Troca de senha: {msg}"})
            continue

        # Marca flag precisa_trocar_senha no SQLite
        try:
            with auth.get_db_connection() as conn:
                conn.execute("UPDATE alunos SET precisa_trocar_senha = 1 WHERE email = ?", (email,))
                conn.commit()
        except Exception:
            pass

        # 2. Monta e envia o e-mail
        dados_email = {
            "nome": nome,
            "email": email,
            "senha": nova_senha,
            "validade": VALIDADE.strftime("%d/%m/%Y"),
        }

        try:
            mensagem = email_envio.montar(dados_email, url_plataforma, email_remetente)
            email_envio.enviar(mensagem, smtp_host, smtp_port, smtp_usuario, smtp_senha)
            print(f"   [SUCESSO] Senha atualizada e e-mail enviado com {url_plataforma}!")
            sucessos.append({"aluno": nome, "email": email, "status": "enviado"})
        except Exception as e:
            print(f"   [AVISO] Senha alterada, mas falhou ao enviar e-mail: {e}")
            erros.append({"aluno": nome, "email": email, "motivo": f"Envio: {e}"})

        # Pausa de 3.0s para respeitar limites do Google
        time.sleep(3.0)

    print("=" * 60)
    print(f"Processamento concluído: {len(sucessos)} sucessos, {len(erros)} erros.")
    return len(erros) == 0


if __name__ == "__main__":
    sucesso = executar()
    sys.exit(0 if sucesso else 1)
