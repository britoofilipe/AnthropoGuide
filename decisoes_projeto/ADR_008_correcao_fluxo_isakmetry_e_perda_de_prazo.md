# ADR 008: Correção do Fluxo do ISAKMetry, da Planilha Oficial e da Regra de Perda de Prazo

**Data:** 28/09/2026
**Status:** Aprovado
**Contexto:** Formação de Avaliadores ISAK Nível 1 pelo Prof. Filipe Brito (Instrutor Nível 3)
**Substitui parcialmente:** ADR 005 (itens 2.1.1, 2.1.2 e 2.1.3)
**Fontes:** ISAK Accreditation Handbook 2026, pp. 14–15, 54, 57, 58–59; planilha oficial ISAK do
perfil restrito (`.xltx`) inspecionada célula a célula; quatro tutoriais oficiais do canal ISAK
Global analisados quadro a quadro.

---

## 1. Contexto e Motivação

O ADR 005 (19/09/2026) mapeou os fluxos do ISAKMetry a partir da descrição dos tutoriais oficiais.
A produção do guia do aluno para a tarefa pós-curso exigiu verificar cada passo contra a fonte
primária — o arquivo da planilha e os vídeos, quadro a quadro. **Quatro descrições do ADR 005 e da
base de conhecimento não correspondem ao comportamento real da plataforma.** Este ADR as corrige e
acrescenta a regra de perda de prazo, que não estava documentada em lugar nenhum do projeto.

---

## 2. Correções Adotadas

### 2.1 O envio NÃO é por planilha, e não existe "Send to Instructor"

**Descrição anterior (incorreta):** navegar até *Courses / Mis Cursos* → selecionar o curso →
*Sending 20 subjects* → subir a planilha → clicar em *Send to Instructor*.

**Comportamento real,** confirmado no tutorial *Students: Sending 20 subjects*:

1. **Menu lateral → "Post-course" / "Post-curso".** É um item de menu de primeiro nível, ao lado
   de Home, Profiles, Subjects, Account e Population. Não fica dentro de "Courses".
2. A tela **"Enviar trabalho pós-curso (20 medições)"** lista **todas as avaliações realizadas
   após a data da prova do curso**, com as colunas **Sujeito · Medições · Identificador de
   medição**, o tipo de perfil ("Restringido"), data e hora.
3. O aluno **marca a caixa de seleção** das avaliações que deseja enviar. Pode ter medido mais de
   20 e escolher as melhores.
4. O botão **"Enviar"** só fica ativo com **exatamente 20** selecionadas.
5. Diálogo de confirmação: *"¿Desea enviar las mediciones a su instructor?"*
6. **A própria plataforma monta a proforma analítica** dos 20 perfis e a encaminha ao instrutor. O
   aluno não exporta, não anexa e não monta relatório nenhum.

**Regra derivada para o AnthropoGuide:** nunca instruir o aluno a "enviar a planilha". A planilha
é ferramenta de coleta; o envio é da plataforma.

### 2.2 A planilha oficial é UM sujeito por arquivo, não 20 linhas

**Descrição anterior (incorreta):** "o aluno preenche as 20 linhas sem alterar a estrutura".

**Comportamento real,** por inspeção do arquivo
`Plantilla restringido-Restricted template -Planilha restrito- Modello ristretto- Profil restreint.xltx`:

- Aba única `Isak Metry`, **um único sujeito por arquivo** — 21 linhas de variáveis (linhas 9–29).
  Para os 20 perfis são **20 arquivos**.
- O aluno preenche **apenas quatro coisas**: idioma (`Br` para português do Brasil — `Pt` é o
  europeu e muda os rótulos), data da avaliação, coluna **1ª** e coluna **2ª**.
- Existe **coluna própria para a 3ª medida**, que a planilha habilita sozinha.
- A aba é **protegida** e a coluna de tolerância é **travada**: o aluno não consegue alterá-la.
- Instrução da própria planilha: **no máximo 1 casa decimal**; preencher até que **todas as
  células fiquem verdes** (vermelho/laranja = pendência).
- Ordem das 21 variáveis, com os `MeasureItemId` oficiais: básicas 1–4; dobras 5–12; perímetros
  15, 16, 20, 21, 23, 24; diâmetros 40, 41, 42.

### 2.3 Tolerância da 3ª medida: NÃO citar valor

A planilha é gerada com a tolerância do **nível de acreditação de quem a exportou** — a de um
Nível 3 difere da de um Nível 1. Já o tutorial de medições afirma, em cartão de tela e sem
mencionar nível, que a 3ª medida é pedida quando a diferença passa de *"5% nas dobras e 1% nas
demais variáveis"*. Não foi possível determinar pela documentação disponível se a plataforma
ajusta o valor por nível, como a planilha faz.

**Decisão do Filipe (28/09/2026):** o AnthropoGuide **não cita valor** para o gatilho da 3ª medida
no contexto do pós-curso. Orienta que **a planilha ou o próprio ISAKMetry sempre indicam** se a
terceira medida é necessária, com a tolerância já embutida conforme o nível do usuário, e que o
aluno não precisa conhecê-la nem calculá-la.

**Permanece explícito, porque é outra grandeza:** o **critério de aprovação** do %ETM —
$\le 7,5\%$ nas dobras e $\le 1,5\%$ nas demais medidas.

**Retirado:** a "meta do curso" de $\le 5,0\%$ / $\le 1,0\%$ registrada no ADR 005. Esses são os
valores pós-curso dos **Níveis 2, 3 e 4** (Handbook, Tabela 1), não metas do N1.

### 2.4 O prazo conta da PROVA PRÁTICA, não do curso

**Descrição anterior (incorreta):** "até 4 meses após a data do curso presencial N1".

**Handbook 2026, p. 15:** *"Level 1s have 4 months **from the date of their practical examination**
to submit their 20 proformas."* A validade da certificação — 4 anos e 4 meses — conta da mesma
data.

---

## 3. Regra Nova: Perda de Prazo

Não estava documentada no projeto. Handbook 2026, p. 57 (*Finish of course*):

- Vencido o prazo, o instrutor encerra o curso. Quem não entregou recebe e-mail informando que
  **não passou**, e fica como **membro não acreditado por quatro anos**.
- **Segunda chance:** quem não entregou a proforma pode **refazer a prova prática** e, sendo
  aprovado, **recebe novo prazo** para os 20 perfis.
- **Janela: até um mês contado do encerramento do curso** — não da data da prova. *(Situação
  distinta, p. 54: quem **reprovou na prova** conta um mês **a partir da reprovação**.)*
- **Em qualquer curso ISAK, com qualquer instrutor** (p. 58–59), **sem nova taxa ISAK** e sem
  ocupar vaga na relação máxima aluno/instrutor. O examinador pode cobrar custos adicionais
  (modelos, locação).
- **Falhando de novo** — na prova ou na entrega — é preciso **matricular-se no curso completo
  outra vez, como aluno novo**.

**Atenção:** a ISAK **não** prevê janela de 12 meses para esta situação. Os 12 meses aparecem no
Handbook em contextos não relacionados (p. 29, *Designated Level 3*; p. 32, renomeação a Level 4).

**Dever do instrutor** (p. 57, recomendação): lembrar os alunos **um mês antes** do vencimento e
acompanhar individualmente quem não entregou.

---

## 4. Conteúdo Novo Incorporado

### 4.1 Cadastro de sujeito (tutorial *Create Subjects*)

Blocos do formulário: Dados pessoais · Foto · Características · Histórico de massa corporal ·
Dados de interesse · Grupos de usuários.
**Campos obrigatórios (\*):** Nome, Sobrenome, Telefone, Sexo, Data de nascimento, Raça.

**Regra do campo "Grupos de usuários":** o tutorial instrui a **não preenchê-lo**, salvo quando se
quer compartilhar os dados daquele sujeito com outro antropometrista. Na tarefa pós-curso, fica em
branco.

### 4.2 Medição direta na plataforma (tutorial *Subjects – Measurements*)

Assistente em três passos:
1. **Escolher o perfil** a aplicar e clicar em *Start / Empezar*.
2. **"Take measures"** — tabela **Tipo · Número · Medida antropométrica · 1ª · 2ª · 3ª medida**,
   agrupada por Medidas básicas, Dobras, Perímetros e Diâmetros. Instrução literal da plataforma:
   *inserir o valor de cada variável **na mesma ordem estabelecida pelo ISAK** e em seguida
   realizar a segunda coleta*. A célula da 3ª medida é habilitada pelo sistema onde necessário.
   Botões *Previous step / Next step*.
3. **Salvar.** O tutorial orienta usar *Previous step* para revisar antes de confirmar.

### 4.3 Relatório para o avaliado (tutorial *Reports*)

Sujeitos → cartão do sujeito → **"Measures history"** → lista de avaliações (Perfil · Data ·
Ações) → ícone de relatório → tela **"Gerar informe"**, com: nome do relatório (padrão
`ISAKMetry_Nome_Perfil_data`), comparação opcional com avaliação anterior do mesmo sujeito e
referência opcional — **a referência precisa ter sido carregada antes**, em *Account / References*.
O relatório baixa **em formato Excel**.

Esse relatório **não** é o que vai ao instrutor. Serve ao voluntário — e é argumento útil de
recrutamento para quem precisa reunir 20 pessoas.

### 4.4 Autoconferência do %ETM antes do envio

O %ETM auditado é calculado **sobre as duplicatas** (1ª e 2ª medida). A **terceira medida define o
valor final do sujeito, mas não entra no cálculo do ETM**.

$$\text{ETM} = \sqrt{\frac{\sum d^2}{2n}} \qquad \%\text{ETM} = \frac{\text{ETM}}{\bar{x}} \times 100$$

São 21 cálculos, um por variável. Orientação ao aluno: conferir **a cada 5 sujeitos**, exportando
as medidas por *"Download your measures"*, e não esperar o fechamento dos 20 — no fim, corrigir não
é redigitar, é recoletar.

---

## 5. Impactos na Base de Conhecimento e no System Prompt

- **`knowledge_base/02_qualidade_da_medida.md` §5.3:** reescrita integral (A–F), com o fluxo real
  de envio, a planilha de um sujeito por arquivo, o cadastro, a medição na plataforma, os
  relatórios, a autoconferência e a regra de perda de prazo.
- **`SYSTEM_PROMPT_ANTHROPOGUIDE.md` (v2.6):** bloco de submissão pós-curso corrigido; prazo
  ancorado na prova prática; gatilho da 3ª medida sem valor numérico; regra de perda de prazo
  acrescentada.
- **`versions/system_prompt_v2_6_isakmetry_corrigido.md`:** snapshot da versão.
- **ADR 005:** permanece como registro histórico. Os itens 2.1.1 a 2.1.3 ficam **superados por
  este ADR**.

## 6. Pendência

Confirmar, em conta de aluno **Nível 1**, se a célula da 3ª medida na plataforma é habilitada com a
mesma tolerância da planilha daquele nível. Enquanto não houver essa verificação, o AnthropoGuide
não cita valor, conforme §2.3.
