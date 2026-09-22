# ADR 007 — Técnica Oficial do Perímetro da Perna, Posicionamento do Avaliador e Distinção entre Padrão ISAK e Adaptação Clínica

**Data:** 22/09/2026  
**Status:** Aprovado e Implementado  
**Decisores:** Prof. Filipe Brito (Instrutor Internacional ISAK Nível 3) e Antigravity AI  

---

## 1. Contexto

Durante a fase de testes com usuários beta testers, o tutor **AnthropoGuide** gerou uma instrução metodologicamente inadequada ao afirmar que o perímetro máximo da perna (*calf maximum girth*) poderia ser aferido com o avaliado apoiando o pé sobre o banco antropométrico, com a perna e a coxa flexionadas a 90°.

O Prof. Filipe Brito apontou formalmente que:
1. **Essa postura NÃO constitui a técnica preconizada pela ISAK:** A técnica oficial e original exige que o indivíduo esteja em pé, postura ereta, com o peso corporal distribuído igualmente em ambos os membros inferiores, e o antropometrista posicionado **DE FRENTE para a perna direita do avaliado**, mantendo os olhos no nível da fita métrica para anular o erro de paralaxe.
2. **Posturas com flexão a 90° ou sentado são estritamente ADAPTAÇÕES DE EXCEÇÃO:** Apenas na impossibilidade clínica do paciente de manter a ortostase adequada (dor, vertigem, debilidade física extrema ou limitação motora), autoriza-se a medição adaptada.
3. **Exigência de Registro:** Quando uma adaptação for realizada, o antropometrista deve obrigatoriamente registrar na ficha antropométrica que a medida foi obtida sob condição adaptada e não sob o protocolo padrão.

---

## 2. Decisão

1. **Blindagem no System Prompt (v2.5):**
   - Inclusão de regra mandatória negativa e positiva:
     * O avaliado deve estar em pé, peso distribuído uniformemente em ambas as pernas.
     * O avaliador posiciona-se **DE FRENTE para a perna direita**.
     * NUNCA ensinar ou sugerir a postura de 90° com pé no banco ou sentado como técnica padrão ou alternativa habitual.
     * Ensinar taxativamente que essa postura é exclusivamente uma **ADAPTAÇÃO CLÍNICA DE EXCEÇÃO** que demanda **anotação obrigatória na ficha**.

2. **Refinamento do Módulo 01 da Base de Conhecimento:**
   - Adicionada a seção `4.2.2 Perímetro Máximo da Perna (Calf Maximum Girth)` em `knowledge_base/01_escopo_e_protocolo_isak.md`, com o passo a passo da técnica de varredura (*sliding search*), posicionamento do avaliador e alerta metodológico em destaque sobre a distinção entre protocolo preconizado e adaptação.

3. **Arquivamento e Versionamento:**
   - Prompt do sistema atualizado para a versão 2.5 e arquivado em `versions/system_prompt_v2_5_perimetro_perna.md`.

---

## 3. Consequências

- **Governança:**
  - O tutor responderá com precisão cirúrgica qualquer consulta sobre o perímetro da perna, orientando a técnica padrão e educando os alunos sobre quando e como registrar adaptações clínicas.
  - Elimina-se o risco de contaminação com manuais genéricos ou orientações informais pré-ISAK.
