# Liberação automática via Eduzz — status da execução

**Última atualização:** 23/09/2026 (execução pausada a pedido do Filipe)
**Branch:** `feat/liberacao-automatica-eduzz` (a partir de `main`, commit `1d01af0`)
**Plano:** [docs/superpowers/plans/2026-09-23-liberacao-automatica-eduzz.md](superpowers/plans/2026-09-23-liberacao-automatica-eduzz.md) — versão 2, escrita contra a persistência híbrida real
**Suíte:** 28 testes, todos passando (`cd web_app && python -m pytest tests/ -v`)
**Nada foi enviado ao `main` nem ao GitHub.**

## Onde paramos

| # | Tarefa | Situação | Commits |
|---|---|---|---|
| 1 | Colunas `origem`, `eduzz_sale_id`, `precisa_trocar_senha` no SQLite | Concluída | `abbdc9d` |
| 2 | Senha com scrypt e salt, migrando os hashes antigos | Concluída (1 correção) | `72c1f5c`, `087e1bf` |
| 3 | Ações `trocar_senha` e `bloquear` para o Apps Script | Concluída (1 correção) | `8585ad4`, `368b5a9` |
| 4 | Camada da planilha estendida em `auth.py` | Concluída (2 correções) | `8497228`, `df07544`, `536d604` |
| 5 | Troca obrigatória da senha provisória nos dois stores | Concluída (1 correção) | `c9e735d`, `4556684` |
| 6 | Cliente da API de vendas da Eduzz | Concluída (1 correção) | `b77b868`, `f47951b` |
| 7 | Liberação e bloqueio sobre a camada híbrida | Concluída (1 correção) | `88bb819`, `375a204` |
| 8 | E-mail de liberação | **Não iniciada** | — |
| 9 | Orquestrador da sincronização | **Não iniciada** | — |
| 10 | Agendamento no Windows e runbook | **Não iniciada** | — |

Cada tarefa passou por revisão independente e, quando reprovada, por correção e re-revisão.

## O que já funciona

- O banco local e a planilha aceitam os campos que identificam a origem da venda.
- As senhas usam scrypt com salt; os hashes antigos migram sozinhos no primeiro login.
- O aluno com senha provisória é obrigado a trocá-la antes de usar o tutor, e a troca vale nos dois stores.
- Existe um cliente da API de vendas da Eduzz, com paginação e respeito ao limite de requisições.
- Uma venda paga vira acesso, e um reembolso vira bloqueio, de forma idempotente.

## O que falta para funcionar de ponta a ponta

1. **Task 8** — o e-mail que entrega o endereço, o login e a senha provisória.
2. **Task 9** — o orquestrador que junta tudo e roda uma vez por dia.
3. **Task 10** — o agendamento no Windows e o runbook de operação.

## Pendências suas (Task 0 do plano)

1. Criar a aplicação na Eduzz com o escopo `myeduzz_sales_read` e guardar o token em `web_app/.env` como `EDUZZ_TOKEN`.
2. Descobrir o `productId` do AnthropoGuide depois de cadastrar o produto e guardar como `EDUZZ_PRODUCT_ID`.
3. Gerar uma senha de app do Gmail e completar as variáveis de SMTP, além de `URL_PLATAFORMA` e `PRAZO_ACESSO_DIAS`.
4. Aplicar no Apps Script o material de `web_app/apps_script/` e acrescentar à planilha as colunas `origem`, `eduzz_sale_id` e `precisa_trocar_senha`. **Reimplantar como nova versão da mesma implantação**, para a URL não mudar.

Enquanto o item 4 não for feito, o código novo continua funcionando: as ações novas só são chamadas nos fluxos da automação, que ainda não estão ligados.

## Ponto aberto que precisa de decisão na Task 9

`liberacao.liberar()` devolve `None` tanto quando a venda já foi processada quanto quando a planilha recusou a gravação. Se o orquestrador for escrito sem tratar isso, uma falha real da planilha será contada como "venda ignorada" e não aparecerá na lista de erros. Ao implementar a Task 9, `liberar` precisa distinguir os dois casos.

## Registro completo

O andamento tarefa a tarefa, com as revisões e as decisões que tomei, está em
`.superpowers/sdd/2026-09-23-liberacao-automatica-eduzz/progress.md` (fora do controle de versão).
