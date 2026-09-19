"""
AnthropoGuide Web App — Plataforma Exclusiva para Alunos do Prof. Filipe Brito
Tutor Especialista em Cineantropometria e Certificação ISAK Nível 1
"""

import os
import datetime
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

import auth
from gemini_service import AnthropoGuideBot

load_dotenv()

st.set_page_config(
    page_title="AnthropoGuide — Prof. Filipe Brito",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

# ==========================================
# TELA DE LOGIN
# ==========================================
def render_login():
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='color: #0F52BA; margin-bottom: 0;'>🧭 AnthropoGuide</h1>
            <p style='font-size: 1.15rem; color: #555;'>Tutor Especialista em Cineantropometria e Certificação ISAK Nível 1</p>
            <p style='font-size: 0.95rem; color: #888;'>Coordenação: <b>Prof. Filipe Brito</b> (Instrutor Internacional ISAK Nível 3)</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_aluno, tab_admin = st.tabs(["🎓 Acesso do Aluno", "🔐 Acesso do Instrutor"])
        
        with tab_aluno:
            st.info("Acesse com o e-mail cadastrado no seu curso presencial.")
            email = st.text_input("E-mail cadastrado", key="login_email").strip()
            senha = st.text_input("Senha", type="password", key="login_senha").strip()
            
            if st.button("Entrar no AnthropoGuide", type="primary", use_container_width=True):
                if not email or not senha:
                    st.warning("Preencha todos os campos.")
                else:
                    sucesso, msg, aluno_data = auth.verificar_acesso(email, senha)
                    if sucesso:
                        st.session_state.authenticated = True
                        st.session_state.user_type = "aluno"
                        st.session_state.user_data = aluno_data
                        st.session_state.bot = AnthropoGuideBot()
                        st.success("Acesso autorizado com sucesso!")
                        st.rerun()
                    else:
                        st.error(msg)
                        
        with tab_admin:
            st.markdown("Painel de gerenciamento exclusivo do Prof. Filipe Brito.")
            senha_admin = st.text_input("Senha Mestre do Instrutor", type="password", key="admin_senha").strip()
            if st.button("Acessar Painel do Instrutor", use_container_width=True):
                if senha_admin == ADMIN_PASS:
                    st.session_state.authenticated = True
                    st.session_state.user_type = "admin"
                    st.session_state.user_data = {"nome": "Prof. Filipe Brito", "email": "instrutor@filipebrito.com.br"}
                    st.session_state.bot = AnthropoGuideBot()
                    st.success("Login de administrador realizado!")
                    st.rerun()
                else:
                    st.error("Senha de administrador incorreta.")

# ==========================================
# PAINEL DO ALUNO (CHAT + STATUS)
# ==========================================
def render_aluno_view():
    aluno = st.session_state.user_data
    
    with st.sidebar:
        st.markdown(f"### 👤 {aluno['nome']}")
        st.caption(f"Turma: {aluno.get('turma', 'ISAK N1')}")
        
        # Exibição de Status e Validade Temporal
        status = aluno.get("status")
        dias = aluno.get("dias_restantes", 0)
        data_exp = datetime.date.fromisoformat(aluno["data_expiracao"]).strftime("%d/%m/%Y")
        
        if status == "acreditado":
            st.success("🏆 **Acreditado ISAK Nível 1**")
            st.markdown(f"**Acesso Estendido:** Válido até **{data_exp}**")
            st.caption(f"⏳ {dias} dias de acesso restantes")
        else:
            st.warning("📝 **Em Fase Pós-Curso (20 Sujeitos)**")
            st.markdown(f"**Prazo ISAKMetry:** Até **{data_exp}**")
            st.caption(f"⏳ {dias} dias restantes para submissão")
            
        st.divider()
        st.markdown("""
        **Diretrizes Rápidas:**
        - Prazos: 4 meses para enviar os 20 perfis.
        - Tolerância ETM: Dobras ≤ 7,5%; outras ≤ 1,5%.
        - Nomenclatura: **Dobra da perna** (nunca "perna medial").
        """)
        
        if st.button("Sair (Logout)", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # Área de Chat Principal
    st.markdown("### 🧭 AnthropoGuide — Seu Tutor de Cineantropometria")
    st.caption("Consulte sobre landmarks, qualidade da medida (ETM), equações de Petroski, curvas centílicas (Campa vs. Costa) e manuseio do ISAKMetry.")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Digite sua dúvida técnica ou caso clínico..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analisando protocolo e evidências..."):
                resposta = st.session_state.bot.send_message(prompt)
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})

# ==========================================
# PAINEL DO INSTRUTOR (ADMIN)
# ==========================================
def render_admin_view():
    st.markdown("## ⚙️ Painel de Gestão do Instrutor — Prof. Filipe Brito")
    
    with st.sidebar:
        st.markdown("### 👨‍🏫 Instrutor Nível 3")
        st.caption("Filipe Brito")
        if st.button("Sair (Logout)", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    tab_alunos, tab_novo, tab_chat = st.tabs(["📋 Gestão de Alunos & Acreditação", "➕ Cadastrar Novo Aluno", "💬 Testar Chat do Tutor"])
    
    with tab_alunos:
        st.subheader("Alunos Cadastrados e Controle de Validade")
        alunos = auth.listar_alunos()
        
        if not alunos:
            st.info("Nenhum aluno cadastrado ainda. Use a aba ao lado para cadastrar.")
        else:
            for al in alunos:
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                with col1:
                    st.markdown(f"**{al['nome']}** (`{al['email']}`)")
                    st.caption(f"Turma: {al['turma']} | Curso: {datetime.date.fromisoformat(al['data_curso']).strftime('%d/%m/%Y')}")
                with col2:
                    if al['status'] == 'acreditado':
                        st.success(f"🏆 Acreditado\nAté {datetime.date.fromisoformat(al['data_expiracao']).strftime('%d/%m/%Y')}")
                    elif al['status'] == 'expirado':
                        st.error(f"❌ Expirado\n({datetime.date.fromisoformat(al['data_expiracao']).strftime('%d/%m/%Y')})")
                    else:
                        st.warning(f"📝 Pós-Curso (4 meses)\nAté {datetime.date.fromisoformat(al['data_expiracao']).strftime('%d/%m/%Y')}")
                with col3:
                    st.metric("Dias Restantes", f"{al['dias_restantes']} dias")
                with col4:
                    if al['status'] != 'acreditado':
                        if st.button(f"Homologar (+4 Anos)", key=f"btn_homologar_{al['id']}"):
                            sucesso, msg = auth.homologar_acreditacao(al['email'])
                            if sucesso:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
                    else:
                        st.write("Acreditação Vigente")
                st.divider()

    with tab_novo:
        st.subheader("Cadastrar Aluno de Turma Presencial")
        st.caption("Por padrão, novos alunos recebem acesso de **4 meses** a partir da data do curso para entrega dos 20 voluntários.")
        
        with st.form("form_novo_aluno"):
            novo_nome = st.text_input("Nome do Aluno")
            novo_email = st.text_input("E-mail do Aluno")
            nova_senha = st.text_input("Senha Inicial Provisória", value="isak2026")
            nova_turma = st.text_input("Identificador da Turma", value="ISAK N1 - São Paulo")
            nova_data_curso = st.date_input("Data de Término do Curso", value=datetime.date.today())
            
            submitted = st.form_submit_button("Cadastrar e Liberar Acesso (4 Meses)")
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
        st.subheader("Simulação do Chat do Tutor (Visão do Instrutor)")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        if admin_prompt := st.chat_input("Faça uma pergunta técnica para testar o bot...", key="admin_chat_input"):
            st.session_state.messages.append({"role": "user", "content": admin_prompt})
            with st.chat_message("user"):
                st.markdown(admin_prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("Analisando..."):
                    resp = st.session_state.bot.send_message(admin_prompt)
                    st.markdown(resp)
                    st.session_state.messages.append({"role": "assistant", "content": resp})

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
