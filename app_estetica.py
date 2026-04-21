import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página para Celular
st.set_page_config(page_title="Estética Letícia", page_icon="✨", layout="centered")

# Estilo para botões grandes e cores do seu código original
st.markdown("""
    <style>
    div.stButton > button { width: 100%; height: 50px; font-weight: bold; border-radius: 10px; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ REGISTRO ESTÉTICA")

arquivo = "dados_estetica.csv"

# --- FUNÇÕES DE DADOS ---
def carregar_dados():
    if os.path.exists(arquivo):
        return pd.read_csv(arquivo)
    return pd.DataFrame(columns=['Data', 'Mes', 'Descrição', 'Categoria', 'Profissional', 'Valor Bruto', 'Comissão Paga', 'Líquido Estética'])

df = carregar_dados()

# --- FORMULÁRIO DE LANÇAMENTO ---
with st.form("registro_form", clear_on_submit=True):
    desc = st.text_input("Descrição (ex: Limpeza de Pele)")
    cat = st.selectbox("Categoria", ["Serviço", "Produtos", "Aluguel Máquina", "Aluguel (Inc. Água)", "Luz"])
    prof = st.text_input("Profissional (quem fez o serviço)")
    tipo = st.radio("Tipo", ["Entrada", "Saída"], horizontal=True)
    valor_texto = st.text_input("Valor Bruto (Ex: 150.00)")
    
    btn_salvar = st.form_submit_button("SALVAR NO SISTEMA")

if btn_salvar:
    if desc and valor_texto:
        try:
            bruto = float(valor_texto.replace(",", "."))
            profissional = prof.strip().capitalize()
            mes_atual = datetime.now().strftime("%m/%Y")
            
            comissao_paga = 0
            liquido_empresa = bruto

            if tipo == "Entrada" and cat == "Serviço":
                if profissional != "Leticia":
                    comissao_paga = bruto * 0.30
                    liquido_empresa = bruto - comissao_paga
            
            if tipo == "Saída":
                liquido_empresa = -bruto

            nova_linha = {
                'Data': datetime.now().strftime("%d/%m %H:%M"),
                'Mes': mes_atual,
                'Descrição': desc,
                'Categoria': cat,
                'Profissional': profissional if profissional else "-",
                'Valor Bruto': bruto,
                'Comissão Paga': comissao_paga,
                'Líquido Estética': liquido_empresa
            }
            
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
            df.to_csv(arquivo, index=False)
            st.success("✅ Dados salvos!")
            st.rerun()
        except:
            st.error("❌ Erro no valor. Use apenas números e ponto.")

# --- RELATÓRIO MENSAL (BOTÃO AZUL) ---
st.divider()
mes_atual = datetime.now().strftime("%m/%Y")
df_mes = df[df['Mes'] == mes_atual] if not df.empty else df

if not df_mes.empty:
    faturamento = df_mes[df_mes['Líquido Estética'] >= 0]['Valor Bruto'].sum()
    comissoes = df_mes['Comissão Paga'].sum()
    gastos = df_mes[df_mes['Líquido Estética'] < 0]['Valor Bruto'].sum()
    lucro = df_mes['Líquido Estética'].sum()

    st.subheader(f"📊 Relatório {mes_atual}")
    c1, c2 = st.columns(2)
    c1.metric("Fat. Bruto", f"R${faturamento:,.2f}")
    c1.metric("Comissões", f"R${comissoes:,.2f}")
    c2.metric("Gastos", f"R${gastos:,.2f}")
    c2.metric("LUCRO", f"R${lucro:,.2f}")

# --- HISTÓRICO E EXCLUSÃO ---
st.divider()
st.subheader("Últimos 5 Lançamentos")
if not df.empty:
    st.table(df.tail(5)[['Data', 'Descrição', 'Valor Bruto', 'Profissional']])
    
    if st.button("🗑️ EXCLUIR ÚLTIMO LANÇAMENTO"):
        df = df.drop(df.index[-1])
        df.to_csv(arquivo, index=False)
        st.warning("Removido!")
        st.rerun()
