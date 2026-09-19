"""
Script de Teste Automatizado — Validação das Regras de Negócio e Contexto
"""

import sys
import datetime
from pathlib import Path

# Garante suporte a emojis no console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import auth
from gemini_service import load_system_context

def run_tests():
    print("Iniciando testes da Plataforma Web AnthropoGuide...")
    
    # 1. Teste de Inicialização do Banco
    auth.init_db()
    print("✅ 1. Banco SQLite inicializado com sucesso.")
    
    # 2. Teste de Cadastro com Regra de 4 Meses (120 dias)
    hoje = datetime.date.today()
    email_teste = "aluno.teste@isak.com"
    
    # Limpa caso já exista
    with auth.get_db_connection() as conn:
        conn.execute("DELETE FROM alunos WHERE email = ?", (email_teste,))
        conn.commit()
        
    sucesso, msg = auth.cadastrar_aluno(
        nome="Aluno Teste Pós-Curso",
        email=email_teste,
        senha="senha123",
        turma="Turma N1 - 2026",
        data_curso=hoje
    )
    assert sucesso, f"Falha no cadastro: {msg}"
    print(f"✅ 2. Aluno cadastrado: {msg}")
    
    # 3. Teste de Verificação de Acesso Ativo (Pós-Curso)
    valido, msg, dados = auth.verificar_acesso(email_teste, "senha123")
    assert valido, f"Deveria estar válido: {msg}"
    assert dados["status"] == "pos_curso", "Status deve ser pos_curso"
    assert dados["perfis_aprovados"] == 0, "Perfis ainda não aprovados"
    assert dados["dias_restantes"] >= 119, f"Dias restantes esperados ~120, obtido {dados['dias_restantes']}"
    print(f"✅ 3. Acesso ativo confirmado (Dias restantes: {dados['dias_restantes']}).")
    
    # 4. Teste de Homologação de Acreditação (+4 Anos / 1460 dias)
    sucesso_homolog, msg_homolog = auth.homologar_acreditacao(email_teste, hoje)
    assert sucesso_homolog, f"Falha na homologação: {msg_homolog}"
    print(f"✅ 4. Homologação efetuada: {msg_homolog}")
    
    # Re-verifica dados após homologação
    valido, msg, dados_homolog = auth.verificar_acesso(email_teste, "senha123")
    assert valido, "Deve continuar válido após homologação"
    assert dados_homolog["status"] == "acreditado", "Status deve ser acreditado"
    assert dados_homolog["perfis_aprovados"] == 1, "Perfis devem estar aprovados"
    assert dados_homolog["dias_restantes"] >= 1450, f"Dias restantes esperados ~1460, obtido {dados_homolog['dias_restantes']}"
    print(f"✅ 5. Extensão de +4 anos validada com sucesso ({dados_homolog['dias_restantes']} dias restantes).")
    
    # 5. Teste de Contexto da IA (System Prompt v2.4 + 8 Módulos)
    contexto = load_system_context()
    assert "AnthropoGuide" in contexto, "Nome do bot deve constar no contexto"
    assert "BLINDAGEM E PROTEÇÃO DA PROPRIEDADE INTELECTUAL" in contexto, "Blindagem deve constar no contexto"
    assert "01_escopo_e_protocolo_isak.md" in contexto, "Módulo 01 deve constar"
    assert "02_qualidade_da_medida.md" in contexto, "Módulo 02 deve constar"
    assert "03_equacoes_brasileiras.md" in contexto, "Módulo 03 deve constar"
    assert "04_equacoes_atletas.md" in contexto, "Módulo 04 deve constar"
    assert "05_percentis_e_referencias.md" in contexto, "Módulo 05 deve constar"
    assert "06_indicadores_e_cortes.md" in contexto, "Módulo 06 deve constar"
    assert "07_metodos_e_limitacoes.md" in contexto, "Módulo 07 deve constar"
    assert "08_bibliografia_e_procedencia.md" in contexto, "Módulo 08 deve constar"
    print(f"✅ 6. Contexto completo da IA verificado ({len(contexto)} caracteres injetados com blindagem e 8 módulos).")
    
    print("\n🎉 TODOS OS TESTES PASSARAM COM 100% DE SUCESSO!")

if __name__ == "__main__":
    run_tests()
