# ADR 009 — Correção de coeficientes de equações na base de conhecimento

**Data:** 12/11/2026
**Status:** Aprovado e Implementado em 12/11/2026
**Origem:** conferência com os PDFs originais (Zotero), feita durante a produção da aula 21 do
curso Dobras Cutâneas. Detalhes em
`Curso_Dobras/Producao/VERIFICACAO_EQUACOES_M6_2026_11_12.md`.

**Revoga parcialmente o ADR 003**: a diretriz pedagógica do ADR 003 continua de pé (não
contraindicar Petroski para mulheres por causa da axilar média), mas a equação que ele oficializou
**não existe na tese**.

---

## 1. Correções necessárias

| # | Onde | Como está | Correção (fonte original) |
|---|---|---|---|
| 1 | `knowledge_base/03_equacoes_brasileiras.md` §2.2 e ADR 003 | Petroski mulheres "versão oficial N1": `D = 1,12948287 − 0,00072714 Σ4 + 0,00000188 Σ4² − 0,00044733 ID` | **Não existe** na tese (dava ~10 %G para Σ8 = 141 mm). Usar a **F9**: `D = 1,02902361 − 0,00067159 (X4) + 0,00000242 (X4)² − 0,00026073 (ID) − 0,00056009 (MC) + 0,00054649 (ES)`, X4 = SE + TR + SI + PM, MC em kg, ES em cm; R = 0,848, EPE = 0,0068 g/ml; mulheres 18–51 anos. Petroski, 1995, Tab. 4, p. 68. O próprio autor recomenda a F9 no resumo |
| 2 | `knowledge_base/04_equacoes_atletas.md` §2.1 B | Withers mulheres atletas: `1,17280 − 0,07408 log(TR+SE+SP+PE)` | **BD(2)**: `1,17830 − 0,07179 log10(TR+SE+SP+PE)`; amostra geral, n = 182; R = 0,863; EPE 0,00597. Withers et al., 1987, *Eur J Appl Physiol* 56:169–180, Tab. 5 |
| 3 | `knowledge_base/04_equacoes_atletas.md` §2.1 A | Withers "homens atletas": `1,17484 − 0,07229 log(7 dobras)` | **Atribuição errada**: é a BD(4) **feminina** (jogadoras de esportes coletivos, n = 107), mesmo artigo, Tab. 5. A equação masculina de Withers (artigo à parte, 1987) **não foi conferida**: retirar ou marcar como não verificada até conferir |
| 4 | `knowledge_base/03_equacoes_brasileiras.md` §3 | Guedes "1985", `1,1714 − 0,0671 log` (H) e `1,1665 − 0,0706 log` (M) | Fonte é **Guedes & Guedes, 1991**, *Semina* 12(2):61–70 (eq. III e XI); 18–30 anos. Coeficientes completos: homens `1,17136 − 0,06706 log10(TR+SI+AB)`; mulheres `1,16650 − 0,07063 log10(CX+SI+SE)`. O artigo de 1985 (*Kinesis*) é descritivo, sem equações |

## 2. Conferidas e corretas

- Petroski homens, M7 (Tab. 9, p. 81).
- Petroski mulheres log com axilar média, F11 (Tab. 4).
- Jackson, Pollock & Ward 1980, mulheres 3 dobras, BD(13) (Tab. 4).
- Siri (1956) na conversão.

## 3. Também a revisar

- O §2.2 da base afirma que a versão das 4 dobras é "oficialmente indicada e ensinada no curso ISAK
  N1". Conferir se os materiais do N1 (Macroaula 13 e o guia de escolha de equações, em PDF/DOCX,
  que a busca de texto não alcança) reproduzem a equação inexistente.
- O §5 da base cita "subestima 2 a 4 pontos" para JP em brasileiros, atribuído a Cyrino 2003 e
  Silva 2003. Não foi conferido.
- A F9 exige massa corporal e estatura, não só idade: o app e o system prompt precisam pedir esses
  dados.

## 4. Execução (12/11/2026)

- `knowledge_base/03_equacoes_brasileiras.md`: §2.2 trocada pela F9 (com MC e ES); §3 reescrita como
  Guedes & Guedes 1991, coeficientes completos, 18–30 anos.
- `knowledge_base/04_equacoes_atletas.md`: §2.1 refeita com BD(2) e BD(4) femininas; a masculina
  ficou marcada como não conferida.
- `knowledge_base/08_bibliografia_e_procedencia.md`: entradas 6 (Guedes) e 10 (Withers) corrigidas.
- `SYSTEM_PROMPT_ANTHROPOGUIDE.md`: diretriz de Petroski para mulheres passa a citar a F9 e a exigir
  massa e estatura; Guedes 1991; Withers só feminino. Snapshot em
  `versions/system_prompt_v2_7_correcao_equacoes.md`.
- O `web_app` não tem coeficientes no código: lê a base e o system prompt dos arquivos.
- Materiais do N1 (PDFs das Macroaulas 13 e 14, todos os DOCX e PPTX de `N1/`): busca de texto pelos
  coeficientes errados **sem ocorrências** (12/11). Imagens embutidas em slides não são alcançadas.
- Afirmação de Cyrino/Silva 2003 (§5 da base) **continua não conferida**.
