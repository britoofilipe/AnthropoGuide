import sqlite3
import pytest
import auth


def test_init_db_adiciona_colunas_em_banco_antigo(tmp_path, monkeypatch):
    db = tmp_path / "antigo.db"
    with sqlite3.connect(db) as conn:
        conn.execute(
            "CREATE TABLE alunos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL,"
            " email TEXT UNIQUE NOT NULL, senha_hash TEXT NOT NULL, turma TEXT,"
            " data_curso DATE NOT NULL, status TEXT NOT NULL, data_expiracao DATE NOT NULL,"
            " perfis_aprovados INTEGER DEFAULT 0, data_aprovacao DATE)"
        )
    monkeypatch.setattr(auth, "DB_PATH", db)

    auth.init_db()
    auth.init_db()  # idempotente

    with sqlite3.connect(db) as conn:
        colunas = {linha[1] for linha in conn.execute("PRAGMA table_info(alunos)")}
    assert {"origem", "eduzz_sale_id", "precisa_trocar_senha"} <= colunas


def test_eduzz_sale_id_e_unico(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "novo.db")
    auth.init_db()
    with auth.get_db_connection() as conn:
        conn.execute(
            "INSERT INTO alunos (nome, email, senha_hash, turma, data_curso, status,"
            " data_expiracao, eduzz_sale_id) VALUES (?,?,?,?,?,?,?,?)",
            ("N", "a@x.com", "h", "T", "2026-09-23", "pos_curso", "2027-01-21", 777),
        )
        conn.commit()

        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO alunos (nome, email, senha_hash, turma, data_curso, status,"
                " data_expiracao, eduzz_sale_id) VALUES (?,?,?,?,?,?,?,?)",
                ("N", "b@x.com", "h", "T", "2026-09-23", "pos_curso", "2027-01-21", 777),
            )
            conn.commit()
