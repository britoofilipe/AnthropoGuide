/**
 * AnthropoGuide — Backend Google Apps Script (Código.gs Completo)
 * 
 * Este arquivo unifica TODAS as operações da planilha de alunos do AnthropoGuide:
 * - Leitura de alunos (doGet)
 * - Cadastro de alunos (doPost action="cadastrar")
 * - Homologação de acreditação ISAK (doPost action="homologar")
 * - Troca obrigatória de senha provisória (doPost action="trocar_senha")
 * - Bloqueio de acesso por reembolso/cancelamento Eduzz (doPost action="bloquear")
 *
 * Estrutura de colunas esperada na linha 1 da planilha:
 * nome | email | senha_hash | turma | data_curso | status | data_expiracao | origem | eduzz_sale_id | precisa_trocar_senha
 */

// Helper para obter a aba da planilha
function obterAba() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  return ss.getSheetByName("alunos") || ss.getActiveSheet();
}

// Helper para padronizar respostas JSON
function responderJSON(objeto) {
  return ContentService.createTextOutput(JSON.stringify(objeto))
    .setMimeType(ContentService.MimeType.JSON);
}

// Helper para formatar data com segurança
function formatarData(valor) {
  if (valor instanceof Date) {
    return Utilities.formatDate(valor, "America/Sao_Paulo", "yyyy-MM-dd");
  }
  return valor ? String(valor).trim() : "";
}

// =============================================================================
// GET: Listagem de Alunos
// =============================================================================
function doGet(e) {
  try {
    var aba = obterAba();
    var dados = aba.getDataRange().getValues();
    if (dados.length <= 1) {
      return responderJSON([]);
    }

    var cabecalho = dados[0].map(function(col) {
      return String(col).trim().toLowerCase();
    });

    var lista = [];
    for (var i = 1; i < dados.length; i++) {
      var linha = dados[i];
      var aluno = {};
      var temIdentificacao = false;

      for (var j = 0; j < cabecalho.length; j++) {
        var campo = cabecalho[j];
        if (!campo) continue;

        var valor = linha[j];
        if (campo === "data_curso" || campo === "data_expiracao") {
          aluno[campo] = formatarData(valor);
        } else if (campo === "email") {
          aluno[campo] = String(valor || "").trim().toLowerCase();
          if (aluno[campo]) temIdentificacao = true;
        } else if (campo === "nome") {
          aluno[campo] = String(valor || "").trim();
          if (aluno[campo]) temIdentificacao = true;
        } else if (campo === "precisa_trocar_senha") {
          aluno[campo] = (valor !== "" && valor !== null && !isNaN(valor)) ? Number(valor) : 0;
        } else if (campo === "eduzz_sale_id") {
          aluno[campo] = (valor !== "" && valor !== null) ? String(valor).trim() : "";
        } else {
          aluno[campo] = valor !== undefined && valor !== null ? String(valor).trim() : "";
        }
      }

      // Garante campos default caso a coluna não exista na planilha antiga
      if (!aluno.hasOwnProperty("origem")) aluno["origem"] = "manual";
      if (!aluno.hasOwnProperty("eduzz_sale_id")) aluno["eduzz_sale_id"] = "";
      if (!aluno.hasOwnProperty("precisa_trocar_senha")) aluno["precisa_trocar_senha"] = 0;

      if (temIdentificacao) {
        lista.push(aluno);
      }
    }

    return responderJSON(lista);
  } catch (erro) {
    return responderJSON({ ok: false, erro: "Erro ao listar alunos: " + erro.toString() });
  }
}

// =============================================================================
// POST: Roteamento de Ações
// =============================================================================
function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return responderJSON({ ok: false, erro: "Dados de requisição ausentes" });
    }

    var dados = JSON.parse(e.postData.contents);
    var aba = obterAba();
    var resultado;

    switch (dados.action) {
      case "cadastrar":
        resultado = acaoCadastrar(dados, aba);
        break;
      case "homologar":
        resultado = acaoHomologar(dados, aba);
        break;
      case "trocar_senha":
        resultado = acaoTrocarSenha(dados, aba);
        break;
      case "bloquear":
        resultado = acaoBloquear(dados, aba);
        break;
      default:
        resultado = { ok: false, erro: "Acao desconhecida: " + dados.action };
    }

    return responderJSON(resultado);
  } catch (erro) {
    return responderJSON({ ok: false, erro: "Erro no processamento POST: " + erro.toString() });
  }
}

// =============================================================================
// Ação 1: Cadastrar Aluno
// =============================================================================
function acaoCadastrar(dados, aba) {
  var linhas = aba.getDataRange().getValues();
  var cabecalho = linhas[0].map(function(c) { return String(c).trim().toLowerCase(); });

  var colEmail = cabecalho.indexOf("email");
  var colNome = cabecalho.indexOf("nome");
  var colHash = cabecalho.indexOf("senha_hash");
  var colTurma = cabecalho.indexOf("turma");
  var colDataCurso = cabecalho.indexOf("data_curso");
  var colStatus = cabecalho.indexOf("status");
  var colDataExp = cabecalho.indexOf("data_expiracao");
  var colOrigem = cabecalho.indexOf("origem");
  var colEduzzSale = cabecalho.indexOf("eduzz_sale_id");
  var colTrocarSenha = cabecalho.indexOf("precisa_trocar_senha");

  if (colEmail < 0 || colNome < 0 || colHash < 0) {
    return { ok: false, erro: "Colunas essenciais (email, nome, senha_hash) ausentes na planilha" };
  }

  var novoEmail = String(dados.email || "").trim().toLowerCase();
  if (!novoEmail) {
    return { ok: false, erro: "E-mail obrigatorio nao informado" };
  }

  // Verifica duplicidade por email
  for (var i = 1; i < linhas.length; i++) {
    if (String(linhas[i][colEmail]).trim().toLowerCase() === novoEmail) {
      return { ok: false, erro: "Ja existe aluno cadastrado com este e-mail na planilha" };
    }
  }

  // Monta a nova linha de acordo com a ordem do cabeçalho
  var novaLinha = new Array(cabecalho.length).fill("");
  novaLinha[colEmail] = novoEmail;
  novaLinha[colNome] = String(dados.nome || "").trim();
  novaLinha[colHash] = String(dados.senha_hash || "").trim();
  
  if (colTurma >= 0) novaLinha[colTurma] = String(dados.turma || "ISAK N1").trim();
  if (colDataCurso >= 0) novaLinha[colDataCurso] = String(dados.data_curso || "").trim();
  if (colStatus >= 0) novaLinha[colStatus] = String(dados.status || "pos_curso").trim();
  if (colDataExp >= 0) novaLinha[colDataExp] = String(dados.data_expiracao || "").trim();
  if (colOrigem >= 0) novaLinha[colOrigem] = String(dados.origem || "manual").trim();
  if (colEduzzSale >= 0) novaLinha[colEduzzSale] = (dados.eduzz_sale_id !== undefined && dados.eduzz_sale_id !== null) ? String(dados.eduzz_sale_id).trim() : "";
  if (colTrocarSenha >= 0) novaLinha[colTrocarSenha] = (dados.precisa_trocar_senha !== undefined && dados.precisa_trocar_senha !== null) ? Number(dados.precisa_trocar_senha) : 0;

  aba.appendRow(novaLinha);
  return { ok: true, mensagem: "Aluno cadastrado com sucesso" };
}

// =============================================================================
// Ação 2: Homologar Acreditação
// =============================================================================
function acaoHomologar(dados, aba) {
  var linhas = aba.getDataRange().getValues();
  var cabecalho = linhas[0].map(function(c) { return String(c).trim().toLowerCase(); });

  var colEmail = cabecalho.indexOf("email");
  var colStatus = cabecalho.indexOf("status");
  var colDataExp = cabecalho.indexOf("data_expiracao");

  if (colEmail < 0 || colStatus < 0 || colDataExp < 0) {
    return { ok: false, erro: "Colunas email, status ou data_expiracao ausentes na planilha" };
  }

  var alvo = String(dados.email || "").trim().toLowerCase();
  for (var i = 1; i < linhas.length; i++) {
    if (String(linhas[i][colEmail]).trim().toLowerCase() === alvo) {
      aba.getRange(i + 1, colStatus + 1).setValue("acreditado");
      aba.getRange(i + 1, colDataExp + 1).setValue(String(dados.nova_expiracao || "").trim());
      return { ok: true, mensagem: "Acreditacao homologada com sucesso" };
    }
  }

  return { ok: false, erro: "Aluno nao encontrado para homologacao" };
}

// =============================================================================
// Ação 3: Trocar Senha (com limpeza da flag precisa_trocar_senha)
// =============================================================================
function acaoTrocarSenha(dados, aba) {
  var linhas = aba.getDataRange().getValues();
  var cabecalho = linhas[0].map(function(c) { return String(c).trim().toLowerCase(); });

  var colEmail = cabecalho.indexOf("email");
  var colHash = cabecalho.indexOf("senha_hash");
  var colTrocar = cabecalho.indexOf("precisa_trocar_senha");

  if (colEmail < 0) return { ok: false, erro: "coluna email nao encontrada na planilha" };
  if (colHash < 0) return { ok: false, erro: "coluna senha_hash nao encontrada na planilha" };

  var alvo = String(dados.email || "").trim().toLowerCase();
  for (var i = 1; i < linhas.length; i++) {
    if (String(linhas[i][colEmail]).trim().toLowerCase() === alvo) {
      aba.getRange(i + 1, colHash + 1).setValue(dados.senha_hash);
      if (colTrocar >= 0) {
        aba.getRange(i + 1, colTrocar + 1).setValue(0);
      }
      return { ok: true, mensagem: "Senha alterada com sucesso" };
    }
  }

  return { ok: false, erro: "aluno nao encontrado" };
}

// =============================================================================
// Ação 4: Bloquear Acesso (Cancelamento / Reembolso Eduzz)
// =============================================================================
function acaoBloquear(dados, aba) {
  var linhas = aba.getDataRange().getValues();
  var cabecalho = linhas[0].map(function(c) { return String(c).trim().toLowerCase(); });

  var colVenda = cabecalho.indexOf("eduzz_sale_id");
  var colStatus = cabecalho.indexOf("status");
  var colExp = cabecalho.indexOf("data_expiracao");

  if (colVenda < 0) return { ok: false, erro: "coluna eduzz_sale_id nao encontrada na planilha" };
  if (colStatus < 0) return { ok: false, erro: "coluna status nao encontrada na planilha" };
  if (colExp < 0) return { ok: false, erro: "coluna data_expiracao nao encontrada na planilha" };

  var alvo = String(dados.eduzz_sale_id || "").trim();
  var hoje = Utilities.formatDate(new Date(), "America/Sao_Paulo", "yyyy-MM-dd");

  for (var i = 1; i < linhas.length; i++) {
    if (String(linhas[i][colVenda]).trim() === alvo) {
      aba.getRange(i + 1, colStatus + 1).setValue("expirado");
      aba.getRange(i + 1, colExp + 1).setValue(hoje);
      return { ok: true, mensagem: "Acesso bloqueado com sucesso" };
    }
  }

  return { ok: false, erro: "venda nao encontrada" };
}
