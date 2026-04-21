import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página para focar no celular
st.set_page_config(page_title="Estética Registro", page_icon="✨", layout="centered")

# Estilo para deixar os botões maiores e com a cor dourada que você gostou
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        background-color: #D4AF37;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("LANÇAMENTO DE FLUXO")

arquivo = "dados_estetica.csv"

# Carregar dados
if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)
else:
    df = pd.DataFrame(columns=['Data', 'Descrição', 'Categoria', 'Profissional', 'Tipo', 'Valor'])

# --- INTERFACE DIRETA (IGUAL AO CUSTOMTKINTER) ---
# Usamos um formulário que limpa os dados automaticamente ao enviar
with st.form("meu_formulario", clear_on_submit=True):
    
    desc = st.text_input("Descrição (ex: Limpeza de Pele)")
    
    cat = st.selectbox("Escolha a Categoria", 
                      ["Serviço", "Produtos", "Aluguel Máquina", "Estacionamento", "Água/Luz"])
    
    prof = st.text_input("Profissional (Deixe vazio se for gasto)")
    
    tipo = st.radio("Tipo", ["Entrada", "Saída"], horizontal=True)
    
    valor_texto = st.text_input("Valor (Ex: 150.00)")

    # Botão de Salvar grande
    enviado = st.form_submit_button("SALVAR NO SISTEMA")

    if enviado:
        if desc and valor_texto:
            try:
                valor_float = float(valor_texto.replace(",", "."))
                
                nova_linha = {
                    'Data': datetime.now().strftime("%d/%m/%Y"),
                    'Descrição': desc,
                    'Categoria': cat,
                    'Profissional': prof if prof else "-",
                    'Tipo': tipo,
                    'Valor': valor_float
                }
                
                # Salvar no arquivo
                df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
                df.to_csv(arquivo, index=False)
                
                st.success("✅ Dados salvos com sucesso!")
                # O formulário vai limpar os campos automaticamente aqui
            except ValueError:
                st.error("❌ Por favor, digite um valor numérico válido.")
        else:
            st.warning("⚠️ Preencha a descrição e o valor.")

# --- RESUMO RÁPIDO ABAIXO ---
st.divider()
faturamento = df[df['Tipo'] == 'Entrada']['Valor'].sum()
gastos = df[df['Tipo'] == 'Saída']['Valor'].sum()
st.metric("Saldo Atual", f"R$ {faturamento - gastos:,.2f}")

# Link para ver o histórico em outra aba se precisar
if st.checkbox("Ver últimos lançamentos"):
    st.dataframe(df.tail(5), use_container_width=True)
