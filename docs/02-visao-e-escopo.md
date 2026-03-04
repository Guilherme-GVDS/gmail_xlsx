# 02 - Visão e Escopo

## Visão do projeto

`gmail_xlsx_sync` é um script CLI em Python para:

- autenticar na Gmail API via OAuth2;
- buscar e-mails por assunto (`ASSUNTO`);
- baixar anexos `.xlsx`;
- consolidar dados na planilha base `core/base.xlsx`.

## Escopo funcional definido no PRD

- Autenticação com reutilização de `token.json`.
- Busca por assunto com query nativa (`subject:VALOR`).
- Processamento de anexos apenas `.xlsx`.
- Concatenação usando apenas colunas existentes na base.
- Registro de operações em `logs/app.log`.
- Controle de idempotência para não reprocessar e-mails.

## Fora de escopo

- Interface gráfica.
- Framework web (ex.: Django).
- Componentes não necessários ao fluxo principal.
