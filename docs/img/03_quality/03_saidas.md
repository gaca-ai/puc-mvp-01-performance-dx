# Saidas de `03_bronze_data_quality`

Extraido de `03_bronze_data_quality.html`. Gerado por `src/notebook_html_outputs.py`; nao editar a mao.

## 2. Configuração

**Cmd 4** — `import os`

```
Catalogo........: mvp_aneel.bronze
Janela..........: 2023 a 2025 (anos civis)
Tolerancia......: 0.05
```

## 3. Panorama das tabelas Bronze

**Cmd 7** — `tabelas = [r["tableName"] for r in spark.sql(f"SHOW TABLES IN {BRONZE}").collect()`

| colunas | linhas | tabela | tipos |
|---|---|---|---|
| 9 | 1493698 | commercial_quality | bigint:3, double:1, string:4, timestamp:1 |
| 24 | 29260295 | complaints | string:23, timestamp:1 |
| 11 | 5108332 | continuity_indicators | bigint:4, date:1, double:1, string:4, timestamp:1 |
| 17 | 36390229 | emergency_occurrences_v1 | bigint:3, date:1, double:3, string:7, timestamp:1, timestamp_ntz:2 |
| 25 | 6789484 | emergency_occurrences_v2 | string:24, timestamp:1 |
| 65 | 267550 | indger_commercial | bigint:48, date:2, double:9, string:4, timestamp:1, timestamp_ntz:1 |
| 24 | 23922861 | indger_commercial_services | bigint:9, date:2, double:4, string:7, timestamp:1, timestamp_ntz:1 |
| 13 | 5484 | pdd_investment | string:12, timestamp:1 |
| 10 | 5506240 | voltage_conformity | bigint:3, double:1, string:5, timestamp:1 |

### 4.1 Estrutura e domínios

**Cmd 10** — `FONTE = "continuity_indicators"`

```
=== schema ===
  DatGeracaoConjuntoDados    date
  IdeConjUndConsumidoras     bigint
  DscConjUndConsumidoras     string
  SigAgente                  string
  NumCNPJ                    bigint
  SigIndicador               string
  AnoIndice                  bigint
  NumPeriodoIndice           bigint
  VlrIndiceEnviado           double
  _source_file               string
  _ingested_at               timestamp

linhas.....................: 5,108,332
grao conjunto x ano x mes..: 247,261
indicadores por grao.......: 20.7
```

**Cmd 11** — `# Domain of SigIndicador, with volume and coverage per year`

| SigIndicador | linhas | primeiro_ano | ultimo_ano | linhas_com_valor |
|---|---|---|---|---|
| DEC | 247259 | 2020 | 2026 | 246793 |
| DECINC | 247157 | 2020 | 2026 | 77773 |
| DECIND | 247261 | 2020 | 2026 | 246644 |
| DECINE | 247261 | 2020 | 2026 | 93118 |
| DECINO | 247209 | 2020 | 2026 | 3424 |
| DECIP | 247261 | 2020 | 2026 | 195978 |
| DECIPC | 247261 | 2020 | 2026 | 12281 |
| DECXN | 247261 | 2020 | 2026 | 10233 |
| DECXNC | 102694 | 2020 | 2026 | 346 |
| DECXP | 247261 | 2020 | 2026 | 1213 |
| DECXPC | 102786 | 2020 | 2026 | 16 |
| FEC | 247133 | 2020 | 2026 | 246029 |
| FECINC | 247157 | 2020 | 2026 | 72092 |
| FECIND | 247261 | 2020 | 2026 | 245853 |
| FECINE | 247261 | 2020 | 2026 | 87697 |
| FECINO | 247209 | 2020 | 2026 | 3633 |
| FECIP | 247261 | 2020 | 2026 | 174117 |
| FECIPC | 247261 | 2020 | 2026 | 6845 |
| FECXN | 247261 | 2020 | 2026 | 10696 |
| FECXNC | 102694 | 2020 | 2026 | 352 |
| FECXP | 247263 | 2020 | 2026 | 1173 |
| FECXPC | 102637 | 2020 | 2026 | 25 |
| NumCon | 247263 | 2020 | 2026 | 247263 |

**Cmd 12** — `# Period coverage: which months exist in each year`

| AnoIndice | primeiro_mes | ultimo_mes | meses | conjuntos | distribuidoras |
|---|---|---|---|---|---|
| 2020 | 1 | 12 | 12 | 3131 | 101 |
| 2021 | 1 | 12 | 12 | 3131 | 104 |
| 2022 | 1 | 12 | 12 | 3114 | 105 |
| 2023 | 1 | 12 | 12 | 3119 | 103 |
| 2024 | 1 | 12 | 12 | 3132 | 102 |
| 2025 | 1 | 12 | 12 | 3150 | 102 |
| 2026 | 1 | 8 | 8 | 3177 | 102 |

```
[OK      ] Estrutura    cobertura temporal
           Serie de 2020 a 2026. Anos com menos de 12 meses: [2026]. A janela 2023-2025 esta integralmente coberta.
           Tratamento: Anos parciais ficam fora da janela por construcao, ao adotar anos civis completos.
```

### 4.2 Completude:

**Cmd 14** — `# Null count per column`

```
AnoIndice                           0  (0.0000%)
  DatGeracaoConjuntoDados             0  (0.0000%)
  DscConjUndConsumidoras              0  (0.0000%)
  IdeConjUndConsumidoras              0  (0.0000%)
  NumCNPJ                             0  (0.0000%)
  NumPeriodoIndice                    0  (0.0000%)
  SigAgente                           0  (0.0000%)
  SigIndicador                        0  (0.0000%)
  VlrIndiceEnviado                    0  (0.0000%)
  _ingested_at                        0  (0.0000%)
  _source_file                        0  (0.0000%)
[OK      ] Completude   nulos por coluna
           Colunas com nulo: nenhuma.
```

**Cmd 15** — `# Presence of each parcel across the full conjunto x ano x mes grid.`

| AnoIndice | SigIndicador | presentes | grao_total | ausentes | cobertura_pct |
|---|---|---|---|---|---|
| 2023 | DEC | 37421 | 37421 | 0 | 100.0 |
| 2024 | DEC | 37584 | 37584 | 0 | 100.0 |
| 2025 | DEC | 37795 | 37795 | 0 | 100.0 |
| 2023 | DECINC | 37377 | 37421 | 44 | 99.88 |
| 2024 | DECINC | 37584 | 37584 | 0 | 100.0 |
| 2025 | DECINC | 37795 | 37795 | 0 | 100.0 |
| 2023 | DECIND | 37421 | 37421 | 0 | 100.0 |
| 2024 | DECIND | 37584 | 37584 | 0 | 100.0 |
| 2025 | DECIND | 37795 | 37795 | 0 | 100.0 |
| 2023 | DECINE | 37421 | 37421 | 0 | 100.0 |
| 2024 | DECINE | 37584 | 37584 | 0 | 100.0 |
| 2025 | DECINE | 37795 | 37795 | 0 | 100.0 |
| 2023 | DECINO | 37421 | 37421 | 0 | 100.0 |
| 2024 | DECINO | 37584 | 37584 | 0 | 100.0 |
| 2025 | DECINO | 37795 | 37795 | 0 | 100.0 |
| 2023 | DECIP | 37421 | 37421 | 0 | 100.0 |
| 2024 | DECIP | 37584 | 37584 | 0 | 100.0 |
| 2025 | DECIP | 37795 | 37795 | 0 | 100.0 |
| 2023 | DECIPC | 37421 | 37421 | 0 | 100.0 |
| 2024 | DECIPC | 37584 | 37584 | 0 | 100.0 |
| 2025 | DECIPC | 37795 | 37795 | 0 | 100.0 |
| 2023 | DECXN | 37421 | 37421 | 0 | 100.0 |
| 2024 | DECXN | 37584 | 37584 | 0 | 100.0 |
| 2025 | DECXN | 37795 | 37795 | 0 | 100.0 |
| 2023 | DECXNC | 5980 | 37421 | 31441 | 15.98 |

_69 linhas no total; 25 exibidas._

**Cmd 16** — `# Parcels used by the composition must be complete inside the analysis window`

| AnoIndice | SigIndicador | presentes | grao_total | ausentes | cobertura_pct |
|---|---|---|---|---|---|
| 2023 | FECINC | 37377 | 37421 | 44 | 99.88 |
| 2023 | DECINC | 37377 | 37421 | 44 | 99.88 |

```
[ATENCAO ] Completude   presenca das parcelas usadas
           Parcelas avaliadas: ['DECINC', 'DECIND', 'DECINE', 'DECIP', 'FECINC', 'FECIND', 'FECINE', 'FECIP']. Combinacoes conjunto-ano-mes sem a parcela na janela: 2.
           Tratamento: Ausencia tratada como zero: a parcela INC so e informada quando ha Dia Critico, portanto a ausencia da linha equivale a ausencia de evento. Distribuidoras afetadas listadas na celula seguinte, para conferencia contra o publicado.
```

**Cmd 17** — `# Which distributors, years and months are behind the missing parcels.`

| SigAgente | NumCNPJ | SigIndicador | AnoIndice | celulas_ausentes | conjuntos_afetados | meses |
|---|---|---|---|---|---|---|
| EMR | 19527639000158 | FECINC | 2023 | 44 | 44 | [12] |
| EMR | 19527639000158 | DECINC | 2023 | 44 | 44 | [12] |

```
Distribuidoras com parcela ausente: EMR
```

**Cmd 18** — `# NumCon is the weight of the weighted average; it must exist everywhere`

```
grao total.................: 247,261
grao com NumCon............: 247,263
NumCon nulo................: 0
NumCon zero ou negativo....: 0
[PROBLEMA] Completude   NumCon como peso
           NumCon presente em 247,263 de 247,261 combinacoes, com 0 zeros e 0 nulos.
           Tratamento: Conjuntos sem peso valido nao podem ser agregados; definir tratamento.
```

### 4.3 Consistência

**Cmd 20** — `# Published types against the ANEEL data dictionary`

```
NumCNPJ: dicionario string(14), publicado bigint
  IdeConjUndConsumidoras: dicionario string(5), publicado bigint
  AnoIndice: dicionario string(4), publicado bigint
[PROBLEMA] Consistencia tipos contra o dicionario
           3 campos divergem do dicionario: NumCNPJ: dicionario string(14), publicado bigint; IdeConjUndConsumidoras: dicionario string(5), publicado bigint; AnoIndice: dicionario string(4), publicado bigint
           Tratamento: Normalizar na Silver: CNPJ para 14 e conjunto para 5 caracteres, com zeros a esquerda.
```

**Cmd 21** — `# How many identifiers actually lose leading zeros when read as integer`

| len_cnpj | len_conj | count |
|---|---|---|
| 13 | 5 | 3068970 |
| 14 | 3 | 1597 |
| 14 | 4 | 6596 |
| 14 | 5 | 2031169 |

```
[PROBLEMA] Consistencia zeros a esquerda perdidos
           Linhas com CNPJ abaixo de 14 digitos: 3,068,970. Linhas com codigo de conjunto abaixo de 5 digitos: 8,193.
           Tratamento: Aplicar lpad na Silver antes de qualquer juncao por esses campos.
```

**Cmd 22** — `# Label stability: one code should map to one name`

```
conjuntos com mais de um nome....: 0 de 3,980
CNPJs com mais de uma sigla......: 0 de 105
[OK      ] Consistencia estabilidade de rotulos
           0 de 3980 conjuntos tem mais de uma descricao; 0 de 105 CNPJs tem mais de uma sigla.
```

**Cmd 23** — `# NumPeriodoIndice domain`

```
[OK      ] Consistencia dominio de NumPeriodoIndice
           Valores encontrados: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]. Fora do intervalo 1 a 12: nenhum. Confirma granularidade mensal unica, sem coexistencia de trimestral ou anual.
```

**Cmd 24** — `# Restructuring of consumer unit sets: full series from 2022 on.`

| SigAgente | NumCNPJ | mes_ref | qtd_ant | qtd_conjuntos | delta | entrantes | saintes |
|---|---|---|---|---|---|---|---|
| CEMIG-D | 6981180000116 | 2024-01 | 295 | 265 | -30 | 88 | 118 |
| EQUATORIAL PI | 6840748000189 | 2024-01 | 42 | 68 | 26 | 44 | 18 |
| EQUATORIAL MA | 6272793000184 | 2026-01 | 98 | 117 | 19 | 47 | 28 |
| Âmbar Amazonas | 2341467000120 | 2025-01 | 19 | 30 | 11 | 28 | 17 |
| ERO | 5914650000166 | 2024-01 | 26 | 36 | 10 | 27 | 17 |
| EQUATORIAL GO | 1543032000104 | 2024-01 | 156 | 147 | -9 | 19 | 28 |
| EQUATORIAL AL | 12272084000100 | 2025-01 | 38 | 47 | 9 | 26 | 17 |
| COELBA | 15139629000194 | 2024-01 | 203 | 211 | 8 | 55 | 47 |
| Neoenergia PE | 10835932000108 | 2026-01 | 134 | 142 | 8 | 17 | 9 |
| EPB | 9095183000140 | 2024-01 | 67 | 75 | 8 | 8 | 0 |
| EMT | 3467321000199 | 2024-01 | 94 | 88 | -6 | 14 | 20 |
| EMR | 19527639000158 | 2023-01 | 39 | 44 | 5 | 5 | 0 |
| ENEL RJ | 33050071000158 | 2024-01 | 82 | 78 | -4 | 7 | 11 |
| EQUATORIAL PA | 4895728000180 | 2024-01 | 145 | 149 | 4 | 26 | 22 |
| CPFL-PAULISTA | 33050196000188 | 2024-01 | 179 | 176 | -3 | 9 | 12 |
| EDP ES | 28152650000171 | 2023-01 | 41 | 44 | 3 | 24 | 21 |
| EAC | 4065033000170 | 2024-01 | 12 | 15 | 3 | 6 | 3 |
| COSERN | 8324196000181 | 2024-01 | 56 | 59 | 3 | 27 | 24 |
| EPB | 9095183000140 | 2026-01 | 75 | 72 | -3 | 21 | 24 |
| CPFL-PIRATINING | 4172213000151 | 2024-01 | 42 | 45 | 3 | 6 | 3 |
| ÂMBAR ENERGIA RR | 2341470000144 | 2025-01 | 17 | 15 | -2 | 12 | 14 |
| ENEL CE | 7047251000170 | 2024-01 | 113 | 115 | 2 | 7 | 5 |
| ETO | 25086034000171 | 2026-01 | 55 | 57 | 2 | 19 | 17 |
| EDP SP | 2302100000106 | 2024-01 | 48 | 50 | 2 | 28 | 26 |
| ELEKTRO | 2328280000197 | 2024-01 | 128 | 130 | 2 | 13 | 11 |

_33 linhas no total; 25 exibidas._

```
[ATENCAO ] Consistencia reestruturacao de conjuntos
           33 meses com entrada ou saida de conjuntos desde 2022; 27 dentro da janela 2023-2025; 0 fora de janeiro.
           Tratamento: Acumular sempre em dezembro neutraliza o efeito dentro do ano civil. Distribuidoras que reestruturaram exigem cautela na comparacao entre blocos.
```

### 4.4 Unicidade

**Cmd 26** — `chave = ["NumCNPJ", "IdeConjUndConsumidoras", "AnoIndice", "NumPeriodoIndice", "SigIndicad`

| SigAgente | NumCNPJ | IdeConjUndConsumidoras | AnoIndice | NumPeriodoIndice | SigIndicador | ocorrencias | valores_distintos |
|---|---|---|---|---|---|---|---|
| ELEKTRO | 2328280000197 | 15911 | 2025 | 6 | FECXP | 2 | 1 |
| ELEKTRO | 2328280000197 | 13575 | 2025 | 6 | NumCon | 2 | 1 |
| ELEKTRO | 2328280000197 | 13532 | 2025 | 6 | FECXP | 2 | 1 |
| ELEKTRO | 2328280000197 | 17326 | 2025 | 6 | NumCon | 2 | 1 |

```
[PROBLEMA] Unicidade    duplicatas no grao declarado
           4 chaves duplicadas, das quais 4 com valor identico e 0 com valores divergentes.
           Tratamento: Duplicata com valor identico: deduplicar. Com valor divergente: investigar antes de escolher o registro valido.
```

### 4.5 Acurácia:

**Cmd 28** — `# Wide layout: one row per conjunto x ano x mes, one column per indicator.`

```
linhas duplicadas removidas para o pivo: 4
grao conjunto x ano x mes: 247,261 linhas, 27 colunas
```

**Cmd 29** — `def testar_composicao(df, indicador, parcelas, rotulo):`

| indicador | regime | AnoIndice | linhas | aderentes | aderencia_pct | maior_desvio |
|---|---|---|---|---|---|---|
| DEC | ate_2021 | 2020 | 37559 | 37559 | 100.0 | 0.010000000000001563 |
| DEC | ate_2021 | 2021 | 37442 | 37442 | 100.0 | 0.010000000000001563 |
| DEC | desde_2022 | 2022 | 37363 | 37363 | 100.0 | 0.010000000000001563 |
| DEC | desde_2022 | 2023 | 37421 | 37421 | 100.0 | 0.010000000000001563 |
| DEC | desde_2022 | 2024 | 37584 | 37584 | 100.0 | 0.010000000000001563 |
| DEC | desde_2022 | 2025 | 37795 | 37795 | 100.0 | 0.010000000000001563 |
| DEC | desde_2022 | 2026 | 22097 | 22095 | 99.99 | 0.91 |
| FEC | ate_2021 | 2020 | 37559 | 37559 | 100.0 | 0.010000000000000675 |
| FEC | ate_2021 | 2021 | 37442 | 37442 | 100.0 | 0.019999999999999796 |
| FEC | desde_2022 | 2022 | 37363 | 37363 | 100.0 | 0.010000000000000675 |
| FEC | desde_2022 | 2023 | 37421 | 37421 | 100.0 | 0.010000000000000675 |
| FEC | desde_2022 | 2024 | 37584 | 37584 | 100.0 | 0.010000000000000675 |
| FEC | desde_2022 | 2025 | 37795 | 37672 | 99.67 | 1.32 |
| FEC | desde_2022 | 2026 | 22097 | 22097 | 100.0 | 0.010000000000000675 |

**Cmd 30** — `# Detail of the rows that do not adhere, under the regime in force since 2022`

| SigAgente | NumCNPJ | AnoIndice | NumPeriodoIndice | indicador | conjuntos | dif_min | dif_max |
|---|---|---|---|---|---|---|---|
| ELEKTRO | 2328280000197 | 2025 | 6 | FEC | 123 | 0.06 | 1.32 |
| DCELT | 83855973000130 | 2026 | 7 | DEC | 1 | 0.91 | 0.91 |
| UHENPAL | 89889604000144 | 2026 | 7 | DEC | 1 | 0.9 | 0.9 |

```
[PROBLEMA] Acuracia     composicao normativa do DEC e do FEC
           Regime desde 2022 (IND + IP): 125 combinacoes conjunto-ano-mes em que a soma das parcelas difere do consolidado publicado em mais de 0.05.
           Tratamento: Compor o indicador sempre a partir das parcelas. O consolidado da ANEEL serve apenas como conferencia, com tolerancia de arredondamento.
```

**Cmd 31** — `# Does the divergence reach the universe of interest? Concentration matters more`

| SigAgente | linhas | conjuntos | meses | maior_desvio |
|---|---|---|---|---|
| ELEKTRO | 123 | 123 | 1 | 1.32 |
| UHENPAL | 1 | 1 | 1 | 0.9 |
| DCELT | 1 | 1 | 1 | 0.91 |

### 4.6 Outliers

**Cmd 33** — `# Impossible values`

```
[OK      ] Outliers     valores impossiveis
           Colunas com valor negativo: nenhuma. Linhas com NumCon menor ou igual a zero: 0.
```

**Cmd 34** — `# Distribution of the own indicator, DEC-FI, inside the analysis window`

| dec_fi_media | dec_fi_mediana | dec_fi_p99 | dec_fi_max | fec_fi_media | fec_fi_mediana | fec_fi_p99 | fec_fi_max |
|---|---|---|---|---|---|---|---|
| 1.8154 | 0.9 | 13.79 | 481.28 | 0.6665 | 0.42 | 3.84 | 16.9 |

```
[OK      ] Outliers     concentracao nos extremos
           O 1% de combinacoes com maior DEC-FI (acima de 13.79 h) responde por 11.9% da duracao total ponderada da janela.
           Tratamento: Extremos sao mantidos: temporal severo produz DEC alto e legitimo. A concentracao e reportada para dimensionar a sensibilidade do ranking.
```

**Cmd 35** — `# Missing months inside a year distort the twelve month accumulation`

| SigAgente | AnoIndice | conjuntos_incompletos | menor_cobertura |
|---|---|---|---|
| COPREL | 2023 | 2 | 9 |
| CASTRO-DIS | 2025 | 1 | 11 |
| CERAL ANITÁPOLIS | 2025 | 1 | 10 |
| Ceraçá | 2025 | 1 | 11 |
| CERIPa | 2025 | 1 | 11 |
| CERAL ANITÁPOLIS | 2023 | 1 | 11 |

```
[ATENCAO ] Outliers     meses faltantes no ano civil
           7 de 9,401 combinacoes conjunto-ano tem menos de 12 meses na janela.
           Tratamento: Conjunto com ano incompleto tem acumulado subestimado. Definir na Silver se e excluido do bloco ou anualizado.
```

### 4.7 Síntese: problemas encontrados e tratamentos definidos

**Cmd 37** — `display(resumo_achados(FONTE))`

```
continuity_indicators: 14 verificacoes
  OK         6
  ATENCAO    3
  PROBLEMA   5
```

| criterio | detalhe | fonte | status | teste | tratamento |
|---|---|---|---|---|---|
| Estrutura | Serie de 2020 a 2026. Anos com menos de 12 meses: [2026]. A janela 2023-2025 esta integralmente coberta. | continuity_indicators | OK | cobertura temporal | Anos parciais ficam fora da janela por construcao, ao adotar anos civis completos. |
| Completude | Colunas com nulo: nenhuma. | continuity_indicators | OK | nulos por coluna |  |
| Completude | Parcelas avaliadas: ['DECINC', 'DECIND', 'DECINE', 'DECIP', 'FECINC', 'FECIND', 'FECINE', 'FECIP']. Combinacoes conjunto-ano-mes sem a parcela na janela: 2. | continuity_indicators | ATENCAO | presenca das parcelas usadas | Ausencia tratada como zero: a parcela INC so e informada quando ha Dia Critico, portanto a ausencia da linha equivale a ausencia de evento. Distribuidoras afetadas listadas na celula seguinte, para conferencia contra o publicado. |
| Completude | NumCon presente em 247,263 de 247,261 combinacoes, com 0 zeros e 0 nulos. | continuity_indicators | PROBLEMA | NumCon como peso | Conjuntos sem peso valido nao podem ser agregados; definir tratamento. |
| Consistencia | 3 campos divergem do dicionario: NumCNPJ: dicionario string(14), publicado bigint; IdeConjUndConsumidoras: dicionario string(5), publicado bigint; AnoIndice: dicionario string(4), publicado bigint | continuity_indicators | PROBLEMA | tipos contra o dicionario | Normalizar na Silver: CNPJ para 14 e conjunto para 5 caracteres, com zeros a esquerda. |
| Consistencia | Linhas com CNPJ abaixo de 14 digitos: 3,068,970. Linhas com codigo de conjunto abaixo de 5 digitos: 8,193. | continuity_indicators | PROBLEMA | zeros a esquerda perdidos | Aplicar lpad na Silver antes de qualquer juncao por esses campos. |
| Consistencia | 0 de 3980 conjuntos tem mais de uma descricao; 0 de 105 CNPJs tem mais de uma sigla. | continuity_indicators | OK | estabilidade de rotulos |  |
| Consistencia | Valores encontrados: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]. Fora do intervalo 1 a 12: nenhum. Confirma granularidade mensal unica, sem coexistencia de trimestral ou anual. | continuity_indicators | OK | dominio de NumPeriodoIndice |  |
| Consistencia | 33 meses com entrada ou saida de conjuntos desde 2022; 27 dentro da janela 2023-2025; 0 fora de janeiro. | continuity_indicators | ATENCAO | reestruturacao de conjuntos | Acumular sempre em dezembro neutraliza o efeito dentro do ano civil. Distribuidoras que reestruturaram exigem cautela na comparacao entre blocos. |
| Unicidade | 4 chaves duplicadas, das quais 4 com valor identico e 0 com valores divergentes. | continuity_indicators | PROBLEMA | duplicatas no grao declarado | Duplicata com valor identico: deduplicar. Com valor divergente: investigar antes de escolher o registro valido. |
| Acuracia | Regime desde 2022 (IND + IP): 125 combinacoes conjunto-ano-mes em que a soma das parcelas difere do consolidado publicado em mais de 0.05. | continuity_indicators | PROBLEMA | composicao normativa do DEC e do FEC | Compor o indicador sempre a partir das parcelas. O consolidado da ANEEL serve apenas como conferencia, com tolerancia de arredondamento. |
| Outliers | Colunas com valor negativo: nenhuma. Linhas com NumCon menor ou igual a zero: 0. | continuity_indicators | OK | valores impossiveis |  |
| Outliers | O 1% de combinacoes com maior DEC-FI (acima de 13.79 h) responde por 11.9% da duracao total ponderada da janela. | continuity_indicators | OK | concentracao nos extremos | Extremos sao mantidos: temporal severo produz DEC alto e legitimo. A concentracao e reportada para dimensionar a sensibilidade do ranking. |
| Outliers | 7 de 9,401 combinacoes conjunto-ano tem menos de 12 meses na janela. | continuity_indicators | ATENCAO | meses faltantes no ano civil | Conjunto com ano incompleto tem acumulado subestimado. Definir na Silver se e excluido do bloco ou anualizado. |
