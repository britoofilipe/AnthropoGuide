# ADR 001 — Arquitetura Modular da Base de Conhecimento

**Data:** 19/09/2026  
**Status:** Aprovado e Implementado  
**Decisores:** Prof. Filipe Brito (Instrutor ISAK N3) e Antigravity AI  

---

## 1. Contexto

Para capacitar o Gem AnthropoGuide com conhecimento técnico e pedagógico sem sobrecarregar a janela de contexto com PDFs brutos (muitos deles com restrições de direitos autorais ou tabelas mal extraídas por OCR), era necessário definir como estruturar a base de dados enviada ao Gemini (Google AI Pro).

## 2. Decisão

Adotar uma arquitetura de **Base de Conhecimento Modular em 8 Arquivos Markdown Autorais**, curados diretamente das fontes primárias (Manual ISAK 2019, Handbook 2026, Springer 2025, teses de Petroski e Costa, e artigos de Withers e Campa):

- `01_escopo_e_protocolo_isak.md`: 21 medidas N1, convenções e regras de medição.
- `02_qualidade_da_medida.md`: ETM intra/inter, %ETM, tolerâncias e troika.
- `03_equacoes_brasileiras.md`: Petroski (1995), Guedes (1985/1994) e Lee (2000).
- `04_equacoes_atletas.md`: Paradigma dos somatórios em mm, Withers et al. (1987) e Somatotipo de Heath-Carter (1990).
- `05_percentis_e_referencias.md`: Curvas de Campa et al. (2025) para $\sum 6$ e $\sum 8$, regras de Frisancho e dados de Costa (2001).
- `06_indicadores_e_cortes.md`: IMC, Cintura (OMS/IDF), RCEst, RCQ e Índice de Conicidade.
- `07_metodos_e_limitacoes.md`: Modelos 2C a 5C, Siri, Brozek, premissas da densidade da MLG e comparativo instrumental.
- `08_bibliografia_e_procedencia.md`: Inventário e controle de procedência de 22 referências primárias.

## 3. Consequências

- **Positivas:** Indexação semântica ultrarrápida no Gemini Gems, ausência de alucinação sobre normas oficiais, conformidade estrita com direitos autorais e facilidade de manutenção/versionamento módulo a módulo.
- **Negativas/Atenção:** Exige transcrição e conferência visual rigorosa de toda nova tabela percentílica antes de incorporá-la à base.
