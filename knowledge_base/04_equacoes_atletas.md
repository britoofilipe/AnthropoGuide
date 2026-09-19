# Módulo 04 — Avaliação Antropométrica de Atletas, Equações Esportivas e Somatotipo

**Versão:** 1.0  
**Data:** 19/09/2026  
**Público-alvo:** Alunos e instrutores da certificação ISAK Nível 1  
**Prioridade de uso:** Avaliação de praticantes de atividade física intensa, desportistas e atletas competitivos  

---

## 1. O Paradigma do Monitoramento no Esporte: Por que Somatórios de Dobras?

A literatura cineantropométrica internacional contemporânea (ISAK, Stewart, Ackland et al.) adverte fortemente contra a dependência cega da conversão de dobras cutâneas em "percentual de gordura" (%G) em atletas de elite:

1. **Premissas Biológicas Violadas:** Fórmulas de regressão densitométrica assumem que a Massa Livre de Gordura (MLG) possui densidade biológica constante de $1,100\text{ g/cm}^3$. Atletas frequentemente apresentam densidade mineral óssea aumentada, maior hipertrofia muscular e variações de água corporal total, distorcendo os modelos de 2 componentes (2C).
2. **Propagação de Erro:** Converter a medida milimétrica direta em densidade ($D_b$) e depois em %G via Siri ou Brozek acrescenta um erro metodológico desnecessário de 3 a 5%.
3. **Padrão Ouro de Campo:** O **Somatório de Dobras Cutâneas ($\sum D$ em $mm$)** é a variável mais fidedigna, sensível e transparente para avaliar o impacto real do treinamento físico e da periodização nutricional.

### Somatórios Padronizados:
- **$\sum 6$ Dobras ISAK:** Tríceps + Subescapular + Supraespinal + Abdominal + Coxa + Perna.
- **$\sum 8$ Dobras ISAK (Perfil Restrito Completo):** Tríceps + Subescapular + Bíceps + Crista Ilíaca + Supraespinal + Abdominal + Coxa + Perna.

---

## 2. Equações Específicas para Atletas

Quando houver demanda institucional ou do atleta por uma estimativa de densidade e %G, o antropometrista deve selecionar equações derivadas especificamente de populações atléticas, explicitando sempre o erro padrão da estimativa ($EPE$).

### 2.1 Withers et al. (1987) — Atletas de Rendimento
Desenvolvidas na Austrália em atletas de elite de ambos os sexos, validadas contra pesagem hidrostática. É uma das referências mais compatíveis com a padronização anatômica ISAK.

#### A. Homens Atletas:
- **Fórmula (6 Dobras ISAK):**
$$D_b = 1,17484 - 0,07229 \times \log_{10}(\text{Tríceps} + \text{Subescapular} + \text{Bíceps} + \text{Supraespinal} + \text{Abdominal} + \text{Coxa} + \text{Perna})$$
*(Nota: a soma utiliza 7 dobras ou a variante de 6 dobras sem o bíceps; manter a consistência da soma).*
- **Conversão:** Siri (1956).

#### B. Mulheres Atletas:
- **Fórmula:**
$$D_b = 1,17280 - 0,07408 \times \log_{10}(\text{Tríceps} + \text{Subescapular} + \text{Supraespinal} + \text{Perna})$$
- **Conversão:** Siri (1956).

---

### 2.2 Jackson, Pollock & Ward (1978, 1980)
Equações generalizadas bastante difundidas, desenvolvidas com pesagem hidrostática.
- **Homens (3 dobras):** Peitoral (não ISAK N1), Abdominal, Coxa medial.
$$D_b = 1,10938 - 0,0008267 \times (\sum 3D) + 0,0000016 \times (\sum 3D)^2 - 0,0002574 \times (\text{Idade})$$
- **Mulheres (3 dobras):** Tríceps, Suprailíaca (Crista Ilíaca), Coxa medial.
$$D_b = 1,0994921 - 0,0009929 \times (\sum 3D) + 0,0000023 \times (\sum 3D)^2 - 0,0001392 \times (\text{Idade})$$
- **Limitação em Brasileiros:** Conforme discutido no Módulo 03, tendem a subestimar levemente a gordura em brasileiros em comparação a equações nativas.

---

### 2.3 Equação de Faulkner (1968) — Análise Crítica
Historicamente muito aplicada no futebol sul-americano:
$$\%G = (\text{Tríceps} + \text{Subescapular} + \text{Suprailíaca} + \text{Abdominal}) \times 0,153 + 5,783$$
- **Alerta Metodológico do AnthropoGuide:** A equação foi desenvolvida em uma amostra restrita de nadadores universitários norte-americanos na década de 1960. É uma equação linear direta que fixa uma constante arbitrária de $5,783\%$ de gordura essencial. Tende a subestimar severamente em indivíduos com baixa adiposidade e superestimar em indivíduos com adiposidade intermediária. **Não é recomendada como ferramenta de precisão científica**, devendo ser substituída por Withers ou somatórios puros.

---

## 3. Somatotipo de Heath-Carter (1990)

O somatotipo é a descrição quantitativa do fenótipo corporal atual do indivíduo, expresso em três componentes numéricos contínuos: **Endomorfia - Mesomorfia - Ectomorfia**.

### 3.1 As 10 Medidas Necessárias (Todas presentes no Perfil Restrito ISAK N1):
1. Massa corporal ($kg$)
2. Estatura ($cm$)
3. Dobra do Tríceps ($mm$)
4. Dobra Subescapular ($mm$)
5. Dobra Supraespinal ($mm$)
6. Dobra da Perna ($mm$)
7. Perímetro do Braço Fletido e Contraído ($cm$)
8. Perímetro Máximo da Perna ($cm$)
9. Diâmetro Biepicondilar do Úmero ($cm$)
10. Diâmetro Biepicondilar do Fêmur ($cm$)

---

### 3.2 Fórmulas de Cálculo dos Três Componentes

#### 1. Endomorfia (Adiposidade Relativa):
Primeiro calcula-se a soma de 3 dobras corrigida pela estatura Phantom ($170,18\text{ cm}$):
$$X_c = (\text{Tríceps} + \text{Subescapular} + \text{Supraespinal}) \times \left( \frac{170,18}{\text{Estatura em cm}} \right)$$

Em seguida, aplica-se a equação polinomial cúbica:
$$\text{Endomorfia} = -0,7182 + 0,1451 \times X_c - 0,00068 \times X_c^2 + 0,0000014 \times X_c^3$$

#### 2. Mesomorfia (Robustez Musculoesquelética Relativa):
Requer o cálculo dos perímetros corrigidos da musculatura esquelética:
- Perímetro corrigido do braço ($PB_{\text{corr}}$): $\text{Braço contraído (cm)} - \left( \frac{\text{Dobra do Tríceps (mm)}}{10} \right)$
- Perímetro corrigido da perna ($PP_{\text{corr}}$): $\text{Perna máxima (cm)} - \left( \frac{\text{Dobra da Perna (mm)}}{10} \right)$
*(Nota histórica Heath-Carter: no método clássico, a subtração é feita diretamente em cm sem multiplicar por $\pi$)*.

Fórmula da Mesomorfia:
$$\text{Mesomorfia} = 0,858 \times D_{\text{úmero}} + 0,601 \times D_{\text{fêmur}} + 0,188 \times PB_{\text{corr}} + 0,161 \times PP_{\text{corr}} - 0,131 \times \text{Estatura} + 4,55$$
*(com diâmetros e perímetros em cm; estatura em cm)*.

#### 3. Ectomorfia (Linearidade Relativa):
Calcula-se o Índice Ponderal Inverso (HWR - *Height-Weight Ratio*):
$$HWR = \frac{\text{Estatura em cm}}{\sqrt[3]{\text{Massa corporal em kg}}}$$

Equações condicionais para Ectomorfia:
- Se $HWR \ge 40,75$:
$$\text{Ectomorfia} = 0,732 \times HWR - 28,58$$
- Se $38,28 < HWR < 40,75$:
$$\text{Ectomorfia} = 0,463 \times HWR - 17,63$$
- Se $HWR \le 38,28$:
$$\text{Ectomorfia} = 0,1$$

*(Regra de consistência: valores calculados $\le 0$ são ajustados para $0,1$ após verificação de consistência dos dados brutos)*.

---

### 3.3 A Somatocarta e as Coordenadas Bidimensionais ($X, Y$)

Para plotar o ponto do indivíduo (*somatopoint*) no gráfico bidimensional da Somatocarta (Triângulo de Franz Reuleaux):

$$X = \text{Ectomorfia} - \text{Endomorfia}$$
$$Y = 2 \times \text{Mesomorfia} - (\text{Endomorfia} + \text{Ectomorfia})$$

### 3.4 Interpretação no Desempenho Esportivo:
- **Deslocamento para a Esquerda ($X < 0$):** Predomínio de adiposidade (endomorfia > ectomorfia).
- **Deslocamento para a Direita ($X > 0$):** Predomínio de linearidade e alavanca (ectomorfia > endomorfia).
- **Deslocamento para Cima ($Y > 0$):** Predomínio musculoesquelético (típico de esportes de potência, força e combate).
- **Deslocamento para Baixo ($Y < 0$):** Baixa mesomorfia em relação à adiposidade e linearidade.
