# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

O agente vai realizar o controle de metas financeiras.

### Solução
> Como o agente resolve esse problema de forma proativa?

Para resolver esse problema, o agente vai calcular quanto dinheiro o indivíduo precisa guardar por mês, vai simular cenários, enviar lembretes semanais para o usuário contar para o agente seus gastos semanais.

### Público-Alvo
> Quem vai usar esse agente?

Adultos com renda própria. 

---

## Persona e Tom de Voz

### Nome do Agente
Fernando.

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Direto e objetivo.

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Técnico, formal-mas-não-tanto

### Exemplos de Linguagem
- Saudação: "Olá. Como posso ajudar com suas finanças hoje?"
- Confirmação: "Entendo. Vou verificar isso para você."
- Erro/Limitação: "Desculpe, não tenho essa informação no momento. Você gostaria de ajuda em outro tópico?"

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD

A[Usuário] --> B[Interface do Agente\nApp / Chat / CLI]

B --> C[Processador de Entrada\nLLM / Parser]

C --> D{Tipo de Solicitação}

D --> E[Definir Meta Financeira]
D --> F[Atualizar Gastos Semanais]
D --> G[Solicitar Simulação]
D --> H[Consultar Progresso]

E --> I[Motor de Planejamento Financeiro\nCalcula economia mensal]

F --> J[Gerenciador de Gastos]

G --> K[Motor de Simulação\nCenários de gastos e ganhos]

H --> L[Monitor de Progresso]

I --> M[Banco de Dados\nMetas / Gastos / Histórico]
J --> M
K --> M
L --> M

M --> L

L --> N[Geração de Feedback]

N --> B

M --> O[Serviço de Lembretes Semanais\nScheduler]

O --> P[Notificação ao Usuário\nSolicita atualização de gastos]

P --> B
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | [ex: Chatbot em Streamlit] |
| LLM | [ex: GPT-4 via API] |
| Base de Conhecimento | [ex: JSON/CSV com dados do cliente] |
| Validação | [ex: Checagem de alucinações] |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [ ] [ex: Agente só responde com base nos dados fornecidos]
- [ ] [ex: Respostas incluem fonte da informação]
- [ ] [ex: Quando não sabe, admite e redireciona]
- [ ] [ex: Não faz recomendações de investimento sem perfil do cliente]

### Limitações Declaradas
> O que o agente NÃO faz?

[Liste aqui as limitações explícitas do agente]
