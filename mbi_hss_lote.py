import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Avaliação de Burnout (MBI-HSS)", page_icon="📚", layout="wide")

# Índices das colunas correspondentes a cada dimensão do MBI-HSS (nomes de colunas como strings)
indices_ee = ["1", "2", "3", "6", "8", "13", "14", "16", "21"]  # Exaustão emocional
indices_dp = ["5", "11", "12", "15", "22"]                      # Despersonalização
indices_rp = ["4", "7", "9", "10", "17", "18", "19", "20"]      # Realização pessoal

# Função para cálculo e classificação
def calcular_mbi_hss(row):
    escore_ee = sum(row[col] for col in indices_ee if col in row)
    escore_dp = sum(row[col] for col in indices_dp if col in row)
    escore_rp = sum(row[col] for col in indices_rp if col in row)

    def classificar(valor, limites):
        if valor <= limites[0]:
            return "Baixo"
        elif valor <= limites[1]:
            return "Moderado"
        else:
            return "Alto"

    nivel_ee = classificar(escore_ee, [16, 26])
    nivel_dp = classificar(escore_dp, [5, 9])
    nivel_rp = classificar(escore_rp, [31, 38])

    return pd.Series([escore_ee, nivel_ee, escore_dp, nivel_dp, escore_rp, nivel_rp],
                     index=["Exaustão Emocional", "Nível EE", "Despersonalização", "Nível DP", "Realização Pessoal", "Nível RP"])

# Título da aplicação
st.title("📊 Avaliação de Burnout (MBI-HSS)")
st.write("Carregue um arquivo Excel com as respostas dos participantes ao questionário MBI-HSS.")
st.write("As colunas devem ser nomeadas de '1' a '22', cada uma representando uma pergunta.")

# Upload do arquivo
uploaded_file = st.file_uploader("📁 Faça upload do arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df_scores = df.apply(calcular_mbi_hss, axis=1)
    df_scores.insert(0, "Instância", df["Instância"] if "Instância" in df.columns else df.index + 1)

    if st.button("Calcular Burnout"):
        st.subheader("📄 Resultados Individuais")

        alertas = []
        for _, row in df_scores.iterrows():
            st.markdown(f"### {row['Instância']}")
            st.write(f"**Exaustão Emocional**: {row['Exaustão Emocional']} ({row['Nível EE']})")
            st.write(f"**Despersonalização**: {row['Despersonalização']} ({row['Nível DP']})")
            st.write(f"**Realização Pessoal**: {row['Realização Pessoal']} ({row['Nível RP']})")

            if row["Nível EE"] == "Alto" and row["Nível DP"] == "Alto" and row["Nível RP"] == "Baixo":
                st.error("⚠️ **Alerta de Burnout**: Alta possibilidade de burnout.")
                alertas.append("Alto Risco")
            elif row["Nível EE"] == "Moderado" or row["Nível DP"] == "Moderado":
                st.warning("⚠️ **Sinais Moderados de Burnout**: Algumas dimensões indicam risco.")
                alertas.append("Risco Moderado")
            else:
                st.success("✅ **Sem sinais de Burnout**: Baixos níveis em todas as dimensões.")
                alertas.append("Baixo Risco")

        df_scores["Classificação Final"] = alertas

        # Gráfico de barras
        st.subheader("📊 Gráfico Comparativo das Dimensões")
        df_melted = df_scores[["Instância", "Exaustão Emocional", "Despersonalização", "Realização Pessoal"]].melt(
            id_vars=["Instância"], var_name="Dimensão", value_name="Pontuação")
        fig = px.bar(df_melted, x="Instância", y="Pontuação", color="Dimensão", barmode="group",
                     title="Comparação das Dimensões do Burnout por Instância")
        st.plotly_chart(fig)

        # Frequência por dimensão
        st.subheader("📊 Distribuição por Dimensão (n e %)")
        for dim, col in [("EE", "Nível EE"), ("DP", "Nível DP"), ("RP", "Nível RP")]:
            dist = df_scores[col].value_counts().sort_index()
            percent = (dist / len(df_scores) * 100).round(2).astype(str) + "%"
            df_dist = pd.DataFrame({
                "Nível": dist.index,
                "n": dist.values,
                "%": percent.values
            })
            st.markdown(f"**{dim}**")
            st.dataframe(df_dist, use_container_width=True)

        # Relatório final
        st.subheader("📝 Relatório dos Achados")
        total = len(df_scores)
        alto = alertas.count("Alto Risco")
        moderado = alertas.count("Risco Moderado")
        baixo = alertas.count("Baixo Risco")

        st.markdown(f"""
        - **Total de participantes avaliados:** {total}
        - **Alta possibilidade de burnout:** {alto} ({(alto/total)*100:.1f}%)
        - **Risco moderado:** {moderado} ({(moderado/total)*100:.1f}%)
        - **Sem sinais de burnout:** {baixo} ({(baixo/total)*100:.1f}%)

        ### Instruções e Recomendações
        - Participantes com **alto risco** devem ser acompanhados por profissionais da saúde mental.
        - Participantes com **risco moderado** devem receber orientação preventiva.
        - Participantes **sem sinais de burnout** devem manter hábitos saudáveis.
        """)

        # Exportar Excel
        output_file = "resultados_mbi_hss_classificados.xlsx"
        df_scores.to_excel(output_file, index=False)
        with open(output_file, "rb") as file:
            st.download_button("📥 Baixar Resultados em Excel", file, file_name=output_file,
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
