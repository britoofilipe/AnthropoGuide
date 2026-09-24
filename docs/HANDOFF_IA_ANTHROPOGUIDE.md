# AnthropoGuide — documentação de passagem para outra IA

**Data:** 24/09/2026
**Autor deste documento:** sessão Claude Code que executou as tarefas 1 a 7 da automação de liberação de acesso.
**Para quem:** o próximo assistente que for continuar este projeto.
**Titular do projeto:** Filipe Brito, nutricionista, Instrutor Internacional ISAK Nível 3.

Leia este arquivo inteiro antes de escrever qualquer linha de código. Ele descreve o produto, as regras que não podem ser quebradas, o estado exato do código e o que falta fazer.

---

## 1. O que é o AnthropoGuide

Um **tutor digital de antropometria e composição corporal**. O aluno descreve uma dúvida ou uma situação prática e recebe orientação técnica com o raciocínio explicado, as alternativas possíveis, os limites de cada uma e as referências.

Existe em duas formas:

1. **Gem do Google Gemini** — a forma original, montada na conta Google AI Pro do Filipe a partir do `SYSTEM_PROMPT_ANTHROPOGUIDE.md` (versão vigente 2.5) e dos 8 módulos de `knowledge_base/`.
2. **Plataforma web privada** (`web_app/`) — app Streamlit com login por e-mail e senha, controle de validade de acesso, painel do instrutor e chat que consome a API do Gemini com o mesmo system prompt e a mesma base de conhecimento. É esta a forma que está sendo comercializada.

### Fronteira funcional (decisão do titular, não negociável)

O tutor **não executa a avaliação** de uma pessoa a partir dos dados recebidos e **não entrega decisão clínica pronta**. Ele analisa o contexto, explica as opções e suas limitações e orienta o profissional a escolher. Não emite laudo. Não concede acreditação ISAK.

### Público

Alunos e egressos dos cursos ISAK Nível 1 do Filipe (recebem como bônus) e, a partir da venda na Eduzz, profissionais de saúde que medem mas não necessariamente têm certificação.

---

## 2. Regras que não podem ser quebradas

### 2.1 Marca FilipeBrito

A base normativa é `D:\ISAK_Filipe_Instrutor\referencias\MARCA FILIPE BRITO\BC_MARCA_FILIPEBRITO.md` (versão 0.2). O essencial:

- Grafia **FilipeBrito**, sem espaço, em identidade visual. "Filipe Brito" com espaço só em autoria, bio e texto corrido.
- A marca aparece como **grafismo + nome**, nunca o grafismo sozinho — exceto o ícone da aba do navegador, autorizado em 23/09/2026 e registrado na seção 7.6 do manual. O avatar do tutor no chat é o monograma "AG", justamente para o aluno não atribuir a resposta da IA ao Filipe pessoalmente.
- Paleta: verde `#7FB961`, turquesa `#01978F`, magenta `#C40B7B`, azul `#014393`, cinza `#5C5B5F`. Gradiente principal verde→turquesa; secundário magenta→azul; magenta só como detalhe.
- Tipografia: Gotham quando disponível (está instalada na máquina do Filipe); Montserrat nos títulos e Inter no corpo como alternativas web.
- Tom: técnico, didático, acessível, em primeira pessoa quando representa o Filipe. **Sem emoji em material técnico**, sem sensacionalismo, sem promessa de resultado.
- Palavras proibidas no posicionamento atual: "funcional", "evolutiva", "emagrecimento", "transformação", "biohacking". A frase de apoio autorizada é "Transformando medidas em propósito", usada solta e nunca acoplada ao logotipo.
- Nunca associar a marca a atendimento clínico em consultório.

Arquivos prontos da marca: `referencias/MARCA FILIPE BRITO/PNG_transparente/` (logo horizontal e vertical, colorida e branca, fundo transparente).

### 2.2 ISAK

Fonte: `referencias/Antropometria e ISAK/ISAK_Accreditation_Handbook_2026_knowledge_base.md` e o Handbook 2026 em PDF.

- Curso ISAK só existe com autorização prévia da ISAK Secretariat. Conduzir algo apresentado como curso ISAK sem aprovação pode custar a acreditação do instrutor. **Nada no produto pode se apresentar como curso ISAK nem prometer acreditação.**
- O Manual ISAK (Esparza-Ros, Vaquero-Cristóbal & Marfell-Jones, 2019) é publicação da ISAK, liberada ao aluno pelo instrutor dentro do sistema ISAK. **Não reproduzir nem distribuir o Manual** no produto.
- Declarar a credencial do Filipe (Nível 3) é legítimo. Sugerir chancela institucional da ISAK sobre o produto, não.
- Limites de %ETM: **10% para dobras e 2% para as demais medidas** durante o curso e a prova; **7,5% e 1,5%** na fase pós-curso (os 20 perfis). Nunca 5%/1% — esses são Nível 2.
- Nomenclatura: "dobra da perna" (nunca "perna medial"). Nomes oficiais dos landmarks em latim (*acromiale*, *radiale*, *subscapulare*, *iliocristale*, *supraspinale*).

### 2.3 Privacidade

Os alunos devem enviar casos **sem nome, contato, documento, data exata ou qualquer identificador**. Esse aviso aparece no cabeçalho do chat e no e-mail de boas-vindas, e precisa continuar aparecendo.

---

## 3. Estrutura do repositório

Repositório: `D:\ISAK_Filipe_Instrutor\AnthropoGuide` — remoto `https://github.com/britoofilipe/AnthropoGuide.git`.

```
AnthropoGuide/
├── SYSTEM_PROMPT_ANTHROPOGUIDE.md     # instruções do tutor, versão vigente 2.5
├── versions/                          # histórico do system prompt (v1.0 a v2.5)
├── knowledge_base/                    # 8 módulos temáticos carregados no contexto do tutor
├── decisoes_projeto/                  # ADRs 001 a 007 + histórico de testes + plano original
├── docs/
│   ├── STATUS_LIBERACAO_AUTOMATICA_EDUZZ.md      # status resumido da automação
│   ├── HANDOFF_IA_ANTHROPOGUIDE.md               # este arquivo
│   └── superpowers/plans/2026-09-23-...md        # o plano de implementação, versão 2
├── CADASTRO_EDUZZ_ANTHROPOGUIDE_v1_0.md          # textos e decisões do cadastro do produto
├── marketing/                          # arte do produto e PDF de boas-vindas
└── web_app/                            # a plataforma
```

### web_app

| Arquivo | Papel |
|---|---|
| `app.py` | Streamlit: login, tela de troca de senha, chat do aluno, painel do instrutor |
| `ui.py` | Identidade visual FilipeBrito: CSS, cabeçalhos, cartão de status, avatares |
| `auth.py` | **Núcleo.** Hash de senha, persistência híbrida, ciclo de vida do acesso |
| `gemini_service.py` | Cliente do Gemini com streaming e fallback de modelo |
| `integracao_eduzz/eduzz_api.py` | Cliente somente-leitura da API de vendas da Eduzz |
| `integracao_eduzz/liberacao.py` | Venda paga vira acesso; reembolso vira bloqueio |
| `apps_script/` | Código e instruções para o Filipe colar no Apps Script da planilha |
| `assets/` | Logos, favicon, avatar AG, fonte Montserrat |
| `.streamlit/config.toml` | Tema da marca |
| `tests/` | 28 testes pytest |
| `test_app.py`, `test_api_connection.py`, `test_bot_chat.py` | scripts antigos de verificação manual, **não** são pytest |

Arquivos fora do git, só na máquina do Filipe: `web_app/.env` (segredos) e `web_app/anthropoguide.db` (banco local).

---

## 4. Arquitetura que importa

### 4.1 Persistência híbrida

**A fonte da verdade dos alunos é uma planilha Google**, servida por um Web App do Google Apps Script cuja URL vem de `GSHEETS_URL`. O SQLite local (`anthropoguide.db`) é **fallback**.

- `GET <GSHEETS_URL>` devolve as linhas em JSON.
- `POST <GSHEETS_URL>` com `{"action": "..."}` executa: `cadastrar`, `homologar` (já existiam) e `trocar_senha`, `bloquear` (entregues por nós, ainda **não aplicados** pelo Filipe).
- O Apps Script responde **HTTP 200 mesmo em erro**, com `{"ok": false, "erro": "..."}` no corpo. Por isso `auth.py` confere o corpo, não só o status. **Não desfaça isso.**
- **O código do Apps Script de produção não está no repositório.** Ninguém, nem IA nem revisão, consegue auditar as ações `cadastrar` e `homologar` existentes. Seria bom pedir ao Filipe para versionar o `Código.gs` dele em `web_app/apps_script/`.

Colunas da planilha: `nome`, `email`, `senha_hash`, `turma`, `data_curso`, `status`, `data_expiracao` e — **a criar** — `origem`, `eduzz_sale_id`, `precisa_trocar_senha`.

### 4.2 Contrato de escrita (decidido durante a execução, vale sobre o texto do plano)

Tanto `cadastrar_aluno` quanto `trocar_senha` seguem a mesma regra:

1. Sem `GSHEETS_URL`: grava no SQLite e pronto.
2. Com `GSHEETS_URL` e a planilha **recusando ou falhando**: **não grava em lugar nenhum** e devolve `(False, mensagem)`.
3. Com `GSHEETS_URL` e a planilha **aceitando**: grava também no SQLite como espelho; falha do espelho vai para log e a função ainda devolve sucesso.

O motivo é concreto: `verificar_acesso` consulta a planilha primeiro. Gravar só no SQLite produz um aluno que "existe" para a automação mas não para o login — pessoa paga, fica cadastrada e nunca recebe acesso, com a rodada seguinte achando que já tratou aquela venda.

### 4.3 Ciclo de vida do acesso

- Pós-curso: `data_curso + 120 dias` (4 meses para entregar os 20 perfis).
- Acreditado: `homologar_acreditacao` estende por 1.460 dias (4 anos, a vigência da acreditação ISAK).
- Expirado: `verificar_acesso` nega e explica.
- Venda da Eduzz: validade = data do pagamento + `PRAZO_ACESSO_DIAS` do `.env`. **O Filipe ainda não definiu esse número.**

### 4.4 Senhas

- `hash_password` usa `scrypt` com salt: formato `scrypt$<salt_hex>$<hash_hex>`, n=2^14, r=8, p=1, dklen=32.
- `conferir_senha` aceita esse formato e o legado (SHA-256 puro, 64 hex), sempre com `hmac.compare_digest`, e devolve `False` em qualquer formato malformado, sem lançar exceção.
- `verificar_acesso` regrava o hash legado no formato novo ao autenticar com sucesso.
- Senha gerada por máquina: `liberacao.gerar_senha_provisoria()`, `secrets`, 10 caracteres, alfabeto sem `O`, `0`, `I`, `l`, `1`.
- O aluno com `precisa_trocar_senha = 1` é obrigado a trocar antes de usar o tutor.
- **A senha em texto só existe em memória e no corpo do e-mail.** Nunca em log, nunca na planilha.

### 4.5 Pontos de segurança ainda abertos (o Filipe adiou de propósito)

- `ADMIN_PASSWORD` tem fallback `filipe123` no código (`app.py`). Se o `.env` falhar, qualquer pessoa entra como instrutor.
- O formulário de cadastro vem preenchido com a senha inicial `isak2026`.

O Filipe pediu para tratar isso **depois dos testes**. Não insista antes de ele pedir, mas não piore a situação.

---

## 5. Comercialização na Eduzz

Documento completo: `CADASTRO_EDUZZ_ANTHROPOGUIDE_v1_0.md`.

- Conta vendedora: **SizeLab Academy** (empresa do Filipe). A marca de comunicação continua FilipeBrito.
- Tipo de entrega escolhido: **Arquivos** (PDF de boas-vindas em `marketing/`), com liberação manual — até a automação entrar no ar. O passo seguinte natural é a entrega "Outros › Customizado", que é um webhook da Eduzz e reaproveita quase todo o código da automação.
- Arte do produto: `marketing/AnthropoGuide_Eduzz_400x400_v1_0.png` (a Eduzz recomenda 200×200; o dobro fica nítido em tela retina).
- Ainda faltam: preço, prazo de acesso vendido, e-mail de suporte institucional.

---

## 6. Status da automação de liberação

**Branch de trabalho:** `feat/liberacao-automatica-eduzz`, a partir de `main` (`1d01af0`). **Nada foi para o `main` nem para o GitHub.**
**Suíte:** 28 testes passando.
**Plano:** `docs/superpowers/plans/2026-09-23-liberacao-automatica-eduzz.md` (versão 2).

### Pronto

| # | Tarefa | Commits |
|---|---|---|
| 1 | Colunas `origem`, `eduzz_sale_id`, `precisa_trocar_senha` no SQLite, migração idempotente, índice único parcial | `abbdc9d` |
| 2 | scrypt com salt, migração dos hashes legados | `72c1f5c`, `087e1bf` |
| 3 | Ações `trocar_senha` e `bloquear` para o Apps Script, com LEIA-ME | `8585ad4`, `368b5a9` |
| 4 | Camada da planilha estendida em `auth.py` | `8497228`, `df07544`, `536d604` |
| 5 | Troca obrigatória da senha provisória nos dois stores | `c9e735d`, `4556684` |
| 6 | Cliente da API de vendas da Eduzz | `b77b868`, `f47951b` |
| 7 | Liberação e bloqueio idempotentes | `88bb819`, `375a204` |

### Falta

- **Task 8 — e-mail de liberação.** `web_app/integracao_eduzz/email_envio.py` com `montar(dados, url_plataforma, remetente)` e `enviar(mensagem, host, porta, usuario, senha)` via `starttls`. Código e testes completos estão na Task 8 do plano.
- **Task 9 — orquestrador.** `web_app/sincronizar_eduzz.py`: janela de 3 dias, consulta vendas `paid` e depois `refunded`/`canceled`, libera, envia e-mail, bloqueia, devolve `{"liberados", "bloqueados", "erros"}`. Código e testes na Task 9 do plano. **Leia o item 7 abaixo antes de implementar.**
- **Task 10 — agendamento e runbook.** `schtasks` diário às 8h e `docs/RUNBOOK_LIBERACAO_EDUZZ.md`.

### Pendências do Filipe (sem elas nada roda de verdade)

1. Aplicação na Eduzz com escopo `myeduzz_sales_read` → `EDUZZ_TOKEN` no `.env`.
2. `productId` do produto → `EDUZZ_PRODUCT_ID`.
3. Senha de app do Gmail → `SMTP_*`, mais `EMAIL_REMETENTE`, `URL_PLATAFORMA`, `PRAZO_ACESSO_DIAS`.
4. Aplicar `web_app/apps_script/` no Apps Script e criar as três colunas novas na planilha, **reimplantando como nova versão da mesma implantação** — implantação nova gera outra URL e derruba o login de todos os alunos.

---

## 7. Armadilha conhecida, a resolver na Task 9

`liberacao.liberar()` devolve `None` em dois casos diferentes: "venda já processada" e "a planilha recusou a gravação". Se o orquestrador for escrito ingenuamente, uma falha real da planilha será contada como venda ignorada e **não** aparecerá na lista de erros — ninguém fica sabendo que a venda não foi liberada.

Resolva antes de escrever o orquestrador: faça `liberar` distinguir os dois casos (por exemplo devolvendo `None` só para idempotência e levantando exceção específica, ou devolvendo um resultado tipado). Há um `except sqlite3.IntegrityError` morto em `liberar` que pode ser limpo na mesma passagem.

---

## 8. Como rodar e testar

```bash
# app
cd D:\ISAK_Filipe_Instrutor\AnthropoGuide\web_app
python -m streamlit run app.py     # ou o iniciar_anthropoguide.bat

# testes
cd D:\ISAK_Filipe_Instrutor\AnthropoGuide\web_app
python -m pytest tests/ -v
```

O tema da marca só carrega quando o Streamlit sobe **de dentro de `web_app`**, porque o `config.toml` é lido do diretório de trabalho. O `.bat` já faz o `cd`.

Aluno de teste no banco local: `aluno.teste@isak.com` / `senha123`.

---

## 9. Convenções deste projeto

- Código, comentários, mensagens de commit e textos de interface **em português**.
- Toda escrita de aluno passa por `auth.py`. Nenhum módulo novo fala direto com a planilha ou com o SQLite.
- Testes com pytest, banco em `tmp_path`, **sem rede**: a API da Eduzz, o SMTP e o Apps Script são sempre dublês.
- Nenhum segredo em código, log ou planilha. Tudo vem do `.env`, que está no `.gitignore`.
- Toda alteração que cruza um limite (planilha, rede, e-mail) precisa de teste para o **caminho de falha**, não só o feliz.
- Commits pequenos, um por unidade de trabalho.

### Método que estava em uso

Cada tarefa do plano foi implementada por um agente e depois revisada por outro, independente, com dois veredictos: conformidade com a especificação e qualidade. Achado sério voltava para correção e passava por uma re-revisão focada. Isso pegou sete defeitos que teriam ido para produção, **todos no caminho de erro** — não no caminho feliz. Se você for continuar sozinho, revise o próprio trabalho perguntando explicitamente: o que acontece quando isso falha?

---

## 10. Decisões tomadas durante a execução

Cada uma destas contraria ou completa o texto do plano, e o motivo importa:

1. **Guardas de coluna no Apps Script.** Sem elas, esquecer de criar a coluna `eduzz_sale_id` fazia o bloqueio responder "venda não encontrada", escondendo erro de configuração num fluxo que revoga acesso pago.
2. **Passo de reimplantação reescrito** com a sequência real da interface, porque a redação anterior podia levar a criar uma implantação nova e mudar a URL da planilha.
3. **Valores não numéricos digitados na planilha** (`eduzz_sale_id`, `precisa_trocar_senha`) tratados linha a linha: um "sim" numa célula derrubava a listagem inteira de alunos e jogava todo mundo no fallback.
4. **Contrato de escrita do item 4.2**, aplicado a `trocar_senha` e depois a `cadastrar_aluno`.
5. **Conferência do campo `ok`** no corpo das respostas do Apps Script, não só do HTTP 200.
6. **`referenceDate`** = `paidAt` para vendas pagas e `updatedAt` para reembolso e cancelamento, porque é quando o status muda.

---

## 11. Onde estão as outras coisas

- Manual da marca e logos: `D:\ISAK_Filipe_Instrutor\referencias\MARCA FILIPE BRITO\`
- Handbook ISAK 2026 e base derivada: `D:\ISAK_Filipe_Instrutor\referencias\Antropometria e ISAK\`
- Material dos cursos N1 (roteiros, slides, imagens): `D:\ISAK_Filipe_Instrutor\N1\`
- Registro detalhado da execução, tarefa a tarefa, com revisões e decisões: `.superpowers/sdd/2026-09-23-liberacao-automatica-eduzz/progress.md` (fora do git)

Atenção: em `D:\ISAK_PROCESSAMENTO_ROBERTOCOSTA` há arquivos de credenciais. **Nunca abrir, copiar, indexar nem enviar esses arquivos a um modelo.**

---

## 12. O que eu faria a seguir, na ordem

1. Resolver a armadilha do item 7 e implementar a **Task 8** (e-mail), que é isolada e não depende de credencial para ser testada.
2. Implementar a **Task 9** com os testes do plano, incluindo o caso de falha de envio de e-mail.
3. Pedir ao Filipe as credenciais da Task 0 e rodar o orquestrador em seco, sem vendas, só para ver o `{'liberados': 0, ...}`.
4. Só então **Task 10**: agendar e escrever o runbook.
5. Depois de a primeira venda real passar pelo fluxo, retomar os dois pontos de segurança do item 4.5 com o Filipe.
