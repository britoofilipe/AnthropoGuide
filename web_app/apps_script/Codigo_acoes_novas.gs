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
