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
import hmac
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
    """Gera hash de senha com salt aleatório usando scrypt.

    Formato: "scrypt$<salt_hex>$<hash_hex>"
    """
    salt = os.urandom(16)
    derivado = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return f"scrypt${salt.hex()}${derivado.hex()}"


def conferir_senha(senha: str, armazenado: str) -> bool:
    """Verifica se a senha corresponde ao hash armazenado.

    Aceita dois formatos:
    - Novo: "scrypt$<salt_hex>$<hash_hex>" (com salt aleatório)
    - Legado: SHA-256 puro (64 caracteres hexadecimais)

    Sempre usa hmac.compare_digest para evitar timing attacks.
    Retorna False em qualquer formato inesperado sem lançar exceção.
    """
    if armazenado.startswith("scrypt$"):
        partes = armazenado.split("$")
        if len(partes) != 3:
            return False

        _, salt_hex, esperado = partes
        try:
            salt = bytes.fromhex(salt_hex)
            derivado = hashlib.scrypt(
                senha.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32
            )
            return hmac.compare_digest(derivado.hex(), esperado)
        except (ValueError, OverflowError):
            return False

    return hmac.compare_digest(hashlib.sha256(senha.encode("utf-8")).hexdigest(), armazenado)

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

        # Parse eduzz_sale_id com tolerância a valores não-numéricos
        eduzz_sale_id_valor = None
        try:
            sale_id_str = str(r.get("eduzz_sale_id") or "").strip()
            if sale_id_str:
                eduzz_sale_id_valor = int(sale_id_str)
        except (TypeError, ValueError):
            # Valor não-numérico ou inválido: mantém None
            pass

        # Parse precisa_trocar_senha com tolerância a valores não-numéricos
        precisa_trocar_senha_valor = 0
        try:
            senha_val = r.get("precisa_trocar_senha") or 0
            precisa_trocar_senha_valor = int(senha_val)
        except (TypeError, ValueError):
            # Valor não-numérico ou inválido: default seguro 0 (não precisa trocar)
            pass

        resultado.append({
            "id": r.get("id", len(resultado) + 1),
            "nome": nome,
            "email": email,
            "senha_hash": str(r.get("senha_hash", "")).strip(),
            "turma": str(r.get("turma", "ISAK N1")).strip(),
            "data_curso": data_curso.isoformat(),
            "status": status,
            "data_expiracao": data_exp.isoformat(),
            "dias_restantes": dias_restantes,
            "origem": str(r.get("origem") or "manual").strip().lower(),
            "eduzz_sale_id": eduzz_sale_id_valor,
            "precisa_trocar_senha": precisa_trocar_senha_valor
        })
    return resultado

def gsheets_cadastrar(nome: str, email: str, senha_hash: str, turma: str, data_curso: datetime.date, data_expiracao: datetime.date, origem: str = "manual", eduzz_sale_id: Optional[int] = None, precisa_trocar_senha: int = 0) -> Tuple[bool, str]:
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
        "data_expiracao": data_expiracao.isoformat(),
        "origem": origem,
        "eduzz_sale_id": eduzz_sale_id,
        "precisa_trocar_senha": precisa_trocar_senha
    }

    resp = requests.post(url, json=payload, timeout=12, allow_redirects=True)
    if resp.status_code == 200:
        return True, f"Aluno cadastrado com sucesso na planilha! Acesso ativo até {data_expiracao.strftime('%d/%m/%Y')} (4 meses)."
    return False, f"Falha ao gravar no Google Sheets: {resp.text}"

def gsheets_trocar_senha(email: str, senha_hash: str) -> Tuple[bool, str]:
    url = get_gsheets_url()
    if not url:
        return False, "URL do Google Sheets não configurada."
    resp = requests.post(
        url, json={"action": "trocar_senha", "email": email, "senha_hash": senha_hash},
        timeout=12, allow_redirects=True,
    )
    if resp.status_code == 200:
        return True, "Senha alterada na planilha."
    return False, f"Falha ao trocar a senha no Google Sheets: {resp.text}"


def gsheets_bloquear(eduzz_sale_id: int) -> Tuple[bool, str]:
    url = get_gsheets_url()
    if not url:
        return False, "URL do Google Sheets não configurada."
    resp = requests.post(
        url, json={"action": "bloquear", "eduzz_sale_id": eduzz_sale_id},
        timeout=12, allow_redirects=True,
    )
    if resp.status_code == 200:
        return True, "Acesso bloqueado na planilha."
    return False, f"Falha ao bloquear no Google Sheets: {resp.text}"

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
        colunas = {linha[1] for linha in conn.execute("PRAGMA table_info(alunos)")}
        for nome, definicao in (
            ("origem", "TEXT DEFAULT 'manual'"),
            ("eduzz_sale_id", "INTEGER"),
            ("precisa_trocar_senha", "INTEGER DEFAULT 0"),
        ):
            if nome not in colunas:
                conn.execute(f"ALTER TABLE alunos ADD COLUMN {nome} {definicao}")
        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_alunos_eduzz_sale"
            " ON alunos (eduzz_sale_id) WHERE eduzz_sale_id IS NOT NULL"
        )
        conn.commit()

# ==========================================
# INTERFACE PÚBLICA (ROTEAMENTO INTELIGENTE)
# ==========================================

def cadastrar_aluno(nome: str, email: str, senha: str, turma: str, data_curso: datetime.date, origem: str = "manual", eduzz_sale_id: Optional[int] = None, precisa_trocar_senha: int = 0) -> Tuple[bool, str]:
    email_clean = email.strip().lower()
    data_expiracao = data_curso + datetime.timedelta(days=120)
    senha_h = hash_password(senha)

    if get_gsheets_url():
        try:
            # Verifica se já existe na planilha
            existentes = gsheets_listar()
            if any(a["email"] == email_clean for a in existentes):
                return False, "Já existe um aluno cadastrado com este e-mail na planilha."
            return gsheets_cadastrar(nome.strip(), email_clean, senha_h, turma.strip(), data_curso, data_expiracao, origem=origem, eduzz_sale_id=eduzz_sale_id, precisa_trocar_senha=precisa_trocar_senha)
        except Exception as e:
            print(f"[Auth] Erro ao cadastrar no Google Sheets: {e}. Tentando fallback SQLite.")

    # Fallback SQLite
    try:
        with get_db_connection() as conn:
            conn.execute("""
                INSERT INTO alunos (nome, email, senha_hash, turma, data_curso, status, data_expiracao, perfis_aprovados, origem, eduzz_sale_id, precisa_trocar_senha)
                VALUES (?, ?, ?, ?, ?, 'pos_curso', ?, 0, ?, ?, ?)
            """, (nome.strip(), email_clean, senha_h, turma.strip(), data_curso.isoformat(), data_expiracao.isoformat(), origem, eduzz_sale_id, precisa_trocar_senha))
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
    hoje = datetime.date.today()

    # 1. Tenta buscar no Google Sheets
    if get_gsheets_url():
        try:
            alunos = gsheets_listar()
            aluno = next((a for a in alunos if a["email"] == email_clean), None)
            if aluno:
                if not conferir_senha(senha, aluno["senha_hash"]):
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

        if not conferir_senha(senha, row["senha_hash"]):
            return False, "E-mail ou senha incorretos.", None

        # Regravar hash se for legado (SHA-256 sem scrypt) — mesma conexão
        if not row["senha_hash"].startswith("scrypt$"):
            novo_hash = hash_password(senha)
            conn.execute("UPDATE alunos SET senha_hash = ? WHERE email = ?", (novo_hash, email_clean))
            conn.commit()

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
