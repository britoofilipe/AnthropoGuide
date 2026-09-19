# Módulo 02 — Qualidade da Medida, Controle de Erro e ETM na ISAK

**Versão:** 1.0  
**Data:** 19/09/2026  
**Público-alvo:** Alunos e instrutores da certificação ISAK Nível 1  
**Fontes de referência:**  
- Esparza-Ros, F., & Vaquero-Cristóbal, R. (2025). *Sources of Error and Statistics Applied to Anthropometry*. In: Anthropometry: Fundamentals of Application and Interpretation. Springer Nature. DOI: 10.1007/978-3-031-77535-2_4.  
- Esparza-Ros, F., Vaquero-Cristóbal, R., & Marfell-Jones, M. (2026). *ISAK Accreditation Handbook (10th version)*. ISAK.  
- Pederson, D., & Gore, C. (1996). *Error in Anthropometry*. In: Norton, K. & Olds, T. (Eds.), Anthropometrica. UNSW Press.

---

## 1. Fundamentos da Garantia de Qualidade

Na cineantropometria, a padronização não é mera formalidade: é o alicerce que garante que uma variação observada em uma medida ao longo do tempo seja reflexo de **mudança biológica real do indivíduo** (como hipertrofia ou perda de gordura) e não fruto do **erro técnico do avaliador**.

### A Tríade da Medição
- **Precisão (Reprodutibilidade):** Grau de concordância entre medições repetidas feitas pelo *mesmo* avaliador no mesmo indivíduo e sob as mesmas condições (avaliada pelo ETM intra-avaliador).
- **Acurácia (Exatidão):** Proximidade entre a medida obtida pelo avaliador e a medida "real" ou de referência (critério), avaliada pela comparação contra um antropometrista Instrutor Nível 3 ou Critério Nível 4 (avaliada pelo ETM inter-avaliador).
- **Validade:** Grau em que a variável mensurada realmente representa o construto anatômico ou biológico pretendido.

---

## 2. O Trabalho em Troika e Minimização de Erros

A ISAK recomenda formalmente que a rotina de medições seja executada em **Troika**:
1. **Antropometrista:** Posiciona o sujeito, palpa os landmarks, manuseia os instrumentos e realiza a leitura.
2. **Sujeito Avaliado:** Permanece na postura anatômica recomendada, com vestimenta adequada e colaborando com o relaxamento muscular.
3. **Assistente / Registrador (Anotador):**
   - Garante que o sujeito não altere a postura durante a medição.
   - Confirma verbalmente cada medida lida pelo antropometrista (repetição audível: se o avaliador diz "doze vírgula quatro", o assistente repete "doze vírgula quatro" ao registrar).
   - Anota na linha e coluna corretas da ficha, evitando erros de posicionamento e transcrição.
   - Confere se a diferença entre a 1ª e a 2ª medida exige uma 3ª medida antes que o sujeito seja dispensado.

---

## 3. Protocolo de Medidas Repetidas e Tomada de Decisão

A mensuração nunca deve ser feita em duplicata imediata sobre o mesmo ponto (o que causaria compressão cumulativa nos tecidos adiposos e viés de memória).

1. **Circuito Completo:** Realiza-se a 1ª rodada de todas as medidas (básicas $\rightarrow$ dobras $\rightarrow$ perímetros $\rightarrow$ diâmetros). Em seguida, realiza-se a 2ª rodada completa.
2. **Gatilho da 3ª Medida:**
   - **Dobras cutâneas:** Se $|M_1 - M_2| > 5\%$ do valor de $M_1$.
   - **Demais medidas (perímetros, diâmetros, básicas):** Se $|M_1 - M_2| > 1\%$ do valor de $M_1$.
3. **Valor Final a Registrar:**
   - Se foram realizadas **2 medidas**: adota-se a **média aritmética** ($\frac{M_1 + M_2}{2}$).
   - Se foi realizada **3ª medida**: adota-se a **mediana** (o valor central entre $M_1$, $M_2$ e $M_3$).

---

## 4. O Erro Técnico de Medida (ETM / TEM)

O Erro Técnico de Medida (ETM, ou *Technical Error of Measurement* - TEM) é a métrica estatística padrão internacional para determinar a variabilidade de um antropometrista.

### 4.1 ETM Intra-avaliador Absoluto
Calculado a partir de medidas repetidas tomadas pelo mesmo antropometrista em $N$ sujeitos:

$$TEM_{\text{intra}} = \sqrt{\frac{\sum d^2}{2N}}$$

Onde:
- $d = X_1 - X_2$ (diferença entre a 1ª e a 2ª medição do mesmo sujeito na mesma variável).
- $N$ = número total de sujeitos avaliados.

### 4.2 ETM Relativo (%ETM)
Para comparar a precisão entre variáveis com ordens de grandeza distintas (por exemplo, comparar uma dobra de 8 mm com a estatura de 175 cm), converte-se o ETM absoluto em porcentagem da média:

$$\%TEM = \left( \frac{TEM}{\bar{X}} \right) \times 100$$

Onde $\bar{X}$ é a média aritmética geral de todas as medições daquela variável no grupo amostral.

### 4.3 ETM Inter-avaliador (Acurácia)
Calculado comparando-se as medições do antropometrista em treinamento ($X_1$) com as medições de referência de um Antropometrista Critério (Nível 4) ou Instrutor (Nível 3) ($X_2$):

$$TEM_{\text{inter}} = \sqrt{\frac{\sum (X_1 - X_2)^2}{2N}}$$

---

## 5. Limites de Tolerância para Acreditação ISAK (Nível 1)

Conforme o **ISAK Accreditation Handbook (Edição 2026)**, os critérios formais para certificação Nível 1 são:

### 5.1 No Exame Prático do Curso Presencial
Durante a prova prática (composta por 10 variáveis do perfil restrito avaliadas em 3 voluntários):
- **ETM Intra-avaliador máximo permitido:**
  - Dobras cutâneas: $\le 10,0\%$
  - Outras medidas (perímetros, diâmetros, básicas): $\le 2,0\%$
- **ETM Inter-avaliador máximo permitido (vs. Instrutor):**
  - Dobras cutâneas: $\le 12,5\%$
  - Outras medidas: $\le 2,5\%$

### 5.2 Na Tarefa Pós-Curso (Submissão dos 20 Perfis no ISAKMetry)
Para a concessão final da certificação internacional de Nível 1, o aluno deve mensurar **20 sujeitos em duplicata** dentro do prazo improrrogável de **4 meses** (a contar da data do exame prático presencial):
- **Tolerância formal exigida (Critérios ISAK):**
  - Dobras cutâneas: $\%TEM \le 7,5\%$ (Recomendação de excelência do Prof. Filipe: $\le 5,0\%$)
  - Outras medidas (básicas, perímetros e diâmetros): $\%TEM \le 1,5\%$ (Recomendação de excelência: $\le 1,0\%$)

### 5.3 Guia Operacional do ISAKMetry (Tutoriais Oficiais ISAK Global)
O **ISAKMetry** é o software oficial em nuvem da International Society for the Advancement of Kinanthropometry, acessível gratuitamente para alunos e profissionais com credenciamento ativo através do portal [www.isak.global](https://www.isak.global).

#### A. Acesso e Localização do Curso
1. O aluno acessa [www.isak.global](https://www.isak.global) e efetua login com as credenciais de membro criadas durante a inscrição no curso presencial.
2. No painel principal ou menu superior, acessa a plataforma **ISAKMetry**.
3. Navega até a seção **"Courses" / "Mis Cursos"** (Meus Cursos) e seleciona o curso de Nível 1 realizado sob coordenação do Prof. Filipe Brito (Instrutor Nível 3).
4. Localiza o módulo de submissão: **"Sending 20 subjects" / "Envío de 20 sujetos"**.

#### B. Métodos de Alimentação de Dados (20 Sujeitos em Duplicata)
Para cada um dos 20 voluntários, devem ser registradas as 21 variáveis do Perfil Restrito N1 em duas tomadas de medida independentes (Medida 1 e Medida 2):
- **Método 1: Carga em Lote via Excel ("Measurements from Excel") — *Altamente Recomendado***:
  - No menu do ISAKMetry, o aluno baixa a planilha padrão (*template* oficial em formato `.xlsx`).
  - A planilha já possui os cabeçalhos devidamente codificados para identificação (ID/Nome, sexo, data de nascimento, data da avaliação) e duas colunas por variável (M1 e M2).
  - O aluno preenche as 20 linhas sem alterar a estrutura de linhas, colunas ou cabeçalhos do arquivo.
  - Retorna ao ISAKMetry e faz o upload em lote. O sistema faz o *parsing* instantâneo e valida todas as variáveis de uma única vez.
- **Método 2: Cadastro Manual ("Create Subjects" & "Measurements")**:
  - O aluno cadastra sujeito por sujeito no sistema ("Create Subject") com dados demográficos e vincula ao curso.
  - Acessa o formulário de medição e digita manualmente as séries M1 e M2 variável por variável.

#### C. Auditoria Automática do %ETM e Envio ("Send to Instructor")
- O motor de cálculo do ISAKMetry gera automaticamente o relatório consolidado de $\%ETM$ intra-avaliador para todas as variáveis dos 20 sujeitos.
- Caso alguma variável ultrapasse o limite formal ($\le 7,5\%$ para dobras ou $\le 1,5\%$ para perímetros/diâmetros/básicas), o sistema sinaliza o erro. O aluno deve revisar suas anotações para certificar-se de que não houve erro de digitação antes de reenviar.
- Estando todas as variáveis aprovadas dentro da tolerância, o aluno clica no botão oficial de submissão: **"Send to Instructor" / "Enviar al Instructor"**.
- O status da submissão passa para **"Pending Review" (Pendente de Revisão)** e os dados ficam bloqueados para novas edições enquanto o instrutor avalia.

#### D. Fluxo de Confirmação pelo Instrutor e Emissão do Certificado
1. O Prof. Filipe Brito (Instrutor Nível 3) acessa o portal com credenciais de instrutor e visualiza a submissão do aluno na fila de auditoria do curso.
2. O instrutor inspeciona o relatório analítico de $\%ETM$, a plausibilidade biológica das medidas e a consistência técnica dos dados.
3. Se os dados atenderem a todos os requisitos, o instrutor clica em **"Confirm / Approve" (Aprovar 20 sujeitos)**. Caso haja anomalias técnicas ou de digitação, o instrutor pode rejeitar com apontamentos para retificação.
4. Após a confirmação no sistema pelo instrutor, a validação é transmitida automaticamente à Secretaria Central da ISAK Global, que formaliza o credenciamento internacional de Nível 1 e disponibiliza o diploma digital oficial com o número de registro internacional do antropometrista.

#### E. Recursos Adicionais da Plataforma ISAKMetry
- **Download de Medidas ("Downloading your measures")**: Permite ao profissional exportar todo o seu banco histórico de avaliados e medições em formato Excel/CSV para fins de pesquisa, auditoria ou backup.
- **Gestão Clínica e Atendimentos ("Appointments" e "Reports")**: O ISAKMetry oferece suporte para agendamento de consultas e emissão de relatórios antropométricos completos pós-certificação (somatórios de dobras, fracionamento corporal e gráficos somatotipológicos de Heath-Carter).

---

## 6. Aplicação Clínica e Esportiva: Mudança Real vs. Ruído

Para saber se um atleta realmente reduziu gordura corporal ou ganhou perímetro muscular entre duas consultas, o profissional deve considerar o **Erro Padrão da Diferença (SED - Standard Error of Difference)**:

$$SED = TEM \times \sqrt{2} \approx TEM \times 1,414$$

### Tomada de Decisão com Intervalo de Confiança de 95%:
Para afirmar com 95% de certeza estatística que houve alteração na composição corporal do avaliado:
$$\Delta_{\text{mínima}} \ge 1,96 \times SED \approx 2,77 \times TEM$$

- **Se a diferença observada for menor que $1,96 \times SED$:** O resultado está dentro da margem de ruído do método/avaliador; não se pode assegurar mudança real.
- **Se a diferença for maior:** Há evidência estatística de mudança tecidual efetiva.
