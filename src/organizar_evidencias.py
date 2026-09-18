"""
Evidence catalog manager: renames screenshots and regenerates the Markdown index.

The catalog lives in docs/screenshots.xlsx, which is the single source of truth and the
file meant to be edited by hand. Each row describes one piece of evidence: the target
file name following the project convention, the folder it belongs to, what it proves,
and the original file name as produced by the capture tool.

Workflow
--------
1. Capture the screenshots. They land in the inbox folder with arbitrary names such as
   "Captura de tela 2026-09-15 143022.png".
2. Open docs/screenshots.xlsx and fill `nome_original_arquivo` on the matching rows.
3. Run this script. It moves and renames each file into its target folder, records the
   capture date, and rewrites docs/screenshots.md from the spreadsheet.

Running it again is safe: rows whose target file already exists are skipped.

Usage
-----
    python organizar_evidencias.py --check       # report status, change nothing
    python organizar_evidencias.py               # rename pending files and rebuild the index
    python organizar_evidencias.py --only nb03   # restrict to rows whose origem matches
    python organizar_evidencias.py --inbox "C:/Users/gaca/Pictures/Screenshots"

Requirements: pandas, openpyxl
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

import pandas as pd

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOGO = REPO_ROOT / "docs" / "screenshots.xlsx"
INDICE_MD = REPO_ROOT / "docs" / "screenshots.md"
INBOX_PADRAO = REPO_ROOT / "docs" / "img" / "_inbox"

ABA = "evidencias"

COLUNAS = [
    "arquivo_destino",
    "pasta_destino",
    "secao_readme",
    "origem",
    "prioridade",
    "o_que_evidencia",
    "nome_original_arquivo",
    "capturado_em",
]

SECOES_README = {
    "01-contexto": "Contexto de Negócios e Perguntas (Etapa 2 e 4.1)",
    "02-carga": "Carga dos Dados (Etapa 4.2)",
    "03-modelagem": "Modelagem e Catálogo de Dados (Etapa 4.3)",
    "04-pipeline": "Pipeline de Dados (Etapa 4.4)",
    "05-qualidade": "Qualidade de Dados (Etapa 4.5)",
    "06-analise": "Análise de Dados (Etapa 4.5)",
    "07-autoavaliacao": "Autoavaliação",
}


# --------------------------------------------------------------------------
# Catalog
# --------------------------------------------------------------------------

def carregar_catalogo() -> pd.DataFrame:
    """Read the spreadsheet and validate its columns."""
    if not CATALOGO.exists():
        raise SystemExit(f"ERRO: catalogo nao encontrado em {CATALOGO}")

    df = pd.read_excel(CATALOGO, sheet_name=ABA, dtype=str).fillna("")
    faltando = [c for c in COLUNAS if c not in df.columns]
    if faltando:
        raise SystemExit(f"ERRO: colunas ausentes no catalogo: {faltando}")

    df["arquivo_destino"] = df["arquivo_destino"].str.strip()
    df["pasta_destino"] = df["pasta_destino"].str.strip().str.replace("\\", "/", regex=False)
    df["nome_original_arquivo"] = df["nome_original_arquivo"].str.strip()
    return df[df["arquivo_destino"] != ""].reset_index(drop=True)


def salvar_catalogo(df: pd.DataFrame) -> None:
    """Write the spreadsheet back, preserving column widths and the frozen header."""
    with pd.ExcelWriter(CATALOGO, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=ABA, index=False)
        planilha = writer.sheets[ABA]
        larguras = {"A": 46, "B": 32, "C": 14, "D": 9, "E": 13, "F": 95, "G": 38, "H": 14}
        for coluna, largura in larguras.items():
            planilha.column_dimensions[coluna].width = largura
        planilha.freeze_panes = "A2"


# --------------------------------------------------------------------------
# File handling
# --------------------------------------------------------------------------

def localizar_origem(nome: str, inbox: Path) -> Path | None:
    """Find the captured file, accepting either a bare name or a full path."""
    candidato = Path(nome)
    if candidato.is_absolute() and candidato.exists():
        return candidato

    direto = inbox / nome
    if direto.exists():
        return direto

    # Tolerate a missing or different extension
    for encontrado in inbox.glob(f"{candidato.stem}.*"):
        return encontrado
    return None


def processar(df: pd.DataFrame, inbox: Path, filtro: str | None, simular: bool) -> pd.DataFrame:
    """Move and rename every pending row that has an original file name filled in."""
    hoje = datetime.now().strftime("%d/%m/%Y")
    movidos = pendentes = ausentes = prontos = 0

    for posicao, linha in df.iterrows():
        if filtro and filtro.lower() not in str(linha["origem"]).lower():
            continue

        destino = REPO_ROOT / linha["pasta_destino"] / linha["arquivo_destino"]
        original = linha["nome_original_arquivo"]

        if destino.exists() and not original:
            prontos += 1
            continue

        if not original:
            pendentes += 1
            print(f"  PENDENTE   {linha['arquivo_destino']}")
            continue

        # Already renamed in a previous run: the name in the catalog matches the target
        if original == linha["arquivo_destino"] and destino.exists():
            prontos += 1
            continue

        fonte = localizar_origem(original, inbox)

        # The file may already sit in the target folder under its original name
        if fonte is None:
            alternativa = REPO_ROOT / linha["pasta_destino"] / original
            fonte = alternativa if alternativa.exists() else None

        if fonte is None:
            ausentes += 1
            print(f"  AUSENTE    {original}  ->  {linha['arquivo_destino']}")
            continue

        print(f"  MOVER      {fonte.name}  ->  {linha['pasta_destino']}/{linha['arquivo_destino']}")
        if not simular:
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(fonte), str(destino))
            df.at[posicao, "nome_original_arquivo"] = linha["arquivo_destino"]
            if not str(linha["capturado_em"]).strip():
                df.at[posicao, "capturado_em"] = hoje
        movidos += 1

    print(f"\n  movidos {movidos} | ja prontos {prontos} | "
          f"sem captura {pendentes} | arquivo nao encontrado {ausentes}")
    return df


# --------------------------------------------------------------------------
# Markdown index
# --------------------------------------------------------------------------

def gerar_indice(df: pd.DataFrame) -> str:
    """Rebuild docs/screenshots.md from the spreadsheet."""
    linhas = [
        "# Catálogo de Evidências",
        "",
        "Arquivo gerado por `src/organizar_evidencias.py` a partir de `docs/screenshots.xlsx`.",
        "Não editar à mão: alterações se perdem na próxima execução do script.",
        "",
        "As imagens ficam em `docs/img/<notebook>/`, uma subpasta por notebook de origem.",
        "",
        "## Convenção de nomes",
        "",
        "Formato: `<seção>_<origem>_<seq>_<assunto>.png`, em minúsculas, sem acentos e sem",
        "espaços, para garantir os links no GitHub. A origem é o notebook (`nb00`, `nb01`,",
        "`nb02`, ...) ou a interface visual (`ui`).",
        "",
        "A exportação do notebook em HTML conta como evidência da execução completa e",
        "dispensa capturar cada saída em separado. As capturas listadas aqui são as que",
        "sustentam pontos específicos do README.",
        "",
        "| Prefixo | Seção do README |",
        "|---|---|",
    ]
    for prefixo, titulo in SECOES_README.items():
        linhas.append(f"| `{prefixo}` | {titulo} |")

    total = len(df)
    capturadas = int((df["capturado_em"].str.strip() != "").sum())
    linhas += [
        "",
        "## Índice",
        "",
        f"{capturadas} de {total} evidências capturadas. "
        "Campo \"Capturado em\" vazio indica evidência pendente.",
        "",
    ]

    for pasta, grupo in df.groupby("pasta_destino", sort=True):
        linhas += [
            f"### `{pasta}`",
            "",
            "| Arquivo | Seção | Prioridade | O que evidencia | Capturado em |",
            "|---|---|---|---|---|",
        ]
        for _, r in grupo.sort_values("arquivo_destino").iterrows():
            caminho = f"{pasta}/{r['arquivo_destino']}".replace("docs/", "")
            data = r["capturado_em"].strip() or " "
            linhas.append(
                f"| `{caminho}` | {r['secao_readme']} | {r['prioridade']} | "
                f"{r['o_que_evidencia']} | {data} |"
            )
        linhas.append("")

    pendentes = df[df["capturado_em"].str.strip() == ""]
    essenciais = pendentes[pendentes["prioridade"] == "essencial"]
    if len(essenciais):
        linhas += [
            "## Pendentes essenciais",
            "",
            "Evidências marcadas como essenciais e ainda não capturadas:",
            "",
        ]
        for _, r in essenciais.sort_values("arquivo_destino").iterrows():
            linhas.append(f"- `{r['arquivo_destino']}` — {r['o_que_evidencia']}")
        linhas.append("")

    return "\n".join(linhas)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organiza as evidencias visuais e regenera o indice em Markdown.")
    parser.add_argument("--inbox", default=str(INBOX_PADRAO),
                        help="pasta onde as capturas sao depositadas")
    parser.add_argument("--only", metavar="TEXTO",
                        help="restringe as linhas cuja coluna origem contenha o texto")
    parser.add_argument("--check", action="store_true",
                        help="apenas relata a situacao, sem mover nem gravar")
    args = parser.parse_args()

    inbox = Path(args.inbox)
    inbox.mkdir(parents=True, exist_ok=True)

    df = carregar_catalogo()
    print(f"Catalogo...: {CATALOGO}")
    print(f"Inbox......: {inbox}")
    print(f"Evidencias.: {len(df)}\n")

    df = processar(df, inbox, args.only, simular=args.check)

    if args.check:
        print("\nModo --check: nada foi movido nem gravado.")
        return

    salvar_catalogo(df)
    INDICE_MD.write_text(gerar_indice(df), encoding="utf-8")
    print(f"\nCatalogo atualizado: {CATALOGO}")
    print(f"Indice regenerado..: {INDICE_MD}")


if __name__ == "__main__":
    main()
