# AnthropoGuide — Gem Tutor ISAK Nível 1

Este repositório contém a documentação completa, instruções calibradas do sistema, registros de decisões arquiteturais (ADRs), histórico de testes e a base de conhecimento modular do **AnthropoGuide**, o tutor especializado para alunos da certificação internacional ISAK Nível 1, desenvolvido pelo **Prof. Filipe Brito (Instrutor Internacional ISAK Nível 3)**.

---

## 📁 Estrutura do Projeto

```
d:\ISAK_Filipe_Instrutor\AnthropoGuide\
├── PROJETO_ANTHROPOGUIDE_HANDOFF.md    # Diretrizes originais e handoff
├── SYSTEM_PROMPT_ANTHROPOGUIDE.md       # [VIGENTE v2.4] Instruções calibradas e blindadas
├── README.md                            # Guia de implantação e índice
├── decisoes_projeto/                    # Registros de decisões arquiteturais e pedagógicas
│   ├── ADR_001_arquitetura_modular_knowledge_base.md
│   ├── ADR_002_calibracao_pedagogica_e_anti_prolixidade.md
│   ├── ADR_003_orientacao_equacao_petroski_feminina.md
│   ├── ADR_004_comparativo_campa_vs_costa_e_nomenclatura_perna.md
│   ├── ADR_005_incorporacao_tutoriais_isakmetry.md # Tutoriais oficiais YouTube @isakglobal410
│   ├── ADR_006_blindagem_propriedade_intelectual.md # Proteção anti-vazamento de prompt/arquivos
│   └── HISTORICO_INTERACOES_E_TESTES.md # Testes reais e análises de desempenho
├── versions/                            # Histórico e versionamento de System Prompts
│   ├── system_prompt_v1_0_rigido.md     # Versão inicial com template rígido de 7 passos
│   ├── system_prompt_v2_0_calibrado.md  # Versão calibrada (Pirâmide Invertida e 3 Níveis)
│   ├── system_prompt_v2_1_petroski_mulheres.md # Versão com Petroski feminino 4 dobras
│   ├── system_prompt_v2_2_calibrado.md  # Versão com Perna e Campa vs. Costa
│   ├── system_prompt_v2_3_isakmetry_tutoriais.md # Versão com ISAKMetry & 20 sujeitos pós-curso
│   └── system_prompt_v2_4_blindagem_ip.md # Versão vigente (Blindagem de IP & Anti-Leaking)
└── knowledge_base/                      # Base de conhecimento modular do Gem (8 módulos)
    ├── 01_escopo_e_protocolo_isak.md    # Medidas N1, regras do lado direito e técnica
    ├── 02_qualidade_da_medida.md        # ETM intra/inter, troika e Guia Oficial ISAKMetry pós-curso
    ├── 03_equacoes_brasileiras.md       # Petroski 1995 (homens e mulheres 4 dobras ISAK), Guedes, Lee
    ├── 04_equacoes_atletas.md           # Withers 1987, Faulkner, somatotipo Heath-Carter
    ├── 05_percentis_e_referencias.md    # Campa 2025 (Σ6 e Σ8), Costa 2001 (Σ5), Frisancho, OMS
    ├── 06_indicadores_e_cortes.md       # IMC, Cintura (OMS/IDF), RCEst, RCQ, Conicidade
    ├── 07_metodos_e_limitacoes.md       # Modelos 2C a 5C, Siri, Brozek, DXA, BIA e limites
    └── 08_bibliografia_e_procedencia.md # Catálogo de referências primárias e rastreabilidade
```

---

## 🚀 Como Atualizar o Gem no Google Gemini (Google AI Pro)

1. Acesse o [Gemini](https://gemini.google.com/) com a sua conta Google AI Pro.
2. No menu lateral, clique em **Gerenciador de Gems** $\rightarrow$ selecione o **AnthropoGuide** $\rightarrow$ **Editar**.
3. **Descrição:**
   ```text
   Tutor e Guia Especialista em Cineantropometria, Protocolo ISAK Nível 1 e Composição Corporal. Elaborado pelo Prof. Filipe Brito, Instrutor ISAK Nível 3.
   ```
4. **Instruções (Instructions):**
   - Substitua o texto pelo conteúdo integral de [`SYSTEM_PROMPT_ANTHROPOGUIDE.md`](SYSTEM_PROMPT_ANTHROPOGUIDE.md) (versão 2.3).
5. **Conhecimento (Knowledge / Arquivos):**
   - Atualize os arquivos alterados da pasta [`knowledge_base/`](knowledge_base/):
     * [`02_qualidade_da_medida.md`](knowledge_base/02_qualidade_da_medida.md) (inclui o Guia Oficial do ISAKMetry)
     * [`01_escopo_e_protocolo_isak.md`](knowledge_base/01_escopo_e_protocolo_isak.md)
     * [`03_equacoes_brasileiras.md`](knowledge_base/03_equacoes_brasileiras.md)
     * [`05_percentis_e_referencias.md`](knowledge_base/05_percentis_e_referencias.md)
6. Clique em **Salvar**.
