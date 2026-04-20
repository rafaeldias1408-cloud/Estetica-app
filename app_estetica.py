import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página para celular
st.set_page_config(page_title="Estética Pro", page_icon="✨")

st.title("✨ Gestão Estética")

# Arquivo onde os dados serão salvos
arquivo = "dados_estetica.csv"

# Carregar dados existentes
if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)
else:
    df = pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Profissional', 'Tipo', 'Valor'])

# --- MENU LATERAL PARA LANÇAMENTOS ---
st.sidebar.header("➕ Novo Registro")
with st.sidebar.form("novo_registro"):
    desc = st.text_input("Descrição (Ex: Limpeza de Pele)")
    cat = st.selectbox("Categoria", ["Serviço", "Produtos", "Aluguel Máquina", "Estacionamento", "Água/Luz"])
    prof = st.text_input("Profissional (se for serviço)")
    tipo = st.radio("Tipo", ["Entrada", "Saída"])
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    
    salvar = st.form_submit_button("Salvar")

if salvar:
    nova_linha = {
        'Data': datetime.now().strftime("%d/%m/%Y"),
        'Descrição': desc,
        'Categoria': cat,
        'Profissional': prof if prof else "-",
        'Tipo': tipo,
        'Valor': valor
    }
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    df.to_csv(arquivo, index=False)
    st.sidebar.success("Salvo!")
    st.rerun()

# --- PAINEL DE RESULTADOS ---
st.subheader("📊 Resumo Financeiro")
faturamento = df[df['Tipo'] == 'Entrada']['Valor'].sum()
gastos = df[df['Tipo'] == 'Saída']['Valor'].sum()
lucro = faturamento - gastos

c1, c2, c3 = st.columns(3)
c1.metric("Faturamento", f"R$ {faturamento:,.2f}")
c2.metric("Gastos", f"R$ {gastos:,.2f}")
c3.metric("Lucro", f"R$ {lucro:,.2f}")

st.write("### 📝 Últimos Lançamentos")
st.dataframe(df.tail(10), use_container_width=True)

# Botão para baixar a planilha
st.download_button("📥 Baixar Planilha", df.to_csv(index=False).encode('utf-8'), "financas.csv", "text/csv")
