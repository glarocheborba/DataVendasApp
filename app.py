import pandas as pd
import streamlit as st
import plotly.express as px



#Lendo arquivos
df_vendas = pd.read_excel("Vendas.xlsx")
df_produtos = pd.read_excel("Produtos.xlsx")

#merge
df = pd.merge(df_vendas,df_produtos, how="left", on="ID Produto")

#Novas colunas
df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
df["Lucro"] = df["Valor Venda"] - df["Custo"]
df["mes_ano"] = df["Data Venda"].dt.to_period("M").astype(str)

#Agrupamentos    
produtos_vendidos_marca = df.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
lucro_categoria = df.groupby("Categoria")["Lucro"].sum().reset_index()


def main():

    st.title("Análise de Vendas")
    st.image("vendas.png")

    total_custo = (df["Custo"].sum()).astype(str)
    total_custo = total_custo.replace(".", ",")
    total_custo = "R$" + total_custo[:2] + "." + total_custo[2:5] + "." + total_custo[5:]

    lucro = (df["Lucro"].sum()).astype(str)
    lucro = lucro.replace(".", ",")
    lucro = "R$" + lucro[:2] + "." + lucro[2:5] + "." + lucro[5:]

    st.markdown(
    """
    <style>
    [data-testid="stMetricValue] {
        font-size: 25px;        
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    col1, col2 , col3=  st.columns(3)
    with col1:
        st.metric("Total Custo", total_custo)
    with col2:
        st.metric("Lucro", lucro)
    with col3:
        st.metric("Total Clientes", df["ID Cliente"].nunique())

    col1, col2 = st.columns(2)

    fig = px.bar(produtos_vendidos_marca, x='Quantidade', y='Marca', orientation="h", width=380, height=400, title="Total Produtos vendidos por Marca")
    col1.plotly_chart(fig)

    fig1 = px.pie(lucro_categoria, values='Lucro', names='Categoria', width=450, height=400, title="Lucro por categoria")
    col2.plotly_chart(fig1)

if __name__=='__main__':
    main()