# AnthropoGuide — projeto e passagem de contexto para o Antigravity

**Data da consolidação:** 19/09/2026  
**Responsável pelo projeto:** Filipe Brito  
**Produto pretendido:** Gem do Google Gemini para alunos da certificação ISAK Nível 1.  
**Estado:** planejamento e triagem inicial das fontes; o Gem ainda não foi construído nem validado.

## 1. Objetivo e decisões já tomadas

O AnthropoGuide será um **guia e tutor** dos alunos da certificação ISAK Nível 1. Deve esclarecer dúvidas, contextualizar situações reais apresentadas pelos alunos e sugerir abordagens profissionais fundamentadas nas fontes curadas. O conteúdo abrange técnica antropométrica, qualidade da medida, equações, indicadores, pontos de corte, tabelas percentílicas, composição corporal e aplicações em saúde e esporte.

**Fronteira funcional definida pelo solicitante:** o Gem não deve executar a avaliação de um paciente a partir dos dados recebidos nem entregar uma decisão clínica pronta. Deve analisar o contexto, explicar as opções e suas limitações e orientar o profissional a escolher e aplicar o método adequado. Evitar solicitar ou reproduzir identificadores de pacientes; trabalhar com casos desidentificados.

**Prioridade de referências:** (1) evidência pertinente à população brasileira; (2) grandes estudos populacionais; (3) outras referências, explicitando diferenças de população e método. Quando o caso envolver atleta, apresentar, além da equação pertinente à população brasileira, equação validada em atletas preferencialmente da mesma modalidade ou com características físicas semelhantes. Explicitar que o profissional deve decidir qual das alternativas se aplica melhor à pessoa naquele momento; não declarar equivalência automática entre modelos.

**Estilo pretendido:** combinação de resposta didática e técnica, com raciocínio aplicado e referências rastreáveis. As interações típicas serão situações reais trazidas pelos alunos. O uso inicial será por meio de um Gem, na conta Google AI Pro do responsável; modalidade final de compartilhamento e permissões ainda requerem decisão após teste.

## 2. Especificação funcional proposta

Para cada pergunta de aplicação, a resposta deve, conforme o caso:

1. Resumir a questão e declarar dados contextuais faltantes que realmente mudam a escolha (idade, sexo quando exigido pela referência, condição clínica, modalidade, nível competitivo, protocolo de medidas, equipamento e objetivo).
2. Distinguir **medição ISAK**, cálculo, consulta de tabela e interpretação. Não inferir que uma medida isolada equivale a diagnóstico.
3. Oferecer as abordagens candidatas em ordem de adequação, com **fórmula exata, variáveis, unidades, população de desenvolvimento/validação, faixa etária, domínio de aplicação e limitações**, quando esses elementos estiverem conferidos na fonte original.
4. Ao citar percentis ou pontos de corte, informar tabela/edição, população, sexo, idade ou faixa, método e unidade. Se a célula numérica não tiver sido conferida visualmente, não fornecer o número; indicar a fonte e a pendência.
5. Em atletas, comparar explicitamente a referência brasileira e a referência esportiva específica, inclusive diferenças de modalidade e características físicas, sem escolher automaticamente pelo profissional.
6. Mostrar referência bibliográfica verificável e, se houver conflito entre fontes ou normas, explicar o conflito. Declarar incerteza quando faltar validação.
7. Encerrar com a próxima decisão prática que cabe ao profissional, sem transformar a resposta em laudo ou prescrição.

**Limite pedagógico:** o Gem pode explicar cálculos e exemplos hipotéticos, mas o fluxo para dados reais deve permanecer orientativo. A redação final das instruções deverá ser testada para impedir que ele passe a avaliar automaticamente perfis individuais.

## 3. Fontes e levantamento realizado

Foi feita **inspeção somente de leitura** das pastas abaixo. Contagens de arquivos locais incluem cópias, imagens, scripts, ambientes de execução e derivados; não são contagens de estudos únicos. Listagens do Drive com 100 itens podem estar incompletas.

### 3.1 Pastas locais

| Pasta | Verificação e função provável |
|---|---|
| `D:\Bases_de_conhecimento\Antropometria e ISAK` | Existe. Cerca de 4.002 arquivos, muitos de ambiente Python. Possui bases temáticas em Markdown/JSON, versões sucessivas de sínteses e planejamento N1. É apoio editorial e de localização de fontes, não prova primária de fórmulas ou limites. Selecionar sempre a versão vigente. |
| `D:\ISAK_Filipe_Instrutor` | Existe. Cerca de 1.406 arquivos, incluindo manual ISAK, Handbook 2026, slides oficiais restritos, artigos, aulas, roteiros e materiais N1. O planejamento `referencias\Antropometria e ISAK\ISAK Base de conhecimento\N1\TRILHA_ONLINE_DETALHADA_ISAK_N1_BLENDED_v1_3.md` é a versão encontrada, datada de 17/09/2026; a trilha prepara a prática presencial. Há material marcado para uso do instrutor e não distribuição. |
| `D:\Projetos\B160 — Antropometria em Nutrição — Desenvolvimento 2026.2\07_Fontes_Tecnicas_e_Referencias` | Existe. Cerca de 401 arquivos: sobretudo imagens de páginas, cinco PDFs e cinco extrações Markdown. Inclui Canda 2012, Manual ISAK, Mussoi 2014, Rossi 2015 e Frisancho 2008. É candidato para equações e percentis, sujeito a conferência numérica e direitos de uso. |
| `D:\ISAK_PROCESSAMENTO_ANTROPOMETRIA` | Existe. Cerca de 142 arquivos, sobretudo texto extraído. Relatório local indica processamento e classificação ainda incompletos. Usar para localizar originais. |
| `D:\ISAK_PROCESSAMENTO_ARTIGOS` | Existe. Dois textos extraídos sobre confiabilidade de medidas e comparação de adipômetros; originais não foram identificados nessa pasta. |
| `D:\ISAK_PROCESSAMENTO_ROBERTOCOSTA` | Existe. Cerca de 1.237 arquivos, principalmente texto extraído e metadados de um corpus maior. O relatório da primeira passagem declara validação científica individual pendente. **Contém arquivos de credenciais; nunca abrir, copiar, indexar nem enviar esses arquivos ao Gem.** |

Há **40 arquivos Markdown com mesmo caminho relativo e hash SHA-256 idêntico** na base de conhecimento e no espelho em `D:\ISAK_Filipe_Instrutor\referencias\Antropometria e ISAK`. Deduplicar antes de contar evidências.

**Ponto crítico — percentis:** a extração Markdown de Frisancho 2008 tem OCR e imagens de 53 páginas, mas as tabelas não foram preservadas como dados estruturados confiáveis. Números devem ser transcritos e revisados contra as páginas renderizadas; registrar página, cabeçalho, idade, sexo, unidade e conferência independente.

### 3.2 Pastas do Google Drive acessadas pela conexão autenticada

Conta identificada na conexão: `brito.o.filipe@gmail.com`. IDs e links abaixo identificam as pastas efetivamente inspecionadas. Evitar confundir pastas homônimas.

| Pasta | Link e estrutura observada |
|---|---|
| `G:\Meu Drive\ACERVO_COMPOSICAO_CORPORAL` | [Pasta principal](https://drive.google.com/drive/folders/1NwnTysWehVt4C8yLXS5AxYCiNo6-eqah). Filhas: `01_ARTIGOS_REFERENCIA` (fundamentos/modelos, antropometria/ISAK, BIA e DXA) e `02_MATERIAIS_DIDATICOS` (casos e slides). A listagem de fundamentos/modelos atingiu 100 itens e não constitui inventário completo. Existe outra pasta com o mesmo nome sob `Artigos para organização`; o ID deste registro é o da pasta na raiz do Meu Drive. |
| `G:\Meu Drive\ARTIGOS_NUTRICAO_CLINICA_E_ESPORTIVA` | [Pasta principal](https://drive.google.com/drive/folders/1HC0zS_BKpDx0S3vMvbcdK64HCMrZ3zb6). Filhas clínica, esportiva e transversal. A pasta esportiva apareceu vazia na inspeção; a transversal contém material sobre padrões metodológicos de composição corporal. |
| `G:\Meu Drive\Vigilância Semanal - ChatGPT\Antropometria e Composição Corporal` | [Pasta temática](https://drive.google.com/drive/folders/1Z3C4Y5pqjv_O-zYhUvoK_HhJqBwU6PAn). Há temas como valores de referência/curvas normativas, técnicas, métodos, esporte e somatotipo; PDFs e sínteses em Google Docs. A pasta esportiva atingiu o limite de 100 itens. Relatórios de vigilância e sínteses são **pistas bibliográficas**, não substitutos da publicação original. |

Exemplos localizados no Drive para a etapa de curadoria: Costa 2001, Pitanga 2011, Perini 2005, Cyrino 2013, Silva 2003 (fisiculturistas brasileiros), Must 1991, Frisancho 1981, curvas CDC 2000, Janssen 2004 e trabalhos sobre atletas. **A presença de um arquivo não confirma, por si, pertinência, exatidão de valores ou permissão de redistribuição.**

## 4. Hierarquia de evidência e controle de procedência

Manter quatro camadas separadas:

1. **Norma/protocolo ISAK vigente:** medidas, técnica, qualidade e limites próprios da certificação. Confirmar edição, validade e escopo N1 antes de incorporar.
2. **Publicações originais:** equações, estudos de validação, estudos populacionais e tabelas. Conferir PDF/versão editorial e registrar DOI ou URL de origem.
3. **Sínteses didáticas e bases temáticas:** úteis para orientar a leitura, sempre confrontadas com as camadas 1–2 antes de virar regra ou valor numérico.
4. **OCR, extrações e vigilância:** índices de busca e candidatos para curadoria. Não usar como fonte normativa ou numérica sem conferência do original.

Para cada item candidato, registrar no mínimo: ID, título, autores, ano, DOI/URL, caminho local ou Drive, tipo de fonte, edição, população, amostra, idade, sexo, modalidade, protocolo/instrumento, variável de desfecho, fórmula/unidades ou tabela/página, validação, limites de aplicação, conflitos, status da conferência e direitos de uso. Separar **texto comprovado pela fonte, inferência científica e decisão pedagógica**.

## 5. Direitos, privacidade e compartilhamento

- Não carregar o acervo inteiro no Gem. Selecionar apenas fontes necessárias, legíveis, verificadas e cuja inclusão em um Gem compartilhado seja permitida.
- Um `LEIA-ME` em `N1\Materiais_Complementares\Macroaula_02` distingue leituras entregáveis de dois artigos com aviso de copyright destinados somente ao instrutor. Essa classificação local é uma pista; verificar licença e condições de cada documento, inclusive livros e manual ISAK.
- O uso anterior do Manual ISAK 2019 foi delimitado a materiais didáticos internos dos cursos de certificação; não presumir que isso autorize incluir o PDF integral em um Gem compartilhado. OCR e imagens derivadas preservam essa restrição até análise de direitos.
- Antes de compartilhar, revisar as opções atuais do Gemini: público autorizado, visibilidade de instruções e arquivos, políticas da conta Google AI Pro, limites de arquivos e retenção de dados. Referência a reconfirmar: [Ajuda oficial sobre compartilhamento de Gems](https://support.google.com/gemini/answer/16504957).
- Os alunos devem enviar casos **sem nome, contato, documento, data exata ou outros identificadores**. Definir aviso de privacidade e procedimento para remover dados incidentais.

## 6. Plano de construção e validação

### Fase A — inventário e deduplicação

Completar a listagem das pastas do Drive que atingiram 100 itens; consolidar arquivos locais e Drive; localizar originais correspondentes aos TXT/OCR; identificar versões, duplicatas e fontes restritas. Produzir uma planilha ou CSV de rastreabilidade sem copiar credenciais.

### Fase B — curadoria temática

Priorizar: (1) protocolo e qualidade da medida ISAK N1; (2) equações brasileiras e suas populações; (3) equações esportivas por modalidade; (4) referências populacionais e percentis; (5) indicadores/pontos de corte; (6) métodos complementares de composição corporal. Não transformar documentos de planejamento ou slides em autoridade normativa quando divergem do original.

### Fase C — base de conhecimento do Gem

Preparar arquivos temáticos curtos, versionados e rastreáveis, em vez de um acervo bruto. Sugestão de módulos: `01_escopo_e_protocolo_isak`, `02_qualidade_da_medida`, `03_equacoes_brasileiras`, `04_equacoes_atletas`, `05_percentis_e_referencias`, `06_indicadores_e_cortes`, `07_metodos_e_limitacoes`, `08_bibliografia_e_procedencia`. Incluir somente números conferidos e conteúdo autorizado.

### Fase D — instruções e testes do Gem

Redigir instruções com função, limites, prioridade de fontes, formato de resposta, tratamento de dúvida e recusa de cálculo/avaliação individual automática. Testar casos: adulto brasileiro, adolescente com percentis, atleta de modalidade com e sem equação específica, perfil fora da população de validação, fonte conflitante, tabela OCR ambígua e caso com dados pessoais. Conferir cada resposta contra a fonte e registrar falhas/correções.

### Fase E — piloto e disponibilização

Realizar piloto privado com casos simulados/desidentificados, revisar licenças e controles de compartilhamento, definir público e instrução de uso aos alunos; só então disponibilizar o Gem. Registrar versão das instruções e da base de conhecimento para permitir revisão periódica.

## 7. Pendências e próximo passo imediato no Antigravity

1. Confirmar que este documento e os caminhos continuam atuais; não assumir que a triagem é uma auditoria exaustiva.
2. Reconfirmar na documentação oficial do Google as capacidades e limites **atuais** de Gems e compartilhamento antes da implementação.
3. Criar o inventário estruturado das fontes, começando por manual/protocolo ISAK e equações/tabelas mais usadas no N1; documentar direitos por item.
4. Conferir numericamente percentis e equações nos originais, com pelo menos uma checagem independente para fórmulas e tabelas críticas.
5. Propor ao responsável uma primeira seleção de fontes e a minuta das instruções do Gem para revisão. Ainda não houve autorização para publicar ou compartilhar um Gem.

## 8. Estado desta passagem

Confirmado: pastas locais existem; três pastas indicadas do Drive foram acessadas pela conexão autenticada; há espelhos/derivados, fontes originais e materiais restritos; a extração de tabelas percentílicas requer validação visual.  
Inferência de projeto: arquitetura modular da base, sequência de curadoria e casos de teste acima.  
Pendente: curadoria artigo a artigo, conferência de valores, revisão de direitos, instruções finais, criação, testes e compartilhamento do Gem.

**Nenhum arquivo de origem foi alterado, carregado no Gem ou compartilhado nesta triagem.**
