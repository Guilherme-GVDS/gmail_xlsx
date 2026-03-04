# 05 - Estrutura Planejada

> Documento de referência da estrutura **planejada no PRD**. Esta estrutura ainda não está implementada no repositório atual.

## Diretórios e arquivos esperados

- `core/`: configuração, logger e planilha base.
- `gmail/`: autenticação OAuth2, cliente e busca de e-mails.
- `spreadsheet/`: download, processamento e merge de planilhas.
- `downloads/`: anexos baixados temporariamente.
- `logs/`: arquivos de log.
- `main.py`: orquestração do fluxo principal.
- `processed_ids.txt`: controle de e-mails já processados.

## Fluxo macro previsto

1. Carregar `.env`.
2. Autenticar Gmail API.
3. Buscar e-mails por assunto.
4. Baixar anexos `.xlsx`.
5. Filtrar colunas com base em `core/base.xlsx`.
6. Concatenar e salvar base atualizada.
7. Marcar e-mails processados e registrar logs.
