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
    "indger_commercial": "ANEEL - INDGER - Dados Comerciais",
    "indger_commercial_services": "ANEEL - INDGER - Dados de Servicos Comerciais",
    "complaints": "ANEEL - Manifestacoes no 1o e 2o niveis das Distribuidoras",
    "pdd_investment": "ANEEL - Plano de Desenvolvimento da Distribuicao (PDD)",
    "reference": "Tabelas de-para de autoria propria, derivadas de dados publicos",
}

# ANEEL open data portal (CKAN API)
ANEEL_API_URL = "https://dadosabertos.aneel.gov.br/api/3/action"
