# ADR 005: Incorporação dos Tutoriais Oficiais do ISAKMetry e Envio dos 20 Perfis Pós-Curso

**Data:** 19/09/2026  
**Status:** Aprovado  
**Contexto:** Formação de Avaliadores ISAK Nível 1 pelo Prof. Filipe Brito (Instrutor Nível 3)  
**Fontes Oficiais:** Canal Oficial da ISAK Global no YouTube (`@isakglobal410`), Manual ISAK 2019 e ISAK Accreditation Handbook 2026 (10ª versão).

---

## 1. Contexto e Motivação
A conclusão do curso presencial ISAK Nível 1 não encerra o processo de certificação internacional. Para obter o título de Antropometrista Credenciado Nível 1, o aluno deve realizar a tarefa pós-curso: mensurar **20 voluntários em duplicata** dentro do prazo improrrogável de **4 meses** e submetê-los para auditoria através da plataforma oficial em nuvem **ISAKMetry** ([www.isak.global](https://www.isak.global)).

A análise detalhada dos vídeos tutoriais publicados pelo canal oficial da ISAK Global revelou fluxos operacionais críticos (tanto para o aluno quanto para o instrutor) que precisam ser dominados pelo tutor **AnthropoGuide** para orientar os alunos com máxima precisão.

---

## 2. Decisões Adotadas

### 2.1 Mapeamento dos Fluxos do ISAKMetry
1. **Acesso do Aluno:**
   - Login no portal `www.isak.global` com as credenciais de membro ISAK.
   - Navegação: Menu **ISAKMetry** -> **"Courses / Mis Cursos"** -> Seleção do curso do Prof. Filipe Brito -> Seção **"Sending 20 subjects" / "Envío de 20 sujetos"**.
2. **Métodos de Entrada de Dados (21 variáveis em duplicata):**
   - **Carga em Lote via Excel ("Measurements from Excel") [Preferencial]:** Download do *template* oficial `.xlsx`, preenchimento padronizado das 2 séries de medidas (M1 e M2) e upload simultâneo.
   - **Cadastro Manual ("Create Subjects" & "Measurements"):** Cadastro individual de cada sujeito seguido da digitação pontual das medidas.
3. **Auditoria Estatística Automática do %ETM:**
   - O ISAKMetry calcula o %ETM intra-avaliador do conjunto dos 20 sujeitos.
   - Limites obrigatórios da ISAK:
     * Dobras cutâneas: $\%ETM \le 7,5\%$ (Meta do curso: $\le 5,0\%$).
     * Demais medidas: $\%ETM \le 1,5\%$ (Meta do curso: $\le 1,0\%$).
   - Estando em conformidade, o aluno clica no botão oficial **"Send to Instructor" / "Enviar al Instructor"**.
4. **Fluxo de Confirmação pelo Instrutor (Prof. Filipe Brito):**
   - O Instrutor Nível 3 acessa a fila de submissões pós-curso do sistema.
   - Avalia a consistência dos relatórios de ETM e a plausibilidade dos dados.
   - Clica em **"Confirm / Approve" (Aprovar)**.
   - A aprovação aciona a validação automática perante a Secretaria Central da ISAK Global, liberando o diploma digital e o número de registro internacional do aluno.
5. **Recursos Complementares:**
   - **"Downloading your measures":** Download de toda a base de dados histórica do profissional em planilha Excel/CSV para backup e pesquisas.
   - Módulos de agendamento de consultas (*Appointments*) e relatórios clínicos (*Reports*).

---

## 3. Impactos na Base de Conhecimento e System Prompt
- **`02_qualidade_da_medida.md`:** Seção 5.3 adicionada contendo o roteiro passo a passo do ISAKMetry, carga via Excel, limites de tolerância e fluxo de auditoria do instrutor.
- **`SYSTEM_PROMPT_ANTHROPOGUIDE.md` (v2.3):** Adicionado bloco específico no item 1 de evidências com as orientações operacionais do ISAKMetry e prazo de 4 meses.
- **`versions/system_prompt_v2_3_isakmetry_tutoriais.md`:** Registrado o snapshot da nova versão estável.
