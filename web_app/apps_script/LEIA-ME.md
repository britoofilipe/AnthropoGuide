# Integração das Ações Novas no Apps Script

Este documento detalha como integrar as duas funções novas (`acaoTrocarSenha` e `acaoBloquear`) ao projeto do Apps Script que já atende as ações "cadastrar" e "homologar".

## Passo 1: Acrescentar Colunas à Planilha

Adicione três colunas novas à direita das colunas existentes, na seguinte ordem e grafia exata:

- `origem` (texto; origem da venda: "eduzz", "manual", etc.)
- `eduzz_sale_id` (número da venda no Eduzz; pode estar vazio)
- `precisa_trocar_senha` (0 ou 1; indica se o aluno precisa trocar a senha na primeira autenticação)

As colunas existentes são: nome, email, senha_hash, turma, data_curso, status, data_expiracao.

## Antes de Começar: Conferir o Histórico de Versões

Antes de colar qualquer código novo, recomenda-se conferir o histórico de versões do projeto. Abra o menu Arquivo › Histórico de versões (File › Version history) para visualizar as versões anteriores. Isto permite reverter rapidamente a mudanças caso algo saia errado durante a integração.

## Passo 2: Colar as Funções no Apps Script

Abra o projeto do Apps Script (aquele que já contém o `doPost` e `doGet`).

Crie um novo arquivo com extensão `.gs` (por exemplo, `Codigo_acoes_novas.gs`) ou cole o conteúdo do arquivo `Codigo_acoes_novas.gs` deste repositório em um arquivo novo do seu projeto.

As duas funções são:
- `acaoTrocarSenha(dados, aba)`: grava o novo hash de senha e zera `precisa_trocar_senha`.
- `acaoBloquear(dados, aba)`: marca `status = "expirado"` e preence `data_expiracao` com a data de hoje.

## Passo 3: Encaminhar as Ações no doPost Existente

Localize a função `doPost` no seu projeto. Ela já trata `action === "cadastrar"` e `action === "homologar"`.

Acrescente dois novos trechos para as ações novas:

```javascript
} else if (dados.action === "trocar_senha") {
  resultado = acaoTrocarSenha(dados, aba);
} else if (dados.action === "bloquear") {
  resultado = acaoBloquear(dados, aba);
```

Estes trechos devem estar no mesmo bloco condicional que já trata as outras ações, antes do `ContentService.createTextOutput(...)` que devolve o JSON.

## Passo 4: Acrescentar Campos Novos à Ação "cadastrar"

Localize o trecho que trata `action === "cadastrar"` dentro do `doPost`.

Quando gravar a linha nova, acrescente também os três campos novos:
- `dados.origem` na coluna `origem`
- `dados.eduzz_sale_id` na coluna `eduzz_sale_id`
- `dados.precisa_trocar_senha` na coluna `precisa_trocar_senha`

Estes campos devem estar presentes no payload JSON recebido (se não estiverem, use valores padrão como string vazia ou 0).

## Passo 5: Incluir Colunas Novas no doGet

Localize a função `doGet` no seu projeto. Ela deve devolver um JSON com todas as linhas da planilha.

Modifique o trecho que monta o objeto JSON de cada linha para incluir também:
- `origem`: o valor da coluna `origem`
- `eduzz_sale_id`: o valor da coluna `eduzz_sale_id`
- `precisa_trocar_senha`: o valor da coluna `precisa_trocar_senha`

## Passo 6: Reimplantar como Nova Versão da Mesma Implantação

Salve o projeto Apps Script.

Siga exatamente esta sequência para garantir que a URL NÃO mude:

1. Menu Implantar › Gerenciar implantações (Deploy › Manage deployments).
2. Localize a implantação existente do Web App (aquela cuja URL está em uso).
3. Clique no ícone de lápis (Edit) ao lado dessa implantação.
4. No campo Versão, escolha "Nova versão" (New version) — aparecerá uma nova entrada no dropdown.
5. Clique em Implantar (Deploy).

**Importante:** Não use a opção "Nova implantação" (New deployment) no passo 5. Isso criaria outra implantação com URL diferente e derrubaria o acesso de todos os alunos, já que o app usa a GSHEETS_URL atual. A URL deve permanecer exatamente a mesma.

## Passo 7: Conferir com curl

Após reimplantar, abra um terminal e execute:

```bash
curl -s "$GSHEETS_URL" | head
```

Substitua `$GSHEETS_URL` pela URL do seu Web App do Apps Script.

Verifique que o JSON devolvido inclui os campos `origem`, `eduzz_sale_id` e `precisa_trocar_senha` em cada aluno.

Exemplo de saída esperada (primeiras linhas):

```json
[
  {
    "nome": "João Silva",
    "email": "joao@example.com",
    "senha_hash": "...",
    "turma": "N1_2025_01",
    "data_curso": "2025-01-15",
    "status": "ativo",
    "data_expiracao": "2025-02-15",
    "origem": "eduzz",
    "eduzz_sale_id": "12345",
    "precisa_trocar_senha": 1
  },
  ...
]
```

## Contrato HTTP: Ações Novas

Após a integração, o Web App aceitará também:

### POST {action: "trocar_senha"}
Parâmetros:
- `action`: "trocar_senha"
- `email`: email do aluno (identificador)
- `senha_hash`: novo hash da senha

Resposta:
```json
{"ok": true}
```

ou

```json
{"ok": false, "erro": "aluno nao encontrado"}
```

### POST {action: "bloquear"}
Parâmetros:
- `action`: "bloquear"
- `eduzz_sale_id`: ID da venda no Eduzz (identificador)

Resposta:
```json
{"ok": true}
```

ou

```json
{"ok": false, "erro": "venda nao encontrada"}
```
