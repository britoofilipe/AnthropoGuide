# ADR 004 — Nomenclatura da Dobra da Perna, Escopo Anatômico ISAK e Dialética Campa vs. Costa

**Data:** 19/09/2026  
**Status:** Aprovado e Implementado  
**Decisores:** Prof. Filipe Brito (Instrutor Internacional ISAK Nível 3) e Antigravity AI  

---

## 1. Contexto

Durante a evolução das diretrizes pedagógicas e da base de conhecimento do tutor **AnthropoGuide**, foram identificados três pontos críticos de alinhamento com a doutrina de ensino do Prof. Filipe Brito e com os manuais oficiais da ISAK:

1. **Nomenclatura da Dobra Cutânea:** O tutor vinha utilizando em alguns trechos a expressão *"perna medial"* para se referir à dobra cutânea. No protocolo ISAK em língua portuguesa e nas diretrizes do curso, a dobra cutânea do membro inferior distal é referenciada estritamente como **dobra da perna** (ou simplesmente **perna**).
2. **Escopo Anatômico da ISAK (A Dobra Axilar):** Havia uma inferência incorreta de que a dobra axilar média faria parte do Perfil Completo (Nível 2) da ISAK. Na realidade técnica da ISAK, a **dobra axilar média NÃO faz parte de NENHUM perfil antropométrico** (nem N1 com 8 dobras, nem N2 com 9 dobras, cuja única dobra adicional é a do antebraço).
3. **Avaliação Centílica de Somatórios (Campa vs. Costa):** O tutor havia priorizado exclusivamente as curvas centílicas internacionais de Campa et al. (2025). Porém, na prática clínica brasileira, o somatório de 5 dobras de Costa (2001) é amplamente utilizado e possui valor formativo inestimável quando ensinado com suas devidas ressalvas metodológicas.

---

## 2. Decisão

1. **Padronização Terminológica da Dobra da Perna:**
   - Em toda a base de conhecimento, prompts do sistema e diálogos pedagógicos, utilizar a denominação **dobra da perna** (ou **perna**), banindo a expressão "perna medial" para dobras cutâneas.

2. **Registro Explícito sobre a Ausência da Dobra Axilar na ISAK:**
   - Declarar e documentar com clareza cristalina que a dobra axilar é um sítio anatômico totalmente externo à ISAK. Equações que exigem axilar média (como a versão logarítmica de Petroski ou Pollock) utilizam medições não padronizadas pela sociedade internacional.

3. **Apresentação Dialética: Campa et al. (2025) vs. Costa (2001):**
   - O AnthropoGuide deve apresentar **ambas as referências como legítimas e aplicáveis**, contextualizando prós e contras:
     * **Campa et al. (2025):** 
       - *Prós:* Dados contemporâneos (2025), rigor metodológico ISAK absoluto, somatórios consagrados de $\sum 6D$ e $\sum 8D$ com percentis de $P_3$ a $P_{97}$.
       - *Contras / Ressalvas:* Amostra multicêntrica internacional (não específica da população brasileira).
     * **Costa (2001):**
       - *Prós:* Amostra 100% brasileira (n=1.092 em Santos/SP), somatório clássico de 5 dobras ($\sum 5DC = \text{Tríceps} + \text{Subescapular} + \text{Suprailíaca} + \text{Abdominal} + \text{Perna}$), todas do N1.
       - *Contras / Ressalvas:* Tabela histórica de 2001 que necessita de atualização temporal decorrente da transição nutricional e do aumento secular da adiposidade corporal no Brasil ao longo das últimas duas décadas; padronização de marcos pré-ISAK.

---

## 3. Consequências

- **Governança:**
  - `knowledge_base/01_escopo_e_protocolo_isak.md`, `03_equacoes_brasileiras.md`, `04_equacoes_atletas.md` e `05_percentis_e_referencias.md` revisados e harmonizados.
  - `SYSTEM_PROMPT_ANTHROPOGUIDE.md` atualizado para a versão 2.2.
  - Versão arquivada em `versions/system_prompt_v2_2_calibrado.md`.
  - `README.md` atualizado.
