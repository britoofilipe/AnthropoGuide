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
Para a concessão final da certificação internacional de Nível 1, o aluno deve mensurar **20 sujeitos em duplicata** dentro do prazo de **4 meses a contar da data do exame prático** (ver §5.3-I sobre perda de prazo):
- **Tolerância formal exigida (Critérios ISAK):**
  - Dobras cutâneas: $\%TEM \le 7,5\%$
  - Outras medidas (básicas, perímetros e diâmetros): $\%TEM \le 1,5\%$

> **Não apresentar $\le 5,0\%$ / $\le 1,0\%$ como meta do Nível 1** (ADR 008, §2.3). Esses são os
> valores pós-curso dos Níveis 2, 3 e 4 (Handbook, Tabela 1). Citá-los ao aluno de N1 cria dois
> números concorrentes num contexto operacional e induz a erro.

### 5.3 Guia Operacional do ISAKMetry (verificado nos tutoriais oficiais e na planilha oficial)

O **ISAKMetry** é o software oficial em nuvem da International Society for the Advancement of
Kinanthropometry, acessível gratuitamente para alunos e profissionais com credenciamento ativo
através do portal [www.isak.global](https://www.isak.global).

> **Conteúdo corrigido em 28/09/2026 (ADR 008).** A versão anterior desta seção descrevia um fluxo
> de envio por planilha em lote com 20 linhas e um botão "Send to Instructor". Nenhum dos dois
> existe. O que segue foi verificado contra os quatro tutoriais oficiais, quadro a quadro, e
> contra o arquivo da planilha oficial.

#### A. Distinção fundamental: lançar ≠ enviar

Duas operações diferentes, e confundi-las é a origem da maior parte das dúvidas dos alunos:

- **Lançar** é colocar as medidas de um sujeito dentro do ISAKMetry. Pode ser digitando direto na
  plataforma ou preenchendo a planilha oficial e subindo o arquivo.
- **Enviar** é escolher, entre tudo que já foi lançado, quais 20 avaliações formam a tarefa
  pós-curso, no menu **"Post-course"**. **Nenhuma planilha é enviada ao instrutor.**

#### B. Cadastro do sujeito ("Create Subjects")

Toda avaliação pertence a um sujeito cadastrado. Em **Subjects / Sujeitos → Add / Criar**.

Blocos do formulário: Dados pessoais · Foto · Características · Histórico de massa corporal ·
Dados de interesse · Grupos de usuários.

**Campos obrigatórios (\*):** Nome, Sobrenome, Telefone, Sexo, Data de nascimento, Raça.

Orientação útil ao aluno em tarefa pós-curso: registrar no campo "Motivo da avaliação" algo que
identifique a tarefa (ex.: "Perfil pós-curso ISAK N1"), o que facilita localizar as avaliações na
hora da seleção dos 20.

> **Não orientar o preenchimento de "Grupos de usuários".** O tutorial oficial *Create Subjects* é
> explícito: *"The field 'user group' should not be filled in, unless you want to share this
> subject's values with another anthropometrist."* Para a tarefa pós-curso, o campo fica em branco.

#### C. Caminho 1 — Medir direto na plataforma ("Subjects – Measurements")

Assistente em três passos:

1. **Escolher o perfil** a aplicar — para o N1, o **perfil restrito** — e clicar em
   *Start / Empezar*.
2. **"Take measures"**: tabela com as colunas **Tipo · Número · Medida antropométrica · 1ª medida ·
   2ª medida · 3ª medida**, agrupada em Medidas básicas, Dobras, Perímetros e Diâmetros. A
   instrução literal da plataforma é *inserir o valor de cada variável **na mesma ordem
   estabelecida pelo ISAK** e, em seguida, realizar a segunda coleta das variáveis*. Botões
   *Previous step / Next step*.
3. **Salvar** para confirmar. A plataforma orienta usar *Previous step* para revisar os dados
   carregados antes de confirmar, porque corrigir depois é mais trabalhoso.

**A célula da 3ª medida é habilitada pelo próprio sistema** onde a diferença entre a 1ª e a 2ª
medida exigir. Ver §5.4 sobre como orientar quanto a esse gatilho.

#### D. Caminho 2 — Planilha oficial offline + upload

A ISAK fornece um modelo de Excel (`.xltx`) do perfil restrito, exportado do próprio ISAKMetry.
Funciona sem internet: preenche-se no laboratório e sobe-se o arquivo depois.

- **Um único sujeito por arquivo** — 21 linhas de variáveis. Para os 20 perfis são **20 arquivos**.
- **O aluno preenche apenas quatro coisas:** idioma, data da avaliação, coluna **1ª** e coluna
  **2ª**. Todo o resto é calculado e está bloqueado.
- **Idioma:** o aluno brasileiro escolhe **`Br`**. O código `Pt` é o português europeu e muda os
  rótulos (em `Br`, a segunda variável lê "Estatura alongada"; em `Pt`, "Estatura").
- **Coluna própria para a 3ª medida**, habilitada pela planilha quando necessário.
- **Regras de digitação da própria planilha:** no máximo **1 casa decimal**; preencher até que
  **todas as células fiquem verdes** — vermelho ou laranja indica pendência.
- **Aba protegida** e coluna de tolerância travada: o aluno não consegue alterá-la.
- **Cada aluno exporta a planilha do próprio login.** As tolerâncias embutidas são as do **nível de
  acreditação de quem exportou**. Usar a cópia de um colega ou do instrutor significa trabalhar com
  critério alheio.
- Ordem das 21 variáveis, com os `MeasureItemId` oficiais: básicas 1–4 (massa corporal, estatura
  alongada, estatura sentado, envergadura); dobras 5–12 (tríceps, subescapular, bíceps, crista
  ilíaca, supraespinal, abdominal, coxa, perna); perímetros 15, 16, 20, 21, 23, 24 (braço relaxado,
  braço fletido e contraído, cintura, quadril, coxa média, perna); diâmetros 40, 41, 42 (úmero,
  biestiloide, fêmur).

O upload é feito em **Subjects / Sujeitos**. Após importar, conferir: importação bem-sucedida não
é sinônimo de importação correta.

#### E. O envio dos 20 perfis ("Post-course")

1. **Menu lateral → "Post-course" / "Post-curso"** — item de primeiro nível, ao lado de Home,
   Profiles, Subjects, Account e Population.
2. A tela **"Enviar trabalho pós-curso (20 medições)"** lista **todas as avaliações realizadas após
   a data da prova do curso**, com **Sujeito · Medições · Identificador de medição**, o tipo de
   perfil ("Restringido"), data e hora.
3. O aluno **marca as caixas de seleção** das avaliações que quer enviar. **Pode ter medido mais de
   20 e escolher as melhores** — estratégia recomendável, por proteger contra o sujeito que estourou
   uma variável.
4. O botão **"Enviar"** só fica ativo com **exatamente 20** selecionadas. Não é possível enviar em
   partes.
5. Diálogo de confirmação: *"Deseja enviar as medições ao seu instrutor?"*
6. **A plataforma monta a proforma analítica** dos 20 perfis — valores, cálculos e %ETM variável a
   variável — e a encaminha ao instrutor. O aluno não exporta nem anexa nada.

#### F. Aprovação pelo instrutor e emissão do certificado

O instrutor analisa a proforma analítica: %ETM variável a variável, plausibilidade biológica e
consistência técnica. Aprova ou devolve com apontamentos para retificação.

**Dois sinais automáticos de aprovação, ambos verificáveis pelo aluno:**

1. Recebe **e-mail automático** com o link para baixar o certificado.
2. **A aba "Post-course" desaparece do menu.** Se ela ainda está lá, o processo não fechou.

#### G. Relatório para entregar ao avaliado ("Reports")

Distinto da proforma do instrutor. Serve ao voluntário, e é argumento útil de recrutamento para
quem precisa reunir 20 pessoas.

Sujeitos → cartão do sujeito → **"Measures history"** → lista de avaliações (Perfil · Data ·
Ações) → ícone de relatório → tela **"Gerar informe"**:

| Campo | Função |
|---|---|
| Nome do relatório | Vem com um padrão (`ISAKMetry_Nome_Perfil_data`), editável |
| Escolha uma medida com a qual comparar | Opcional — avaliação anterior do mesmo sujeito, para comparação longitudinal |
| Escolha uma referência | Opcional — **precisa ter sido carregada antes**, em *Account / References* |

O relatório é baixado **em formato Excel**. Pode ser gerado sem nenhuma comparação.

#### H. Autoconferência do %ETM antes do envio

O %ETM auditado é calculado **sobre as duplicatas** — 1ª e 2ª medida. A **terceira medida define o
valor final daquele sujeito, mas não entra no cálculo do ETM**: o Handbook fala explicitamente do
%ETM "das duplicatas".

São 21 cálculos, um por variável, e nenhum pode ultrapassar 7,5% (dobras) ou 1,5% (demais).

**Orientação operacional ao aluno:** conferir **a cada 5 sujeitos**, não no 20º. As medidas podem
ser exportadas por **"Download your measures"**, que baixa toda a base histórica em Excel/CSV.
Com 5 ou 10 sujeitos o número ainda oscila — vale como alerta precoce, para identificar a variável
sistematicamente fora. O motivo é prático: quando a plataforma consolidar o %ETM dos 20, corrigir
não é redigitar, é **recoletar**.

Nunca orientar ajuste de valores para "fechar" o %ETM. O instrutor recebe o relatório analítico
completo, e dispersão pequena demais para ser real é detectável. Isso é fraude de dados e
compromete a acreditação, não apenas a submissão.

#### I. Perda do prazo de 4 meses

O prazo é de **4 meses a contar da data da prova prática** — não do fim do curso. A certificação
vale 4 anos e 4 meses, contados da mesma data.

Vencido o prazo, o instrutor encerra o curso no sistema. Quem não entregou recebe e-mail
informando que **não passou** e fica como **membro não acreditado por quatro anos**.

**Existe uma segunda chance** (Handbook, p. 57):

| Aspecto | Regra |
|---|---|
| O quê | Refazer a **prova prática**; aprovado, recebe **novo prazo** para os 20 perfis |
| Quando | Até **um mês contado do encerramento do curso** — não da data da prova |
| Onde | **Qualquer curso ISAK, com qualquer instrutor** (p. 58–59) |
| Custo | **Sem nova taxa ISAK.** O examinador pode cobrar custos adicionais (modelos, locação) |
| Vagas | Não ocupa vaga na relação máxima aluno/instrutor |
| Se falhar de novo | Na prova **ou** na entrega: matrícula no **curso completo**, como aluno novo |

**A ISAK não prevê janela de 12 meses para esta situação.** Os 12 meses no Handbook referem-se a
contextos não relacionados (p. 29, *Designated Level 3*; p. 32, renomeação a Level 4).

Recomendação do Handbook ao instrutor (p. 57): lembrar os alunos **um mês antes** do vencimento e
acompanhar individualmente quem não entregou. Ao aluno que percebe que não vai conseguir, a
orientação é **falar com o instrutor antes do vencimento**, e não esperar para usar a segunda
chance — que custa refazer a prova e recoletar 20 perfis.

### 5.4 Regra de comunicação sobre o gatilho da 3ª medida no pós-curso

**Não citar valor numérico.** A planilha é gerada com a tolerância do nível de acreditação de quem
a exportou, e não foi possível determinar se a plataforma faz o mesmo ajuste. Orientar que **a
planilha ou o próprio ISAKMetry sempre indicam** quando a terceira medida é necessária — a
tolerância já vem embutida na ferramenta, e o aluno não precisa conhecê-la nem calculá-la.

O que cabe ao aluno é **não ignorar o aviso** e estar em condições de atendê-lo: com o avaliado
ainda presente e as marcações ainda no lugar. Daí a orientação de digitar as duas rodadas antes de
liberar o voluntário.

**Permanece explícito** o **critério de aprovação** do %ETM ($\le 7,5\%$ dobras, $\le 1,5\%$
demais), que é outra grandeza e que o aluno precisa conhecer.

---

## 6. Aplicação Clínica e Esportiva: Mudança Real vs. Ruído

Para saber se um atleta realmente reduziu gordura corporal ou ganhou perímetro muscular entre duas consultas, o profissional deve considerar o **Erro Padrão da Diferença (SED - Standard Error of Difference)**:

$$SED = TEM \times \sqrt{2} \approx TEM \times 1,414$$

### Tomada de Decisão com Intervalo de Confiança de 95%:
Para afirmar com 95% de certeza estatística que houve alteração na composição corporal do avaliado:
$$\Delta_{\text{mínima}} \ge 1,96 \times SED \approx 2,77 \times TEM$$

- **Se a diferença observada for menor que $1,96 \times SED$:** O resultado está dentro da margem de ruído do método/avaliador; não se pode assegurar mudança real.
- **Se a diferença for maior:** Há evidência estatística de mudança tecidual efetiva.
