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

    # Índices de cada dimensão (ajustados para base 1 → subtrai-se 1 para usar como índice Python)
    indices_ee = [1, 2, 3, 6, 8, 13, 14, 16, 21]
    indices_dp = [5, 11, 12, 15, 22]
    indices_rp = [4, 7, 9, 10, 17, 18, 19, 20]

    # Corrigir para base 0 do Python
    indices_ee = [i - 1 for i in indices_ee]
    indices_dp = [i - 1 for i in indices_dp]
    indices_rp = [i - 1 for i in indices_rp]

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

# Perguntas atualizadas
perguntas = [
    "Eu me sinto emocionalmente exausto pelo meu trabalho.",
    "Eu me sinto esgotado ao final de um dia de trabalho.",
    "Eu me sinto cansado quando me levanto de manhã e tenho que encarar outro dia de trabalho.",
    "Eu posso entender facilmente o que sentem os meus pacientes acerca das coisas que acontecem no dia a dia.",
    "Eu sinto que eu trato alguns dos meus pacientes como se eles fossem objetos.",
    "Trabalhar com pessoas o dia inteiro é realmente um grande esforço pra mim.",
    "Eu trato de forma adequada os problemas dos meus pacientes.",
    "Eu me sinto esgotado com meu trabalho.",
    "Eu sinto que estou influenciando positivamente a vida de outras pessoas através do meu trabalho.",
    "Eu sinto que me tornei mais insensível com as pessoas desde que comecei este trabalho.",
    "Eu sinto que este trabalho está me endurecendo emocionalmente.",
    "Eu me sinto muito cheio de energia.",
    "Eu me sinto muito frustrado com meu trabalho.",
    "Eu sinto que estou trabalhando demais no meu emprego.",
    "Eu não me importo realmente com o que acontece com alguns dos meus pacientes.",
    "Trabalhar diretamente com pessoas me deixa muito estressado.",
    "Eu posso criar facilmente um ambiente tranquilo com os meus pacientes.",
    "Eu me sinto estimulado depois de trabalhar lado a lado com os meus pacientes.",
    "Eu tenho realizado muitas coisas importantes neste trabalho.",
    "No meu trabalho, eu me sinto como se estivesse no final do meu limite.",
    "No meu trabalho eu lido com os problemas emocionais com calma.",
    "Eu sinto que os pacientes me culpam por alguns dos seus problemas."
]

# Entrada de respostas
respostas = []
for i, pergunta in enumerate(perguntas):
    resposta = st.slider(f"{i+1}. {pergunta}", 0, 6, 3)
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
