# 03 - Guidelines de Implementação

Estas diretrizes vêm do PRD e devem guiar a implementação.

## Princípios

- Código simples, direto e sem over-engineering.
- Organização por responsabilidade (config, auth, fetch, download, processamento, merge).
- Tratamento de erros sem interromper o processamento dos demais e-mails.

## Regras de implementação

- Ler configuração via `.env`.
- Validar entradas obrigatórias no início da execução.
- Processar apenas e-mails ainda não processados.
- Ignorar silenciosamente colunas que não existam na base.
- Registrar logs com nível, timestamp, módulo e mensagem.

## Segurança

- Nunca versionar `credentials.json`, `token.json` e `.env`.
- Manter credenciais fora do código-fonte.
