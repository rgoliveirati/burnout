import streamlit as st

st.set_page_config(
    page_title="Avaliação de Burnout",
    page_icon="📚",
    layout="wide"
)


# Função para calcular MBI-HSS
def calcular_mbi_hss(respostas):
    if len(respostas) != 22:
        st.error("A lista de respostas deve conter exatamente 22 valores.")
        return None

    # Índices de cada dimensão
    indices_ee = [0, 1, 2, 5, 7, 12, 13, 15, 19]  # Exaustão emocional
    indices_dp = [4, 9, 10, 14, 21]              # Despersonalização
    indices_rp = [3, 6, 8, 11, 16, 17, 18, 20]   # Realização pessoal

    # Cálculo das pontuações
    escore_ee = sum(respostas[i] for i in indices_ee)
    escore_dp = sum(respostas[i] for i in indices_dp)
    escore_rp = sum(respostas[i] for i in indices_rp)

    # Classificação dos escores
    def classificar(valor, limites):
        if valor <= limites[0]:
            return "Baixo"
        elif limites[0] < valor <= limites[1]:
            return "Moderado"
        else:
            return "Alto"

    classificacao_ee = classificar(escore_ee, [16, 26])
    classificacao_dp = classificar(escore_dp, [5, 9])
    classificacao_rp = classificar(escore_rp, [31, 38])

    return {
        "Exaustão Emocional": (escore_ee, classificacao_ee),
        "Despersonalização": (escore_dp, classificacao_dp),
        "Realização Pessoal": (escore_rp, classificacao_rp),
    }

# Interface Streamlit
st.title("📊 Avaliação de Burnout (MBI-HSS)")

st.write("O questionário abaixo mede três dimensões do burnout: **Exaustão Emocional, Despersonalização e Realização Pessoal**.")
st.write("Responda cada pergunta selecionando a frequência com que você se sente da forma indicada.")

# Criar lista de respostas
respostas = []
perguntas = [
    "Sinto-me emocionalmente exausto(a) pelo meu trabalho.",
    "Sinto-me esgotado(a) no final de um dia de trabalho.",
    "Sinto-me cansado(a) ao acordar e ter que enfrentar mais um dia de trabalho.",
    "Sinto que posso ajudar as pessoas de maneira eficaz no trabalho.",
    "Sinto que trato algumas pessoas como se fossem objetos.",
    "Sinto que o trabalho está me desgastando.",
    "Sinto que consigo lidar bem com os problemas emocionais no trabalho.",
    "Sinto que estou no meu limite emocional.",
    "Sinto que inspiro confiança nos meus colegas e pacientes.",
    "Sinto-me indiferente com algumas pessoas no trabalho.",
    "Sinto que estou me tornando insensível ao lidar com as pessoas.",
    "Sinto-me realizado(a) ao trabalhar diretamente com as pessoas.",
    "Sinto que estou consumido(a) pelo meu trabalho.",
    "Sinto que não posso mais continuar do jeito que estou.",
    "Sinto que trato as pessoas de forma fria ou impessoal.",
    "Sinto que estou no meu limite de trabalho.",
    "Sinto que consigo lidar eficazmente com os problemas que surgem no trabalho.",
    "Sinto que estou ajudando as pessoas da melhor maneira possível.",
    "Sinto-me bem ao ajudar outras pessoas.",
    "Sinto que o meu trabalho está me desgastando emocionalmente.",
    "Sinto-me feliz ao realizar um bom trabalho.",
    "Sinto que as pessoas me deixam irritado(a) com seus problemas."
]

# Criar sliders para entrada de respostas
for i, pergunta in enumerate(perguntas):
    resposta = st.slider(f"{i+1}. {pergunta}", 0, 6, 3)  # Valor inicial = 3 (neutro)
    respostas.append(resposta)

# Botão para calcular resultado
if st.button("Calcular Burnout"):
    resultado = calcular_mbi_hss(respostas)
    
    if resultado:
        st.subheader("📊 Resultados da Avaliação")
        
        for categoria, (escore, nivel) in resultado.items():
            st.write(f"**{categoria}**: {escore} ({nivel})")
        
        # Avaliação final do Burnout
        if resultado["Exaustão Emocional"][1] == "Alto" and resultado["Despersonalização"][1] == "Alto" and resultado["Realização Pessoal"][1] == "Baixo":
            st.error("⚠️ **Alerta de Burnout**: Seus níveis indicam uma alta possibilidade de burnout.")
        elif resultado["Exaustão Emocional"][1] == "Moderado" or resultado["Despersonalização"][1] == "Moderado":
            st.warning("⚠️ **Sinais Moderados de Burnout**: Algumas dimensões indicam risco. Atenção aos sinais!")
        else:
            st.success("✅ **Sem sinais de Burnout**: Seus resultados indicam baixos níveis de burnout. Continue cuidando do seu bem-estar!")

