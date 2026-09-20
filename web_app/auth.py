"""
Módulo de Autenticação e Controle de Ciclo de Vida de Acesso — AnthropoGuide
Persistência Híbrida: Google Sheets (produção/permanente) com Fallback em SQLite local.

Regras de Acesso do Prof. Filipe Brito:
1. Pós-curso regular: Data do curso + 4 meses (120 dias).
2. Acreditação concluída (20 perfis aprovados): Data da aprovação + 4 anos (1460 dias).
"""

import os
import sqlite3
import hashlib
import datetime
import requests
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

try:
    import streamlit as st
except ImportError:
    st = None

DB_PATH = Path(__file__).parent / "anthropoguide.db"

def get_gsheets_url() -> Optional[str]:
    """Recupera a URL do Google Sheets do Streamlit Secrets ou do .env."""
    url = os.getenv("GSHEETS_URL")
    if not url and st is not None:
        try:
            url = st.secrets.get("GSHEETS_URL")
        except Exception:
            url = None
    return url.strip() if url else None

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def parse_date(val: Any) -> datetime.date:
    """Converte strings ISO, timestamps do Google Sheets ou objetos date para datetime.date."""
    if isinstance(val, datetime.date):
        return val
    s = str(val).split("T")[0].strip()
    return datetime.date.fromisoformat(s)

# ==========================================
# CAMADA GOOGLE SHEETS (PERSISTÊNCIA PERMANENTE)
# ==========================================

def gsheets_listar() -> List[Dict[str, Any]]:
    url = get_gsheets_url()
    if not url:
        return []
    
    resp = requests.get(url, timeout=12, allow_redirects=True)
    if resp.status_code != 200:
        raise RuntimeError(f"Google Sheets retornou status {resp.status_code}")
        
    rows = resp.json()
    hoje = datetime.date.today()
    resultado = []
    
    for r in rows:
        email = str(r.get("email", "")).strip().lower()
        nome = str(r.get("nome", "")).strip()
        if not email or not nome:
            continue
            
        data_curso_raw = r.get("data_curso") or hoje.isoformat()
        data_exp_raw = r.get("data_expiracao") or hoje.isoformat()
        
        try:
            data_exp = parse_date(data_exp_raw)
            data_curso = parse_date(data_curso_raw)
        except Exception:
            data_exp = hoje
            data_curso = hoje
            
        dias_restantes = (data_exp - hoje).days
        status = str(r.get("status", "pos_curso")).strip().lower()
        if hoje > data_exp and status != "expirado":
            status = "expirado"
            
        resultado.append({
            "id": r.get("id", len(resultado) + 1),
            "nome": nome,
            "email": email,
            "senha_hash": str(r.get("senha_hash", "")).strip(),
            "turma": str(r.get("turma", "ISAK N1")).strip(),
            "data_curso": data_curso.isoformat(),
            "status": status,
            "data_expiracao": data_exp.isoformat(),
            "dias_restantes": dias_restantes
        })
    return resultado

def gsheets_cadastrar(nome: str, email: str, senha_hash: str, turma: str, data_curso: datetime.date, data_expiracao: datetime.date) -> Tuple[bool, str]:
    url = get_gsheets_url()
    if not url:
        return False, "URL do Google Sheets não configurada."
        
    payload = {
        "action": "cadastrar",
        "nome": nome,
        "email": email,
        "senha_hash": senha_hash,
        "turma": turma,
        "data_curso": data_curso.isoformat(),
        "status": "pos_curso",
        "data_expiracao": data_expiracao.isoformat()
    }
    
    resp = requests.post(url, json=payload, timeout=12, allow_redirects=True)
    if resp.status_code == 200:
        return True, f"Aluno cadastrado com sucesso na planilha! Acesso ativo até {data_expiracao.strftime('%d/%m/%Y')} (4 meses)."
    return False, f"Falha ao gravar no Google Sheets: {resp.text}"

def gsheets_homologar(email: str, nova_expiracao: datetime.date) -> Tuple[bool, str]:
    url = get_gsheets_url()
    if not url:
        return False, "URL do Google Sheets não configurada."
        
    payload = {
        "action": "homologar",
        "email": email,
        "nova_expiracao": nova_expiracao.isoformat()
    }
    
    resp = requests.post(url, json=payload, timeout=12, allow_redirects=True)
    if resp.status_code == 200:
        return True, f"Acreditação homologada na planilha! Acesso estendido por +4 anos (até {nova_expiracao.strftime('%d/%m/%Y')})."
    return False, f"Falha ao homologar no Google Sheets: {resp.text}"

# ==========================================
# CAMADA SQLITE (FALLBACK LOCAL)
# ==========================================

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                turma TEXT,
                data_curso DATE NOT NULL,
                status TEXT NOT NULL,
                data_expiracao DATE NOT NULL,
                perfis_aprovados INTEGER DEFAULT 0,
                data_aprovacao DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# ==========================================
# INTERFACE PÚBLICA (ROTEAMENTO INTELIGENTE)
# ==========================================

def cadastrar_aluno(nome: str, email: str, senha: str, turma: str, data_curso: datetime.date) -> Tuple[bool, str]:
    email_clean = email.strip().lower()
    data_expiracao = data_curso + datetime.timedelta(days=120)
    senha_h = hash_password(senha)
    
    if get_gsheets_url():
        try:
            # Verifica se já existe na planilha
            existentes = gsheets_listar()
            if any(a["email"] == email_clean for a in existentes):
                return False, "Já existe um aluno cadastrado com este e-mail na planilha."
            return gsheets_cadastrar(nome.strip(), email_clean, senha_h, turma.strip(), data_curso, data_expiracao)
        except Exception as e:
            print(f"[Auth] Erro ao cadastrar no Google Sheets: {e}. Tentando fallback SQLite.")
            
    # Fallback SQLite
    try:
        with get_db_connection() as conn:
            conn.execute("""
                INSERT INTO alunos (nome, email, senha_hash, turma, data_curso, status, data_expiracao, perfis_aprovados)
                VALUES (?, ?, ?, ?, ?, 'pos_curso', ?, 0)
            """, (nome.strip(), email_clean, senha_h, turma.strip(), data_curso.isoformat(), data_expiracao.isoformat()))
            conn.commit()
        return True, f"Aluno cadastrado com sucesso! Acesso ativo até {data_expiracao.strftime('%d/%m/%Y')} (4 meses)."
    except sqlite3.IntegrityError:
        return False, "Já existe um aluno cadastrado com este e-mail."
    except Exception as e:
        return False, f"Erro ao cadastrar aluno: {str(e)}"

def homologar_acreditacao(email: str, data_aprovacao: Optional[datetime.date] = None) -> Tuple[bool, str]:
    if data_aprovacao is None:
        data_aprovacao = datetime.date.today()
        
    nova_expiracao = data_aprovacao + datetime.timedelta(days=1460)
    email_clean = email.strip().lower()
    
    if get_gsheets_url():
        try:
            return gsheets_homologar(email_clean, nova_expiracao)
        except Exception as e:
            print(f"[Auth] Erro ao homologar no Google Sheets: {e}. Tentando fallback SQLite.")
            
    # Fallback SQLite
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT id, nome FROM alunos WHERE email = ?", (email_clean,))
        aluno = cursor.fetchone()
        if not aluno:
            return False, "Aluno não encontrado."
            
        conn.execute("""
            UPDATE alunos 
            SET status = 'acreditado',
                perfis_aprovados = 1,
                data_aprovacao = ?,
                data_expiracao = ?
            WHERE email = ?
        """, (data_aprovacao.isoformat(), nova_expiracao.isoformat(), email_clean))
        conn.commit()
        
    return True, f"Acreditação homologada! Acesso de {aluno['nome']} estendido por +4 anos (até {nova_expiracao.strftime('%d/%m/%Y')})."

def verificar_acesso(email: str, senha: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    email_clean = email.strip().lower()
    senha_h = hash_password(senha)
    hoje = datetime.date.today()
    
    # 1. Tenta buscar no Google Sheets
    if get_gsheets_url():
        try:
            alunos = gsheets_listar()
            aluno = next((a for a in alunos if a["email"] == email_clean), None)
            if aluno:
                if aluno["senha_hash"] != senha_h:
                    return False, "E-mail ou senha incorretos.", None
                data_exp = parse_date(aluno["data_expiracao"])
                if hoje > data_exp:
                    return False, f"Seu período de acesso ao AnthropoGuide expirou em {data_exp.strftime('%d/%m/%Y')}. Entre em contato com o Prof. Filipe Brito para regularizar sua situação ou revalidação de acreditação.", aluno
                aluno["dias_restantes"] = (data_exp - hoje).days
                return True, "Acesso autorizado", aluno
        except Exception as e:
            print(f"[Auth] Falha na consulta ao Google Sheets: {e}. Recorrendo ao SQLite.")
            
    # 2. Fallback SQLite
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM alunos WHERE email = ?", (email_clean,))
        row = cursor.fetchone()
        
    if not row:
        return False, "E-mail ou senha incorretos.", None
        
    if row["senha_hash"] != senha_h:
        return False, "E-mail ou senha incorretos.", None
        
    aluno = dict(row)
    data_exp = parse_date(aluno["data_expiracao"])
    
    if hoje > data_exp:
        return False, f"Seu período de acesso ao AnthropoGuide expirou em {data_exp.strftime('%d/%m/%Y')}. Entre em contato com o Prof. Filipe Brito para regularizar sua situação ou revalidação de acreditação.", aluno

    aluno["dias_restantes"] = (data_exp - hoje).days
    return True, "Acesso autorizado", aluno

def listar_alunos() -> List[Dict[str, Any]]:
    # 1. Tenta listar do Google Sheets
    if get_gsheets_url():
        try:
            return gsheets_listar()
        except Exception as e:
            print(f"[Auth] Falha ao listar do Google Sheets: {e}. Listando do SQLite.")
            
    # 2. Fallback SQLite
    hoje = datetime.date.today()
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM alunos ORDER BY data_curso DESC, nome ASC")
        rows = cursor.fetchall()
        
    resultado = []
    for r in rows:
        d = dict(r)
        exp = parse_date(d["data_expiracao"])
        d["dias_restantes"] = (exp - hoje).days
        resultado.append(d)
    return resultado
