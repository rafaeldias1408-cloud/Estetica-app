import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração da página - Tema mais focado em estética
st.set_page_config(page_title="Leticia Estética", page_icon="🌸", layout="centered")

# CSS Personalizado para Mobile
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    div.stButton > button { 
        width: 100%; height: 60px; font-weight: bold; 
        border-radius: 15px; background-color: #ff85a2; color: white;
        border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #ff4d7d; border: none; }
    .stMetric { background-color: white; padding: 15px; border-radius: 15px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

arquivo = "dados_estetica.csv"

def carregar_dados():
    colunas = ['Data', 'Mes', 'Descrição', 'Categoria', 'Profissional', 'Valor Bruto', 'Comissão Paga', 'Líquido Estética']
    if os.path.exists(arquivo):
        df = pd.read_csv(arquivo)
        for col in colunas:
            if col not in df.columns: df[col] = "-"
        return df
    return pd.DataFrame(columns=colunas)

df = carregar_dados()

# --- NAVEGAÇÃO POR ABAS (Melhor para Celular) ---
aba1, aba2 = st.tabs(["📝 Novo Lançamento", "📊 Financeiro"])

with aba1:
    st.markdown("### ✨ Registrar Atendimento")
    
    with st.form("registro_form", clear_on_submit=True):
        desc = st.text_input("O que foi feito?", placeholder="Ex: Microagulhamento")
        
        c1, c2 = st.columns(2)
        with c1:
            cat = st.selectbox("Categoria", ["Serviço", "Produtos", "Aluguel", "Luz", "Outros"])
        with c2:
            # Lista pré-definida evita erros no cálculo de comissão
            prof = st.selectbox("Profissional", ["Leticia", "Outro Profissional"])
        
        tipo = st.radio("Tipo de Movimentação", ["Entrada", "Saída"], horizontal=True)
        
        # Uso de number_input facilita o teclado numérico no iOS
        valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
        
        submit = st.form_submit_button("REGISTRAR AGORA")

    if submit:
        if desc and valor > 0:
            mes_atual = datetime.now().strftime("%m/%Y")
            comissao_paga = 0
            liquido_empresa = valor

            if tipo == "Entrada" and cat == "Serviço":
                if prof != "Leticia":
                    comissao_paga = valor * 0.30
                    liquido_empresa = valor - comissao_paga
            
            if tipo == "Saída":
                liquido_empresa = -valor

            nova_linha = {
                'Data': datetime.now().strftime("%d/%m %H:%M"),
                'Mes': mes_atual,
                'Descrição': desc,
                'Categoria': cat,
                'Profissional': prof,
                'Valor Bruto': valor,
                'Comissão Paga': comissao_paga,
                'Líquido Estética': liquido_empresa
            }
            
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
            df.to_csv(arquivo, index=False)
            st.success("Salvo com sucesso!")
            st.rerun()

with aba2:
    st.markdown("### 📈 Resumo Mensal")
    mes_hoje = datetime.now().strftime("%m/%Y")
    
    if not df.empty:
        df_mes = df[df['Mes'] == mes_hoje]
        
        if not df_mes.empty:
            faturamento = df_mes[df_mes['Líquido Estética'] >= 0]['Valor Bruto'].sum()
            comissoes = df_mes['Comissão Paga'].sum()
            lucro = df_mes['Líquido Estética'].sum()

            col1, col2 = st.columns(2)
            col1.metric("Faturamento", f"R${faturamento:,.2f}")
            col2.metric("Comissões", f"R${comissoes:,.2f}")
            st.metric("LUCRO LÍQUIDO", f"R${lucro:,.2f}", delta=f"{lucro:,.2f}")

        st.divider()
        st.write("**Histórico Recente**")
        # Mostra apenas as colunas essenciais para não apertar no celular
        st.dataframe(df.tail(10)[['Data', 'Descrição', 'Líquido Estética']], use_container_width=True)
        
        if st.button("🗑️ Remover Último Registro"):
            df = df.drop(df.index[-1])
            df.to_csv(arquivo, index=False)
            st.warning("Registro removido!")
            st.rerun()
