"""Cria e revoga o acesso do aluno a partir de uma venda da Eduzz.
Toda escrita passa por auth.py, que cuida da planilha e do fallback SQLite."""
import datetime
import secrets
import sqlite3

import auth

ALFABETO = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789"


def gerar_senha_provisoria() -> str:
    return "".join(secrets.choice(ALFABETO) for _ in range(10))


def ja_processada(sale_id: int) -> bool:
    if auth.get_gsheets_url():
        try:
            if any(a.get("eduzz_sale_id") == sale_id for a in auth.gsheets_listar()):
                return True
        except Exception as e:
            print(f"[Liberacao] Nao foi possivel conferir a planilha: {e}. Usando o SQLite.")
    with auth.get_db_connection() as conn:
        achou = conn.execute(
            "SELECT 1 FROM alunos WHERE eduzz_sale_id = ?", (sale_id,)
        ).fetchone()
    return achou is not None


def liberar(venda: dict, prazo_dias: int):
    sale_id = venda["id"]
    if ja_processada(sale_id):
        return None

    email = venda["buyer"]["email"].strip().lower()
    nome = venda["buyer"]["name"].strip()
    compra = datetime.datetime.fromisoformat(venda["paidAt"]).date()
    validade = compra + datetime.timedelta(days=prazo_dias)
    senha = gerar_senha_provisoria()

    try:
        ok, msg = auth.cadastrar_aluno(
            nome, email, senha, "Eduzz", compra,
            origem="eduzz", eduzz_sale_id=sale_id, precisa_trocar_senha=1,
            data_expiracao=validade,
        )
    except sqlite3.IntegrityError:
        return None
    if not ok:
        return None
    return {"nome": nome, "email": email, "senha": senha, "validade": validade, "sale_id": sale_id}


def bloquear(venda: dict) -> bool:
    sale_id = venda["id"]
    bloqueou_planilha = False
    if auth.get_gsheets_url():
        try:
            bloqueou_planilha, _ = auth.gsheets_bloquear(sale_id)
        except Exception as e:
            print(f"[Liberacao] Falha ao bloquear na planilha: {e}. Seguindo pelo SQLite.")

    with auth.get_db_connection() as conn:
        cur = conn.execute(
            "UPDATE alunos SET status = 'expirado', data_expiracao = ?"
            " WHERE eduzz_sale_id = ? AND status != 'expirado'",
            (datetime.date.today().isoformat(), sale_id),
        )
        conn.commit()
    return bloqueou_planilha or cur.rowcount > 0
