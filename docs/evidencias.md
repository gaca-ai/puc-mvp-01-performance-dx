# Evidências da plataforma

Prints do Databricks Free Edition que mostram o pipeline persistido no Unity Catalog (o catálogo de dados do Databricks), na ordem das seções do [README](../README.md). A evidência principal são os notebooks, salvos com as saídas e os testes; os prints mostram o mesmo resultado na interface.

- [Carga dos Dados](#carga-dos-dados)
- [Modelagem e Catálogo de Dados](#modelagem-e-catálogo-de-dados)
- [Pipeline de Dados](#pipeline-de-dados)
- [Qualidade de Dados](#qualidade-de-dados)

---

## Carga dos Dados

**Estrutura criada pelo `02_base/01_setup`.** Os três schemas da arquitetura medalhão (`bronze`, `silver`, `gold`) e o volume `landing`, onde ficam os arquivos baixados. O `information_schema` é criado pelo próprio Databricks.

![Schemas e volume criados pelo setup](img/base/01_setup/02-carga_nb01_01_schemas-volume.png)

**Uma pasta por fonte no volume `landing`.** Os arquivos de cada conjunto de dados da ANEEL caem na sua própria pasta antes de virar tabela.

![Pastas do volume landing](img/base/01_setup/02-carga_nb01_02_landing-folders.png)

**Catálogo `mvp_aneel` no Catalog Explorer.**

![Catálogo no Catalog Explorer](img/base/01_setup/02-carga_ui_01_catalog-explorer.png)

**Schema `bronze`: 10 tabelas e o volume `landing`.** Nove tabelas de dados, como publicadas pela ANEEL, e a tabela de controle `_ingestion_log`, que registra cada carga.

![Tabelas da Bronze](img/Bronze/bronze_tbls.png)

**Bronze com a descrição da ANEEL.** A descrição da tabela e de cada coluna vem do dicionário de dados publicado pela ANEEL, com a fonte e a versão citadas no próprio comentário.

![Bronze complaints](img/Bronze/mvp_aneel.bronze.complaints.png)

![Bronze continuity_indicators](img/Bronze/mvp_aneel.bronze.continuity_indicators.png)

---

## Modelagem e Catálogo de Dados

Cada tabela da Silver e da Gold foi gravada com descrição da tabela e de todas as colunas. O conteúdo completo, em texto, está em [`catalogo_dados.md`](catalogo_dados.md).

**Fonte do catálogo.** O `05_catalogo_dados` lê as descrições do `information_schema`, a área de metadados que o Unity Catalog mantém para cada catálogo.

![information_schema](img/schema/schema_tbls.png)

### Silver: dimensões

Distribuidoras, conjuntos elétricos, tipologias de reclamação e calendário.

![dim_distribuidora](img/Silver/dim_distribuidora.png)

![dim_conjunto](img/Silver/dim_conjunto.png)

![dim_tipologia](img/Silver/dim_tipologia.png)

![dim_tempo](img/Silver/dim_tempo.png)

### Silver: fatos

**`fato_manifestacao`.** Reclamações por distribuidora, tipologia, nível de atendimento e mês.

![fato_manifestacao](img/Silver/mvp_aneel.silver.fato_manifestacao.png)

**`fato_continuidade_mensal`.** DEC-FI e FEC-FI (duração e frequência das interrupções de origem interna, sem expurgos) e número de consumidores, por conjunto e mês.

![fato_continuidade_mensal](img/Silver/mvp_aneel.silver.fato_continuidade_mensal.png)

### Silver: tabelas de controle

**`exclusao_ranking_manifestacao`.** Distribuidoras fora do ranking de reclamações, com motivo e evidência. A Silver guarda as linhas; a Gold aplica a exclusão.

![exclusao_ranking_manifestacao](img/Silver/exclusao_ranking_manifestacao.png)

**`recon_continuidade`.** Conferência entre o indicador composto pelas parcelas e o consolidado publicado pela ANEEL.

![recon_continuidade](img/Silver/mvp_aneel.silver.recon_continuidade.png)

### Gold: descrição e linhagem

Para cada tabela, dois prints: a descrição com as colunas e a linhagem (de quais tabelas e notebooks ela vem, e quem a consome), registrada automaticamente pelo Unity Catalog.

**`fato_reclamacao_janela`.** Reclamações em janelas de 12 meses, com o denominador de consumidores.

![fato_reclamacao_janela](img/Gold/mvp_aneel.gold.fato_reclamacao_janela.png)

![fato_reclamacao_janela, linhagem](img/Gold/mvp_aneel.gold.fato_reclamacao_janela_lineage.png)

**`ranking_reclamacoes`.** Ranking de variação das reclamações entre as janelas.

![ranking_reclamacoes](img/Gold/mvp_aneel.gold.ranking_reclamacoes.png)

![ranking_reclamacoes, linhagem](img/Gold/mvp_aneel.gold.ranking_reclamacoes_lineage.png)

**`continuidade_janela`.** DEC-FI e FEC-FI nas mesmas janelas das reclamações.

![continuidade_janela](img/Gold/mvp_aneel.gold.continuidade_janela.png)

![continuidade_janela, linhagem](img/Gold/mvp_aneel.gold.continuidade_janela_lineage.png)

**`ranking_continuidade`.** Ranking de variação da continuidade, usado na validação.

![ranking_continuidade](img/Gold/mvp_aneel.gold.ranking_continuidade.png)

![ranking_continuidade, linhagem](img/Gold/mvp_aneel.gold.ranking_continuidade_lineage.png)

**`fato_continuidade_anual`.** Indicador anual por distribuidora.

![fato_continuidade_anual](img/Gold/mvp_aneel.gold.fato_continuidade_anual.png)

![fato_continuidade_anual, linhagem](img/Gold/mvp_aneel.gold.fato_continuidade_anual_lineage.png)

**`fato_continuidade_global_mensal`.** Indicador mensal do agregado nacional.

![fato_continuidade_global_mensal](img/Gold/mvp_aneel.gold.fato_continuidade_global_mensal.png)

![fato_continuidade_global_mensal, linhagem](img/Gold/mvp_aneel.gold.fato_continuidade_global_mensal_lineage.png)

**`ranking_evolucao`.** Evolução da continuidade entre o primeiro e o último ano.

![ranking_evolucao](img/Gold/mvp_aneel.gold.ranking_evolucao.png)

![ranking_evolucao, linhagem](img/Gold/mvp_aneel.gold.ranking_evolucao_lineage.png)

---

## Pipeline de Dados

**Silver: 9 tabelas**, todas com descrição.

![Tabelas da Silver](img/Silver/silver_tbls.png)

**Gold: 7 tabelas**, todas com descrição.

![Tabelas da Gold](img/Gold/gold_tbls.png)

---

## Qualidade de Dados

**Evidência externa: a própria ANEEL alerta para a quebra entre 2022 e 2023.** Painel da ANEEL que compara as reclamações de 1º nível de 2022 (tipologias antigas) com as de 2023 (tipologias novas somadas para equivaler às antigas) e marca em vermelho diferenças acima de 10%. A mudança de codificação compromete a comparação entre anos, um dos motivos para a série começar em janeiro de 2024.

![Painel de validação da ANEEL](img/complaints/05-qualidade_ui_01_validacao-aneel-2022-2023.png)
