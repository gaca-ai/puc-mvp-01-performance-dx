"""Central configuration shared by all notebooks of the MVP."""

# Unity Catalog objects: one project catalog with one schema per medallion layer
CATALOG = "mvp_aneel"
SCHEMA_BRONZE = "bronze"
SCHEMA_SILVER = "silver"
SCHEMA_GOLD = "gold"

# Volume that stores raw files before they are loaded into Bronze tables
LANDING_VOLUME = "landing"
LANDING_PATH = f"/Volumes/{CATALOG}/{SCHEMA_BRONZE}/{LANDING_VOLUME}"

# One landing sub-folder per source dataset (folder name -> source description)
SOURCE_FOLDERS = {
    "continuity": "ANEEL - Indicadores Coletivos de Continuidade (DEC e FEC)",
    "voltage_conformity": "ANEEL - Indicadores de Conformidade do Nivel de Tensao em Regime Permanente",
    "emergency_occurrences": "ANEEL - Ocorrencias Emergenciais nas Redes de Distribuicao",
    "commercial_quality": "ANEEL - Qualidade do Atendimento Comercial",
    "indger_commercial": "ANEEL - INDGER - Dados Comerciais",
    "indger_commercial_services": "ANEEL - INDGER - Dados de Servicos Comerciais",
    "complaints": "ANEEL - Manifestacoes no 1o e 2o niveis das Distribuidoras",
    "pdd_investment": "ANEEL - Plano de Desenvolvimento da Distribuicao (PDD)",
    "reference": "Tabelas de-para de autoria propria, derivadas de dados publicos",
}

# ANEEL open data portal (CKAN API)
ANEEL_API_URL = "https://dadosabertos.aneel.gov.br/api/3/action"

# Source catalog: which CKAN dataset feeds which landing folder and Bronze table.
#
# `dataset_id` is the CKAN package id, resolved at runtime through `package_show`
# so that resource URLs and licence terms are always read from the portal instead
# of being hardcoded. `tables` maps a Bronze table name to the resource file names
# that compose it. Emergency occurrences are split into two tables because the
# 2026 publication layout differs from the previous years; harmonising them is
# Silver layer work, not Bronze.
DATASETS = {
    "complaints": {
        "dataset_id": "364859a2-7cb8-45ea-9c88-b4392516a6ba",
        "folder": "complaints",
        "format": "parquet",
        "tables": {
            "complaints": [
                "manifestacoes-1-2-niveis-distribuidora-2023.parquet",
                "manifestacoes-1-2-niveis-distribuidora-2024.parquet",
                "manifestacoes-1-2-niveis-distribuidora-2025.parquet",
                "manifestacoes-1-2-niveis-distribuidora-2026.parquet",
            ],
        },
    },
    "emergency_occurrences": {
        "dataset_id": "ced06b4c-45a5-4cae-8a7e-f576ffc3b412",
        "folder": "emergency_occurrences",
        "format": "parquet",
        "tables": {
            "emergency_occurrences_v1": [
                "ocorrencias-emergenciais-rede-distribuicao-2023.parquet",
                "ocorrencias-emergenciais-rede-distribuicao-2024.parquet",
                "ocorrencias-emergenciais-rede-distribuicao-2025.parquet",
            ],
            "emergency_occurrences_v2": [
                "ocorrencias-emergenciais-rede-distribuicao-2026.parquet",
            ],
        },
    },
    "continuity": {
        "dataset_id": "d5f0712e-62f6-4736-8dff-9991f10758a7",
        "folder": "continuity",
        "format": "parquet",
        "tables": {
            "continuity_indicators": [
                "indicadores-continuidade-coletivos-2020-2029.parquet",
            ],
        },
    },
    "voltage_conformity": {
        "dataset_id": "51f2d7ea-3171-4d22-9115-3384113d01df",
        "folder": "voltage_conformity",
        "format": "parquet",
        "tables": {
            "voltage_conformity": [
                "indicadores-conformidade-nivel-tensao.parquet",
            ],
        },
    },
    "commercial_quality": {
        "dataset_id": "b7b32b0c-4bac-4584-b9ec-76a32c05ca02",
        "folder": "commercial_quality",
        "format": "parquet",
        "tables": {
            "commercial_quality": [
                "qualidade-atendimento-comercial.parquet",
            ],
        },
    },
    "indger_commercial_services": {
        "dataset_id": "7cacb2c4-b165-4591-a793-9ed20d1f167d",
        "folder": "indger_commercial_services",
        "format": "parquet",
        "tables": {
            "indger_commercial_services": [
                "indger-dados-servicos-comerciais.parquet",
            ],
        },
    },
    "indger_commercial": {
        "dataset_id": "7cacb2c4-b165-4591-a793-9ed20d1f167d",
        "folder": "indger_commercial",
        "format": "parquet",
        "tables": {
            "indger_commercial": [
                "indger-dados-comerciais.parquet",
            ],
        },
    },
    "pdd_investment": {
        "dataset_id": "6838f13d-7ea5-4482-a2b9-1515fa56ef42",
        "folder": "pdd_investment",
        "format": "csv",
        "csv_options": {"sep": ";", "encoding": "ISO-8859-1", "header": True},
        "tables": {
            "pdd_investment": [
                "pdd-distribuicao-aneel.csv",
            ],
        },
    },
}

# Columns appended to every Bronze table to preserve ingestion lineage
INGESTION_COLUMNS = ["_source_file", "_ingested_at"]

# Bronze control table holding one row per ingested resource (licence, URL, counts)
INGESTION_LOG_TABLE = "_ingestion_log"
