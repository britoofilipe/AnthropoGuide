# ADR 003 — Orientação e Validação da Equação de Petroski Feminina (4 Dobras ISAK)

**Data:** 19/09/2026  
**Status:** Aprovado e Implementado  
**Decisores:** Prof. Filipe Brito (Instrutor Internacional ISAK Nível 3) e Antigravity AI  

---

## 1. Contexto

Durante os testes de validação com o tutor AnthropoGuide (versão 2.0), identificou-se uma resposta inadequada do modelo ao analisar a avaliação de mulheres: o tutor contraindicou o uso da equação de Petroski (1995) com a justificativa de que a fórmula exigiria a dobra cutânea *axilar média*.

### Problema Identificado:
1. A literatura comercial de massa e diversos softwares de nutrição/educação física difundiram quase que exclusivamente a versão logarítmica feminina de Petroski com a dobra axilar média ($AXM + SI + CX + PE$).
2. **Fato Metodológico Crucial da ISAK:** A dobra cutânea axilar (ou axilar média) **NÃO faz parte de NENHUM perfil antropométrico da ISAK** (nem do Perfil Restrito N1 com 8 dobras, nem do Perfil Completo N2 com 9 dobras, onde a única dobra adicionada é a do antebraço). Portanto, a dobra axilar é totalmente estranha ao protocolo ISAK.
3. No entanto, na sua tese de doutorado original (UFSM, 1995), Edio Luiz Petroski desenvolveu e validou **16 modelos matemáticos para cada sexo**, incluindo uma versão feminina que utiliza **exatamente as mesmas 4 dobras da equação masculina**: Tríceps (TR), Subescapular (SE), Crista Ilíaca/Suprailíaca (SI) e Perna (PE).
4. Todas as 4 dobras desse modelo fazem parte do **Perfil Restrito ISAK Nível 1**.
5. Contraindicar Petroski para mulheres no curso ISAK N1 privava os alunos de uma das ferramentas nacionais mais consagradas e validadas por pesagem hidrostática.

---

## 2. Decisão

1. **Adotar Oficialmente a Versão de 4 Dobras ISAK para Mulheres:**
   - Para mulheres brasileiras adultas (18 a 51 anos), a equação de escolha indicada no curso do Prof. Filipe Brito é o modelo quadrático com as 4 dobras padronizadas:
     $$D_b = 1,12948287 - 0,00072714 \times (\sum 4D) + 0,00000188 \times (\sum 4D)^2 - 0,00044733 \times (\text{Idade})$$
     Onde:
     $$\sum 4D = \text{TR} + \text{SE} + \text{SI} + \text{PE} \quad (\text{todas em } mm)$$
     E conversão para %G via equação de Siri (1956).

2. **Nomenclatura Padronizada:**
   - A dobra cutânea da região distal do membro inferior deve ser denominada estritamente como **dobra da perna** (ou **perna**), nunca como "perna medial".

3. **Diretriz Mandatória no System Prompt:**
   - O tutor AnthropoGuide fica expressamente proibido de contraindicar Petroski para o público feminino alegando ausência da dobra axilar média (reafirmando que a dobra axilar não existe em nenhum nível da ISAK).
   - O tutor deve atuar de forma pedagógica e desmistificadora: esclarecer que a dobra axilar não é ISAK, e que existe a versão de Petroski com as 4 dobras ISAK (TR, SE, SI, PE), amplamente validada para a população brasileira e **oficialmente recomendada e ensinada no curso ISAK N1**.

4. **Atualização da Base de Conhecimento:**
   - O arquivo `knowledge_base/03_equacoes_brasileiras.md` foi atualizado na seção 2.2, documentando a fórmula oficial das 4 dobras ISAK e criando uma subseção histórica sobre a versão com axilar média.

---

## 3. Consequências

- **Positivas:**
  - Alinha perfeitamente as orientações do Gem às aulas práticas e teóricas ministradas pelo Prof. Filipe Brito no credenciamento ISAK N1.
  - Elimina uma falsa barreira metodológica para os alunos ao avaliarem mulheres não atletas no Brasil.
  - O tutor ganha autoridade conceitual ao explicar o contexto histórico dos 16 modelos da tese de Petroski frente ao reducionismo de softwares comerciais.
- **Governança:**
  - `knowledge_base/03_equacoes_brasileiras.md` e `knowledge_base/01_escopo_e_protocolo_isak.md` atualizados.
  - `SYSTEM_PROMPT_ANTHROPOGUIDE.md` atualizado para a versão 2.2.
  - Cópia arquivada em `versions/system_prompt_v2_2_calibrado.md`.
