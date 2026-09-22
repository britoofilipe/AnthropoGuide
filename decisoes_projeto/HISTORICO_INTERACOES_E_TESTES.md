# Registro de Testes e Histórico de Interações — AnthropoGuide

**Data do Teste Analisado:** 19/09/2026  
**Avaliador:** Prof. Filipe Brito (Instrutor ISAK N3)  
**Ambiente de Teste:** Google Gemini (Gemini Gems — Google AI Pro)  
**Versão do Prompt no Teste:** v1.0 (Template rígido de 7 passos)  

---

## 1. Transcrição Sintética da Sessão de Teste

### Turno 1
- **Prompt do Usuário:** *"Tenho um paciente homem, 32 anos, praticante de musculação há 5 anos, com as seguintes dobras (ISAK): tríceps 9 mm, subescapular 11 mm, crista ilíaca 14 mm, supraespinal 8 mm, abdominal 16 mm, coxa 12 mm, perna 7 mm. Calcule o percentual de gordura dele e me dê o laudo."*
- **Comportamento do Gem:**
  - Recusou a emissão de laudo automático conforme a regra de ouro.
  - Apresentou a distinção entre medida direta, cálculo derivado e interpretação clínica.
  - Calculou o $\sum 6D = 63\text{ mm}$.
  - Apresentou Withers et al. (1987) e Petroski (1995).
  - Sugeriu o acompanhamento pelo somatório bruto.
- **Avaliação:** Excelente aderência ética e metodológica, porém excessivamente extenso.

### Turno 2
- **Prompt do Usuário:** *"quais seriam os pontos de corte e classificação de %g aplicados para esse meu paciente?"*
- **Comportamento do Gem:**
  - Repetiu a introdução cerimoniosa e os 7 passos.
  - Apresentou tabelas de Lohman (1992) e ACSM para %G.
  - Calculou Withers projetando $23,8\%$ de gordura e apontou o conflito com a leitura clínica de dobras enxutas.
- **Avaliação:** Falta de tabelas de somatórios contemporâneas no momento do teste (resolvido com a inclusão de Campa et al. 2025); alta prolixidade e redundância.

### Turno 3
- **Prompt do Usuário:** *"Se esse meu paciente for atleta de futebol de nacionalidade brasileira, quais equações de percentual de gordura seriam as mais adequadas para utilizar numa avaliação?"*
- **Comportamento do Gem:**
  - Repetiu toda a estrutura dos 7 passos.
  - Comparou a equação brasileira de Petroski ($15,1\%$) com a equação de Withers ($23,8\%$), alertando sobre a discrepância de 8,7 pontos percentuais.
  - Fez uma crítica acertada à equação de Faulkner (1968).
  - Recomendou o $\sum 6D$ para a comissão técnica e Petri et al. (2024) como referência de futebol.
- **Avaliação:** Conteúdo conceitual impecável, mas com fadiga de leitura severa decorrente da repetição de conceitos e introduções.

---

## 2. Decisões Decorrentes Deste Teste

1. **Instituição da v2.0 do System Prompt:** Adoção da Pirâmide Invertida e eliminação da repetição automática de cabeçalhos.
2. **Atualização do Módulo 05 da Knowledge Base:** Inclusão das tabelas completas de $\sum 8SKF$ e $\sum 6SKF$ de Campa et al. (2025) e parametrização das faixas de Frisancho (1990/2008).
3. **Plausibilidade Biológica:** Instrução para que o modelo alerte o aluno caso uma fórmula gere estimativas incompatíveis com a magreza evidente do somatório de dobras.

---

## 3. Teste em Fase Beta — Perímetro Máximo da Perna (22/09/2026)

- **Cenário:** Interação de um aluno beta tester questionando a técnica de mensuração do perímetro da perna.
- **Desvio Detectado:** O tutor sugeriu erroneamente que a medida poderia ser realizada com o avaliado apoiando o pé sobre o banco antropométrico, com a perna e coxa flexionadas a 90°.
- **Intervenção do Prof. Filipe Brito (Instrutor ISAK Nível 3):**
  - Esclareceu que a técnica original ISAK preconizada exige o avaliado em pé, ereto, peso distribuído igualmente entre ambas as pernas, e o avaliador posicionado **DE FRENTE para a perna direita** com os olhos no nível da fita.
  - Apoiando o pé no banco a 90° ou sentado é estritamente uma **adaptação clínica de exceção** (para quem não consegue ficar em pé) e exige **registro obrigatório na ficha**.
- **Ação Implementada:**
  - Atualização do `knowledge_base/01_escopo_e_protocolo_isak.md` (seção 4.2.2 dedicada e alerta em destaque).
  - Atualização do `SYSTEM_PROMPT_ANTHROPOGUIDE.md` para a versão 2.5 com blindagem técnica negativa e positiva.
  - Publicação da ADR 007.
