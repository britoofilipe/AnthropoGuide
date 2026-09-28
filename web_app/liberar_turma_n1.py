"""Script de liberação em lote dos alunos do curso ISAK Nível 1."""
import datetime
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Garante saída UTF-8 no Windows
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

TURMA = "ISAK N1 Fortaleza - Setembro 2026"
DATA_CURSO = datetime.date(2026, 9, 27)
VALIDADE = datetime.date(2027, 9, 28)
ORIGEM = "bonus_curso"


def executar():
    auth.init_db()

    url_plataforma = os.environ.get("URL_PLATAFORMA", "https://anthropoguide.streamlit.app")
    email_remetente = os.environ.get("EMAIL_REMETENTE", "AnthropoGuide <sizelab.academy@gmail.com>")
    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ["SMTP_PORT"])
    smtp_usuario = os.environ["SMTP_USUARIO"]
    smtp_senha = os.environ["SMTP_SENHA"]

    sucessos = []
    erros = []

    # Lista alunos já cadastrados para evitar duplicidade
    existentes = {a["email"].strip().lower() for a in auth.listar_alunos()}

    print(f"Iniciando liberação e envio para {len(ALUNOS)} alunos...")
    print("=" * 60)

    for i, a in enumerate(ALUNOS, 1):
        nome = a["nome"].strip()
        email = a["email"].strip().lower()

        print(f"[{i}/{len(ALUNOS)}] Processando: {nome} <{email}>...")

        # Se já existe (caso do aluno 1 que já foi processado na primeira tentativa)
        if email in existentes:
            print(f"   [AVISO] Aluno ja cadastrado anteriormente. Pulando.")
            sucessos.append({"aluno": nome, "email": email, "status": "ja_cadastrado"})
            continue

        senha_provisoria = liberacao.gerar_senha_provisoria()

        # 1. Cadastra no sistema (Planilha + SQLite)
        ok, msg = auth.cadastrar_aluno(
            nome=nome,
            email=email,
            senha=senha_provisoria,
            turma=TURMA,
            data_curso=DATA_CURSO,
            origem=ORIGEM,
            precisa_trocar_senha=1,
            data_expiracao=VALIDADE,
        )

        if not ok:
            print(f"   [ERRO] Falha ao cadastrar: {msg}")
            erros.append({"aluno": nome, "email": email, "motivo": f"Cadastro: {msg}"})
            continue

        # 2. Monta e envia o e-mail
        dados_email = {
            "nome": nome,
            "email": email,
            "senha": senha_provisoria,
            "validade": VALIDADE.strftime("%d/%m/%Y"),
        }

        try:
            mensagem = email_envio.montar(dados_email, url_plataforma, email_remetente)
            email_envio.enviar(mensagem, smtp_host, smtp_port, smtp_usuario, smtp_senha)
            print(f"   [SUCESSO] Cadastrado e e-mail enviado com sucesso!")
            sucessos.append({"aluno": nome, "email": email, "status": "enviado"})
        except Exception as e:
            print(f"   [AVISO] Cadastrado no sistema, mas erro no envio do e-mail: {e}")
            erros.append({"aluno": nome, "email": email, "motivo": f"Envio de e-mail: {e}"})

        # Pausa para respeitar taxa do servidor e da planilha
        time.sleep(2.5)

    print("=" * 60)
    print(f"Processamento concluído: {len(sucessos)} processados com sucesso, {len(erros)} erros.")
    for s in sucessos:
        print(f" - {s['aluno']} ({s['email']}): {s.get('status')}")
    if erros:
        print("Erros:")
        for err in erros:
            print(f" - {err['aluno']} ({err['email']}): {err['motivo']}")

    return len(erros) == 0


if __name__ == "__main__":
    sucesso = executar()
    sys.exit(0 if sucesso else 1)
