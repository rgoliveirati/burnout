import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Avaliação de Burnout (MBI-HSS)", page_icon="📚", layout="wide")

# Índices das colunas correspondentes a cada dimensão do MBI-HSS
indices_ee = ["1", "2", "3", "6", "8", "13", "14", "16", "20"]  # Exaustão emocional
indices_dp = ["5", "10", "11", "15", "22"]  # Despersonalização
indices_rp = ["4", "7", "9", "12", "17", "18", "19", "21"]  # Realização pessoal

# Função para calcular e classificar os escores
def calcular_mbi_hss(row):
    escore_ee = sum(row[col] for col in indices_ee if col in row)
    escore_dp = sum(row[col] for col in indices_dp if col in row)
    escore_rp = sum(row[col] for col in indices_rp if col in row)

    def classificar(valor, limites):
        if valor <= limites[0]:
            return "Baixo"
        elif limites[0] < valor <= limites[1]:
            return "Moderado"
        else:
            return "Alto"

    nivel_ee = classificar(escore_ee, [16, 26])
    nivel_dp = classificar(escore_dp, [5, 9])
    nivel_rp = classificar(escore_rp, [31, 38])

    return pd.Series([escore_ee, nivel_ee, escore_dp, nivel_dp, escore_rp, nivel_rp],
                     index=["Exaustão Emocional", "Nível EE", "Despersonalização", "Nível DP", "Realização Pessoal", "Nível RP"])

# Interface do Streamlit
st.title("📊 Avaliação de Burnout (MBI-HSS)")
st.write("Carregue um arquivo Excel contendo os dados das respostas do questionário MBI-HSS.")

# Upload do arquivo
uploaded_file = st.file_uploader("Faça upload do arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Calcular escores e classificações
    df_scores = df.apply(calcular_mbi_hss, axis=1)
    df_scores.insert(0, "Instância", df["Instância"])
    
    # Botão para calcular resultado
    if st.button("Calcular Burnout"):
        st.subheader("📊 Resultados da Avaliação")

        for index, row in df_scores.iterrows():
            st.write(f"**{row['Instância']}**")
            st.write(f"**Exaustão Emocional**: {row['Exaustão Emocional']} ({row['Nível EE']})")
            st.write(f"**Despersonalização**: {row['Despersonalização']} ({row['Nível DP']})")
            st.write(f"**Realização Pessoal**: {row['Realização Pessoal']} ({row['Nível RP']})")

            if row["Nível EE"] == "Alto" and row["Nível DP"] == "Alto" and row["Nível RP"] == "Baixo":
                st.error("⚠️ **Alerta de Burnout**: Alta possibilidade de burnout.")
            elif row["Nível EE"] == "Moderado" or row["Nível DP"] == "Moderado":
                st.warning("⚠️ **Sinais Moderados de Burnout**: Algumas dimensões indicam risco.")
            else:
                st.success("✅ **Sem sinais de Burnout**: Baixos níveis em todas as dimensões.")

        # Gráfico de barras
        st.write("### Comparação Gráfica das Dimensões do MBI-HSS")
        df_melted = df_scores[["Instância", "Exaustão Emocional", "Despersonalização", "Realização Pessoal"]] \
            .melt(id_vars=["Instância"], var_name="Dimensão", value_name="Pontuação")
        fig = px.bar(df_melted, x="Instância", y="Pontuação", color="Dimensão", 
                     title="Comparação das Dimensões do Burnout por Instância", barmode="group")
        st.plotly_chart(fig)

        # Download dos resultados
        output_file = "resultados_mbi_hss_classificados.xlsx"
        df_scores.to_excel(output_file, index=False)
        with open(output_file, "rb") as file:
            st.download_button("📥 Baixar Resultados", file, file_name=output_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
