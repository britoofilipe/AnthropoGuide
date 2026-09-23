# Liberação automática de acesso via Eduzz — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Uma tarefa agendada diária consulta as vendas do AnthropoGuide na API da Eduzz, cria o acesso do aluno, registra na planilha Google, envia o e-mail de liberação com senha provisória e bloqueia quem foi reembolsado.

**Architecture:** Um pacote `web_app/integracao_eduzz/` com três módulos (API da Eduzz, liberação, e-mail) e um orquestrador `sincronizar_eduzz.py` chamado pelo Agendador de Tarefas do Windows. A gravação do aluno passa pela camada híbrida que já existe em `auth.py` — Google Sheets como store de produção, SQLite como fallback —, estendida com os campos e ações que faltam. O orquestrador é idempotente: cada venda é identificada por `eduzz_sale_id`, gravado nos dois stores, e reprocessar a mesma janela não duplica aluno nem e-mail.

**Tech Stack:** Python 3.14, sqlite3 e hashlib.scrypt (stdlib), requests, smtplib/email (stdlib), Streamlit 1.64, pytest, Google Apps Script (Web App já existente).

**Spec:** este documento — seções "Contexto e decisões" e "Global Constraints" abaixo. O texto comercial e os campos do produto na Eduzz estão em `AnthropoGuide/CADASTRO_EDUZZ_ANTHROPOGUIDE_v1_0.md`.

## Contexto e decisões

> **Revisão de 23/09/2026 (v2).** A v1 deste plano supunha o SQLite como fonte da verdade e previa criar uma segunda planilha como painel operacional. Ao executar a Task 2 descobriu-se que `auth.py` já implementa **persistência híbrida**: Google Sheets (Apps Script Web App em `GSHEETS_URL`) como store de produção e SQLite como fallback, em `cadastrar_aluno`, `homologar_acreditacao`, `verificar_acesso` e `listar_alunos`. As Tasks 1 e 2 permanecem válidas e concluídas; as demais foram reescritas contra o código real. Decisão do titular: manter o desenho híbrido, e a planilha aceita escrita.

- O produto é vendido na conta **SizeLab Academy**; a entrega na Eduzz fica como **Arquivos** (PDF de boas-vindas). A liberação real do acesso é feita por esta automação, não pela Eduzz.
- **Não existe planilha nova.** O registro do acesso é a planilha que já está em produção; a automação grava nela pelas ações do Apps Script.
- Gatilho é a **API da Eduzz**, não a leitura de e-mails: `GET /myeduzz/v1/sales` devolve dado estruturado e, no mesmo retorno, os status `canceled` e `refunded`, o que permite bloquear acesso — coisa que o e-mail de compra não entrega de forma confiável.
- A fonte da verdade é a **planilha de produção**, com o SQLite como fallback. A planilha já guarda `senha_hash` (nunca a senha em texto) — isso não muda.
- A senha provisória é gerada pelo script, enviada só por e-mail e guardada apenas como hash. O aluno é obrigado a trocá-la no primeiro acesso.

## Global Constraints

- Nenhuma senha, token, chave ou segredo em código, em log ou na planilha. Tudo vem de `web_app/.env`, que já está no `.gitignore`.
- Toda data do negócio usa o fuso `America/Sao_Paulo`; datas trocadas com a API usam ISO 8601.
- Idempotência obrigatória: reexecutar qualquer janela de datas não pode criar aluno duplicado nem reenviar e-mail já enviado.
- Falha em uma venda não pode interromper o processamento das demais; cada erro vai para o log e para o resumo enviado ao instrutor.
- A API Eduzz permite 30 requisições por minuto no endpoint de vendas; respeitar com paginação e pausa entre páginas.
- Textos ao aluno seguem `BC_MARCA_FILIPEBRITO.md` v0.2: tom técnico e didático, sem emoji, sem promessa, grafia FilipeBrito.
- Prazo de acesso vendido: variável `PRAZO_ACESSO_DIAS` no `.env` (o valor comercial ainda será definido pelo Filipe; o código nunca fixa o número).
- Toda escrita de aluno passa por `auth.py`; nenhum módulo novo fala com a planilha ou com o SQLite diretamente.
- A senha em texto existe só em memória e no corpo do e-mail; nos stores, apenas o hash.
- Testes com pytest, banco em `tmp_path`, sem rede: a API, o SMTP e o gspread são dublês nos testes.

---

## Task 0: Pré-requisitos manuais (Filipe)

Sem eles, as Tasks 6, 8 e 10 não podem ser testadas de ponta a ponta.

- [ ] **Passo 1: Aplicação e token na Eduzz** — em https://console.eduzz.com/application/apps, criar a aplicação, habilitar o escopo `myeduzz_sales_read`, copiar o token e guardar em `web_app/.env` como `EDUZZ_TOKEN=`.

- [ ] **Passo 2: productId do AnthropoGuide** — depois do produto cadastrado:

```bash
curl -H "authorization: bearer $EDUZZ_TOKEN" "https://api.eduzz.com/myeduzz/v1/products?itemsPerPage=50"
```

Guardar o `id` em `web_app/.env` como `EDUZZ_PRODUCT_ID=`.

- [ ] **Passo 3: senha de app do Gmail** — com verificação em duas etapas ativa, gerar a senha de app e completar o `web_app/.env`:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USUARIO=sizelab.academy@gmail.com
SMTP_SENHA=<senha de app>
EMAIL_REMETENTE=AnthropoGuide <sizelab.academy@gmail.com>
URL_PLATAFORMA=<endereço público do app>
PRAZO_ACESSO_DIAS=<prazo vendido>
```

- [ ] **Passo 4: aplicar a Task 3 no Apps Script** — colar no editor do Apps Script as ações produzidas pela Task 3, acrescentar as três colunas novas à planilha e reimplantar o Web App mantendo a mesma URL (Implantar › Gerenciar implantações › editar › Nova versão). A `GSHEETS_URL` não muda.

---

## File Structure

| Arquivo | Responsabilidade |
|---|---|
| `web_app/auth.py` (Tasks 1-2 concluídas; estendido nas 4, 5 e 7) | Hash forte, colunas novas, camada híbrida Sheets/SQLite, troca de senha, bloqueio |
| `web_app/app.py` (Task 5) | Tela de troca de senha no primeiro acesso |
| `web_app/apps_script/Codigo_acoes_novas.gs` (Task 3) | Ações `trocar_senha` e `bloquear` para colar no Apps Script |
| `web_app/integracao_eduzz/eduzz_api.py` (Task 6) | Cliente HTTP da API de vendas |
| `web_app/integracao_eduzz/liberacao.py` (Task 7) | Venda paga cria acesso; reembolsada bloqueia |
| `web_app/integracao_eduzz/email_envio.py` (Task 8) | E-mail de liberação |
| `web_app/sincronizar_eduzz.py` (Task 9) | Orquestrador da tarefa agendada |
| `AnthropoGuide/docs/RUNBOOK_LIBERACAO_EDUZZ.md` (Task 10) | Operação e recuperação de falhas |

---

## Task 1: Colunas de origem da venda no banco — CONCLUÍDA (commit abbdc9d)

Colunas `origem`, `eduzz_sale_id` e `precisa_trocar_senha` em `alunos`, com migração idempotente e índice único parcial. Revisão limpa.

## Task 2: Hash com salt e verificação compatível — CONCLUÍDA (commits 72c1f5c, 087e1bf)

`hash_password` com scrypt e salt; `conferir_senha` aceitando o formato novo e o legado, robusta a hash malformado; `verificar_acesso` regravando o hash legado na mesma conexão. A revisão reprovou a primeira versão; a correção passou na re-revisão.

---

## Task 3: Ações novas do Apps Script

**Files:**
- Create: `web_app/apps_script/Codigo_acoes_novas.gs`
- Create: `web_app/apps_script/LEIA-ME.md`

**Interfaces:**
- Produces: o contrato HTTP que a Task 4 consome. `POST {"action": "trocar_senha", "email", "senha_hash"}` grava o hash e zera `precisa_trocar_senha`. `POST {"action": "bloquear", "eduzz_sale_id"}` marca `status = "expirado"` e `data_expiracao` de hoje. `POST {"action": "cadastrar", ...}` passa a aceitar também `origem`, `eduzz_sale_id` e `precisa_trocar_senha`. O `GET` passa a devolver essas três colunas.

Esta task entrega **código para o Filipe colar**, não código executado pelo app. Não há teste automatizado: a verificação é manual, no Passo 4 da Task 0.

- [ ] **Step 1: Escrever o arquivo `.gs`**

```javascript
/**
 * Ações novas do AnthropoGuide para o Apps Script da planilha de alunos.
 * Colar dentro do mesmo projeto que já atende "cadastrar" e "homologar".
 * Pré-requisito: a planilha precisa das colunas origem, eduzz_sale_id e precisa_trocar_senha.
 */

function acaoTrocarSenha(dados, aba) {
  var linhas = aba.getDataRange().getValues();
  var cabecalho = linhas[0];
  var colEmail = cabecalho.indexOf("email");
  var colHash = cabecalho.indexOf("senha_hash");
  var colTrocar = cabecalho.indexOf("precisa_trocar_senha");
  var alvo = String(dados.email).trim().toLowerCase();

  for (var i = 1; i < linhas.length; i++) {
    if (String(linhas[i][colEmail]).trim().toLowerCase() === alvo) {
      aba.getRange(i + 1, colHash + 1).setValue(dados.senha_hash);
      if (colTrocar >= 0) {
        aba.getRange(i + 1, colTrocar + 1).setValue(0);
      }
      return {ok: true};
    }
  }
  return {ok: false, erro: "aluno nao encontrado"};
}

function acaoBloquear(dados, aba) {
  var linhas = aba.getDataRange().getValues();
  var cabecalho = linhas[0];
  var colVenda = cabecalho.indexOf("eduzz_sale_id");
  var colStatus = cabecalho.indexOf("status");
  var colExp = cabecalho.indexOf("data_expiracao");
  var alvo = String(dados.eduzz_sale_id).trim();
  var hoje = Utilities.formatDate(new Date(), "America/Sao_Paulo", "yyyy-MM-dd");

  for (var i = 1; i < linhas.length; i++) {
    if (String(linhas[i][colVenda]).trim() === alvo) {
      aba.getRange(i + 1, colStatus + 1).setValue("expirado");
      aba.getRange(i + 1, colExp + 1).setValue(hoje);
      return {ok: true};
    }
  }
  return {ok: false, erro: "venda nao encontrada"};
}
```

- [ ] **Step 2: Escrever o LEIA-ME com o passo a passo**

`web_app/apps_script/LEIA-ME.md`, nesta ordem: (1) acrescentar à planilha as colunas `origem`, `eduzz_sale_id` e `precisa_trocar_senha`, nesta grafia exata, à direita das existentes; (2) colar as duas funções no projeto do Apps Script; (3) no `doPost` existente, encaminhar `action === "trocar_senha"` para `acaoTrocarSenha` e `action === "bloquear"` para `acaoBloquear`; (4) na ação `cadastrar` existente, gravar também `origem`, `eduzz_sale_id` e `precisa_trocar_senha` quando vierem no payload; (5) no `doGet` existente, incluir as três colunas novas no JSON devolvido; (6) reimplantar como nova versão da MESMA implantação, para a URL não mudar; (7) conferir com `curl -s "$GSHEETS_URL" | head` que o JSON traz as colunas novas.

- [ ] **Step 3: Commit**

```bash
git add web_app/apps_script/
git commit -m "docs(sheets): acoes trocar_senha e bloquear para o Apps Script"
```

---

## Task 4: Camada híbrida estendida em auth.py

**Files:**
- Modify: `web_app/auth.py`
- Test: `web_app/tests/test_auth_gsheets.py`

**Interfaces:**
- Consumes: contrato da Task 3.
- Produces: `auth.gsheets_cadastrar(nome, email, senha_hash, turma, data_curso, data_expiracao, origem="manual", eduzz_sale_id=None, precisa_trocar_senha=0)`; `auth.gsheets_trocar_senha(email, senha_hash) -> tuple[bool, str]`; `auth.gsheets_bloquear(eduzz_sale_id) -> tuple[bool, str]`; `auth.gsheets_listar()` devolvendo também `origem`, `eduzz_sale_id` (int ou None) e `precisa_trocar_senha` (int); `auth.cadastrar_aluno(..., origem="manual", eduzz_sale_id=None, precisa_trocar_senha=0)` repassando os campos aos dois stores.

- [ ] **Step 1: Write the failing test**

```python
import datetime
import auth


class RespostaFalsa:
    def __init__(self, payload=None, status_code=200):
        self._payload = payload if payload is not None else []
        self.status_code = status_code
        self.text = "ok"

    def json(self):
        return self._payload


def test_gsheets_cadastrar_envia_campos_da_eduzz(monkeypatch):
    enviados = {}

    def post_falso(url, json=None, timeout=None, allow_redirects=None):
        enviados.update(json)
        return RespostaFalsa()

    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth.requests, "post", post_falso)

    ok, _ = auth.gsheets_cadastrar(
        "Ana Souza", "ana@x.com", "scrypt$aa$bb", "Eduzz",
        datetime.date(2026, 9, 23), datetime.date(2027, 1, 21),
        origem="eduzz", eduzz_sale_id=9001, precisa_trocar_senha=1,
    )

    assert ok
    assert enviados["action"] == "cadastrar"
    assert enviados["origem"] == "eduzz"
    assert enviados["eduzz_sale_id"] == 9001
    assert enviados["precisa_trocar_senha"] == 1


def test_gsheets_trocar_senha_e_bloquear(monkeypatch):
    chamadas = []
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(
        auth.requests, "post",
        lambda url, json=None, timeout=None, allow_redirects=None: (chamadas.append(json), RespostaFalsa())[1],
    )

    assert auth.gsheets_trocar_senha("ana@x.com", "scrypt$cc$dd")[0]
    assert auth.gsheets_bloquear(9001)[0]
    assert chamadas[0] == {"action": "trocar_senha", "email": "ana@x.com", "senha_hash": "scrypt$cc$dd"}
    assert chamadas[1] == {"action": "bloquear", "eduzz_sale_id": 9001}


def test_gsheets_listar_devolve_campos_novos(monkeypatch):
    linha = {"nome": "Ana Souza", "email": "ANA@X.com", "senha_hash": "scrypt$aa$bb",
             "turma": "Eduzz", "data_curso": "2026-09-23", "status": "pos_curso",
             "data_expiracao": "2099-01-01", "origem": "eduzz", "eduzz_sale_id": "9001",
             "precisa_trocar_senha": "1"}
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth.requests, "get",
                        lambda url, timeout=None, allow_redirects=None: RespostaFalsa([linha]))

    aluno = auth.gsheets_listar()[0]
    assert aluno["origem"] == "eduzz"
    assert aluno["eduzz_sale_id"] == 9001
    assert aluno["precisa_trocar_senha"] == 1


def test_gsheets_listar_tolera_linha_sem_campos_novos(monkeypatch):
    linha = {"nome": "Bruno Lima", "email": "b@x.com", "senha_hash": "h", "turma": "ISAK N1",
             "data_curso": "2026-01-10", "status": "pos_curso", "data_expiracao": "2099-01-01"}
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth.requests, "get",
                        lambda url, timeout=None, allow_redirects=None: RespostaFalsa([linha]))

    aluno = auth.gsheets_listar()[0]
    assert aluno["origem"] == "manual"
    assert aluno["eduzz_sale_id"] is None
    assert aluno["precisa_trocar_senha"] == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd web_app && python -m pytest tests/test_auth_gsheets.py -v`
Expected: FAIL — `gsheets_trocar_senha` e `gsheets_bloquear` não existem; `gsheets_cadastrar` não aceita os parâmetros novos.

- [ ] **Step 3: Write minimal implementation**

Em `gsheets_cadastrar`, acrescentar os parâmetros com os padrões `origem="manual"`, `eduzz_sale_id=None`, `precisa_trocar_senha=0` e incluí-los no `payload`. Acrescentar ao módulo:

```python
def gsheets_trocar_senha(email: str, senha_hash: str) -> Tuple[bool, str]:
    url = get_gsheets_url()
    if not url:
        return False, "URL do Google Sheets não configurada."
    resp = requests.post(
        url, json={"action": "trocar_senha", "email": email, "senha_hash": senha_hash},
        timeout=12, allow_redirects=True,
    )
    if resp.status_code == 200:
        return True, "Senha alterada na planilha."
    return False, f"Falha ao trocar a senha no Google Sheets: {resp.text}"


def gsheets_bloquear(eduzz_sale_id: int) -> Tuple[bool, str]:
    url = get_gsheets_url()
    if not url:
        return False, "URL do Google Sheets não configurada."
    resp = requests.post(
        url, json={"action": "bloquear", "eduzz_sale_id": eduzz_sale_id},
        timeout=12, allow_redirects=True,
    )
    if resp.status_code == 200:
        return True, "Acesso bloqueado na planilha."
    return False, f"Falha ao bloquear no Google Sheets: {resp.text}"
```

Em `gsheets_listar`, dentro do dicionário montado por linha, acrescentar:

```python
            "origem": str(r.get("origem") or "manual").strip().lower(),
            "eduzz_sale_id": int(r["eduzz_sale_id"]) if str(r.get("eduzz_sale_id") or "").strip() else None,
            "precisa_trocar_senha": int(r.get("precisa_trocar_senha") or 0),
```

Em `cadastrar_aluno`, acrescentar os mesmos três parâmetros com os mesmos padrões, repassá-los a `gsheets_cadastrar` e incluí-los no INSERT do fallback SQLite.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd web_app && python -m pytest tests/ -v`
Expected: PASS, inclusive os testes das Tasks 1 e 2

- [ ] **Step 5: Commit**

```bash
git add web_app/auth.py web_app/tests/test_auth_gsheets.py
git commit -m "feat(auth): camada Sheets aceita origem, venda Eduzz, troca de senha e bloqueio"
```

---

## Task 5: Troca obrigatória da senha provisória nos dois stores

**Files:**
- Modify: `web_app/auth.py`, `web_app/app.py`
- Test: `web_app/tests/test_auth_troca_senha.py`

**Interfaces:**
- Consumes: Task 4.
- Produces: `auth.trocar_senha(email: str, nova: str) -> tuple[bool, str]`, que grava na planilha quando há `GSHEETS_URL` e sempre atualiza o SQLite.

- [ ] **Step 1: Write the failing test**

```python
import datetime
import auth


def test_troca_senha_atualiza_sqlite_e_limpa_flag(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "t.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    auth.cadastrar_aluno("Ana Souza", "ana@x.com", "provisoria", "Eduzz",
                         datetime.date.today(), precisa_trocar_senha=1)

    ok, _, dados = auth.verificar_acesso("ana@x.com", "provisoria")
    assert ok and dados["precisa_trocar_senha"] == 1

    assert auth.trocar_senha("ana@x.com", "novaSenhaForte")[0]
    ok, _, dados = auth.verificar_acesso("ana@x.com", "novaSenhaForte")
    assert ok and dados["precisa_trocar_senha"] == 0
    assert not auth.verificar_acesso("ana@x.com", "provisoria")[0]


def test_troca_senha_grava_na_planilha_quando_configurada(tmp_path, monkeypatch):
    chamadas = []
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "t2.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_trocar_senha",
                        lambda email, senha_hash: (chamadas.append((email, senha_hash)), (True, "ok"))[1])
    auth.init_db()
    auth.cadastrar_aluno("Ana Souza", "ana@x.com", "provisoria", "Eduzz", datetime.date.today())

    assert auth.trocar_senha("ana@x.com", "novaSenhaForte")[0]
    assert chamadas[0][0] == "ana@x.com"
    assert chamadas[0][1].startswith("scrypt$")


def test_troca_senha_exige_oito_caracteres(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "t3.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    auth.cadastrar_aluno("Ana Souza", "ana@x.com", "provisoria", "Eduzz", datetime.date.today())
    ok, msg = auth.trocar_senha("ana@x.com", "curta")
    assert not ok and "8" in msg
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd web_app && python -m pytest tests/test_auth_troca_senha.py -v`
Expected: FAIL com `AttributeError: module 'auth' has no attribute 'trocar_senha'`

- [ ] **Step 3: Write minimal implementation**

```python
def trocar_senha(email: str, nova: str) -> Tuple[bool, str]:
    """Grava a senha nova nos dois stores. A planilha é a fonte da verdade;
    o SQLite é sempre atualizado para o fallback não ficar com a senha antiga."""
    if len(nova) < 8:
        return False, "A nova senha precisa ter pelo menos 8 caracteres."

    email_clean = email.strip().lower()
    novo_hash = hash_password(nova)
    gravou_planilha = False

    if get_gsheets_url():
        try:
            gravou_planilha, _ = gsheets_trocar_senha(email_clean, novo_hash)
        except Exception as e:
            print(f"[Auth] Falha ao trocar a senha no Google Sheets: {e}. Atualizando apenas o SQLite.")

    with get_db_connection() as conn:
        cur = conn.execute(
            "UPDATE alunos SET senha_hash = ?, precisa_trocar_senha = 0 WHERE email = ?",
            (novo_hash, email_clean),
        )
        conn.commit()

    if not gravou_planilha and cur.rowcount == 0:
        return False, "Aluno não encontrado."
    return True, "Senha alterada."
```

Em `app.py`, dentro de `render_aluno_view`, antes de renderizar o chat:

```python
    if aluno.get("precisa_trocar_senha"):
        ui.cabecalho_chat(aviso=False)
        st.markdown("#### Defina sua senha")
        st.caption("Você entrou com a senha provisória enviada por e-mail. Defina uma senha sua para continuar.")
        nova = st.text_input("Nova senha", type="password")
        conf = st.text_input("Repita a nova senha", type="password")
        if st.button("Salvar senha", type="primary"):
            if nova != conf:
                st.error("As senhas não coincidem.")
            else:
                ok, msg = auth.trocar_senha(aluno["email"], nova)
                if ok:
                    st.session_state.user_data["precisa_trocar_senha"] = 0
                    st.rerun()
                else:
                    st.error(msg)
        return
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd web_app && python -m pytest tests/ -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add web_app/auth.py web_app/app.py web_app/tests/test_auth_troca_senha.py
git commit -m "feat(app): troca obrigatoria da senha provisoria nos dois stores"
```

---

## Task 6: Cliente da API de vendas da Eduzz

**Files:**
- Create: `web_app/integracao_eduzz/__init__.py`, `web_app/integracao_eduzz/eduzz_api.py`
- Test: `web_app/tests/test_eduzz_api.py`

**Interfaces:**
- Produces: `eduzz_api.listar_vendas(token: str, product_id: int, inicio: datetime.date, fim: datetime.date, status: str) -> list[dict]`, que pagina até esgotar e devolve os objetos `items` da API.

- [ ] **Step 1: Write the failing test**

```python
import datetime
from integracao_eduzz import eduzz_api


class RespostaFalsa:
    def __init__(self, payload):
        self._payload = payload
        self.status_code = 200

    def json(self):
        return self._payload

    def raise_for_status(self):
        return None


def test_listar_vendas_percorre_paginas(monkeypatch):
    chamadas = []

    def get_falso(url, headers=None, params=None, timeout=None):
        chamadas.append(params)
        if params["page"] == 1:
            return RespostaFalsa({"items": [{"id": 1}], "pages": 2, "page": 1})
        return RespostaFalsa({"items": [{"id": 2}], "pages": 2, "page": 2})

    monkeypatch.setattr(eduzz_api.requests, "get", get_falso)
    monkeypatch.setattr(eduzz_api.time, "sleep", lambda s: None)

    vendas = eduzz_api.listar_vendas(
        "tok", 55, datetime.date(2026, 9, 1), datetime.date(2026, 9, 2), "paid"
    )

    assert [v["id"] for v in vendas] == [1, 2]
    assert chamadas[0]["productId"] == 55
    assert chamadas[0]["status"] == "paid"
    assert chamadas[0]["referenceDate"] == "paidAt"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd web_app && python -m pytest tests/test_eduzz_api.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'integracao_eduzz'`

- [ ] **Step 3: Write minimal implementation**

```python
"""Cliente da API pública da Eduzz — apenas leitura de vendas."""
import datetime
import time
import requests

BASE = "https://api.eduzz.com/myeduzz/v1/sales"
PAUSA_ENTRE_PAGINAS = 2.1  # limite documentado: 30 requisições por minuto


def listar_vendas(token, product_id, inicio, fim, status):
    vendas, pagina, total_paginas = [], 1, 1
    while pagina <= total_paginas:
        resposta = requests.get(
            BASE,
            headers={"authorization": f"bearer {token}", "content-type": "application/json"},
            params={
                "startDate": inicio.isoformat(),
                "endDate": fim.isoformat(),
                "referenceDate": "paidAt" if status == "paid" else "updatedAt",
                "productId": product_id,
                "status": status,
                "page": pagina,
                "itemsPerPage": 100,
            },
            timeout=30,
        )
        resposta.raise_for_status()
        dados = resposta.json()
        vendas.extend(dados.get("items", []))
        total_paginas = dados.get("pages", 1)
        pagina += 1
        if pagina <= total_paginas:
            time.sleep(PAUSA_ENTRE_PAGINAS)
    return vendas
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd web_app && python -m pytest tests/test_eduzz_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add web_app/integracao_eduzz/ web_app/tests/test_eduzz_api.py
git commit -m "feat(eduzz): cliente de listagem de vendas com paginacao"
```

---

## Task 7: Regra de liberação e bloqueio sobre a camada híbrida

**Files:**
- Create: `web_app/integracao_eduzz/liberacao.py`
- Modify: `web_app/auth.py` (parâmetro `data_expiracao` opcional em `cadastrar_aluno`)
- Test: `web_app/tests/test_liberacao.py`

**Interfaces:**
- Consumes: Tasks 4 e 5.
- Produces: `liberacao.gerar_senha_provisoria() -> str`; `liberacao.ja_processada(sale_id: int) -> bool`; `liberacao.liberar(venda: dict, prazo_dias: int) -> dict | None` devolvendo `{"nome","email","senha","validade","sale_id"}`; `liberacao.bloquear(venda: dict) -> bool`. Também produz `auth.cadastrar_aluno(..., data_expiracao: Optional[date] = None)`.

- [ ] **Step 1: Write the failing test**

```python
import datetime
import auth
from integracao_eduzz import liberacao

VENDA = {"id": 9001, "status": "paid", "paidAt": "2026-09-23T10:00:00-03:00",
         "buyer": {"name": "Ana Souza", "email": "Ana@X.com"}}


def test_liberar_cria_aluno_uma_unica_vez(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "l.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()

    novo = liberacao.liberar(VENDA, prazo_dias=120)
    assert novo["email"] == "ana@x.com"
    assert novo["validade"] == datetime.date(2026, 9, 23) + datetime.timedelta(days=120)
    ok, _, dados = auth.verificar_acesso("ana@x.com", novo["senha"])
    assert ok and dados["precisa_trocar_senha"] == 1 and dados["origem"] == "eduzz"

    assert liberacao.liberar(VENDA, prazo_dias=120) is None


def test_liberar_consulta_planilha_para_idempotencia(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "l2.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_listar", lambda: [
        {"email": "ana@x.com", "eduzz_sale_id": 9001, "nome": "Ana Souza"}])
    auth.init_db()

    assert liberacao.liberar(VENDA, prazo_dias=120) is None


def test_bloquear_usa_planilha_e_sqlite(tmp_path, monkeypatch):
    bloqueios = []
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "b.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: "https://script.exemplo/exec")
    monkeypatch.setattr(auth, "gsheets_listar", lambda: [])
    monkeypatch.setattr(auth, "gsheets_cadastrar", lambda *a, **k: (True, "ok"))
    monkeypatch.setattr(auth, "gsheets_bloquear",
                        lambda sale_id: (bloqueios.append(sale_id), (True, "ok"))[1])
    auth.init_db()
    liberacao.liberar(VENDA, prazo_dias=120)

    assert liberacao.bloquear({"id": 9001, "status": "refunded"})
    assert bloqueios == [9001]
    with auth.get_db_connection() as conn:
        linha = conn.execute("SELECT status FROM alunos WHERE eduzz_sale_id = 9001").fetchone()
    assert linha["status"] == "expirado"


def test_senha_provisoria_sem_caracteres_ambiguos():
    senha = liberacao.gerar_senha_provisoria()
    assert len(senha) == 10 and not set(senha) & set("O0Il1")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd web_app && python -m pytest tests/test_liberacao.py -v`
Expected: FAIL com `ImportError: cannot import name 'liberacao'`

- [ ] **Step 3: Write minimal implementation**

Primeiro, em `auth.cadastrar_aluno`, acrescentar o parâmetro `data_expiracao: Optional[datetime.date] = None`, usado quando informado e mantendo o cálculo atual (`data_curso + 120 dias`) como padrão — compatível com as chamadas existentes no painel do instrutor. Depois:

```python
"""Cria e revoga o acesso do aluno a partir de uma venda da Eduzz.
Toda escrita passa por auth.py, que cuida da planilha e do fallback SQLite."""
import datetime
import secrets
import sqlite3

import auth

ALFABETO = "ABCDEFGHJKMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789"


def gerar_senha_provisoria() -> str:
    return "".join(secrets.choice(ALFABETO) for _ in range(10))


def ja_processada(sale_id: int) -> bool:
    if auth.get_gsheets_url():
        try:
            if any(a.get("eduzz_sale_id") == sale_id for a in auth.gsheets_listar()):
                return True
        except Exception as e:
            print(f"[Liberacao] Nao foi possivel conferir a planilha: {e}. Usando o SQLite.")
    with auth.get_db_connection() as conn:
        achou = conn.execute(
            "SELECT 1 FROM alunos WHERE eduzz_sale_id = ?", (sale_id,)
        ).fetchone()
    return achou is not None


def liberar(venda: dict, prazo_dias: int):
    sale_id = venda["id"]
    if ja_processada(sale_id):
        return None

    email = venda["buyer"]["email"].strip().lower()
    nome = venda["buyer"]["name"].strip()
    compra = datetime.datetime.fromisoformat(venda["paidAt"]).date()
    validade = compra + datetime.timedelta(days=prazo_dias)
    senha = gerar_senha_provisoria()

    try:
        ok, msg = auth.cadastrar_aluno(
            nome, email, senha, "Eduzz", compra,
            origem="eduzz", eduzz_sale_id=sale_id, precisa_trocar_senha=1,
            data_expiracao=validade,
        )
    except sqlite3.IntegrityError:
        return None
    if not ok:
        raise RuntimeError(msg)
    return {"nome": nome, "email": email, "senha": senha, "validade": validade, "sale_id": sale_id}


def bloquear(venda: dict) -> bool:
    sale_id = venda["id"]
    bloqueou_planilha = False
    if auth.get_gsheets_url():
        try:
            bloqueou_planilha, _ = auth.gsheets_bloquear(sale_id)
        except Exception as e:
            print(f"[Liberacao] Falha ao bloquear na planilha: {e}. Seguindo pelo SQLite.")

    with auth.get_db_connection() as conn:
        cur = conn.execute(
            "UPDATE alunos SET status = 'expirado', data_expiracao = ?"
            " WHERE eduzz_sale_id = ? AND status != 'expirado'",
            (datetime.date.today().isoformat(), sale_id),
        )
        conn.commit()
    return bloqueou_planilha or cur.rowcount > 0
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd web_app && python -m pytest tests/ -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add web_app/integracao_eduzz/liberacao.py web_app/auth.py web_app/tests/test_liberacao.py
git commit -m "feat(eduzz): libera e bloqueia acesso pela camada hibrida, de forma idempotente"
```

---

## Task 8: E-mail de liberação

**Files:**
- Create: `web_app/integracao_eduzz/email_envio.py`
- Test: `web_app/tests/test_email_envio.py`

**Interfaces:**
- Consumes: Task 7.
- Produces: `email_envio.montar(dados: dict, url_plataforma: str, remetente: str = "AnthropoGuide") -> EmailMessage`; `email_envio.enviar(mensagem, host, porta, usuario, senha) -> None`.

- [ ] **Step 1: Write the failing test**

```python
from integracao_eduzz import email_envio

DADOS = {"nome": "Ana Souza", "email": "ana@x.com", "senha": "Kd7mTq9xAb",
         "validade": "21/01/2027", "sale_id": 9001}


def test_email_traz_dados_de_acesso():
    msg = email_envio.montar(DADOS, "https://anthropoguide.exemplo.br")
    corpo = msg.get_content()
    assert msg["To"] == "ana@x.com"
    assert "AnthropoGuide" in msg["Subject"]
    assert "Kd7mTq9xAb" in corpo
    assert "https://anthropoguide.exemplo.br" in corpo
    assert "21/01/2027" in corpo
    assert "trocar" in corpo.lower()


def test_envio_usa_starttls(monkeypatch):
    eventos = []

    class SmtpFalso:
        def __init__(self, host, porta, timeout=None):
            eventos.append(("conectou", host, porta))

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def starttls(self):
            eventos.append(("starttls",))

        def login(self, usuario, senha):
            eventos.append(("login", usuario))

        def send_message(self, mensagem):
            eventos.append(("enviou", mensagem["To"]))

    monkeypatch.setattr(email_envio.smtplib, "SMTP", SmtpFalso)
    email_envio.enviar(email_envio.montar(DADOS, "https://x.br"), "smtp.x", 587, "u@x", "s")

    assert [e[0] for e in eventos] == ["conectou", "starttls", "login", "enviou"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd web_app && python -m pytest tests/test_email_envio.py -v`
Expected: FAIL com `ImportError: cannot import name 'email_envio'`

- [ ] **Step 3: Write minimal implementation**

```python
"""E-mail de liberação de acesso, no tom da marca FilipeBrito."""
import smtplib
from email.message import EmailMessage

CORPO = """Olá, {nome}.

Seu acesso ao AnthropoGuide está liberado.

Endereço: {url}
Login: {email}
Senha provisória: {senha}

Ao entrar pela primeira vez, você precisa trocar a senha provisória por uma senha sua.
O acesso é pessoal e intransferível, válido até {validade}.

Uma orientação prática: descreva as dúvidas como você contaria a um colega, com o contexto
do caso, e sempre sem dados que identifiquem o avaliado.

Bom uso.

Prof. Filipe Brito
Instrutor Internacional ISAK Nível 3
"""


def montar(dados: dict, url_plataforma: str, remetente: str = "AnthropoGuide") -> EmailMessage:
    mensagem = EmailMessage()
    mensagem["Subject"] = "Seu acesso ao AnthropoGuide está liberado"
    mensagem["From"] = remetente
    mensagem["To"] = dados["email"]
    mensagem.set_content(CORPO.format(
        nome=dados["nome"].split()[0], url=url_plataforma, email=dados["email"],
        senha=dados["senha"], validade=dados["validade"],
    ))
    return mensagem


def enviar(mensagem: EmailMessage, host: str, porta: int, usuario: str, senha: str) -> None:
    with smtplib.SMTP(host, porta, timeout=30) as servidor:
        servidor.starttls()
        servidor.login(usuario, senha)
        servidor.send_message(mensagem)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd web_app && python -m pytest tests/test_email_envio.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add web_app/integracao_eduzz/email_envio.py web_app/tests/test_email_envio.py
git commit -m "feat(eduzz): e-mail de liberacao com senha provisoria"
```

---

## Task 9: Orquestrador da sincronização

**Files:**
- Create: `web_app/sincronizar_eduzz.py`
- Test: `web_app/tests/test_sincronizar.py`

**Interfaces:**
- Consumes: Tasks 6, 7 e 8.
- Produces: `sincronizar_eduzz.sincronizar(config: dict, enviar_email) -> dict` devolvendo `{"liberados": int, "bloqueados": int, "erros": list[str]}`. `config` traz `token`, `product_id`, `prazo_dias`, `url_plataforma`, `dias_janela`.

- [ ] **Step 1: Write the failing test**

```python
import auth
import sincronizar_eduzz
from integracao_eduzz import eduzz_api

CONFIG = {"token": "t", "product_id": 55, "prazo_dias": 120,
          "url_plataforma": "https://x.br", "dias_janela": 3}
VENDA_PAGA = {"id": 9001, "status": "paid", "paidAt": "2026-09-23T10:00:00-03:00",
              "buyer": {"name": "Ana Souza", "email": "ana@x.com"}}
VENDA_REEMBOLSADA = {"id": 9001, "status": "refunded", "paidAt": "2026-09-23T10:00:00-03:00",
                     "buyer": {"name": "Ana Souza", "email": "ana@x.com"}}


def test_libera_paga_e_bloqueia_reembolsada(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "s.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    enviados = []
    monkeypatch.setattr(
        eduzz_api, "listar_vendas",
        lambda token, product_id, inicio, fim, status:
            [VENDA_PAGA] if status == "paid" else ([VENDA_REEMBOLSADA] if status == "refunded" else []),
    )

    r1 = sincronizar_eduzz.sincronizar(CONFIG, enviados.append)
    assert r1["liberados"] == 1 and r1["bloqueados"] == 1 and r1["erros"] == []
    assert len(enviados) == 1 and enviados[0]["email"] == "ana@x.com"

    r2 = sincronizar_eduzz.sincronizar(CONFIG, enviados.append)
    assert r2["liberados"] == 0 and len(enviados) == 1


def test_erro_em_uma_venda_nao_derruba_as_outras(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "s2.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    ruim = {"id": 9002, "status": "paid", "paidAt": "2026-09-23T10:00:00-03:00", "buyer": {}}
    monkeypatch.setattr(
        eduzz_api, "listar_vendas",
        lambda token, product_id, inicio, fim, status: [ruim, VENDA_PAGA] if status == "paid" else [],
    )

    resultado = sincronizar_eduzz.sincronizar(CONFIG, lambda d: None)
    assert resultado["liberados"] == 1 and len(resultado["erros"]) == 1


def test_falha_de_email_vira_erro_da_venda(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "DB_PATH", tmp_path / "s3.db")
    monkeypatch.setattr(auth, "get_gsheets_url", lambda: None)
    auth.init_db()
    monkeypatch.setattr(
        eduzz_api, "listar_vendas",
        lambda token, product_id, inicio, fim, status: [VENDA_PAGA] if status == "paid" else [],
    )

    def envio_quebrado(dados):
        raise RuntimeError("smtp fora do ar")

    resultado = sincronizar_eduzz.sincronizar(CONFIG, envio_quebrado)
    assert resultado["liberados"] == 0
    assert len(resultado["erros"]) == 1 and "smtp" in resultado["erros"][0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd web_app && python -m pytest tests/test_sincronizar.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'sincronizar_eduzz'`

- [ ] **Step 3: Write minimal implementation**

```python
"""Sincroniza vendas da Eduzz com os acessos do AnthropoGuide (tarefa agendada)."""
import datetime
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

import auth
from integracao_eduzz import eduzz_api, email_envio, liberacao

BASE = Path(__file__).resolve().parent
logging.basicConfig(
    filename=BASE / "sincronizacao_eduzz.log", level=logging.INFO, encoding="utf-8",
    format="%(asctime)s %(levelname)s %(message)s",
)


def sincronizar(config: dict, enviar_email) -> dict:
    hoje = datetime.date.today()
    inicio = hoje - datetime.timedelta(days=config["dias_janela"])
    resultado = {"liberados": 0, "bloqueados": 0, "erros": []}

    for venda in eduzz_api.listar_vendas(config["token"], config["product_id"], inicio, hoje, "paid"):
        try:
            novo = liberacao.liberar(venda, config["prazo_dias"])
            if novo is None:
                continue
            enviar_email({**novo, "validade": novo["validade"].strftime("%d/%m/%Y")})
            resultado["liberados"] += 1
            logging.info("Acesso liberado para a venda %s", venda.get("id"))
        except Exception as erro:
            resultado["erros"].append(f"venda {venda.get('id')}: {erro}")
            logging.exception("Falha ao liberar a venda %s", venda.get("id"))

    for status in ("refunded", "canceled"):
        for venda in eduzz_api.listar_vendas(config["token"], config["product_id"], inicio, hoje, status):
            try:
                if liberacao.bloquear(venda):
                    resultado["bloqueados"] += 1
                    logging.info("Acesso bloqueado para a venda %s", venda.get("id"))
            except Exception as erro:
                resultado["erros"].append(f"venda {venda.get('id')}: {erro}")
                logging.exception("Falha ao bloquear a venda %s", venda.get("id"))

    return resultado


def main() -> int:
    load_dotenv(BASE / ".env")
    auth.init_db()
    config = {
        "token": os.environ["EDUZZ_TOKEN"],
        "product_id": int(os.environ["EDUZZ_PRODUCT_ID"]),
        "prazo_dias": int(os.environ["PRAZO_ACESSO_DIAS"]),
        "url_plataforma": os.environ["URL_PLATAFORMA"],
        "dias_janela": int(os.getenv("EDUZZ_DIAS_JANELA", "3")),
    }

    def enviar(dados):
        email_envio.enviar(
            email_envio.montar(dados, config["url_plataforma"], os.environ["EMAIL_REMETENTE"]),
            os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"]),
            os.environ["SMTP_USUARIO"], os.environ["SMTP_SENHA"],
        )

    resultado = sincronizar(config, enviar)
    logging.info("Resumo: %s", resultado)
    print(resultado)
    return 1 if resultado["erros"] else 0


if __name__ == "__main__":
    sys.exit(main())
```

A janela de 3 dias cobre execuções perdidas sem guardar a data da última rodada; a idempotência por `eduzz_sale_id` impede reprocessamento. O e-mail é enviado dentro do mesmo `try` da liberação: se o envio falhar, a venda entra como erro e o reenvio é manual, pelo runbook — o aluno já existe.

- [ ] **Step 4: Run test to verify it passes**

Run: `cd web_app && python -m pytest tests/ -v`
Expected: PASS (toda a suíte)

- [ ] **Step 5: Commit**

```bash
git add web_app/sincronizar_eduzz.py web_app/tests/test_sincronizar.py
git commit -m "feat(eduzz): orquestrador diario de liberacao e bloqueio de acessos"
```

---

## Task 10: Agendamento no Windows e runbook

**Files:**
- Create: `AnthropoGuide/docs/RUNBOOK_LIBERACAO_EDUZZ.md`
- Modify: `web_app/requirements.txt`

- [ ] **Step 1: Declarar as dependências**

Acrescentar a `web_app/requirements.txt`:

```
requests>=2.32
pytest>=8.3
```

- [ ] **Step 2: Rodar uma vez em modo de conferência**

Run: `cd web_app && python sincronizar_eduzz.py`
Expected: imprime `{'liberados': 0, 'bloqueados': 0, 'erros': []}` quando não há vendas, e cria `sincronizacao_eduzz.log`. Variável faltando no `.env` aparece como `KeyError` com o nome dela.

- [ ] **Step 3: Criar a tarefa agendada**

```bash
schtasks /Create /TN "AnthropoGuide - Sincronizar Eduzz" /TR "cmd /c cd /d D:\ISAK_Filipe_Instrutor\AnthropoGuide\web_app && python sincronizar_eduzz.py >> sincronizacao_eduzz.log 2>&1" /SC DAILY /ST 08:00 /RL LIMITED
```

- [ ] **Step 4: Escrever o runbook**

`AnthropoGuide/docs/RUNBOOK_LIBERACAO_EDUZZ.md` com: o que a tarefa faz e a que horas; onde fica o log; como rodar manualmente; como reenviar o acesso de um aluno cujo e-mail falhou (gerar senha com `python -c "from integracao_eduzz import liberacao; print(liberacao.gerar_senha_provisoria())"`, aplicar com `auth.trocar_senha` e avisar o aluno); o que fazer quando o token da Eduzz expirar; como conferir a planilha contra o SQLite; e o que fazer quando a planilha estiver fora do ar na hora da sincronização (o aluno entra só no SQLite e precisa ser replicado na planilha depois).

- [ ] **Step 5: Commit**

```bash
git add web_app/requirements.txt AnthropoGuide/docs/RUNBOOK_LIBERACAO_EDUZZ.md
git commit -m "docs: runbook e agendamento da sincronizacao com a Eduzz"
```

---

## Riscos conhecidos

- **Token pessoal da Eduzz** é oficialmente "atalho para testes". Se a Eduzz exigir OAuth2 em produção, a Task 6 ganha uma etapa de obtenção de token; o resto não muda.
- **Planilha indisponível na hora da sincronização:** o aluno é criado só no SQLite e a planilha fica defasada. O runbook cobre a reconciliação; uma evolução futura é uma fila de pendências.
- **E-mail caindo em spam:** conferir a primeira venda real; se acontecer, enviar pelo domínio próprio em vez do Gmail.
- **Comprador que já é aluno** (recebeu como bônus e comprou): `cadastrar_aluno` recusa o e-mail duplicado e a venda entra como erro para tratamento manual — o certo, porque o caso é estender a validade de um cadastro existente, não criar outro.
