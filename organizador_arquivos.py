"""
Organizador Inteligente de Diretórios com Log de Auditoria

"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path
from typing import Dict, List

CATEGORIAS: Dict[str, List[str]] = {
    "Documentos_PDF_Texto": [".pdf", ".doc", ".docx", ".txt", ".md"],
    "Planilhas_Dados": [".csv", ".xlsx", ".xls", ".json", ".sql"],
    "Imagens_Midia": [".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"],
    "Codigo_Scripts": [".py", ".java", ".js", ".html", ".css", ".dart"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
}


def identificar_categoria(extensao: str) -> str:
    ext = extensao.lower()
    for pasta, extensoes in CATEGORIAS.items():
        if ext in extensoes:
            return pasta
    return "Outros_Arquivos"


def organizar_diretorio(diretorio_alvo: Path, dry_run: bool = True) -> List[str]:
    acoes: List[str] = []
    if not diretorio_alvo.exists() or not diretorio_alvo.is_dir():
        raise FileNotFoundError(f"Diretório não encontrado: {diretorio_alvo}")

    for item in sorted(diretorio_alvo.iterdir()):
        if item.is_dir() or item.name.startswith("."):
            continue

        pasta_destino = diretorio_alvo / identificar_categoria(item.suffix)
        caminho_final = pasta_destino / item.name

        if dry_run:
            acoes.append(f"[SIMULAÇÃO] Moveria '{item.name}' -> '{pasta_destino.name}/'")
        else:
            pasta_destino.mkdir(exist_ok=True)
            shutil.move(str(item), str(caminho_final))
            acoes.append(f"[MOVIDO] '{item.name}' -> '{pasta_destino.name}/'")

    return acoes


def main() -> None:
    parser = argparse.ArgumentParser(description="Organizador automático de arquivos por extensão.")
    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Caminho do diretório que deseja organizar (padrão: diretório atual)",
    )
    parser.add_argument(
        "--executar",
        action="store_true",
        help="Executa a movimentação real (sem essa flag, roda apenas em modo simulação seguro)",
    )
    args = parser.parse_args()

    alvo = Path(args.dir).resolve()
    modo_simulacao = not args.executar

    print(f"=== Organizador de Arquivos | Alvo: {alvo} ===")
    acoes = organizar_diretorio(alvo, dry_run=modo_simulacao)

    if not acoes:
        print("Nenhum arquivo solto encontrado para organizar.")
        return

    for linha in acoes:
        print(linha)

    horario = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nTotal de arquivos analisados: {len(acoes)} ({horario})")


if __name__ == "__main__":
    main()
