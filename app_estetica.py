import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página para Celular
st.set_page_config(page_title="Estética Letícia", page_icon="✨", layout="centered")

# Estilo para botões grandes e cores
st.markdown("""
    <style>
    div.stButton > button { width: 100%; height: 50px; font-weight: bold; border-radius: 10px; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ REGISTRO ESTÉTICA")

arquivo = "dados_estetica.csv"

# --- FUNÇÃO DE DADOS CORRIGIDA ---
def carregar_dados():
    colunas = ['Data', 'Mes', 'Descrição', 'Categoria', 'Profissional', 'Valor Bruto', 'Comissão Paga', 'Líquido Estética']
    if os.path.exists(arquivo):
        df = pd.read_csv(arquivo)
        # Verifica se todas as colunas necessárias existem (corrige o erro KeyError)
        for col in colunas:
            if col not in df.columns:
                df[col] = "-" # Cria a coluna faltando com valor vazio
        return df
    return pd.DataFrame(columns=colunas)

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
                # Regra: Se for diferente de Leticia, calcula 30%
                if profissional.lower() != "leticia":
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

# --- RELATÓRIO MENSAL ---
st.divider()
mes_hoje = datetime.now().strftime("%m/%Y")

# Filtra pelo mês de forma segura
if not df.empty and 'Mes' in df.columns:
    df_mes = df[df['Mes'] == mes_hoje]
    
    if not df_mes.empty:
        # Tenta converter para numérico para garantir que a soma funcione
        faturamento = pd.to_numeric(df_mes[df_mes['Líquido Estética'] >= 0]['Valor Bruto'], errors='coerce').sum()
        comissoes = pd.to_numeric(df_mes['Comissão Paga'], errors='coerce').sum()
        gastos = pd.to_numeric(df_mes[df_mes['Líquido Estética'] < 0]['Valor Bruto'], errors='coerce').sum()
        lucro = pd.to_numeric(df_mes['Líquido Estética'], errors='coerce').sum()

        st.subheader(f"📊 Relatório {mes_hoje}")
        c1, c2 = st.columns(2)
        c1.metric("Fat. Bruto", f"R${faturamento:,.2f}")
        c1.metric("Comissões", f"R${comissoes:,.2f}")
        c2.metric("Gastos", f"R${gastos:,.2f}")
        c2.metric("LUCRO", f"R${lucro:,.2f}")

# --- HISTÓRICO E EXCLUSÃO ---
st.divider()
st.subheader("Últimos Lançamentos")
if not df.empty:
    st.table(df.tail(5)[['Data', 'Descrição', 'Valor Bruto', 'Profissional']])
    
    if st.button("🗑️ EXCLUIR ÚLTIMO LANÇAMENTO"):
        df = df.drop(df.index[-1])
        df.to_csv(arquivo, index=False)
        st.warning("Removido!")
        st.rerun()
