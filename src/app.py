import json
import requests
import streamlit as st
from datetime import datetime

if "acao_pendente" not in st.session_state:
    st.session_state.acao_pendente = None

# CARREGAR DADOS 

def carregar_json(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# GERAR CONTEXTO

def gerar_contexto():
    # Carregar arquivos
    config = carregar_json("config.json")
    gastos = carregar_json("gastos.json") or []
    logs = carregar_json("logs.json") or []
    metas = carregar_json("metas.json") or {}
    ganhos = carregar_json("outros_ganhos.json") or []
    progresso = carregar_json("progresso.json") or {}

    # Funções auxiliares
    def formatar_lista(lista, campos):
        if not lista:
            return "Nenhum registro encontrado."
        
        linhas = []
        for item in lista[-5:]:  # últimos 5 registros
            linha = " - " + " | ".join(f"{campo}: {item.get(campo, '-')}" for campo in campos)
            linhas.append(linha)
        return "\n".join(linhas)

    # Montagem do contexto
    contexto = f"""
DADOS DE CONFIGURAÇÃO:
- Frequência de lembrete: {config.get('frequencia_lembrete', 'N/A') if config else 'N/A'}
- Dia do lembrete: {config.get('dia_lembrete', 'N/A') if config else 'N/A'}

META FINANCEIRA:
- Valor da meta: R$ {metas.get('valor_meta', 'N/A')}
- Prazo (data final): {metas.get('prazo_data', 'N/A')}
- Valor mensal necessário: R$ {metas.get('valor_mensal', 'N/A')}

PROGRESSO:
- Total guardado: R$ {progresso.get('total_guardado', 'N/A')}
- Percentual da meta: {progresso.get('percentual_meta', 'N/A')}%
- Dias restantes: {progresso.get('dias_restantes', 'N/A')}

GASTOS RECENTES:
{formatar_lista(gastos, ['data', 'valor'])}

OUTROS GANHOS:
{formatar_lista(ganhos, ['data', 'valor'])}

LOGS RECENTES:
{formatar_lista(logs, ['data', 'acao'])}
"""

    return contexto.strip()


contexto = gerar_contexto()

# PROMPT PARA O SISTEMA

system_prompt = """Você é o Henrique, um agente financeiro inteligente especializado em metas financeiras.

OBJETIVO:
Fazer o gerenciamento de gastos e ganhos do usuário tendo em vista o cumprimento de uma meta financeira pré-estabelecida pelo usuário.

REGRAS:
- Sempre baseie suas respostas nos dados fornecidos;
- Nunca invente dados;
- Os valores dos gastos, ganhos e metas devem ser todos positivos;
- Linguagem simples e direta;
- Sempre confirme com o usuário a adição e modificação de gastos, ganhos e metas;
- Você não deve fazer cálculos financeiros. Os calculos devem ser feitos via código em Python;
- Respeite o escopo de atuação definido."""

# CHAMAR OLLAMA
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b"

def perguntar(mensagem):
    prompt = f"""
    {system_prompt}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {mensagem}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# PARA ALTERAR OS ARQUIVOS JSON

def registrar_log(acao, detalhes=""):
    logs = carregar_json("logs.json") or []

    novo_log = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "acao": acao,
        "detalhes": detalhes
    }

    logs.append(novo_log)
    salvar_json("logs.json", logs)

def atualizar_progresso():
    gastos = carregar_json("gastos.json") or []
    ganhos = carregar_json("outros_ganhos.json") or []
    metas = carregar_json("metas.json") or {}

    # soma ganhos
    total_ganhos = sum(item["valor"] for item in ganhos)

    # soma gastos
    total_gastos = sum(item["valor"] for item in gastos)

    # total guardado
    total_guardado = total_ganhos - total_gastos

    valor_meta = metas.get("valor_meta", 0)

    if valor_meta > 0:
        percentual = (total_guardado / valor_meta) * 100
    else:
        percentual = 0

    # dias restantes
    prazo = metas.get("prazo_data")
    if prazo:
        data_final = datetime.strptime(prazo, "%Y-%m-%d")
        dias_restantes = (data_final - datetime.now()).days
    else:
        dias_restantes = None

    progresso = {
        "total_guardado": round(total_guardado, 2),
        "percentual_meta": round(percentual, 2),
        "dias_restantes": dias_restantes
    }

    salvar_json("progresso.json", progresso)

def salvar_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def adicionar_gasto(valor, data):
    gastos = carregar_json("gastos.json") or []
    
    novo = {
        "valor": valor,
        "data": data
    }

    gastos.append(novo)
    salvar_json("gastos.json", gastos)

def adicionar_ganho(valor, data):
    ganhos = carregar_json("outros_ganhos.json") or []

    novo = {
        "valor": valor,
        "data": data
    }

    ganhos.append(novo)
    salvar_json("outros_ganhos.json", ganhos)

def atualizar_meta(valor_meta, prazo_data):
    metas = {
        "valor_meta": valor_meta,
        "prazo_data": prazo_data
    }

    salvar_json("metas.json", metas)

def interpretar_acao(mensagem):
    prompt = f"""
Você é um interpretador de comandos para um agente financeiro.

Sua tarefa é analisar a mensagem do usuário e retornar APENAS um JSON válido.

Ações possíveis:
- adicionar_gasto
- adicionar_ganho
- atualizar_meta
- nenhuma

Regras:
- Nunca invente dados
- Se não houver informação suficiente, use null
- Responda SOMENTE JSON (sem texto extra)

Formato:
{{
  "acao": "...",
  "valor": null,
  "data": null,
  "prazo_data": null
}}

Mensagem do usuário:
"{mensagem}"
"""

    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False
        }
    )

    resposta = r.json()['response']

    try:
        return json.loads(resposta)
    except:
        return {"acao": "nenhuma"}

# INTERFACE

st.title("Henrique, o Gerenciador de Metas Financeiras")

if pergunta := st.chat_input("Sobre sua meta financeira..."):
    st.chat_message("user").write(pergunta)

    # 🔹 Se já existe ação pendente (esperando confirmação)
    if st.session_state.acao_pendente:
        if pergunta.lower() in ["sim", "s", "yes"]:
            acao = st.session_state.acao_pendente

            if acao["acao"] == "adicionar_gasto":
                adicionar_gasto(acao["valor"], acao["data"])
                atualizar_progresso()
                registrar_log("adicionar_gasto", f"R${acao['valor']} em {acao['data']}")
                resposta = "Gasto registrado com sucesso! ✅"

            elif acao["acao"] == "adicionar_ganho":
                adicionar_ganho(acao["valor"], acao["data"])
                atualizar_progresso()
                registrar_log("adicionar_ganho", f"R${acao['valor']} em {acao['data']}")
                resposta = "Ganho registrado com sucesso! ✅"

            elif acao["acao"] == "atualizar_meta":
                atualizar_meta(acao["valor"], acao["prazo_data"])
                atualizar_progresso()
                registrar_log("atualizar_meta", f"Meta: R${acao['valor']} até {acao['prazo_data']}")
                resposta = "Meta atualizada com sucesso! 🎯"

            contexto = gerar_contexto()
            # limpar estado
            st.session_state.acao_pendente = None

        else:
            resposta = "Operação cancelada."
            st.session_state.acao_pendente = None

    # 🔹 Nova solicitação
    else:
        acao = interpretar_acao(pergunta)

        if acao["acao"] == "adicionar_gasto":
            resposta = f"""
Você deseja registrar o seguinte gasto?

- Valor: R$ {acao['valor']}
- Data: {acao['data']}

Confirma? (Sim/Não)
"""
            st.session_state.acao_pendente = acao

        elif acao["acao"] == "adicionar_ganho":
            resposta = f"""
Você deseja registrar o seguinte ganho?

- Valor: R$ {acao['valor']}
- Data: {acao['data']}

Confirma? (Sim/Não)
"""
            st.session_state.acao_pendente = acao

        elif acao["acao"] == "atualizar_meta":
            resposta = f"""
Você deseja atualizar sua meta?

- Novo valor: R$ {acao['valor']}
- Nova data: {acao['prazo_data']}

Confirma? (Sim/Não)
"""
            st.session_state.acao_pendente = acao

        else:
            resposta = perguntar(pergunta)

    # 🔹 Atualizar contexto depois de ação

    st.chat_message("assistant").write(resposta)