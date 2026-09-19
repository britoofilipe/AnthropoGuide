# Plano de Arquitetura e Implementação: Plataforma Web Privada AnthropoGuide

**Autor:** Prof. Filipe Brito (Instrutor Internacional ISAK Nível 3)  
**Projeto:** AnthropoGuide — Tutor Especialista em Cineantropometria  
**Data:** 19/09/2026  
**Status:** Planejado / Especificado  

---

## 1. Visão Geral e Estratégia de Negócio

Para garantir proteção irrestrita da propriedade intelectual do método do Prof. Filipe Brito e evitar o compartilhamento indiscriminado de links públicos, o tutor **AnthropoGuide** será disponibilizado através de uma **plataforma web fechada com controle de acesso por e-mail e ciclo de vida temporal**.

### ⏱️ Política de Acesso e Ciclo de Vida do Aluno

1. **Acesso Inicial (Regra Geral Pós-Curso — 4 Meses):**
   - **Gatilho:** Conclusão do curso presencial ISAK Nível 1.
   - **Janela de validade:** `Data do Curso + 4 meses` (120 dias).
   - **Objetivo:** Dar suporte intensivo ao aluno durante o período oficial de coleta dos 20 sujeitos em duplicata, preenchimento da planilha Excel, cálculo do $\%ETM$ e submissão no ISAKMetry.
   - **Suspensão:** Se o aluno não concluir a entrega e aprovação dos 20 perfis até o término dos 4 meses, o acesso à plataforma é **bloqueado automaticamente**.

2. **Acesso Estendido (Acreditação Concluída — 4 Anos):**
   - **Gatilho:** Aprovação formal dos 20 perfis pelo Prof. Filipe Brito no portal ISAKMetry e validação na Secretaria Central da ISAK Global.
   - **Extensão concedida:** **+4 anos** a contar da data de homologação/certificação.
   - **Fundamentação:** Coincide perfeitamente com a **vigência de 4 anos da acreditação internacional ISAK**, tornando o AnthropoGuide um assistente de cabeceira permanente durante todo o ciclo profissional ativo do antropometrista.

---

## 2. Arquitetura do Sistema

```
[ ALUNO (Celular / Desktop) ]
             │
             ▼
   [ Tela de Autenticação ] ──▶ Validação no Supabase Auth
             │
             ▼
   [ Checagem de Validade ] ──▶ data_expiracao >= data_atual?
      ├── Se NÃO: Exibe tela "Acesso expirado / Entre em contato com Prof. Filipe"
      └── Se SIM: Libera acesso à interface
             │
             ▼
   [ Interface de Chat Privada ] (Next.js / Tailwind / KaTeX)
             │
             ▼ (Requisição segura com Token JWT)
   [ Backend Serverless (API Route) ]
      ├── Injeção do System Prompt v2.4 (Oculto)
      ├── Injeção dos 8 Módulos da Knowledge Base (Ocultos)
      ├── Chave Secreta da API (GEMINI_API_KEY)
      └── Bloqueio de múltiplas sessões simultâneas (anti-rateio)
             │
             ▼
   [ Google Gemini API (Gemini 2.0 Flash / AI Studio) ]
```

---

## 3. Estrutura do Banco de Dados (Supabase / PostgreSQL)

### Tabela `alunos`:
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | `uuid` | Chave primária (ID do Supabase Auth) |
| `nome` | `text` | Nome completo do aluno |
| `email` | `text` | E-mail cadastrado no curso (único) |
| `turma` | `text` | Código da turma (ex.: `ISAK-N1-2026.2-SP`) |
| `data_curso` | `date` | Data de término do curso presencial |
| `status` | `enum` | `'pos_curso'`, `'acreditado'`, `'expirado'` |
| `data_expiracao` | `timestamptz` | Inicialmente `data_curso + 120 dias` |
| `perfis_aprovados`| `boolean` | `true` quando aprovado pelo Prof. Filipe |
| `data_aprovacao` | `date` | Data da aprovação no ISAKMetry |
| `sessao_ativa_id`| `text` | Token de controle de sessão única |

---

## 4. Painel de Administração do Instrutor (Prof. Filipe Brito)

O sistema contará com uma interface administrativa simplificada para o professor:
* **Importação da Turma:** Colar uma lista de e-mails e nomes da nova turma, selecionando a data do curso presencial. O sistema gera os convites por e-mail com validade automática de 4 meses.
* **Homologação 1-Clique:** Ao auditar e aprovar os 20 perfis do aluno no ISAKMetry, o professor pesquisa o aluno no painel e clica em **"Aprovar Acreditação"**. O status muda para `'acreditado'` e a validade é estendida automaticamente por **+4 anos**.
* **Métricas de Uso:** Visualizar quais alunos mais interagem e quais ainda não começaram a tirar dúvidas sobre o pós-curso.
