import streamlit as st
import pandas as pd
import plotly.express as px

# Definir os índices das colunas correspondentes a cada dimensão do MBI-HSS
indices_ee = ["1", "2", "3", "6", "8", "13", "14", "16", "20"]  # Exaustão emocional
indices_dp = ["5", "10", "11", "15", "22"]  # Despersonalização
indices_rp = ["4", "7", "9", "12", "17", "18", "19", "21"]  # Realização pessoal

# Função para calcular os escores do MBI-HSS
def calcular_mbi_hss(row):
    escore_ee = sum(row[col] for col in indices_ee if col in row)
    escore_dp = sum(row[col] for col in indices_dp if col in row)
    escore_rp = sum(row[col] for col in indices_rp if col in row)

    return pd.Series([escore_ee, escore_dp, escore_rp], 
                     index=["Exaustão Emocional", "Despersonalização", "Realização Pessoal"])

# Interface do Streamlit
st.title("📊 Avaliação de Burnout (MBI-HSS)")
st.write("Carregue um arquivo Excel contendo os dados das respostas do questionário MBI-HSS.")

# Upload do arquivo
uploaded_file = st.file_uploader("Faça upload do arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Calcular os escores para cada instância
    df_scores = df.apply(calcular_mbi_hss, axis=1)
    df_scores.insert(0, "Instância", df["Instância"])
    
    # Botão para calcular resultado
    if st.button("Calcular Burnout"):
        st.subheader("📊 Resultados da Avaliação")
        for index, row in df_scores.iterrows():
            st.write(f"**{row['Instância']}**")
            for categoria in ["Exaustão Emocional", "Despersonalização", "Realização Pessoal"]:
                escore = row[categoria]
                st.write(f"**{categoria}**: {escore}")
            
            if row["Exaustão Emocional"] >= 27 and row["Despersonalização"] >= 10 and row["Realização Pessoal"] <= 31:
                st.error("⚠️ **Alerta de Burnout**: Seus níveis indicam uma alta possibilidade de burnout.")
            elif row["Exaustão Emocional"] >= 17 or row["Despersonalização"] >= 6:
                st.warning("⚠️ **Sinais Moderados de Burnout**: Algumas dimensões indicam risco. Atenção aos sinais!")
            else:
                st.success("✅ **Sem sinais de Burnout**: Seus resultados indicam baixos níveis de burnout. Continue cuidando do seu bem-estar!")
    
    # Criar gráficos comparativos
    st.write("### Comparação Gráfica das Dimensões do MBI-HSS")
    df_melted = df_scores.melt(id_vars=["Instância"], var_name="Dimensão", value_name="Pontuação")
    fig = px.bar(df_melted, x="Instância", y="Pontuação", color="Dimensão", 
                 title="Comparação das Dimensões do Burnout por Instância", 
                 barmode="group")
    st.plotly_chart(fig)
    
    # Permitir download dos resultados
    output_file = "resultados_mbi_hss.xlsx"
    df_scores.to_excel(output_file, index=False)
    with open(output_file, "rb") as file:
        st.download_button("📥 Baixar Resultados", file, file_name=output_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

