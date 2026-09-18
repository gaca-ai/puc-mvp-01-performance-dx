# Catálogo de Evidências

Arquivo gerado por `src/organizar_evidencias.py` a partir de `docs/screenshots.xlsx`.
Não editar à mão: alterações se perdem na próxima execução do script.

As imagens ficam em `docs/img/<notebook>/`, uma subpasta por notebook de origem.

## Convenção de nomes

Formato: `<seção>_<origem>_<seq>_<assunto>.png`, em minúsculas, sem acentos e sem
espaços, para garantir os links no GitHub. A origem é o notebook (`nb00`, `nb01`,
`nb02`, ...) ou a interface visual (`ui`).

A exportação do notebook em HTML conta como evidência da execução completa e
dispensa capturar cada saída em separado. As capturas listadas aqui são as que
sustentam pontos específicos do README.

| Prefixo | Seção do README |
|---|---|
| `01-contexto` | Contexto de Negócios e Perguntas (Etapa 2 e 4.1) |
| `02-carga` | Carga dos Dados (Etapa 4.2) |
| `03-modelagem` | Modelagem e Catálogo de Dados (Etapa 4.3) |
| `04-pipeline` | Pipeline de Dados (Etapa 4.4) |
| `05-qualidade` | Qualidade de Dados (Etapa 4.5) |
| `06-analise` | Análise de Dados (Etapa 4.5) |
| `07-autoavaliacao` | Autoavaliação |

## Índice

3 de 23 evidências capturadas. Campo "Capturado em" vazio indica evidência pendente.

### `docs/img/01_setup`

| Arquivo | Seção | Prioridade | O que evidencia | Capturado em |
|---|---|---|---|---|
| `img/01_setup/02-carga_nb01_01_schemas-volume.png` | 02-carga | essencial | Schemas bronze, silver e gold criados no catalogo mvp_aneel, e volume landing no schema bronze | 10/09/2026 |
| `img/01_setup/02-carga_nb01_02_landing-folders.png` | 02-carga | essencial | Subpastas do volume de landing, uma por fonte de dados | 10/09/2026 |
| `img/01_setup/02-carga_ui_01_catalog-explorer.png` | 02-carga | essencial | Catalogo mvp_aneel e seus schemas na interface do Unity Catalog | 10/09/2026 |

### `docs/img/02_bronze_ingestion`

| Arquivo | Seção | Prioridade | O que evidencia | Capturado em |
|---|---|---|---|---|
| `img/02_bronze_ingestion/02-carga_nb02_01_licencas-ckan.png` | 02-carga | essencial | Licenca e data de atualizacao de cada conjunto, resolvidas pela API CKAN. Evidencia direta do criterio Coleta |   |
| `img/02_bronze_ingestion/02-carga_nb02_02_download-recursos.png` | 02-carga | complementar | Download dos 14 recursos para o volume, com tamanho, tempo e taxa de transferencia |   |
| `img/02_bronze_ingestion/02-carga_nb02_03_normalizacao-timestamps.png` | 02-carga | essencial | Deteccao e conversao dos dois arquivos do INDGER com DthCarga em nanossegundos |   |
| `img/02_bronze_ingestion/02-carga_nb02_04_tabelas-bronze.png` | 02-carga | essencial | Registro das 9 tabelas Delta com linhas, colunas e arquivos de origem de cada uma |   |
| `img/02_bronze_ingestion/02-carga_nb02_05_ingestion-log.png` | 02-carga | essencial | Tabela de controle _ingestion_log: licenca, URL de origem, tamanho e tabela de destino por recurso |   |
| `img/02_bronze_ingestion/02-carga_nb02_06_validacao-total.png` | 02-carga | essencial | Validacao final: 9 tabelas persistidas e total de 108.744.173 linhas |   |
| `img/02_bronze_ingestion/02-carga_ui_02_volume-landing.png` | 02-carga | complementar | Arquivos baixados dentro do volume de landing, no Catalog Explorer |   |
| `img/02_bronze_ingestion/02-carga_ui_03_tabelas-bronze.png` | 02-carga | essencial | As 9 tabelas Bronze e a tabela de controle no Catalog Explorer |   |

### `docs/img/03_bronze_data_quality`

| Arquivo | Seção | Prioridade | O que evidencia | Capturado em |
|---|---|---|---|---|
| `img/03_bronze_data_quality/05-qualidade_nb03_01_panorama-tabelas.png` | 05-qualidade | essencial | Panorama das 9 tabelas Bronze: volume, colunas e distribuicao de tipos |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_02_dominio-indicadores.png` | 05-qualidade | essencial | Dominio de SigIndicador na base de continuidade: 23 valores, volume e cobertura por ano |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_03_cobertura-temporal.png` | 05-qualidade | complementar | Serie de 2020 a 2026, meses por ano e contagem de conjuntos e distribuidoras |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_04_presenca-parcelas.png` | 05-qualidade | essencial | Cobertura de cada parcela do DEC e do FEC na grade conjunto-ano-mes, dentro da janela |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_05_tipos-dicionario.png` | 05-qualidade | essencial | Divergencia entre os tipos publicados e o dicionario da ANEEL, com os zeros a esquerda perdidos |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_06_rotulos-instaveis.png` | 05-qualidade | complementar | Conjuntos com mais de uma descricao e CNPJs com mais de uma sigla ao longo da serie |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_07_reestruturacao-conjuntos.png` | 05-qualidade | essencial | Distribuidoras que mudaram a quantidade de conjuntos na virada de dezembro para janeiro |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_08_duplicatas.png` | 05-qualidade | complementar | Teste de unicidade no grao conjunto x ano x mes x indicador |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_09_aderencia-composicao.png` | 05-qualidade | essencial | Aderencia da composicao normativa por ano e regime: 100% em cada regime vigente, comprovando a regra do Modulo 8 Secao 8.2 |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_10_divergencia-consolidado.png` | 05-qualidade | essencial | Erro no consolidado da ANEEL: ELEKTRO, junho de 2025, 123 conjuntos com FEC publicado menor que a soma das parcelas |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_11_outliers-distribuicao.png` | 05-qualidade | complementar | Distribuicao do DEC-FI e do FEC-FI na janela e concentracao da duracao ponderada nos extremos |   |
| `img/03_bronze_data_quality/05-qualidade_nb03_12_sintese-achados.png` | 05-qualidade | essencial | Consolidacao das verificacoes da fonte de continuidade, com status e tratamento de cada achado |   |

## Pendentes essenciais

Evidências marcadas como essenciais e ainda não capturadas:

- `02-carga_nb02_01_licencas-ckan.png` — Licenca e data de atualizacao de cada conjunto, resolvidas pela API CKAN. Evidencia direta do criterio Coleta
- `02-carga_nb02_03_normalizacao-timestamps.png` — Deteccao e conversao dos dois arquivos do INDGER com DthCarga em nanossegundos
- `02-carga_nb02_04_tabelas-bronze.png` — Registro das 9 tabelas Delta com linhas, colunas e arquivos de origem de cada uma
- `02-carga_nb02_05_ingestion-log.png` — Tabela de controle _ingestion_log: licenca, URL de origem, tamanho e tabela de destino por recurso
- `02-carga_nb02_06_validacao-total.png` — Validacao final: 9 tabelas persistidas e total de 108.744.173 linhas
- `02-carga_ui_03_tabelas-bronze.png` — As 9 tabelas Bronze e a tabela de controle no Catalog Explorer
- `05-qualidade_nb03_01_panorama-tabelas.png` — Panorama das 9 tabelas Bronze: volume, colunas e distribuicao de tipos
- `05-qualidade_nb03_02_dominio-indicadores.png` — Dominio de SigIndicador na base de continuidade: 23 valores, volume e cobertura por ano
- `05-qualidade_nb03_04_presenca-parcelas.png` — Cobertura de cada parcela do DEC e do FEC na grade conjunto-ano-mes, dentro da janela
- `05-qualidade_nb03_05_tipos-dicionario.png` — Divergencia entre os tipos publicados e o dicionario da ANEEL, com os zeros a esquerda perdidos
- `05-qualidade_nb03_07_reestruturacao-conjuntos.png` — Distribuidoras que mudaram a quantidade de conjuntos na virada de dezembro para janeiro
- `05-qualidade_nb03_09_aderencia-composicao.png` — Aderencia da composicao normativa por ano e regime: 100% em cada regime vigente, comprovando a regra do Modulo 8 Secao 8.2
- `05-qualidade_nb03_10_divergencia-consolidado.png` — Erro no consolidado da ANEEL: ELEKTRO, junho de 2025, 123 conjuntos com FEC publicado menor que a soma das parcelas
- `05-qualidade_nb03_12_sintese-achados.png` — Consolidacao das verificacoes da fonte de continuidade, com status e tratamento de cada achado
