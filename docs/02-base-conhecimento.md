# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `config.json` | JSON | Configurações dos lembretes do agente |
| `gastos.json` | JSON | Armazena os gastos do usuário |
| `logs.json` | JSON | Histórico de ações |
| `metas.json` | JSON | Armazena a meta financeira do usuário |
| `outros_ganhos.json` | JSON | Armazena outros ganhos monetários (fora da renda mensal) do usuário |
| `perfil.json` | JSON | Armazena informações básicas do usuário |
| `progresso.json` | JSON | Armazena o estado atual da meta do usuário |



> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Eu inclui dados novos relacionados ao funcionamento do meu agente quanto à meta financeira, e removi dados que o meu agente não vai utilizar, como os relacionados a investimentos

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.
```python
import json

with open('config.json','r',encoding='utf-8') as f:
  perfil = json.load(f)
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

No prompt, os dados vão ser consultados dinamicamente e somente as informações necessárias serão inseridas no prompt no momento da requisição. 

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Usuário:
- Nome: João Silva
- Idade: 25
- Profissão: Estudante
- Renda mensal: R$ 2.500
- Patrimônio inicial: R$ 1.000

Meta Financeira:
- Valor da meta: R$ 10.000
- Prazo: 10 meses
- Valor necessário por mês: R$ 900

Progresso Atual:
- Total guardado: R$ 2.400
- Percentual da meta: 24%
- Meses restantes: 6

Resumo de Gastos Recentes:
- 01/04/2026: R$ 250
- 08/04/2026: R$ 300
- 15/04/2026: R$ 200

...
```
