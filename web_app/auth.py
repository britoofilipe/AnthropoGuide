"""
Módulo de Autenticação e Controle de Ciclo de Vida de Acesso — AnthropoGuide
Regras de Acesso do Prof. Filipe Brito:
1. Pós-curso regular: Data do curso + 4 meses (120 dias).
2. Acreditação concluída (20 perfis aprovados): Data da aprovação + 4 anos (1460 dias).
"""

import sqlite3
import hashlib
import datetime
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

DB_PATH = Path(__file__).parent / "anthropoguide.db"

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

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
                status TEXT NOT NULL, -- 'pos_curso', 'acreditado', 'expirado'
                data_expiracao DATE NOT NULL,
                perfis_aprovados INTEGER DEFAULT 0,
                data_aprovacao DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        # Seed inicial: Se o banco na nuvem for recém-criado, garante a conta de teste
        cursor = conn.execute("SELECT COUNT(*) as total FROM alunos")
        if cursor.fetchone()["total"] == 0:
            hoje = datetime.date.today()
            exp_4anos = hoje + datetime.timedelta(days=1460)
            conn.execute("""
                INSERT INTO alunos (nome, email, senha_hash, turma, data_curso, status, data_expiracao, perfis_aprovados, data_aprovacao)
                VALUES ('Aluno Teste Pós-Curso', 'aluno.teste@isak.com', ?, 'Turma N1 - 2026', ?, 'acreditado', ?, 1, ?)
            """, (hash_password("senha123"), hoje.isoformat(), exp_4anos.isoformat(), hoje.isoformat()))
            conn.commit()

def cadastrar_aluno(nome: str, email: str, senha: str, turma: str, data_curso: datetime.date) -> Tuple[bool, str]:
    email_clean = email.strip().lower()
    # Regra 1: Data do curso + 4 meses (120 dias)
    data_expiracao = data_curso + datetime.timedelta(days=120)
    senha_h = hash_password(senha)
    
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
    """
    Regra 2: Para aqueles que entregarem os 20 perfis e concluírem a acreditação:
    Acesso estendido por mais 4 anos (1460 dias) a partir da data de aprovação.
    """
    if data_aprovacao is None:
        data_aprovacao = datetime.date.today()
        
    nova_expiracao = data_aprovacao + datetime.timedelta(days=1460) # 4 anos
    email_clean = email.strip().lower()
    
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
    
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM alunos WHERE email = ?", (email_clean,))
        row = cursor.fetchone()
        
    if not row:
        return False, "E-mail ou senha incorretos.", None
        
    if row["senha_hash"] != senha_h:
        return False, "E-mail ou senha incorretos.", None
        
    aluno = dict(row)
    data_exp = datetime.date.fromisoformat(aluno["data_expiracao"])
    
    # Checagem de expiração temporal
    if hoje > data_exp:
        # Atualiza status para expirado no banco se necessário
        if aluno["status"] != "expirado":
            with get_db_connection() as conn:
                conn.execute("UPDATE alunos SET status = 'expirado' WHERE id = ?", (aluno["id"],))
                conn.commit()
            aluno["status"] = "expirado"
            
        return False, f"Seu período de acesso ao AnthropoGuide expirou em {data_exp.strftime('%d/%m/%Y')}. Entre em contato com o Prof. Filipe Brito para regularizar sua situação ou revalidação de acreditação.", aluno

    dias_restantes = (data_exp - hoje).days
    aluno["dias_restantes"] = dias_restantes
    return True, "Acesso autorizado", aluno

def listar_alunos() -> List[Dict[str, Any]]:
    hoje = datetime.date.today()
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM alunos ORDER BY data_curso DESC, nome ASC")
        rows = cursor.fetchall()
        
    resultado = []
    for r in rows:
        d = dict(r)
        exp = datetime.date.fromisoformat(d["data_expiracao"])
        d["dias_restantes"] = (exp - hoje).days
        resultado.append(d)
    return resultado
