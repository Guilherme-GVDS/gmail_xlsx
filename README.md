# gmail_xlsx_sync

Script CLI em Python para buscar anexos `.xlsx` no Gmail por assunto e
concatenar os dados em uma planilha base.

## Pré-requisitos

-   Python 3.13
-   Conta Google com Gmail habilitado
-   Acesso ao Google Cloud Console

## Configuração

1.  Crie e ative um ambiente virtual.
2.  Instale as dependências:

``` bash
pip install -r requirements.txt
```

3.  Crie credenciais OAuth2 no Google Cloud Console:
    -   Crie um projeto (ou selecione um existente).
    -   Ative a **Gmail API**.
    -   Configure a tela de consentimento OAuth.
    -   Crie um OAuth Client ID do tipo **Desktop app**.
    -   Baixe as credenciais e salve como `credentials.json` na raiz do
        projeto. (ou configure `GOOGLE_CREDENTIALS_PATH` no `.env`).
4.  Copie `.env.example` para `.env` e configure os valores:

``` dotenv
ASSUNTO=Relatorio Financeiro Mensal
BASE_SPREADSHEET_PATH=core/base.xlsx
DOWNLOADS_DIR=downloads
PROCESSED_IDS_FILE=processed_ids.txt
KEEP_DOWNLOADS=true
GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_TOKEN_PATH=token.json
```

5.  Garanta que `core/base.xlsx` exista com as colunas esperadas de
    saída.

6.  Execute `python main.py` uma vez para completar a autenticação OAuth
    no navegador e gerar o arquivo `token.json`. Nas próximas execuções
    o token será reutilizado automaticamente.

## Execução

``` bash
python main.py
```
