"""
AnthropoGuide Web App — Plataforma Exclusiva para Alunos do Prof. Filipe Brito
Tutor Especialista em Cineantropometria e Certificação ISAK Nível 1
"""

import os
import datetime
import streamlit as st
from dotenv import load_dotenv

import auth
import ui
from gemini_service import AnthropoGuideBot

load_dotenv()

st.set_page_config(
    page_title="AnthropoGuide | FilipeBrito",
    page_icon=ui.FAVICON,
    layout="centered",
    initial_sidebar_state="expanded",
)
ui.aplicar_css()

# Inicializa banco de dados
auth.init_db()

# Inicializa estados de sessão
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_type" not in st.session_state:
    st.session_state.user_type = None  # 'aluno' ou 'admin'
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "bot" not in st.session_state:
    st.session_state.bot = None

ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "filipe123")


def fmt_data(iso: str) -> str:
    return datetime.date.fromisoformat(iso).strftime("%d/%m/%Y")


def render_chat(placeholder: str, key: str) -> None:
    """Histórico + campo de mensagem, com avatares da marca (tutor = AG; usuário = iniciais)."""
    avatar_user = ui.avatar_usuario(st.session_state.user_data["nome"])

    def avatar(role: str):
        return ui.AVATAR_TUTOR if role == "assistant" else avatar_user

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=avatar(msg["role"])):
            st.markdown(msg["content"])

    if prompt := st.chat_input(placeholder, key=key):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=avatar("user")):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=avatar("assistant")):
            resposta = st.write_stream(st.session_state.bot.send_message_stream(prompt))
            st.session_state.messages.append({"role": "assistant", "content": resposta})


def botao_sair() -> None:
    if st.button("Sair", icon=":material/logout:", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# ==========================================
# TELA DE LOGIN
# ==========================================
def render_login():
    ui.hero_login()

    tab_aluno, tab_admin = st.tabs([":material/school: Acesso do aluno", ":material/lock: Acesso do instrutor"])

    with tab_aluno:
        st.caption("Use o e-mail cadastrado no seu curso presencial.")
        email = st.text_input("E-mail cadastrado", key="login_email").strip()
        senha = st.text_input("Senha", type="password", key="login_senha").strip()

        if st.button("Entrar", type="primary", use_container_width=True):
            if not email or not senha:
                st.warning("Preencha todos os campos.")
            else:
                sucesso, msg, aluno_data = auth.verificar_acesso(email, senha)
                if sucesso:
                    st.session_state.authenticated = True
                    st.session_state.user_type = "aluno"
                    st.session_state.user_data = aluno_data
                    st.session_state.bot = AnthropoGuideBot()
                    st.rerun()
                else:
                    st.error(msg)

    with tab_admin:
        st.caption("Painel de gestão exclusivo do Prof. Filipe Brito.")
        senha_admin = st.text_input("Senha do instrutor", type="password", key="admin_senha").strip()
        if st.button("Acessar painel do instrutor", type="primary", use_container_width=True):
            if senha_admin == ADMIN_PASS:
                st.session_state.authenticated = True
                st.session_state.user_type = "admin"
                st.session_state.user_data = {"nome": "Prof. Filipe Brito", "email": "instrutor@filipebrito.com.br"}
                st.session_state.bot = AnthropoGuideBot()
                st.rerun()
            else:
                st.error("Senha de administrador incorreta.")

    ui.autoria()

# ==========================================
# PAINEL DO ALUNO (CHAT + STATUS)
# ==========================================
def render_aluno_view():
    aluno = st.session_state.user_data

    with st.sidebar:
        st.markdown(f"#### {aluno['nome']}")
        st.caption(f"Turma: {aluno.get('turma', 'ISAK N1')}")

        # Exibição de Status e Validade Temporal
        ui.cartao_status(aluno.get("status"), aluno.get("dias_restantes", 0), fmt_data(aluno["data_expiracao"]))

        st.divider()
        botao_sair()

    # Área de Chat Principal
    ui.cabecalho_chat()
    render_chat("Sua dúvida ou situação prática", key="aluno_chat_input")

# ==========================================
# PAINEL DO INSTRUTOR (ADMIN)
# ==========================================
def render_admin_view():
    # A lista de alunos precisa de largura; o chat do aluno segue centralizado
    st.set_page_config(layout="wide")
    ui.cabecalho_chat(aviso=False)
    st.markdown("## Painel do instrutor")

    with st.sidebar:
        st.markdown("#### Prof. Filipe Brito")
        st.caption("Instrutor Internacional ISAK Nível 3")
        st.divider()
        botao_sair()

    tab_alunos, tab_novo, tab_chat = st.tabs([
        ":material/group: Alunos e acreditação",
        ":material/person_add: Cadastrar aluno",
        ":material/forum: Testar o tutor",
    ])

    with tab_alunos:
        alunos = auth.listar_alunos()

        if not alunos:
            st.info("Nenhum aluno cadastrado ainda. Use a aba **Cadastrar aluno**.")
        else:
            for al in alunos:
                col1, col2, col3 = st.columns([3, 2.4, 2], vertical_alignment="center")
                with col1:
                    st.markdown(f"**{al['nome']}**  \n`{al['email']}`")
                    st.caption(f"Turma: {al['turma']} · Curso: {fmt_data(al['data_curso'])}")
                with col2:
                    exp = fmt_data(al['data_expiracao'])
                    if al['status'] == 'acreditado':
                        selo = ui.selo("acreditado", f"Acreditado · até {exp}")
                    elif al['status'] == 'expirado':
                        selo = ui.selo("expirado", f"Expirado em {exp}")
                    else:
                        selo = ui.selo("pos_curso", f"Pós-curso · até {exp}")
                    st.html(f'{selo}<div class="fb-dias-admin">{al["dias_restantes"]} <small>dias restantes</small></div>')
                with col3:
                    if al['status'] != 'acreditado':
                        if st.button("Homologar (+4 anos)", key=f"btn_homologar_{al['id']}", icon=":material/verified:"):
                            sucesso, msg = auth.homologar_acreditacao(al['email'])
                            if sucesso:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                    else:
                        st.caption("Acreditação vigente")
                st.divider()

    with tab_novo:
        st.caption("Novos alunos recebem **4 meses** de acesso a partir da data do curso para a entrega dos 20 perfis.")

        with st.form("form_novo_aluno"):
            novo_nome = st.text_input("Nome do aluno")
            novo_email = st.text_input("E-mail do aluno")
            nova_senha = st.text_input("Senha inicial provisória", value="isak2026")
            nova_turma = st.text_input("Identificador da turma", value="ISAK N1 - São Paulo")
            nova_data_curso = st.date_input("Data de término do curso", value=datetime.date.today(), format="DD/MM/YYYY")

            submitted = st.form_submit_button("Cadastrar e liberar acesso (4 meses)", type="primary")
            if submitted:
                if not novo_nome or not novo_email:
                    st.warning("Nome e e-mail são obrigatórios.")
                else:
                    sucesso, msg = auth.cadastrar_aluno(novo_nome, novo_email, nova_senha, nova_turma, nova_data_curso)
                    if sucesso:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    with tab_chat:
        st.caption("Simulação do chat como o aluno vê.")
        render_chat("Faça uma pergunta técnica para testar o tutor", key="admin_chat_input")

# ==========================================
# ROTEAMENTO PRINCIPAL
# ==========================================
if not st.session_state.authenticated:
    render_login()
else:
    if st.session_state.user_type == "admin":
        render_admin_view()
    else:
        render_aluno_view()
