# Módulo 03 — Equações de Composição Corporal Validadas para a População Brasileira

**Versão:** 1.0  
**Data:** 19/09/2026  
**Público-alvo:** Alunos e instrutores da certificação ISAK Nível 1  
**Prioridade de uso:** 1ª linha de escolha para indivíduos não atletas residentes no Brasil  

---

## 1. Contexto Metodológico e Princípio da Especificidade Populacional

Equações duplamente indiretas baseadas em regressão linear ou quadrática dependem estritamente das características antropométricas, étnicas, de densidade corporal e de distribuição de gordura da amostra em que foram desenvolvidas. A aplicação de fórmulas estrangeiras (ex.: Jackson & Pollock nos EUA, Durnin & Womersley no Reino Unido) em brasileiros pode introduzir erros sistemáticos de estimativa.

### Cuidados na Interface com o Protocolo ISAK:
- A maioria das equações brasileiras históricas (décadas de 1980 e 1990) utilizou compassos Cescorf ou Lange e protocolos de demarcação anatômica anteriores à padronização ISAK (ex.: dobra "suprailíaca" com angulação horizontal ou oblíqua logo acima da crista ilíaca, que difere sutilmente da *supraspinale* e da *iliac crest* da ISAK).
- O antropometrista ISAK deve registrar essa diferença metodológica: ao alimentar equações brasileiras com dobras ISAK, utiliza-se a dobra da crista ilíaca ou da supraespinal conforme a correspondência descrita pelo autor da fórmula.

---

## 2. Equações de Petroski (1995)

Desenvolvidas na Universidade Federal de Santa Maria (UFSM) por Edio Luiz Petroski, representam uma das referências mais robustas e amplamente utilizadas para adultos brasileiros de ambos os sexos, validadas contra pesagem hidrostática com determinação de volume residual pulmonar.

### 2.1 Homens (18 a 66 anos)
- **Variáveis:** Tríceps (TR), Subescapular (SE), Crista Ilíaca/Suprailíaca (SI) e Perna (PE) em milímetros ($mm$); Idade em anos.
- **Fórmula da Densidade Corporal ($D_b$ em $g/cm^3$):**

$$D_b = 1,10726863 - 0,00081201 \times (\sum 4D) + 0,00000212 \times (\sum 4D)^2 - 0,00041761 \times (\text{Idade})$$

Onde:
$$\sum 4D = \text{TR} + \text{SE} + \text{SI} + \text{PE}$$

- **Conversão para % Gordura (%G):** Equação de Siri (1956):
$$\%G = \left( \frac{4,95}{D_b} - 4,50 \right) \times 100$$
- **Parâmetros psicométricos originais:** $R = 0,88$; $R^2 = 0,77$; Erro Padrão da Estimativa ($EPE$) $\approx 0,0075\text{ g/cm}^3$ ($\approx 3,3\%G$).

### 2.2 Mulheres (18 a 51 anos)

#### Versão Oficial Recomendada para Alunos ISAK N1 (4 Dobras Padronizadas):
- **Variáveis:** Tríceps (TR), Subescapular (SE), Crista Ilíaca/Suprailíaca (SI) e Perna (PE) em milímetros ($mm$); Idade em anos.
- **Fórmula da Densidade Corporal ($D_b$ em $g/cm^3$):**

$$D_b = 1,12948287 - 0,00072714 \times (\sum 4D) + 0,00000188 \times (\sum 4D)^2 - 0,00044733 \times (\text{Idade})$$

Onde:
$$\sum 4D = \text{TR} + \text{SE} + \text{SI} + \text{PE}$$

- **Conversão para % Gordura (%G):** Equação de Siri (1956):
$$\%G = \left( \frac{4,95}{D_b} - 4,50 \right) \times 100$$
- **Parâmetros psicométricos originais:** $R = 0,84$; $R^2 = 0,70$; $EPE \approx 0,0084\text{ g/cm}^3$ ($\approx 3,7\%G$).
- **Por que esta versão é a indicada no curso ISAK N1:** Esta equação utiliza **exatamente as mesmas 4 dobras da equação masculina de Petroski**, as quais são 100% padronizadas no Perfil Restrito N1 da ISAK. Dessa forma, o antropometrista credenciado não precisa medir dobras fora do seu escopo para obter uma estimativa com excelente validação para mulheres brasileiras.

#### Contexto e Desmistificação da Versão com Axilar Média:
- Em sua tese de doutorado (UFSM, 1995), Petroski testou e propôs 16 equações para cada sexo.
- Uma das equações femininas que se tornou bastante difundida na literatura e em softwares comerciais é o modelo logarítmico que utiliza a dobra **axilar média (AXM)**:
  $$D_b = 1,19547130 - 0,07513507 \times \log_{10}(\text{AXM} + \text{SI} + \text{CX} + \text{PE}) - 0,00041072 \times (\text{Idade})$$
- **Atenção conceitual sobre a ISAK:** A dobra axilar média **NÃO faz parte de NENHUM perfil antropométrico da ISAK** (nem do Perfil Restrito N1, nem do Perfil Completo N2). Por desconhecerem as outras equações da tese de Petroski, muitos avaliadores assumem incorretamente que Petroski estaria "inviabilizado" para mulheres em avaliações ISAK.
- **Diretriz Pedagógica:** Essa contraindicação é um equívoco histórico. O tutor e o antropometrista ISAK devem esclarecer que a dobra axilar não existe no protocolo ISAK, mas que Petroski validou uma equação com as 4 dobras ISAK (TR, SE, SI, PE), e **esta é a versão que oficialmente indicamos e ensinamos** no curso.

---

## 3. Equações de Guedes (1985, 1994)

Desenvolvidas por Dartagnan Pinto Guedes na Universidade de São Paulo (USP) / Universidade Estadual de Londrina (UEL), específicas para jovens adultos brasileiros (17 a 30 anos), utilizando pesagem hidrostática como critério de referência.

### 3.1 Homens Jovens (17 a 30 anos) — 3 Dobras
- **Variáveis:** Tríceps (TR), Suprailíaca (SI) e Abdominal (AB) em milímetros ($mm$).
- **Fórmula de Densidade Corporal ($D_b$):**

$$D_b = 1,1714 - 0,0671 \times \log_{10}(\text{TR} + \text{SI} + \text{AB})$$

- **Conversão para % Gordura:** Siri (1956).
- **Vantagem no N1:** Todas as três dobras (tríceps, crista ilíaca/supraespinal e abdominal) fazem parte do perfil restrito ISAK N1.

### 3.2 Mulheres Jovens (17 a 30 anos) — 3 Dobras
- **Variáveis:** Coxa Medial (CX), Suprailíaca (SI) e Subescapular (SE) em milímetros ($mm$).
- **Fórmula de Densidade Corporal ($D_b$):**

$$D_b = 1,1665 - 0,0706 \times \log_{10}(\text{CX} + \text{SI} + \text{SE})$$

- **Conversão para % Gordura:** Siri (1956).
- **Vantagem no N1:** Todas as três dobras fazem parte do perfil restrito ISAK N1.

---

## 4. Estimativa da Massa Muscular Esquelética no Brasil

Para fracionar a massa livre de gordura e estimar a Massa Muscular Esquelética (MME) em kg na população brasileira, destaca-se a adaptação do modelo antropométrico de **Lee et al. (2000)** (validado por Ressonância Magnética):

### Equação de Lee et al. (2000) com Perímetros Corrigidos por Dobras ISAK:
$$MME (kg) = \text{Estatura} \times (0,00744 \times PB_c^2 + 0,00088 \times PC_c^2 + 0,00441 \times PP_c^2) + 2,4 \times \text{Sexo} - 0,048 \times \text{Idade} + \text{Etnia} + 7,8$$

Onde:
- **Estatura:** em metros ($m$).
- **Sexo:** 1 para homens; 0 para mulheres.
- **Idade:** em anos.
- **Etnia:** 0 para brancos/caucasianos; 1,1 para afrodescendentes; -1,2 para asiáticos.
- **Perímetros Corrigidos ($cm$):**
  - Braço corrigido ($PB_c$): $\text{Perímetro do braço relaxado} - (\pi \times \frac{\text{Dobra tricipital em mm}}{10})$
  - Coxa corrigida ($PC_c$): $\text{Perímetro da coxa média} - (\pi \times \frac{\text{Dobra da coxa em mm}}{10})$
  - Perna corrigida ($PP_c$): $\text{Perímetro máximo da perna} - (\pi \times \frac{\text{Dobra da perna em mm}}{10})$
  *(com $\pi \approx 3,1416$)*.

---

## 5. Validação de Jackson & Pollock em Brasileiros

Diversos grupos de pesquisa no Brasil (ex.: Cyrino et al., 2003; Silva et al., 2003) testaram a acurácia das clássicas equações de Jackson & Pollock (somas de 3 e 7 dobras) em homens e mulheres universitários e atletas brasileiros:
1. **Achado Consistente:** As equações de Jackson & Pollock tendem a **subestimar a gordura corporal relativa em cerca de 2 a 4 pontos percentuais** na população brasileira em comparação à pesagem hidrostática ou DXA.
2. **Recomendação:** Quando o objetivo for obter um valor de percentual de gordura que reflita a realidade biológica da população brasileira não atleta, priorizar Petroski ou Guedes. Quando o objetivo for acompanhar desportistas ao longo do tempo, pode-se utilizar Jackson & Pollock pela vasta literatura comparativa, mantendo a consistência longitudinal e interpretando a tendência.
