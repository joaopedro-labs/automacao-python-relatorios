"""
Automação de Coleta de Dados via API, Análise Inteligente e Geração de Relatórios

"""

from __future__ import annotations

import csv
import datetime as dt
import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List

API_URL = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
OUTPUT_DIR = Path(__file__).parent / "relatorios_gerados"


def buscar_cotacoes() -> Dict[str, Any]:
    """Busca cotações atualizadas na API REST ou retorna dados de contingência."""
    try:
        req = urllib.request.Request(
            API_URL,
            headers={"User-Agent": "JoaoPedroLabs-Automation/1.0"},
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            dados = json.loads(response.read().decode("utf-8"))
            print("[OK] Dados coletados com sucesso da API em tempo real.")
            return dados
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"[AVISO] Sem conexão com a API ({exc}). Utilizando dados locais de simulação.")
        agora = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "USDBRL": {
                "code": "USD",
                "codein": "BRL",
                "name": "Dólar Americano/Real Brasileiro",
                "bid": "5.42",
                "high": "5.47",
                "low": "5.39",
                "pctChange": "0.65",
                "create_date": agora,
            },
            "EURBRL": {
                "code": "EUR",
                "codein": "BRL",
                "name": "Euro/Real Brasileiro",
                "bid": "5.89",
                "high": "5.93",
                "low": "5.85",
                "pctChange": "-0.32",
                "create_date": agora,
            },
            "BTCBRL": {
                "code": "BTC",
                "codein": "BRL",
                "name": "Bitcoin/Real Brasileiro",
                "bid": "485200.00",
                "high": "492000.00",
                "low": "478500.00",
                "pctChange": "2.14",
                "create_date": agora,
            },
        }


def gerar_insight_ia_heuristico(item: Dict[str, Any]) -> str:
    """Classifica automaticamente a tendência do ativo com base na variação percentual."""
    variacao = float(item.get("pctChange", 0.0))
    nome = item.get("code", "Ativo")

    if variacao >= 1.5:
        return f"Alta expressiva (+{variacao:.2f}%): {nome} apresenta forte pressão compradora no período."
    if variacao > 0:
        return f"Leve alta (+{variacao:.2f}%): {nome} mantém estabilidade positiva no dia."
    if variacao <= -1.5:
        return f"Queda acentuada ({variacao:.2f}%): momento favorável para monitorar janelas de compra em {nome}."
    if variacao < 0:
        return f"Leve recuo ({variacao:.2f}%): oscilação normal de mercado para {nome}."
    return f"Estável (0.00%): {nome} sem alteração relevante na sessão."


def processar_dados(dados_brutos: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Transforma o JSON bruto da API em registros estruturados com análise."""
    registros: List[Dict[str, Any]] = []
    for chave, info in dados_brutos.items():
        cotacao_atual = float(info.get("bid", 0.0))
        maxima = float(info.get("high", 0.0))
        minima = float(info.get("low", 0.0))
        variacao = float(info.get("pctChange", 0.0))

        registros.append(
            {
                "par": chave,
                "moeda": info.get("name", chave),
                "cotacao_brl": round(cotacao_atual, 2),
                "minima_brl": round(minima, 2),
                "maxima_brl": round(maxima, 2),
                "variacao_pct": round(variacao, 2),
                "analise_automatica": gerar_insight_ia_heuristico(info),
                "atualizado_em": info.get("create_date", ""),
            }
        )
    return registros


def exportar_csv(registros: List[Dict[str, Any]], caminho_csv: Path) -> None:
    """Salva os registros processados em formato CSV compatível com Excel."""
    if not registros:
        return
    campos = list(registros[0].keys())
    with caminho_csv.open("w", newline="", encoding="utf-8-sig") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
        writer.writeheader()
        writer.writerows(registros)
    print(f"[OK] Planilha CSV exportada em: {caminho_csv}")


def exportar_markdown(registros: List[Dict[str, Any]], caminho_md: Path) -> None:
    """Gera um relatório executivo em Markdown pronto para documentação ou envio."""
    data_geracao = dt.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    linhas = [
        "# 📊 Relatório Automatizado de Indicadores e Cotações",
        f"**Gerado automaticamente em:** {data_geracao}  ",
        "**Autor do Script:** João Pedro Araujo dos Santos (`joaopedro-labs`)",
        "",
        "## 1. Tabela Resumo de Cotações (BRL)",
        "",
        "| Par | Ativo | Cotação (R$) | Mínima (R$) | Máxima (R$) | Variação (%) |",
        "| :--- | :--- | ---: | ---: | ---: | ---: |",
    ]

    for reg in registros:
        sinal = "+" if reg["variacao_pct"] > 0 else ""
        linhas.append(
            f"| `{reg['par']}` | {reg['moeda']} | R$ {reg['cotacao_brl']:,.2f} | "
            f"R$ {reg['minima_brl']:,.2f} | R$ {reg['maxima_brl']:,.2f} | "
            f"{sinal}{reg['variacao_pct']:.2f}% |"
        )

    linhas.extend(
        [
            "",
            "## 2. Diagnóstico e Insights Automatizados",
            "",
        ]
    )

    for reg in registros:
        linhas.append(f"- **{reg['moeda']}**: {reg['analise_automatica']}")

    caminho_md.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"[OK] Relatório Markdown exportado em: {caminho_md}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dados_brutos = buscar_cotacoes()
    registros = processar_dados(dados_brutos)

    caminho_csv = OUTPUT_DIR / "relatorio_cotacoes.csv"
    caminho_md = OUTPUT_DIR / "relatorio_executivo.md"

    exportar_csv(registros, caminho_csv)
    exportar_markdown(registros, caminho_md)
    print("\nAutomação concluída com sucesso!")


if __name__ == "__main__":
    main()
