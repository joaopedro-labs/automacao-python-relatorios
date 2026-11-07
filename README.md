# ⚙️ Automação em Python: Coleta via API, Relatórios Executivos & Organização de Arquivos

Repositório de scripts práticos em **Python 3** desenvolvidos por **João Pedro Araujo dos Santos** ([`@joaopedro-labs`](https://github.com/joaopedro-labs)) para automatizar tarefas recorrentes de coleta de dados, geração de relatórios analíticos e organização de diretórios sem necessidade de bibliotecas pesadas externas.

## 🚀 Scripts Incluídos

### 1. `automacao_relatorio.py` — Coleta de API REST + Geração de Relatórios (CSV & Markdown)
Consome dados de cotações em tempo real via API REST pública (`AwesomeAPI`), aplica regras de classificação automática de tendência e exporta:
- **`relatorios_gerados/relatorio_cotacoes.csv`**: Planilha pronta para abrir no Excel / LibreOffice / Google Sheets.
- **`relatorios_gerados/relatorio_executivo.md`**: Resumo executivo formatado com tabela e diagnóstico automático de variação.
- Possui **fallback inteligente offline**: caso seja executado em um ambiente sem internet, gera o relatório com dados de simulação para testes.

```bash
python automacao_relatorio.py
```

### 2. `organizador_arquivos.py` — Organizador de Diretórios com Modo Simulação (`--dry-run`)
Classifica arquivos soltos em pastas temáticas (`Documentos_PDF_Texto`, `Planilhas_Dados`, `Imagens_Midia`, `Codigo_Scripts`, `Compactados`).
Por segurança, roda em **modo simulação** por padrão e só move os arquivos quando a flag `--executar` é informada:

```bash
# Modo simulação (mostra o que seria feito sem alterar nada)
python organizador_arquivos.py --dir ./caminho

# Execução real
python organizador_arquivos.py --dir ./caminho --executar
```

## 🛠️ Tecnologias Utilizadas
- **Python 3.10+** (`urllib.request`, `json`, `csv`, `pathlib`, `argparse`, `shutil`, `datetime`, `typing`)
- Zero dependências externas (roda nativamente em Windows, Linux Ubuntu e macOS).
