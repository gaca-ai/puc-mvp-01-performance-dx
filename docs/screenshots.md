# Catálogo de Screenshots

Evidências visuais referenciadas no README. Todas as imagens ficam em `docs/img/`.

## Convenção de nomes

Formato: `<seção>_<origem>_<seq>_<assunto>.png`

| Parte | Regra | Exemplo |
|---|---|---|
| `seção` | Prefixo da seção do README (tabela abaixo) | `02-carga` |
| `origem` | Notebook (`nb00`, `nb01`, ...) ou interface visual (`ui`) | `nb00` |
| `seq` | Sequência de dois dígitos dentro da mesma seção e origem | `01` |
| `assunto` | Descrição curta, palavras separadas por hífen | `schemas` |

Regras gerais:

- minúsculas, sem acentos e sem espaços, para garantir os links no GitHub;
- capturar somente após execução completa e bem-sucedida do notebook;
- se o notebook mudar, recapturar as evidências dele e atualizar a data.

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

Campo "Capturado em" vazio indica evidência pendente.

| Arquivo | Seção | Origem | O que evidencia | Capturado em |
|---|---|---|---|---|
| `02-carga_nb00_01_schemas_volume.png` | 02-carga | `00_setup`, seção 6 | Schemas `bronze`, `silver` e `gold` criados no catálogo `mvp_aneel`; Volume `landing` criado no schema `bronze`  |10/09/2026|
| `02-carga_nb00_02_landing-folders.png` | 02-carga | `00_setup`, seção 6 | Pastas de landing, uma por fonte de dados |10/09/2026|
| `02-carga_ui_01_catalog-explorer.png` | 02-carga | Catalog Explorer | Catálogo `mvp_aneel` e seus schemas na interface do Unity Catalog |10/09/2026|
