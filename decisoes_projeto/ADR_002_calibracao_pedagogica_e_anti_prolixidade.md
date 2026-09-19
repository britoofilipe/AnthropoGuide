# ADR 002 — Calibração Pedagógica, Anti-Prolixidade e Flexibilidade em 3 Níveis

**Data:** 19/09/2026  
**Status:** Aprovado e Implementado  
**Decisores:** Prof. Filipe Brito (Instrutor ISAK N3) e Antigravity AI  

---

## 1. Contexto

Após os primeiros testes práticos com o Gem AnthropoGuide (versão 1.0), observou-se que o modelo adotava uma postura excessivamente rígida e prolixa. Ele aplicava a estrutura completa de 7 passos com títulos formais em todas as respostas (inclusive em perguntas de acompanhamento de uma única linha), gerando repetições cerimoniosas da "regra de ouro" e textos de mais de 1.200 palavras, o que causava fadiga cognitiva e afastava o tutor da realidade do aluno.

Além disso, identificou-se que o aluno utiliza o tutor em momentos distintos:
1. Dúvida rápida de consultório/exame (exige resposta em 15 segundos).
2. Discussão de caso clínico ou esportivo (exige comparação enxuta e orientação prática).
3. Estudo conceitual e aprofundamento (exige fundamentação biológica e matemática detalhada).

## 2. Decisão

Substituir o modelo rígido de 7 passos obrigatórios por uma estratégia de **Divulgação Progressiva (*Progressive Disclosure*)** estruturada em:

1. **Princípio da Pirâmide Invertida:** A resposta direta e inequívoca vem logo no primeiro parágrafo, eliminando cerimônias de abertura e repetições automáticas da regra de ouro.
2. **Os 3 Níveis de Profundidade:**
   - **Nível 1 (Factual/Rápido):** 2 a 4 linhas ou 1 tabela compacta com a fonte.
   - **Nível 2 (Discussão de Caso/Método):** Recomendação executiva, comparação enxuta das opções cabíveis (destacando somatórios vs %G) e **fechamento com gancho reflexivo**.
   - **Nível 3 (Imersão Teórica):** Dissecção profunda das premissas biológicas, modelos matemáticos e história dos métodos (acionada apenas quando o aluno pede explicitamente).
3. **Follow-ups Ágeis:** Proibição de reintroduzir os dados do paciente ou recitar conceitos já expostos nas mensagens anteriores da mesma conversa.
4. **Incorporação Oficial de Campa et al. (2025) e Frisancho (1990/2008):** O enquadramento de somatórios de 6 e 8 dobras é feito prioritariamente pelas tabelas de Campa 2025 sob as categorias percentílicas de Frisancho.
5. **Trava de Plausibilidade Biológica:** Verificação ativa da compatibilidade entre a magnitude do somatório milimétrico e o %G estimado, evitando discrepâncias matemáticas não fisiológicas.

## 3. Consequências

- **Positivas:** O tutor torna-se extremamente ágil, agradável e próximo de uma conversa real com o Prof. Filipe Brito. Reduz drasticamente o tempo de leitura do aluno e estimula o pensamento crítico ativo através dos ganchos pedagógicos.
- **Governança:** A versão 1.0 foi arquivada em `versions/system_prompt_v1_0_rigido.md` e a versão 2.0 ativada em `SYSTEM_PROMPT_ANTHROPOGUIDE.md`.
