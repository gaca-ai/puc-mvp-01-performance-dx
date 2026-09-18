# Projeto MVP — Contexto de Trabalho

Última atualização: 13/09/2026 (rev. 3)

Arquivo de continuidade entre sessões. Registra decisões, trabalho concluído, pendências e próximos passos.

---

## 1. Identificação

| Item | Valor |
|---|---|
| Curso | Pós-graduação em Ciência de Dados e Analytics (PUC-Rio), Sprint 1 — Engenharia de Dados |
| Trabalho | MVP: construção de um pipeline de dados na nuvem (individual) |
| Entrega | 27/09/2026, via fórum, com link do GitHub (resultado em 12/10/2026) |
| Sessões de dúvidas restantes | 16/09 e 23/09 |
| Repositório | https://github.com/gaca-ai/puc-mvp-01-performance-dx (público, licença MIT) |
| Plataforma | Databricks Free Edition, compute serverless |
| Pasta de trabalho local | `C:\python_projects\puc-mvp-01-performance-dx`, clone do repositório |
| Fluxo de versionamento | Desenvolvimento local no VS Code → commit e push pelo GitHub Desktop → Pull no Git folder do Databricks. O Databricks não commita, apenas atualiza |
| Documento de entrega | README.md no GitHub |

---

## 2. Objetivo

Problema: quais concessionárias de grande porte (acima de 400 mil UCs) apresentaram a melhor evolução na qualidade percebida pelo consumidor nos últimos 36 meses?

1. Quais distribuidoras mais reduziram as reclamações procedentes por mil UCs?
2. Quais mais aumentaram o percentual de serviços comerciais realizados no prazo?
3. Quais mais reduziram o DEC-FI e o FEC-FI?
4. Quais mais reduziram a transgressão de nível de tensão (DRP/DRC)?
5. Quais mais investiram em Melhoria e Renovação por UC?
6. Quais mais reduziram o tempo médio de atendimento a ocorrências com interrupção (TMA-CI)?
7. Maior investimento por UC está associado a maior melhora de DEC/FEC?
8. A redução de DEC/FEC se reflete em menos reclamações por falta de energia?
9. Qual o peso das interrupções que o indicador deixa de fora — programadas e de origem externa — na indisponibilidade total sentida pelo consumidor?
10. Há distribuidoras com DEC-FI e FEC-FI em queda e TMA-CI em alta simultaneamente? Par de sinais compatível com automação de redes.

Tese do trabalho: a ANEEL já apura e publica esses indicadores, inclusive em painéis de BI. O adicional do MVP não é reproduzir o dado, é propor métricas redefinidas para avaliar a distribuidora sob a ótica do consumidor, e não sob a ótica da penalidade regulatória. Esse princípio é o critério para resolver qualquer dúvida de escopo.

Regra da especificação: não remover perguntas não respondidas; discuti-las na autoavaliação.

---

## 3. Escopo e decisões metodológicas

| Tema | Decisão |
|---|---|
| Universo | Concessionárias com mais de 400 mil UCs (mesmo corte do ranking de continuidade da ANEEL) |
| Chave da distribuidora | `NumCNPJ` (siglas mudam após aquisições e renomeações) |
| Janela | Móvel de 36 meses até M, o último mês disponível simultaneamente em todas as bases |
| Evolução | Bloco final (M−11 a M) versus bloco inicial (M−35 a M−24); elimina sazonalidade |
| Resultado | 6 rankings, um por métrica, sem índice composto |
| Sinal | Evolução positiva sempre significa melhora |
| Pilares | Comercial, Técnico e Investimento |

### Critério único de exclusão (rev. 3)

Os indicadores medem **anomalia na prestação do serviço**: interrupção não planejada do fornecimento, originada no sistema de distribuição. O que se enquadra entra, ainda que a regulação expurgue; o que não se enquadra sai, ainda que a regulação inclua. O critério vale igualmente para continuidade e para atendimento.

| Caso de fronteira | Decisão | Razão |
|---|---|---|
| Manutenção programada | Fora | Antecedida de aviso prévio (Módulo 1, item 211); não é falha do serviço, é condição de mantê-lo; e incluí-la premiaria quem adia manutenção, contrariando a métrica 5 |
| Origem externa ao sistema de distribuição | Fora | É anomalia, mas não da prestação deste serviço; a distribuidora não a originou nem pode evitá-la |
| ISE e Dia Crítico | Dentro | O consumidor ficou sem energia, e os dois gatilhos de expurgo dependem do volume de interrupções do evento — logo, do estado da rede (Módulo 1, itens 116 e 208) |
| Racionamento e ERAC (`DECino`) | Fora | Decisão da União e do ONS, não da distribuidora. Hoje irrelevante em volume |

Vulnerabilidades registradas, ambas observáveis nos dados: a fatia programada pode ser inflada por reclassificação, e a fatia expurgada por ISE e Dia Crítico mede quanto do resultado depende do enquadramento. Por isso `DECip` e `DECine` são acompanhadas como métricas descritivas, fora do ranking, no mesmo papel do PNIE para o TMA-CI.

---

## 4. Métricas dos 6 rankings

| # | Pilar | Métrica | Fonte | Critério do ranking |
|---|---|---|---|---|
| 1 | Comercial | Reclamações procedentes no nível 1 (SAC) por mil UCs | Manifestações + INDGER Comerciais (`QtdUCAtiva`) | −Δ% entre blocos de 12 meses |
| 2 | Comercial | % de serviços no prazo = `1 − Σ QtdServRealizDescPrazo / Σ QtdServRealizado` | INDGER Serviços Comerciais (fonte a confirmar, ver pendência 17) | Δ p.p. entre blocos |
| 3 | Técnico | DEC-FI e FEC-FI, ponderados por UC | Indicadores Coletivos de Continuidade | média(−Δ% DEC-FI, −Δ% FEC-FI) |
| 4 | Técnico | % de UCs sorteadas com transgressão de DRP ou DRC | Conformidade do Nível de Tensão | −Δ p.p. entre primeiro e último ano |
| 5 | Investimento | R$ realizado em Melhoria + Renovação por UC, deflacionado pelo IPCA | PDD + INDGER Comerciais | Nível acumulado 2023–2025 (não variação) |
| 6 | Técnico | TMA-CI = Σ (`NumTempoPreparacao` + `NumTempoDeslocamento` + `NumTempoExecucao`) ÷ contagem de ocorrências com interrupção, em minutos | Ocorrências Emergenciais nas Redes de Distribuição | −Δ% entre blocos de 12 meses |
| — | Técnico (acompanhante) | PNIE = ocorrências com interrupção ÷ total de ocorrências × 100 | Ocorrências Emergenciais nas Redes de Distribuição | Descritivo, não ranqueado |
| — | Técnico (acompanhante) | `DECip` e `DECine` como fatia do DEC total | Indicadores Coletivos de Continuidade | Descritivo, detecta reclassificação e dependência de enquadramento |

### Definição do DEC-FI e do FEC-FI

```
DEC-FI = DECind + DECine + DECinc
```

Origem interna e não programada, incluindo ISE (`DECine`) e Dia Crítico (`DECinc`). Ficam fora `DECip` e `DECipc` (programadas), `DECino` (racionamento e ERAC) e `DECxp` e `DECxn` (origem externa). O FEC-FI segue a mesma composição.

Nota importante, apurada na rev. 3: o DEC comparado ao limite regulatório é `DECip + DECind` — ou seja, **já inclui manutenção programada**. O que o item 187 do Módulo 8 exclui é ISE, Dia Crítico, origem externa, ERAC, racionamento, falha na instalação do cliente, inadimplência e obras de interesse exclusivo. Por isso "DEC total" foi abandonado como nome: o indicador deste trabalho não é a soma de todas as parcelas.

Justificativas registradas:

- Métrica 1: só nível 1, porque somar a Ouvidoria pode contar duas vezes a mesma reclamação escalada. Período por `AnoCompetencia`/`MesCompetencia`, não por `DatReferencia`.
- Métrica 3: peso igual entre DEC e FEC segue o espírito do DGC da ANEEL. Não se usa a razão contra o limite porque o limite vale para o indicador com expurgos e é redefinido nas revisões tarifárias, o que misturaria desempenho com mudança de limite.
- Métrica 5: Expansão fica fora (atende crescimento de mercado, não qualidade da rede existente). Investimento é esforço, não resultado, por isso o ranking é por nível. Taxa de execução do PDD entra apenas como informação descritiva.
- Métrica 6: ranking próprio, e não dentro da métrica 3, porque DEC/FEC medem a qualidade do produto entregue e o tempo de atendimento mede a qualidade da resposta.
- Métrica 6 — nome: o indicador não se chama TMAE. TMAE é indicador regulado, com definição fechada no Módulo 1 do PRODIST, item 364, e universo de todas as ocorrências emergenciais.
- Métrica 6 — universo: ocorrências que causaram interrupção, excluídas as de fato gerador programado e as de origem externa, pelo critério de anomalia da seção 3. ISE permanece.
- Métrica 6 — exclusões adicionais: defeito interno da própria UC (a distribuidora não pode resolver, é falha de manutenção do cliente, e o alcance é de um cliente e não do conjunto) e os casos que o Módulo 8 exclui por não serem emergência de fornecimento (iluminação pública, serviços de caráter comercial, reclamações de nível de tensão).
- Métrica 6 — agregação: o denominador é contagem de ocorrências, não quantidade de clientes, então a soma das parcelas pode ser feita direto no nível distribuidora-mês. Sem ponderação por UC.
- Métrica 6 — referência regulatória, para comparação: Módulo 8, Seção 8.2, Equações 24 a 28.
- Métrica 6 — efeito automação: interrupção restabelecida por telecomando não gera ocorrência e não entra. Automação retira os casos fáceis do denominador e pode elevar o TMA-CI enquanto a qualidade melhora. DEC-FI e FEC-FI em queda com TMA-CI em alta é par de sinais compatível com automação.

Complementos analíticos:

- Princípio geral de validação: todo indicador calculado é reconciliado contra o valor equivalente publicado pela ANEEL, quando há publicação. Dupla função — provar que o pipeline reproduz o número oficial quando aplica a regra oficial, e medir quanto cada escolha metodológica própria desloca o resultado.
- Reconciliação com o DGC oficial de 2025 como validação de qualidade do pipeline.
- Reconciliação da métrica 6: calcular também o TMAE no universo completo, para comparar com a base `Atendimento às Ocorrências Emergenciais`.
- Decomposição do DEC (interna, externa, programada, ISE, dia crítico) como diagnóstico, fora do ranking.
- Gráfico de dispersão: investimento por UC versus evolução de DEC-FI/FEC-FI.

---

## 5. Bases de dados

Portal: https://dadosabertos.aneel.gov.br (API CKAN em `https://dadosabertos.aneel.gov.br/api/3/action`)

A lista de fontes vive em `src/config.py`, na estrutura `DATASETS`, que liga conjunto CKAN → pasta de landing → tabela Bronze → arquivos. As URLs não são fixas no código: o notebook resolve cada recurso por `package_show` a partir do identificador do conjunto, e captura a licença no mesmo passo.

| Base | Identificador CKAN | Granularidade | Uso | Status |
|---|---|---|---|---|
| Indicadores Coletivos de Continuidade | `d5f0712e-…` | conjunto × período × indicador | Métrica 3, perguntas 7–9 | Carregada na Bronze |
| Conformidade do Nível de Tensão | `51f2d7ea-…` | UC sorteada × ano × indicador | Métrica 4 | Carregada na Bronze |
| INDGER Dados Comerciais | `7cacb2c4-…` | município × mês | Denominador de UCs; filtro de universo | Carregada na Bronze |
| INDGER Dados de Serviços Comerciais | `7cacb2c4-…` | município × tipo de serviço × mês | Métrica 2 | Carregada na Bronze |
| Qualidade do Atendimento Comercial | `b7b32b0c-…` | a confirmar | Métrica 2 ou reconciliação | Carregada na Bronze |
| Manifestações nos 1º e 2º níveis | `364859a2-…` | município × canal × tipologia × mês | Métrica 1, pergunta 7 | Carregada na Bronze (2023–2026) |
| Plano de Desenvolvimento da Distribuição (PDD) | `6838f13d-…` | CNPJ × UF × ano × tipo × classe de obra | Métrica 5 | Carregada na Bronze |
| Ocorrências Emergenciais nas Redes de Distribuição | `ced06b4c-…` | ocorrência | Métrica 6, PNIE e pergunta 10 | Carregada na Bronze (2023–2026, em duas tabelas) |
| Atendimento às Ocorrências Emergenciais | — | conjunto × mês × indicador | Apenas reconciliação do TMAE | Não carregada |
| De-paras próprios (dados públicos) | — | variável | Silver | Em `aux_files`; faltam os de-paras 4 e 5 |

O arquivo de ocorrências de 2022 foi descartado: manifestações começam em 2023, então M não pode ser anterior a dez/2025, e com M em 2026 o bloco inicial cai em 2023. A exclusão elimina 13,3 milhões de linhas e 393 MB.

Bases disponíveis e não utilizadas no plano: INDGER Dados Técnicos de Subestações, Linhas de Distribuição e Alimentadores. Alternativa para peso de UCs por conjunto: `QtdConsAtivo` (alimentadores) ou `QtdUCAtivoSub` (subestações).

### Sobre o investimento: PDD e não demonstrações contábeis

Avaliado e descartado na rev. 3. O balanço não segrega por finalidade da obra, que é o corte da métrica 5. Sob a ICPC 01 a infraestrutura de concessão é reconhecida como ativo financeiro ou intangível, não como imobilizado. O perímetro contábil de holdings não coincide com a concessão. E a base de dados abertos da CVM cobre apenas companhias abertas registradas, deixando de fora as distribuidoras de capital fechado — cobertura parcial de um universo que precisa ser fechado.

Registrado como caminho não explorado, para a autoavaliação. Nota técnica para retomada futura: os pacotes DFP e ITR do portal da CVM são ZIPs com CSVs por CNPJ, série desde 2010, legíveis sem programa específico. O Empresas.NET é apenas o software de envio usado pelas companhias.

### Sobre os de-paras

A lista de fatos geradores do Anexo 8.C do Módulo 8 (39 combinações de Origem, Tipo, Causa e Detalhe; anexo alterado pela REN ANEEL 1.137 de 21/10/2025) é de-para pronto para `reference/ref_fato_gerador.csv`. Atenção na leitura de Origem: "Meio ambiente", que inclui descarga atmosférica e vento, está classificado como origem Interna — origem Externa no PRODIST significa falha originada fora do sistema de distribuição, não causa fora do controle da empresa.

De-paras úteis, por ordem de impacto:

1. CNPJ ↔ sigla ↔ nome atual ↔ grupo econômico, com histórico
2. `CodTipoManifestacao` ↔ `IdeTipoRCA` (tipologias de reclamação)
3. `CodTipoServico` ↔ descrição e prazo regulatório
4. Distribuidora ↔ porte (UCs) e distribuidoras designadas
5. Conjunto ↔ distribuidora (transferências)

Arquivos de apoio em `aux_files`, a converter para CSV em `reference/`:

| Arquivo | Conteúdo | De-para que atende |
|---|---|---|
| `cnpj.xlsx` | 90 linhas: `SigAgente`, `NumCPFCNPJ`, `Contagem`, `id_dist` | 1, parcialmente. CNPJ numérico, sem zeros à esquerda |
| `de_para_reclamacoes_novo.xlsx` | Aba `Dados Abertos Nova` (280 linhas, cabeçalho na 5ª linha) e aba `Dados Abertos Antiga` (23 linhas) | 2, e fornece `ind_subtototal`, filtro necessário para não somar subtotais |
| `servicos_dados_abertos.xlsx` | 112 linhas com prazo regulatório e artigo | 3 |
| `servicos_classe.xlsx` | 28 linhas, visão resumida por artigo | 3 |
| `RELATORIO_DTB_BRASIL_MUNICIPIO.xlsx` | DTB IBGE 2022, 5.570 municípios | Dimensão geografia |

---

## 6. Problemas de qualidade já identificados

### Ocorrências emergenciais: troca de padrão de publicação em 2026

O arquivo de 2026 tem 23 colunas contra 15 nos anos anteriores, e apenas `DatGeracaoConjuntoDados` e `NomAgente` mantêm o nome. As demais foram renomeadas para o padrão de prefixos `Cod`/`Num`/`Dsc`/`Dth`. De-para provável, a validar contra os valores:

| 2023–2025 | 2026 | Observação |
|---|---|---|
| `NumCPFCNPJ` | `NumCnpjDistribuidora` | `int64` vira `string`; zeros à esquerda |
| `CodIBGE` | `CodMunicipioIBGE` | `int64` vira `string`; conferir 7 x 8 dígitos |
| `NumOcorrencia` | `CodOcorrenciaEmergencial` | renomeação |
| `IdeConjUndConsumidoras` | `CodConjUnidConsumidora` | `int64` vira `string` |
| `DthInicioOcorrenciaAberta` | `DthIniOcorrencia` | `timestamp[ms]` vira `string` |
| `DthFimOcorrenciaAberta` | `DthFimOcorrencia` | idem |
| `DscCanalAtendimento` | `DscFormaConhecimento` | não é sinônimo, verificar domínios |
| `DscNumInterrupcao` | `DscInterrupcaoAssociada` | campo-chave da métrica 6 |
| `DscOcorrenciaAberta` | `DscFatoGeradorOrigem/Tipo/Causa/Detalhe`? | hipótese: texto livre virou quádrupla categorizada |
| `MdaPreparo/Deslocamento/Execucao` | `NumTempoPreparacao/Deslocamento/Execucao` | `double` vira `string` |
| `NumVeiculo` | — | desaparece |
| — | `SigAgente`, `CodAlimentador`, `CodSubestacao`, `NumAnoCompetencia`, `NumMesCompetencia`, `DscMotivoExpurgo` | novos |

Em 2026 todos os 23 campos são `string`, inclusive datas e números. O esquema novo é semanticamente mais rico e tecnicamente pior: perdeu a tipagem na origem. E o zero de nulos reportado pelas estatísticas do Parquet não indica completude — ausência provavelmente virou string vazia.

O leiaute dos microdados não é regido pelo Módulo 8. O Módulo 8 exige o registro do fato gerador da ocorrência emergencial desde a REN 956/2021, mas só obriga o envio dos indicadores agregados TMP, TMD, TME, NIE e `n` por conjunto. Nunca exigiu vínculo entre ocorrência e interrupção. A mudança de leiaute deve estar no Módulo 6 e nos manuais de coleta.

### Timestamps em nanossegundos

`indger-dados-servicos-comerciais.parquet` e `indger-dados-comerciais.parquet` gravam `DthCarga` como `TIMESTAMP(NANOS)`, que o Spark rejeita com `PARQUET_TYPE_ILLEGAL`. A configuração `spark.sql.legacy.parquet.nanosAsLong` é bloqueada no compute serverless da Free Edition. A precisão é artefato do escritor — `DthCarga` é a data de carga do publicador, metadado de processo. Tratamento na seção 4.1 do notebook 02: cópia convertida para microssegundos em `<pasta>/_normalized/`, gerada por pyarrow em fluxo por row group, com o arquivo original preservado no volume.

### PDD

- 5.484 linhas, 118 CNPJs, anos 2016–2030; realizado até 2025, somente planejado de 2026 a 2030
- 4 linhas exatamente duplicadas
- Um CNPJ com duas siglas (Celg-D e Enel GO): 43 conflitos de grão em 2016–2017
- Nomes de colunas divergem do dicionário: `NumCPFCNPJ` (arquivo) vs `NumCpfCnpj` (dicionário); `IdcAgenteSumarizacao` ausente
- Valores como texto com vírgula decimal; realizado zero em 1.945 linhas
- 15 linhas sem `DscTipoOutorga` (2016); 1 linha com "Obra com Participação Financeira" como tipo de obra

### Dicionários

- Continuidade: `NumPeriodoIndice` sugere coexistência de valores mensais, trimestrais e anuais
- Tensão: `VlrLimite` e `AnoLimiteQualidade` descritos como "valor do índice enviado"; resumo cita "índices de pagamento" (provável erro de cópia)
- Manifestações: `CodMunicipio` (7 caracteres) vs `CodMunicipioIBGE` (8) no INDGER; migração de `CodTipoReclamacao` para `IdeTipoRCA`
- Serviços Comerciais: `QtdServRealizDescPrazo` tipado como decimal (38,9)
- INDGER: dicionários de dez/2023; cobertura da série a verificar

---

## 7. Pendências de validação

1. DEC/FEC: quais parcelas do `dominio-indicadores.csv` correspondem a `DECind`, `DECine`, `DECinc` e às demais?
2. Onde está a quantidade de UCs por conjunto por mês (peso da média ponderada)?
3. O arquivo de continuidade traz o indicador global da distribuidora?
4. DEC de 12 meses (soma dos mensais) bate com o valor anual publicado?
5. Tensão: `VlrLimite` é valor medido ou limite? Tamanho da amostra por distribuidora-ano?
6. PDD: planejado original ou revisado?
7. Excluir distribuidoras designadas, como a ANEEL fez no ranking de 2023?
8. ~~Licença dos datasets~~ — resolvida: capturada automaticamente pelo notebook 02 e gravada em `mvp_aneel.bronze._ingestion_log`
9. ~~Identificadores dos datasets~~ — resolvida: registrados em `DATASETS`, em `src/config.py`
10. Ocorrências emergenciais: domínio de `DscInterrupcaoAssociada` e de `DscNumInterrupcao` — indicador S/N, texto livre ou chave?
11. Ocorrências emergenciais: dimensionar o que o recorte descarta; confirmar que os casos de defeito interno da UC caem fora e medir o volume
12. Ocorrências emergenciais: nulos, zeros e outliers nas três parcelas de tempo; atenção à string vazia no leiaute de 2026
13. Ocorrências emergenciais: `CodMunicipioIBGE` tem 7 ou 8 dígitos, para cruzar com a DTB e com o INDGER
14. Ocorrências emergenciais: a base já vem sem os casos que o Módulo 8 exclui da apuração, ou é preciso filtrar por fato gerador?
15. Ocorrências emergenciais: validar o de-para da seção 6 contra os valores, especialmente a hipótese `DscOcorrenciaAberta` → quádrupla de fato gerador
16. `CNPJ` de `cnpj.xlsx` está numérico — normalizar para 14 caracteres com zeros à esquerda antes de qualquer junção
17. Métrica 2: comparar os universos de `qualidade-atendimento-comercial` (1,5 milhão de linhas) e `indger-dados-servicos-comerciais` (23,9 milhões). Hipótese: INDGER como fonte da métrica pelo detalhe por tipo de serviço, qualidade comercial como base de reconciliação
18. Métrica 6: os campos de fato gerador só existem no leiaute de 2026, então as exclusões por origem e tipo não são aplicáveis a 2023–2025. Avaliar se é limitação intransponível ou se o filtro de interrupção sozinho basta

Arquivos a obter: `dominio-indicadores.csv` (continuidade e tensão), arquivo de atributos dos conjuntos, arquivo de atendimento emergencial (para reconciliação do TMAE), Módulo 6 do PRODIST em duas versões (para datar a mudança de leiaute).

Referências regulatórias em `aux_files/prodist`: Módulo 1 (versão REN 1.137/2025) e Módulo 8.

---

## 8. Ambiente implementado

| Objeto | Situação |
|---|---|
| Catálogo `mvp_aneel` | Criado |
| Schemas `bronze`, `silver`, `gold` | Criados com comentários |
| Schema `default` | Removido pelo `01_setup` |
| Volume `mvp_aneel.bronze.landing` | Criado, com 9 subpastas por fonte |
| Tabelas Bronze | 9 tabelas registradas, mais `_ingestion_log` |

### Resultado da carga Bronze (13/09/2026)

| Tabela | Linhas | Colunas | Arquivos |
|---|---:|---:|---:|
| `complaints` | 29.260.295 | 24 | 4 |
| `emergency_occurrences_v1` | 36.390.229 | 17 | 3 |
| `emergency_occurrences_v2` | 6.789.484 | 25 | 1 |
| `continuity_indicators` | 5.108.332 | 11 | 1 |
| `voltage_conformity` | 5.506.240 | 10 | 1 |
| `commercial_quality` | 1.493.698 | 9 | 1 |
| `indger_commercial_services` | 23.922.861 | 24 | 1 |
| `indger_commercial` | 267.550 | 65 | 1 |
| `pdd_investment` | 5.484 | 13 | 1 |
| **Total** | **108.744.173** | | **14** |

A contagem de colunas inclui as duas de linhagem, `_source_file` e `_ingested_at`.

Reconciliação: o perfil dos arquivos locais somava 116.531.032 linhas. Retirando o arquivo de 2022 (13.293.099) e somando o nível de tensão, baixado depois do perfil (5.506.240), chega-se a 108.744.173 — exatamente o total persistido. Todas as tabelas batem linha a linha com os arquivos de origem.

Decisão de arquitetura: ocorrências emergenciais geram duas tabelas, `_v1` e `_v2`, porque os leiautes divergem. Harmonizar exigiria decidir o de-para antes de examinar os dados, e a Bronze não é o lugar dessa decisão. Uma guarda de esquema aborta a união quando os arquivos que compõem uma tabela divergem.

A carga completa de 1,7 GB coube na cota diária do Free Edition. A estratégia alternativa prevista — filtrar localmente e subir apenas o recorte — não foi necessária, e o pipeline permanece automatizado de ponta a ponta.

---

## 9. Estrutura do repositório

| Caminho | Conteúdo | Status |
|---|---|---|
| `README.md` | Documento de entrega | Placeholder |
| `LICENSE`, `.gitignore` | MIT; template Python mais regras do projeto | Concluído |
| `src/config.py` | Configuração central e catálogo `DATASETS` | Concluído |
| `src/describe_ocorrencias.py` | Comparação de esquema entre leiautes, execução local | Concluído |
| `src/aneel_download.py` | Download e perfil local (fora do versionamento) | Concluído |
| `notebooks/00_objetivo.ipynb` | Problema, perguntas, recorte, arquitetura | Concluído |
| `notebooks/01_setup.ipynb` | Catálogo, schemas, volume, teste ANEEL | Concluído |
| `notebooks/02_bronze_ingestion.ipynb` | Download via API, normalização e tabelas Bronze | Concluído |
| `notebooks/03_bronze_data_quality.ipynb` | Perfil por atributo | Próximo |
| `notebooks/04_silver_reference.ipynb` | De-paras | Pendente |
| `notebooks/05_silver_technical.ipynb` | Continuidade, tensão e ocorrências | Pendente |
| `notebooks/06_silver_commercial.ipynb` | UCs ativas, serviços, reclamações | Pendente |
| `notebooks/07_silver_investment.ipynb` | PDD | Pendente |
| `notebooks/08_gold_model.ipynb` | Dimensões e fatos | Pendente |
| `notebooks/09_gold_rankings.ipynb` | Métricas de evolução e rankings | Pendente |
| `notebooks/10_analysis.ipynb` | Perguntas e reconciliações | Pendente |
| `notebooks/11_data_catalog.ipynb` | COMMENTs no Unity Catalog | Pendente |
| `reference/` | De-paras em CSV | Pendente |
| `docs/screenshots.md` | Catálogo de evidências | Atualizado |
| `docs/img/<notebook>/` | Evidências por notebook | 3 capturas e 1 HTML |
| `md/01_projeto_mvp.md` | Este documento | Atualizado |
| `md/sessions.md` | Registro de decisões da sessão (fora do versionamento) | Em uso |

Fora do versionamento, por `.gitignore`: `data/raw/`, `aux_files/`, `data_dictionary/`, `material_didatico/`, `md/sessions.md`, `src/aneel_download.py` e qualquer `.parquet`.

---

## 10. Convenções

- Conversa em português; código, variáveis e comentários de código em inglês.
- Markdown dos notebooks e COMMENTs do Unity Catalog em português.
- Notebooks em `.ipynb`.
- Nomes completos de objetos sempre no formato `mvp_aneel.<schema>.<tabela>`.
- Commits no padrão `feat:`/`fix:`/`docs:`, com Summary e Description, incluindo resultados de testes.
- Fluxo de versionamento: editar localmente, commitar e empurrar pelo GitHub Desktop, e apenas puxar no Databricks. Sentido único de edição por arquivo.
- Evidências: exportação do notebook em HTML conta como evidência de execução completa; capturas pontuais em `docs/img/<notebook>/`, com índice em `docs/screenshots.md`.
- Prefixos de seção para evidências: `01-contexto`, `02-carga`, `03-modelagem`, `04-pipeline`, `05-qualidade`, `06-analise`, `07-autoavaliacao`.
- De-paras em `reference/`, carregados na Bronze como `ref_*`; Silver reporta códigos sem correspondência.
- Autoavaliação distribuída: cada notebook encerra com a sua, e a autoavaliação final consolida. Altera a estrutura sugerida pelo curso, com a justificativa registrada no notebook 00.
- Decisões são registradas em `md/sessions.md` durante a sessão, com `what`, `why`, `how`, `destino` e `status`, e consolidadas neste documento ao final.
- Camadas: Bronze preserva o dado como publicado, sem correção de tipo nem de duplicata; Silver limpa, tipa e padroniza; Gold modela e calcula.

---

## 11. Especificação: títulos obrigatórios do README e critérios

| Título no README | Critério (peso) | Status |
|---|---|---|
| Contexto de Negócios e Perguntas (Etapa 2 e 4.1) | Objetivo (1,0) | Concluído no notebook 00 |
| Carga dos Dados (Etapa 4.2) | Coleta (0,5) | Concluído; licenças registradas automaticamente |
| Modelagem e Catálogo de Dados (Etapa 4.3) | Modelagem (2,0) | Não iniciada |
| Pipeline de Dados (Etapa 4.4) | Carga e Pipeline (1,0) | Bronze concluída |
| Qualidade de Dados (Etapa 4.5) | Qualidade (1,0) | Achados registrados na seção 6 |
| Análise de Dados (Etapa 4.5) | Análise (2,0) | Métricas definidas |
| Autoavaliação | Autoavaliação (0,5) | Distribuída por notebook; 00 e 02 escritas |
| — | Capricho (2,0) | Contínuo |

Exigências formais: repositório público; screenshots do catálogo, das tabelas persistidas e das respostas; vídeos não aceitos; Google Colab zera a nota.

---

## 12. Cronograma

| Período | Entrega | Status |
|---|---|---|
| 10–13/09 | Objetivo final; setup; teste ANEEL; Bronze | Concluído |
| 14–17/09 | Qualidade na Bronze; validações pendentes; Silver (sessão de dúvidas 16/09) | Próximo |
| 18–21/09 | Gold (dimensões, fatos, métricas, rankings); catálogo no Unity Catalog | Pendente |
| 22–25/09 | Análises e gráficos (sessão de dúvidas 23/09) | Pendente |
| 26/09 | README, screenshots, autoavaliação consolidada | Pendente |
| 27/09 | Folga e entrega | — |

---

## 13. Próximos passos

1. Construir `03_bronze_data_quality`: perfil por atributo das 9 tabelas, com atenção à string vazia no leiaute de 2026 e às três parcelas de tempo.
2. Validar o de-para entre `emergency_occurrences_v1` e `_v2` olhando os valores, e fechar a pendência 15.
3. Comparar as duas últimas versões do Módulo 6 do PRODIST para datar a mudança de leiaute.
4. Converter os arquivos de `aux_files` para CSV em `reference/`, com normalização do CNPJ e documentação de origem.
5. Transcrever o Anexo 8.C para `reference/ref_fato_gerador.csv`.
6. Resolver a pendência 17, comparando os universos das duas bases de serviços comerciais.
7. Resolver a pendência 1, identificando as parcelas do DEC no domínio de indicadores.
