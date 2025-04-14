import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Avaliação de Burnout",
    page_icon="📚",
    layout="wide"
)

# Função para calcular MBI-HSS para uma lista de respostas
def calcular_mbi_hss(respostas):
    if len(respostas) != 22:
        return None

    indices_ee = [1, 2, 3, 6, 8, 13, 14, 16, 20]
    indices_dp = [5, 10, 11, 15, 22]
    indices_rp = [4, 7, 9, 12, 17, 18, 19, 21]

    indices_ee = [i - 1 for i in indices_ee]
    indices_dp = [i - 1 for i in indices_dp]
    indices_rp = [i - 1 for i in indices_rp]

    def classificar(valor, limites):
        if valor <= limites[0]:
            return "Baixo"
        elif valor <= limites[1]:
            return "Moderado"
        else:
            return "Alto"

    escore_ee = sum(respostas[i] for i in indices_ee)
    escore_dp = sum(respostas[i] for i in indices_dp)
    escore_rp = sum(respostas[i] for i in indices_rp)

    classificacao_ee = classificar(escore_ee, [16, 26])
    classificacao_dp = classificar(escore_dp, [5, 9])
    classificacao_rp = classificar(escore_rp, [31, 38])

    return {
        "Exaustão Emocional": (escore_ee, classificacao_ee),
        "Despersonalização": (escore_dp, classificacao_dp),
        "Realização Pessoal": (escore_rp, classificacao_rp),
    }

# Título da aplicação
st.title("📊 Avaliação de Burnout (MBI-HSS)")

# Seção 1: Autoavaliação
st.header("📍 Autoavaliação Individual")

st.write("Responda cada pergunta selecionando a frequência com que você se sente da forma indicada.")

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

respostas = []
for i, pergunta in enumerate(perguntas):
    resposta = st.slider(f"{i+1}. {pergunta}", 0, 6, 3)
    respostas.append(resposta)

if st.button("Calcular Burnout"):
    resultado = calcular_mbi_hss(respostas)
    
    if resultado:
        st.subheader("📊 Resultados da Avaliação")
        
        for categoria, (escore, nivel) in resultado.items():
            st.write(f"**{categoria}**: {escore} ({nivel})")
        
        if resultado["Exaustão Emocional"][1] == "Alto" and resultado["Despersonalização"][1] == "Alto" and resultado["Realização Pessoal"][1] == "Baixo":
            st.error("⚠️ **Alerta de Burnout**: Seus níveis indicam uma alta possibilidade de burnout.")
        elif resultado["Exaustão Emocional"][1] == "Moderado" or resultado["Despersonalização"][1] == "Moderado":
            st.warning("⚠️ **Sinais Moderados de Burnout**: Algumas dimensões indicam risco. Atenção aos sinais!")
        else:
            st.success("✅ **Sem sinais de Burnout**: Seus resultados indicam baixos níveis de burnout. Continue cuidando do seu bem-estar!")

# Seção 2: Upload de arquivo e análise coletiva
st.header("📁 Análise de Várias Instâncias")

arquivo = st.file_uploader("Envie um arquivo Excel com as respostas de múltiplos profissionais", type=["xlsx"])

if arquivo is not None:
    df = pd.read_excel(arquivo)
    dados = df.iloc[:, 1:]  # remove coluna 'Instância' ou similar

    classificacoes = []
    for _, row in dados.iterrows():
        resultado = calcular_mbi_hss(row.tolist())
        classificacoes.append({
            "EE": resultado["Exaustão Emocional"][1],
            "DP": resultado["Despersonalização"][1],
            "RP": resultado["Realização Pessoal"][1],
        })

    df_result = pd.DataFrame(classificacoes)

    st.subheader("📊 Distribuição das Classificações por Dimensão")
    for dim in ["EE", "DP", "RP"]:
        st.markdown(f"**{dim}**")
        dist = df_result[dim].value_counts().sort_index()
        percent = (dist / len(df_result) * 100).round(2).astype(str) + "%"
        dist_df = pd.DataFrame({
            "Nível": dist.index,
            "n": dist.values,
            "%": percent.values
        })
        st.dataframe(dist_df, use_container_width=True)
