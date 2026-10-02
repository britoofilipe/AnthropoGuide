# Runbook — Sincronização e Liberação Automática Eduzz

Este documento orienta a operação, monitoramento e recuperação de falhas do fluxo de sincronização entre a Eduzz e a plataforma web do **AnthropoGuide**.

---

## 1. Visão Geral da Operação

A sincronização é executada pelo script `web_app/sincronizar_eduzz.py`.

* **Frequência padrão:** 3 vezes ao dia, às **06:00**, **14:00** e **22:00** (horário de Brasília).
* **Janela de busca:** Últimos 3 dias (configurável via `EDUZZ_DIAS_JANELA` no `.env`), garantindo resiliência caso o computador esteja desligado em algum dia.
* **O que processa:**
  1. Vendas com status `paid` (Paga): Cria o aluno com senha provisória, validade calculada (`compra + PRAZO_ACESSO_DIAS`), registra na planilha Google (fonte da verdade) e no SQLite (espelho), e envia e-mail com as credenciais.
  2. Vendas com status `refunded` ou `canceled` (Reembolsada/Cancelada): Bloqueia o acesso imediatamente na planilha e no SQLite.
* **Idempotência:** Toda venda é associada ao `eduzz_sale_id`. Reexecuções não duplicam alunos nem reenviam e-mails para vendas já liberadas.

---

## 2. Logs e Monitoramento

* **Arquivo de log:** `D:\ISAK_Filipe_Instrutor\AnthropoGuide\web_app\sincronizacao_eduzz.log`
* **Formato das mensagens:**
  * Sucesso: `INFO Acesso liberado para a venda 12345`
  * Bloqueio: `INFO Acesso bloqueado para a venda 12345`
  * Erros: `ERROR Falha ao liberar a venda 12345` acompanhado do traceback.
  * Resumo final: `INFO Resumo: {'liberados': X, 'bloqueados': Y, 'erros': [...]}`

---

## 3. Execução Manual

Para disparar a sincronização imediatamente sem aguardar o agendador:

```cmd
cd /d D:\ISAK_Filipe_Instrutor\AnthropoGuide\web_app
python sincronizar_eduzz.py
```

O terminal exibirá o resumo da execução no final:
`{'liberados': 0, 'bloqueados': 0, 'erros': []}`

---

## 4. Agendamento de Tarefa no Windows

Para configurar ou recriar os 3 gatilhos diários no Agendador de Tarefas do Windows, abra o PowerShell e execute:

```powershell
$triggers = @(
    (New-ScheduledTaskTrigger -Daily -At "06:00"),
    (New-ScheduledTaskTrigger -Daily -At "14:00"),
    (New-ScheduledTaskTrigger -Daily -At "22:00")
)
Set-ScheduledTask -TaskName "AnthropoGuide - Sincronizar Eduzz" -Trigger $triggers
```

Para verificar se a tarefa está agendada:
```cmd
schtasks /Query /TN "AnthropoGuide - Sincronizar Eduzz"
```

Para forçar a execução imediata da tarefa agendada:
```cmd
schtasks /Run /TN "AnthropoGuide - Sincronizar Eduzz"
```

---

## 5. Procedimentos de Recuperação e Falhas Comuns

### 5.1 Falha de Envio de E-mail (Aluno criado, mas e-mail não entregue)
Se o envio do e-mail falhar (ex.: instabilidade SMTP ou senha de app incorreta), o aluno **já terá sido cadastrado** para preservar o acesso, mas a venda aparecerá na lista de `erros` do resumo.

**Como reenviar manualmente o acesso ao aluno:**
1. Abra um terminal em `web_app`:
   ```bash
   cd D:\ISAK_Filipe_Instrutor\AnthropoGuide\web_app
   ```
2. Gere uma nova senha provisória limpa (sem caracteres ambíguos):
   ```bash
   python -c "from integracao_eduzz import liberacao; print(liberacao.gerar_senha_provisoria())"
   ```
3. Aplique a nova senha ao e-mail do aluno (atualiza planilha e banco):
   ```bash
   python -c "import auth; print(auth.trocar_senha('email.do.aluno@dominio.com', 'SENHA_GERADA'))"
   ```
4. Envie manualmente a mensagem para o aluno com os dados de acesso:
   * Endereço da plataforma (`URL_PLATAFORMA`)
   * E-mail de login
   * Senha provisória

### 5.2 Token da Eduzz Expirado ou Inválido
Se o log apresentar erro 401 ou `KeyError: 'EDUZZ_TOKEN'`:
1. Acesse o console de desenvolvedor da Eduzz (https://console.eduzz.com/application/apps).
2. Gere um novo token pessoal com o escopo `myeduzz_sales_read`.
3. Atualize o arquivo `web_app/.env` na chave `EDUZZ_TOKEN=`.

### 5.3 Planilha Google Indisponível ou Apps Script Rejeitando
Se o Apps Script estiver offline ou retornar erro:
* O sistema **não** cadastra no SQLite isoladamente para evitar dessincronização entre a fonte da verdade e o login dos alunos.
* A venda constará no log como erro.
* Na próxima execução (ou após restabelecer a planilha), a venda será processada automaticamente pela janela de busca.
* Se necessário auditar diferenças entre a planilha e o banco local:
  ```bash
  python -c "import auth; print('Planilha:', len(auth.gsheets_listar())); conn=auth.get_db_connection(); print('SQLite:', conn.execute('SELECT COUNT(*) FROM alunos').fetchone()[0])"
  ```

### 5.4 Comprador que já possui cadastro (ex.: aluno bônus de curso N1)
Se a Eduzz listar uma venda cujo e-mail já existe na base:
* `auth.cadastrar_aluno` recusa a duplicidade para proteger a integridade do histórico do aluno.
* A venda é apontada na lista de erros.
* O instrutor pode acessar o painel administrativo na interface web e ajustar ou homologar o prazo do aluno manualmente.

---

## 6. Lista de Verificação de Variáveis (`.env`)

Certifique-se de que o arquivo `web_app/.env` contém todos os parâmetros obrigatórios:

| Variável | Descrição | Exemplo |
|---|---|---|
| `GEMINI_API_KEY` | Chave de API do Gemini para o tutor | `AIzaSy...` |
| `ADMIN_PASSWORD` | Senha do painel do instrutor | `senha_segura` |
| `GSHEETS_URL` | Web App do Google Apps Script | `https://script.google.com/macros/s/.../exec` |
| `EDUZZ_TOKEN` | Token da aplicação Eduzz | `eyJhbGci...` |
| `EDUZZ_PRODUCT_ID` | ID numérico do produto na Eduzz | `123456` |
| `PRAZO_ACESSO_DIAS` | Período de vigência da compra | `120` |
| `EDUZZ_DIAS_JANELA` | Janela de dias para buscar vendas | `3` |
| `URL_PLATAFORMA` | Link do Streamlit acessível ao aluno | `https://anthropoguide.com.br` |
| `EMAIL_REMETENTE` | Nome e e-mail remetente | `AnthropoGuide <sizelab.academy@gmail.com>` |
| `SMTP_HOST` | Host do servidor de e-mail | `smtp.gmail.com` |
| `SMTP_PORT` | Porta TLS | `587` |
| `SMTP_USUARIO` | Usuário autenticação SMTP | `sizelab.academy@gmail.com` |
| `SMTP_SENHA` | Senha de aplicativo Google | `abcd efgh ijkl mnop` |
