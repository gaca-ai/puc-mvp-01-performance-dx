# Catálogo de dados

Gerado do `information_schema` do catálogo `mvp_aneel` no Unity Catalog pelo notebook `05_catalogo_dados`. As descrições são os comentários gravados por cada notebook ao criar a tabela.

## Tabelas

| Camada | Tabela | Linhas | Descrição |
|---|---|---:|---|
| Bronze | `_ingestion_log` | 14 | Tabela de controle da ingestão: uma linha por recurso baixado, com conjunto, licença, URL de origem, tamanho, data de atualização e tabela de destino. Fonte: Tabela própria deste trabalho. |
| Bronze | `commercial_quality` | 1.493.698 | Este conjunto de dados expressa a lista de Agentes regulados pela ANEEL com dados do CNPJ, sigla do indicador por ano e periodicidade dos dados de valores enviados para o índice. Fonte: dm-qualidade-do-atendimento-comercial.pdf, versão 1.0 (17/8/2022). |
| Bronze | `complaints` | 29.263.282 | Relação das manifestações dos consumidores em relação à distribuidora, por município, canal de atendimento e tipologia, no 1º nível (SAC) e no 2º nível (Ouvidoria) de atendimento. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| Bronze | `continuity_indicators` | 5.108.332 | O conjunto de dados apresenta valores apurados dos indicadores coletivos de continuidade DEC (Duração Equivalente de Interrupção por Unidade Consumidora), expresso em horas e centésimos de horas, e FEC (Frequência Equivalente de Interrupção por Unidade Consumidora), expresso em número de interrupções e centésimos do número de interrupções. Também são fornecidas as parcelas desagregadas dos indicadores. Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| Bronze | `emergency_occurrences_v1` | 36.390.229 | Registro de ocorrências emergenciais contendo informações relativas à data/hora de abertura e encerramento, ao conjunto elétrico afetado, aos tempos de preparação, deslocamento e execução do atendimento, bem como aos dados relacionados ao fato gerador e demais informações correlatas. Arquivos de 2023 a 2025. Fonte: dm-ocorrencias-emergenciais-nas-redes-de-distribuicao.pdf, versão 1.1 (28/07/2026). |
| Bronze | `emergency_occurrences_v2` | 6.789.484 | Registro de ocorrências emergenciais contendo informações relativas à data/hora de abertura e encerramento, ao conjunto elétrico afetado, aos tempos de preparação, deslocamento e execução do atendimento, bem como aos dados relacionados ao fato gerador e demais informações correlatas. Arquivo de 2026, publicado com leiaute diferente dos anos anteriores. Fonte: dm-ocorrencias-emergenciais-nas-redes-de-distribuicao.pdf, versão 1.1 (28/07/2026). |
| Bronze | `indger_commercial` | 267.550 | Relação, por mês, dos dados relacionados a aspectos comerciais (faturamento, danos elétricos, atendimento), informados pelas distribuidoras na base de dados INDGER2, segregados por município. Fonte: dm-indger-dados-comerciais.pdf, versão 1.0 (13/12/2023). |
| Bronze | `indger_commercial_services` | 23.922.861 | Relação, por mês, dos dados relacionados a aspectos dos serviços comerciais (quantidades, prazos, estoques, compensações), informados pelas distribuidoras na base de dados INDGER2, segregados por município. Fonte: dm-indger-dados-de-servicos-comerciais.pdf, versão 1.0 (13/12/2023). |
| Bronze | `pdd_investment` | 5.484 | Plano de Desenvolvimento da Distribuição (PDD): investimentos das distribuidoras por CNPJ, UF, ano e tipo de obra, como publicados pela ANEEL. Fonte: Sem dicionário da ANEEL no repositório; descrição própria. |
| Bronze | `voltage_conformity` | 5.506.240 | Informações anuais de índices de pagamento por determinado período em meses para Unidades Consumidoras a partir de agentes de distribuição. Fonte: dm-indicadores-de-conformidade-de-nivel-de-tensao.pdf, versão 1.1 (27/6/2025). |
| Silver | `controle_anomalias_manifestacao` | 5.940 | Teste de meses anomalos das reclamacoes por distribuidora de grande porte, nivel, bloco      e mes. Evidencia da imputacao do comercial estrito no nivel 1 e sinalizador dos demais      blocos e do nivel 2. |
| Silver | `dim_conjunto` | 3.980 | Conjuntos de unidades consumidoras, com o nome publicado e o periodo de      existencia na serie. O codigo e a identidade; o nome e apenas descritivo. |
| Silver | `dim_distribuidora` | 105 | Dimensao conformada das distribuidoras, compartilhada por todas as metricas do      trabalho. Carrega o criterio de porte como atributo; o recorte do universo e      aplicado na Gold pela flag grande_porte, nao por filtro nesta tabela. |
| Silver | `dim_tempo` | 30 | Dimensao de tempo mensal da Silver de reclamacoes, de janeiro de 2024 a junho de 2026.      Marca os fins de janela do acompanhamento semestral. |
| Silver | `dim_tipologia` | 132 | Dimensao de tipologias de manifestacao conforme Anexo I da REH 2.992/2021. Carrega a      hierarquia de tres niveis e os recortes usados nos rankings como atributos; a Silver      e a Gold apenas filtram por eles. |
| Silver | `exclusao_ranking_manifestacao` | 1 | Distribuidoras excluidas do ranking de reclamacoes por qualidade insuficiente do dado,      com motivo e evidencia. A Silver mantem as linhas; a Gold aplica a exclusao. |
| Silver | `fato_continuidade_mensal` | 247.261 | Indicadores coletivos de continuidade no grao conjunto-ano-mes, tipados,      deduplicados e com DEC e FEC compostos a partir das parcelas. Preserva a serie      inteira publicada pela ANEEL, sem filtro de janela nem de universo. |
| Silver | `fato_manifestacao` | 135.486 | Reclamacoes detalhadas da familia 102 da REH 2.992/2021 no grao CNPJ, tipologia, nivel      e mes, de janeiro de 2024 a junho de 2026. Guarda o valor usado e o publicado lado a      lado; o universo de distribuidoras e aplicado na Gold. |
| Silver | `recon_continuidade` | 494.392 | Conferencia entre o indicador composto pelas parcelas e o consolidado publicado      pela ANEEL, restrita as combinacoes em que o consolidado existe. Evidencia do      criterio de qualidade, nao insumo de calculo. |
| Gold | `continuidade_janela` | 132 | DEC-FI e FEC-FI por distribuidora de grande porte em janelas moveis de 12 meses, pelas Equacoes 41 a 46 do PRODIST Modulo 8, alinhados as janelas das reclamacoes. |
| Gold | `fato_continuidade_anual` | 132 | Indicador anual da distribuidora pelas Equacoes 44 a 46 do PRODIST Modulo 8, com denominador igual a media mensal do universo. Traz ao lado a soma simples dos meses, para dimensionar a distorcao da simplificacao corrente de mercado. |
| Gold | `fato_continuidade_global_mensal` | 1.584 | Indicador de continuidade da distribuidora no grao mensal, agregado dos conjuntos pelas Equacoes 41 a 43 do PRODIST Modulo 8. Restrito as distribuidoras de grande porte e aos anos civis completos. |
| Gold | `fato_reclamacao_janela` | 792 | Reclamacoes do nivel 1 em janelas moveis de 12 meses por distribuidora de grande porte e recorte, com indicadores por mil UCs e taxa de procedencia. Mantem as distribuidoras excluidas do ranking, sinalizadas. |
| Gold | `ranking_continuidade` | 64 | Ranking de variacao do DEC-FI e do FEC-FI entre as mesmas janelas das reclamacoes, no mesmo conjunto de distribuidoras do ranking de Qualidade. |
| Gold | `ranking_evolucao` | 33 | Evolucao da continuidade entre o primeiro e o ultimo ano da janela, por distribuidora de grande porte. Reducao do DEC-FI indica melhora. |
| Gold | `ranking_reclamacoes` | 382 | Rankings de variacao das reclamacoes por mil UCs entre a primeira e a ultima janela, por recorte e medida. Posicao 1 e a maior reducao; inclui a sensibilidade sem imputacao. |

## Bronze

### `bronze.complaints`

Relação das manifestações dos consumidores em relação à distribuidora, por município, canal de atendimento e tipologia, no 1º nível (SAC) e no 2º nível (Ouvidoria) de atendimento. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026).

| Coluna | Tipo | Descrição |
|---|---|---|
| `DatGeracaoConjuntoDados` | `string` | Data do processamento de carga automática no momento da geração para publicação do conjunto de dados abertos. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `DatReferencia` | `string` | Data de referência do envio das informações pela distribuidora à ANEEL. Os dados reportados referem-se às manifestações ocorridas no período de competência indicado pelos campos AnoCompetencia e MesCompetencia. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `SigAgente` | `string` | Sigla da distribuidora de energia elétrica regulada pela ANEEL. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `NumCPFCNPJ` | `string` | Número de inscrição da distribuidora no Cadastro Nacional da Pessoa Jurídica (CNPJ). Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `CodMunicipio` | `string` | Código do município, de acordo com o cadastro do IBGE, relacionado à manifestação do consumidor. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `NomMunicipio` | `string` | Nome do município, de acordo com o cadastro do IBGE, relacionado à manifestação do consumidor. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `SigUF` | `string` | Sigla da Unidade da Federação (UF) associada ao município da manifestação. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `SigRegiao` | `string` | Sigla da Região Geográfica do Brasil associada ao município da manifestação. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `NomClassificacaoAgente` | `string` | Classificação da distribuidora de energia elétrica. Pode assumir os valores Concessionária ou Permissionária. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `CodTipoManifestacao` | `string` | Código identificador da tipologia da manifestação (com até 7 dígitos). Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `NomCanalManifestacao` | `string` | Nível de atendimento em que a manifestação foi registrada: Nível 1 (SAC) ou Nível 2 (Ouvidoria). Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `DscManifestacao` | `string` | Descrição da tipologia da manifestação do consumidor associada aos identificadores informados nos campos CodTipoReclamacao e IdeTipoRCA. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `QtdManifestacoesRecebidas` | `string` | Quantidade de manifestações, do SAC ou da Ouvidoria, recebidas na referência apurada. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `QtdManifestacoesImprocedentes` | `string` | Quantidade de manifestações do SAC ou da Ouvidoria solucionadas e encerradas como improcedentes na referência apurada. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `QtdManifestacoesProcedentes` | `string` | Quantidade de manifestações do SAC ou da Ouvidoria solucionadas e encerradas como procedentes na referência apurada. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `NumPrazoMedioSolucao` | `string` | Prazo médio, em dias, para solução das manifestações procedentes registradas nos canais de atendimento da distribuidora. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `DscFormaContato` | `string` | Forma de contato utilizada pelo consumidor para registrar a manifestação (ex.: telefone, internet, presencial etc.). Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `NumSacPrazoMedioSolucaoImproc` | `string` | Prazo médio, em dias, para solução das manifestações improcedentes registradas no SAC (Serviço de Atendimento ao Cliente). Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `NumOuvPrazoMedioSolucaoImproc` | `string` | Prazo médio, em dias, para solução das manifestações improcedentes registradas na Ouvidoria. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `IdeTipoRCA` | `string` | Identificador da tipologia da manifestação do consumidor utilizado na estrutura atual do sistema. Corresponde à evolução do campo CodTipoReclamacao. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `AnoCompetencia` | `string` | Ano de competência das manifestações dos consumidores registradas no conjunto de dados. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `MesCompetencia` | `string` | Mês de competência das manifestações dos consumidores registradas no conjunto de dados. Fonte: dm-manifestacoes-nos-1-e-2-niveis-da-distribuidora.pdf, versão 1.2 (30/07/2026). |
| `_source_file` | `string` | Nome do arquivo de origem no volume de landing. Fonte: Linhagem própria deste trabalho, gravada na ingestão. |
| `_ingested_at` | `timestamp` | Momento da ingestão, em UTC, comum a todas as linhas da mesma execução. Fonte: Linhagem própria deste trabalho, gravada na ingestão. |

### `bronze.continuity_indicators`

O conjunto de dados apresenta valores apurados dos indicadores coletivos de continuidade DEC (Duração Equivalente de Interrupção por Unidade Consumidora), expresso em horas e centésimos de horas, e FEC (Frequência Equivalente de Interrupção por Unidade Consumidora), expresso em número de interrupções e centésimos do número de interrupções. Também são fornecidas as parcelas desagregadas dos indicadores. Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022).

| Coluna | Tipo | Descrição |
|---|---|---|
| `DatGeracaoConjuntoDados` | `date` | Data do processamento de carga automática no momento da geração para publicação do conjunto de dados abertos. Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| `IdeConjUndConsumidoras` | `bigint` | Identificador do Conjunto de Unidades Consumidoras. Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| `DscConjUndConsumidoras` | `string` | Descrição do Conjunto de Unidades Consumidoras Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| `SigAgente` | `string` | Sigla que abrevia o nome dos Agentes regulados pela ANEEL Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| `NumCNPJ` | `bigint` | CNPJ do Agente do setor elétrico conforme cadastro de agentes da ANEEL Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| `SigIndicador` | `string` | Sigla do Tipo de Indicador. As siglas e descrições completas estão no arquivo dominio-indicadores.csv, versionado em data/reference/dominio_indicadores_aneel.csv. Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| `AnoIndice` | `bigint` | Ano de competência do índice. Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| `NumPeriodoIndice` | `bigint` | Período do índice expressado em meses. Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| `VlrIndiceEnviado` | `double` | Valor do índice enviado. Fonte: dm-indicadores-continuidade.pdf, versão 1.0 (6/6/2022). |
| `_source_file` | `string` | Nome do arquivo de origem no volume de landing. Fonte: Linhagem própria deste trabalho, gravada na ingestão. |
| `_ingested_at` | `timestamp` | Momento da ingestão, em UTC, comum a todas as linhas da mesma execução. Fonte: Linhagem própria deste trabalho, gravada na ingestão. |

## Silver

### `silver.controle_anomalias_manifestacao`

Teste de meses anomalos das reclamacoes por distribuidora de grande porte, nivel, bloco      e mes. Evidencia da imputacao do comercial estrito no nivel 1 e sinalizador dos demais      blocos e do nivel 2.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora de grande porte |
| `nivel` | `int` | Nivel de atendimento: 1 (central de atendimento) ou 2 (ouvidoria) |
| `bloco` | `string` | Bloco da dim_tipologia: comercial_estrito, rede_e_qualidade_outros ou tecnico |
| `ano_mes` | `int` | Ano e mes de competencia no formato AAAAMM |
| `qtd_recebidas` | `bigint` | Total publicado de recebidas no bloco e mes; zero quando nada foi publicado |
| `qtd_procedentes` | `bigint` | Total publicado de procedentes no bloco e mes; zero quando nada foi publicado |
| `qtd_improcedentes` | `bigint` | Total publicado de improcedentes no bloco e mes; zero quando nada foi publicado |
| `med_local_recebidas` | `double` | Mediana de recebidas nos 3 meses anteriores e 3 seguintes do mesmo bloco |
| `med_serie_recebidas` | `double` | Mediana de recebidas nos 30 meses da serie do mesmo bloco |
| `med_seguinte_recebidas` | `double` | Mediana de recebidas nos ate 3 meses seguintes; confirma salto persistente |
| `anomalo_local_recebidas` | `boolean` | Verdadeiro quando recebidas fica fora de 40 a 250 por cento da mediana local sem persistir nos meses seguintes |
| `anomalo_serie_recebidas` | `boolean` | Verdadeiro quando recebidas fica abaixo de 20 por cento da mediana da serie |
| `med_local_procedentes` | `double` | Mediana de procedentes nos 3 meses anteriores e 3 seguintes do mesmo bloco |
| `med_serie_procedentes` | `double` | Mediana de procedentes nos 30 meses da serie do mesmo bloco |
| `med_seguinte_procedentes` | `double` | Mediana de procedentes nos ate 3 meses seguintes; confirma salto persistente |
| `anomalo_local_procedentes` | `boolean` | Verdadeiro quando procedentes fica fora de 40 a 250 por cento da mediana local sem persistir nos meses seguintes |
| `anomalo_serie_procedentes` | `boolean` | Verdadeiro quando procedentes fica abaixo de 20 por cento da mediana da serie |
| `med_local_improcedentes` | `double` | Mediana de improcedentes nos 3 meses anteriores e 3 seguintes do mesmo bloco |
| `med_serie_improcedentes` | `double` | Mediana de improcedentes nos 30 meses da serie do mesmo bloco |
| `med_seguinte_improcedentes` | `double` | Mediana de improcedentes nos ate 3 meses seguintes; confirma salto persistente |
| `anomalo_local_improcedentes` | `boolean` | Verdadeiro quando improcedentes fica fora de 40 a 250 por cento da mediana local sem persistir nos meses seguintes |
| `anomalo_serie_improcedentes` | `boolean` | Verdadeiro quando improcedentes fica abaixo de 20 por cento da mediana da serie |
| `mes_anomalo` | `boolean` | Verdadeiro quando alguma medida falha no teste local ou no teste da serie |
| `meses_vizinhos_validos` | `bigint` | Meses vizinhos nao anomalos usados na imputacao; nulo quando o mes nao foi imputado |
| `imputado` | `boolean` | Verdadeiro quando o mes e imputavel e teve ao menos um vizinho valido |
| `imputavel` | `boolean` | Verdadeiro quando o mes e anomalo, do nivel 1, de bloco sujeito a imputacao e anterior ao ultimo mes da serie |

### `silver.dim_conjunto`

Conjuntos de unidades consumidoras, com o nome publicado e o periodo de      existencia na serie. O codigo e a identidade; o nome e apenas descritivo.

| Coluna | Tipo | Descrição |
|---|---|---|
| `ide_conjunto` | `string` | Codigo do conjunto de unidades consumidoras, texto de 5 caracteres |
| `num_cnpj` | `string` | CNPJ da distribuidora responsavel pelo conjunto |
| `dsc_conjunto` | `string` | Nome do conjunto conforme publicado pela ANEEL |
| `primeiro_mes` | `string` | Primeiro mes em que o conjunto aparece na serie, no formato AAAA-MM |
| `ultimo_mes` | `string` | Ultimo mes em que o conjunto aparece na serie, no formato AAAA-MM |
| `meses_na_serie` | `bigint` | Quantidade de meses em que o conjunto foi informado |

### `silver.dim_distribuidora`

Dimensao conformada das distribuidoras, compartilhada por todas as metricas do      trabalho. Carrega o criterio de porte como atributo; o recorte do universo e      aplicado na Gold pela flag grande_porte, nao por filtro nesta tabela.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres com zeros a esquerda |
| `sig_agente` | `string` | Sigla da distribuidora conforme publicada pela ANEEL |
| `qtd_ucs_dezembro` | `double` | Soma de NumCon dos conjuntos em dezembro do ano de referencia |
| `qtd_ucs_media` | `bigint` | Media mensal da soma de NumCon no ano de referencia |
| `grande_porte` | `boolean` | Verdadeiro quando qtd_ucs_dezembro atinge o corte de 400 mil UCs |
| `grande_porte_media` | `boolean` | Mesmo corte aplicado a qtd_ucs_media, como sensibilidade |
| `fronteira` | `boolean` | Verdadeiro quando os dois criterios discordam sobre o porte |
| `ano_referencia` | `int` | Ano civil usado para medir o porte |

### `silver.dim_tempo`

Dimensao de tempo mensal da Silver de reclamacoes, de janeiro de 2024 a junho de 2026.      Marca os fins de janela do acompanhamento semestral.

| Coluna | Tipo | Descrição |
|---|---|---|
| `ano_mes` | `int` | Ano e mes de competencia no formato AAAAMM, chave da dimensao |
| `ano` | `int` | Ano de competencia |
| `mes` | `int` | Mes de competencia, de 1 a 12 |
| `data_inicio_mes` | `date` | Primeiro dia do mes de competencia |
| `semestre` | `int` | Semestre do ano: 1 (janeiro a junho) ou 2 (julho a dezembro) |
| `ind_fim_janela` | `boolean` | Verdadeiro em junho e dezembro, meses em que termina uma janela movel de 12 meses do acompanhamento semestral |

### `silver.dim_tipologia`

Dimensao de tipologias de manifestacao conforme Anexo I da REH 2.992/2021. Carrega a      hierarquia de tres niveis e os recortes usados nos rankings como atributos; a Silver      e a Gold apenas filtram por eles.

| Coluna | Tipo | Descrição |
|---|---|---|
| `cod_tipologia` | `string` | Codigo da tipologia conforme Anexo I da REH 2.992/2021, texto |
| `descricao` | `string` | Descricao da tipologia conforme publicada no Anexo I da REH 2.992/2021 |
| `nivel` | `int` | Nivel na hierarquia da REH: 1 (familia), 2 (grupo) ou 3 (tipologia) |
| `cod_pai` | `string` | Codigo imediatamente superior na hierarquia; nulo no nivel 1 |
| `cod_nivel_1` | `string` | Codigo da familia (nivel 1) a que a tipologia pertence |
| `desc_nivel_1` | `string` | Descricao da familia (nivel 1) |
| `cod_nivel_2` | `string` | Codigo do grupo (nivel 2) a que a tipologia pertence; nulo no nivel 1 |
| `desc_nivel_2` | `string` | Descricao do grupo (nivel 2); nulo no nivel 1 |
| `ind_subtotal` | `boolean` | Verdadeiro quando o codigo tem filhos na REH; linha de subtotal, fora de toda contagem |
| `ind_fer_item285` | `boolean` | Verdadeiro para reclamacao detalhada que entra no FER pela regra do PRODIST Modulo 8, item 285 |
| `ind_comercial_estrito` | `boolean` | Recorte do item 285 sem Rede e Manutencao (10212) e Outros de Qualidade (1020999) |
| `bloco` | `string` | Agrupamento para deteccao de meses anomalos e analise: comercial_estrito, rede_e_qualidade_outros, tecnico ou fora_da_familia_102 |
| `grupo_ranking` | `string` | Recorte do ranking: faturamento (10204), pagamento (10206), geracao_distribuida (10213) ou outras_comerciais no comercial estrito, e qualidade (10209); nulo fora dos rankings |

### `silver.exclusao_ranking_manifestacao`

Distribuidoras excluidas do ranking de reclamacoes por qualidade insuficiente do dado,      com motivo e evidencia. A Silver mantem as linhas; a Gold aplica a exclusao.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora excluida do ranking de reclamacoes |
| `motivo` | `string` | Motivo da exclusao, registrado na decisao metodologica |
| `meses_procedentes_acima_recebidas` | `int` | Evidencia: meses do comercial estrito do nivel 1 com procedentes acima de recebidas |

### `silver.fato_continuidade_mensal`

Indicadores coletivos de continuidade no grao conjunto-ano-mes, tipados,      deduplicados e com DEC e FEC compostos a partir das parcelas. Preserva a serie      inteira publicada pela ANEEL, sem filtro de janela nem de universo.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres com zeros a esquerda |
| `ide_conjunto` | `string` | Codigo do conjunto de unidades consumidoras, texto de 5 caracteres |
| `ano` | `int` | Ano civil de apuracao do indicador |
| `mes` | `int` | Mes civil de apuracao, de 1 a 12 |
| `regime` | `string` | Regime de composicao vigente no ano: ate_2021 ou desde_2022 |
| `DECINC` | `double` | Parcela publicada pela ANEEL: DEC de interrup. origem interna ao Sist. de Dist. não progr. e ocor. Dia Crítico |
| `DECIND` | `double` | Parcela publicada pela ANEEL: DEC interrup origem interna, não programada e não expurgavel |
| `DECINE` | `double` | Parcela publicada pela ANEEL: DEC interrup. origem interna, não progr. e ocor. Sit. Emerg, n ocor critico. |
| `DECINO` | `double` | Parcela publicada pela ANEEL: DEC interrup. origem interna não progr. Racionamento e ONS, n ocor dia critico. |
| `DECIP` | `double` | Parcela publicada pela ANEEL: DEC de interrupção de origem interna ao Sist. de Dist. e programada |
| `DECIPC` | `double` | Parcela publicada pela ANEEL: DEC interrup. origem inter. ao sist distr, prog. e ocorr. em dia crítico |
| `DECXN` | `double` | Parcela publicada pela ANEEL: DEC de interrupção de origem externa ao Sist. de Dist. e não programada |
| `DECXNC` | `double` | Parcela publicada pela ANEEL: DEC interrup. origem ext. ao sist distr, não prog. e ocorr. em dia crítico |
| `DECXP` | `double` | Parcela publicada pela ANEEL: DEC de interrupção de origem externa ao Sist. de Dist. e programada |
| `DECXPC` | `double` | Parcela publicada pela ANEEL: DEC interrup. origem ext. ao sist distr, prog. e ocorr. em dia crítico |
| `FECINC` | `double` | Parcela publicada pela ANEEL: FEC de interrup. origem interna ao Sist. de Dist. não progr. e ocor. Dia Crítico |
| `FECIND` | `double` | Parcela publicada pela ANEEL: FEC interrup origem interna, não programada e não expurgavel |
| `FECINE` | `double` | Parcela publicada pela ANEEL: FEC interrup. origem interna, não progr. e ocor. Sit. Emerg, n ocor critico. |
| `FECINO` | `double` | Parcela publicada pela ANEEL: FEC interrup. origem interna não progr. Racionamento e ONS, n ocor dia critico. |
| `FECIP` | `double` | Parcela publicada pela ANEEL: FEC de interrupção de origem interna ao Sist. de Dist. e programada |
| `FECIPC` | `double` | Parcela publicada pela ANEEL: FEC interrup. origem inter. ao sist distr, prog. e ocorr. em dia crítico |
| `FECXN` | `double` | Parcela publicada pela ANEEL: FEC de interrupção de origem externa ao Sist. de Dist. e não programada |
| `FECXNC` | `double` | Parcela publicada pela ANEEL: FEC interrup. origem ext. ao sist distr, não prog. e ocorr. em dia crítico |
| `FECXP` | `double` | Parcela publicada pela ANEEL: FEC de interrupção de origem externa ao Sist. de Dist. e programada |
| `FECXPC` | `double` | Parcela publicada pela ANEEL: FEC interrup. origem ext. ao sist distr, prog. e ocorr. em dia crítico |
| `num_con` | `double` | Numero de unidades consumidoras do conjunto no mes; peso da media ponderada |
| `dec` | `double` | DEC composto pelas parcelas do regime vigente, conforme PRODIST Modulo 8 |
| `fec` | `double` | FEC composto pelas parcelas do regime vigente, conforme PRODIST Modulo 8 |
| `dec_fi` | `double` | DEC de falha interna: soma de IND, INE e INC; indicador proprio deste trabalho |
| `fec_fi` | `double` | FEC de falha interna: soma de IND, INE e INC; indicador proprio deste trabalho |
| `meses_no_ano` | `bigint` | Meses distintos enviados pela distribuidora no ano civil |
| `ano_completo` | `boolean` | Verdadeiro quando a distribuidora enviou os doze meses do ano |

### `silver.fato_manifestacao`

Reclamacoes detalhadas da familia 102 da REH 2.992/2021 no grao CNPJ, tipologia, nivel      e mes, de janeiro de 2024 a junho de 2026. Guarda o valor usado e o publicado lado a      lado; o universo de distribuidoras e aplicado na Gold.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres com zeros a esquerda |
| `cod_tipologia` | `string` | Codigo da tipologia conforme Anexo I da REH 2.992/2021; apenas reclamacoes detalhadas da familia 102 |
| `nivel` | `int` | Nivel de atendimento: 1 (central de atendimento) ou 2 (ouvidoria da distribuidora) |
| `ano_mes` | `int` | Ano e mes de competencia no formato AAAAMM |
| `qtd_recebidas` | `bigint` | Manifestacoes recebidas usadas no calculo: imputadas no mes imputado, publicadas nos demais |
| `qtd_procedentes` | `bigint` | Reclamacoes procedentes usadas no calculo: imputadas no mes imputado, publicadas nos demais |
| `qtd_improcedentes` | `bigint` | Reclamacoes improcedentes usadas no calculo: imputadas no mes imputado, publicadas nos demais |
| `qtd_recebidas_publicada` | `bigint` | Manifestacoes recebidas conforme publicadas pela ANEEL, somadas no grao do fato |
| `qtd_procedentes_publicada` | `bigint` | Reclamacoes procedentes conforme publicadas pela ANEEL, somadas no grao do fato |
| `qtd_improcedentes_publicada` | `bigint` | Reclamacoes improcedentes conforme publicadas pela ANEEL, somadas no grao do fato |
| `imputado` | `boolean` | Verdadeiro quando a linha pertence a mes anomalo imputado (comercial estrito, nivel 1) |

### `silver.recon_continuidade`

Conferencia entre o indicador composto pelas parcelas e o consolidado publicado      pela ANEEL, restrita as combinacoes em que o consolidado existe. Evidencia do      criterio de qualidade, nao insumo de calculo.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres com zeros a esquerda |
| `ide_conjunto` | `string` | Codigo do conjunto de unidades consumidoras, texto de 5 caracteres |
| `ano` | `int` | Ano civil de apuracao |
| `mes` | `int` | Mes civil de apuracao, de 1 a 12 |
| `indicador` | `string` | DEC ou FEC |
| `publicado` | `double` | Valor consolidado publicado pela ANEEL para o indicador |
| `composto` | `double` | Valor obtido pela soma das parcelas do regime vigente |
| `diferenca` | `double` | Composto menos publicado |
| `adere` | `boolean` | Verdadeiro quando a diferenca absoluta nao excede a tolerancia de arredondamento |

## Gold

### `gold.continuidade_janela`

DEC-FI e FEC-FI por distribuidora de grande porte em janelas moveis de 12 meses, pelas Equacoes 41 a 46 do PRODIST Modulo 8, alinhados as janelas das reclamacoes.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres |
| `fim_janela` | `int` | Ultimo mes da janela de 12 meses, formato AAAAMM |
| `meses` | `bigint` | Meses com indicador na janela |
| `janela_valida` | `boolean` | Verdadeiro quando a janela tem 12 meses |
| `nuc_media` | `bigint` | Media mensal do universo de UCs na janela (Eq. 46) |
| `dec_fi` | `double` | DEC de falha interna na janela, em horas |
| `fec_fi` | `double` | FEC de falha interna na janela, em interrupcoes |

### `gold.fato_continuidade_anual`

Indicador anual da distribuidora pelas Equacoes 44 a 46 do PRODIST Modulo 8, com denominador igual a media mensal do universo. Traz ao lado a soma simples dos meses, para dimensionar a distorcao da simplificacao corrente de mercado.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres |
| `sig_agente` | `string` | Sigla da distribuidora conforme publicada pela ANEEL |
| `ano` | `int` | Ano civil de apuracao |
| `meses` | `bigint` | Meses que compoem o ano; doze quando o ano esta completo |
| `nuc_gk` | `bigint` | Media mensal das unidades consumidoras no ano (Eq. 46) |
| `dec` | `double` | DEC normativo anual, duas casas decimais |
| `fec` | `double` | FEC normativo anual, duas casas decimais |
| `dec_fi` | `double` | DEC de falha interna anual, indicador proprio do trabalho |
| `fec_fi` | `double` | FEC de falha interna anual, indicador proprio do trabalho |
| `dec_fi_soma_simples` | `double` | DEC-FI pela soma direta dos meses, sem ponderacao |
| `dif_vs_soma_simples` | `double` | Diferenca entre o calculo normativo e a soma simples |

### `gold.fato_continuidade_global_mensal`

Indicador de continuidade da distribuidora no grao mensal, agregado dos conjuntos pelas Equacoes 41 a 43 do PRODIST Modulo 8. Restrito as distribuidoras de grande porte e aos anos civis completos.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres |
| `sig_agente` | `string` | Sigla da distribuidora conforme publicada pela ANEEL |
| `ano` | `int` | Ano civil de apuracao |
| `mes` | `int` | Mes civil de apuracao, de 1 a 12 |
| `conjuntos` | `bigint` | Quantidade de conjuntos agregados no mes |
| `nuc_g` | `bigint` | Universo do mes: soma das unidades consumidoras dos conjuntos (Eq. 43) |
| `dec` | `double` | DEC normativo da distribuidora no mes, duas casas decimais |
| `fec` | `double` | FEC normativo da distribuidora no mes, duas casas decimais |
| `dec_fi` | `double` | DEC de falha interna da distribuidora no mes, indicador proprio |
| `fec_fi` | `double` | FEC de falha interna da distribuidora no mes, indicador proprio |

### `gold.fato_reclamacao_janela`

Reclamacoes do nivel 1 em janelas moveis de 12 meses por distribuidora de grande porte e recorte, com indicadores por mil UCs e taxa de procedencia. Mantem as distribuidoras excluidas do ranking, sinalizadas.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres |
| `recorte` | `string` | comercial_estrito, faturamento, pagamento, geracao_distribuida, outras_comerciais ou qualidade |
| `fim_janela` | `int` | Ultimo mes da janela de 12 meses, formato AAAAMM |
| `meses_com_ucs` | `bigint` | Meses da janela com NumCon informado |
| `meses_com_envio` | `bigint` | Meses da janela com reclamacao publicada pela distribuidora no nivel 1 |
| `janela_valida` | `boolean` | Verdadeiro quando os 12 meses tem UCs e envio de reclamacoes |
| `excluida_ranking` | `boolean` | Verdadeiro quando a distribuidora consta de exclusao_ranking_manifestacao |
| `ucs_media` | `bigint` | Media mensal da soma de NumCon na janela; denominador dos indicadores |
| `qtd_recebidas` | `bigint` | Recebidas na janela, com a imputacao da Silver |
| `qtd_procedentes` | `bigint` | Procedentes na janela, com a imputacao da Silver |
| `qtd_improcedentes` | `bigint` | Improcedentes na janela, com a imputacao da Silver |
| `qtd_recebidas_publicada` | `bigint` | Recebidas na janela conforme publicadas |
| `qtd_procedentes_publicada` | `bigint` | Procedentes na janela conforme publicadas |
| `qtd_improcedentes_publicada` | `bigint` | Improcedentes na janela conforme publicadas |
| `recebidas_por_mil` | `double` | Recebidas por mil UCs na janela |
| `procedentes_por_mil` | `double` | Procedentes por mil UCs na janela |
| `taxa_procedencia` | `double` | Procedentes divididas por procedentes mais improcedentes, de 0 a 1 |
| `recebidas_por_mil_publicada` | `double` | Recebidas por mil UCs com valores publicados, sem imputacao |
| `procedentes_por_mil_publicada` | `double` | Procedentes por mil UCs com valores publicados, sem imputacao |
| `taxa_procedencia_publicada` | `double` | Taxa de procedencia com valores publicados, sem imputacao |
| `qtd_recebidas_nivel_2` | `bigint` | Recebidas no nivel 2 (ouvidoria) na janela; so no recorte comercial_estrito |
| `qtd_procedentes_nivel_2` | `bigint` | Procedentes no nivel 2 na janela; so no recorte comercial_estrito |
| `qtd_improcedentes_nivel_2` | `bigint` | Improcedentes no nivel 2 na janela; so no recorte comercial_estrito |
| `recebidas_nivel_2_por_mil` | `double` | Recebidas no nivel 2 por mil UCs; so no recorte comercial_estrito |
| `taxa_escalada` | `double` | Recebidas no nivel 2 divididas pelas recebidas publicadas no nivel 1; so no recorte comercial_estrito |

### `gold.ranking_continuidade`

Ranking de variacao do DEC-FI e do FEC-FI entre as mesmas janelas das reclamacoes, no mesmo conjunto de distribuidoras do ranking de Qualidade.

| Coluna | Tipo | Descrição |
|---|---|---|
| `indicador` | `string` | dec_fi ou fec_fi |
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres |
| `posicao` | `int` | Posicao pela variacao percentual; 1 e a maior reducao |
| `valor_inicio` | `double` | Indicador na primeira janela |
| `valor_fim` | `double` | Indicador na ultima janela |
| `var_abs` | `double` | Valor final menos inicial |
| `var_pct` | `double` | Variacao percentual entre o valor inicial e o final |

### `gold.ranking_evolucao`

Evolucao da continuidade entre o primeiro e o ultimo ano da janela, por distribuidora de grande porte. Reducao do DEC-FI indica melhora.

| Coluna | Tipo | Descrição |
|---|---|---|
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres |
| `sig_agente` | `string` | Sigla da distribuidora conforme publicada pela ANEEL |
| `dec_inicio` | `double` | DEC normativo anual no primeiro ano da janela |
| `fec_inicio` | `double` | FEC normativo anual no primeiro ano da janela |
| `dec_fi_inicio` | `double` | DEC de falha interna anual no primeiro ano da janela |
| `fec_fi_inicio` | `double` | FEC de falha interna anual no primeiro ano da janela |
| `nuc_inicio` | `bigint` | Media mensal das unidades consumidoras no primeiro ano da janela |
| `dec_fim` | `double` | DEC normativo anual no ultimo ano da janela |
| `fec_fim` | `double` | FEC normativo anual no ultimo ano da janela |
| `dec_fi_fim` | `double` | DEC de falha interna anual no ultimo ano da janela |
| `fec_fi_fim` | `double` | FEC de falha interna anual no ultimo ano da janela |
| `nuc_fim` | `bigint` | Media mensal das unidades consumidoras no ultimo ano da janela |
| `dec_var_abs` | `double` | Variacao do DEC normativo entre o primeiro e o ultimo ano, na unidade do indicador |
| `dec_var_pct` | `double` | Variacao percentual do DEC normativo; nula quando o valor inicial e zero |
| `fec_var_abs` | `double` | Variacao do FEC normativo entre o primeiro e o ultimo ano, na unidade do indicador |
| `fec_var_pct` | `double` | Variacao percentual do FEC normativo; nula quando o valor inicial e zero |
| `dec_fi_var_abs` | `double` | Variacao do DEC de falha interna entre o primeiro e o ultimo ano, na unidade do indicador |
| `dec_fi_var_pct` | `double` | Variacao percentual do DEC de falha interna; nula quando o valor inicial e zero |
| `fec_fi_var_abs` | `double` | Variacao do FEC de falha interna entre o primeiro e o ultimo ano, na unidade do indicador |
| `fec_fi_var_pct` | `double` | Variacao percentual do FEC de falha interna; nula quando o valor inicial e zero |
| `posicao` | `int` | Posicao no ranking, ordenada pela variacao percentual do DEC-FI |
| `melhorou` | `boolean` | Verdadeiro quando o DEC-FI do ultimo ano e menor que o do primeiro |

### `gold.ranking_reclamacoes`

Rankings de variacao das reclamacoes por mil UCs entre a primeira e a ultima janela, por recorte e medida. Posicao 1 e a maior reducao; inclui a sensibilidade sem imputacao.

| Coluna | Tipo | Descrição |
|---|---|---|
| `recorte` | `string` | comercial_estrito, faturamento, pagamento, geracao_distribuida, outras_comerciais ou qualidade |
| `medida` | `string` | procedentes ou recebidas |
| `num_cnpj` | `string` | CNPJ da distribuidora, texto de 14 caracteres |
| `posicao` | `int` | Posicao pela variacao percentual, com a variacao absoluta como desempate |
| `indicador_inicio` | `double` | Indicador por mil UCs na primeira janela |
| `indicador_fim` | `double` | Indicador por mil UCs na ultima janela |
| `var_abs` | `double` | Indicador final menos inicial |
| `var_pct` | `double` | Variacao percentual entre o indicador inicial e o final |
| `volume_inicio` | `bigint` | Quantidade absoluta na primeira janela |
| `volume_fim` | `bigint` | Quantidade absoluta na ultima janela |
| `indicador_inicio_sem_imputacao` | `double` | Indicador inicial com valores publicados |
| `indicador_fim_sem_imputacao` | `double` | Indicador final com valores publicados |
| `var_abs_sem_imputacao` | `double` | Variacao absoluta com valores publicados |
| `var_pct_sem_imputacao` | `double` | Variacao percentual com valores publicados |
| `posicao_sem_imputacao` | `int` | Posicao calculada com valores publicados |
| `variacao_posicao` | `int` | Posicao sem imputacao menos posicao com imputacao |
