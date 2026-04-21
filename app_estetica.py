import customtkinter as ctk
import pandas as pd
import os
from datetime import datetime
from tkinter import messagebox

# Configuração de Aparência
ctk.set_appearance_mode("light") # Modo claro combina mais com estética
ctk.set_default_color_theme("blue") 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Letícia Estética")
        self.geometry("450x800")
        self.configure(fg_color="#FFF5F7") # Fundo levemente rosado

        # Cabeçalho
        self.header = ctk.CTkLabel(self, text="✨ REGISTRO ESTÉTICA", font=("Century Gothic", 24, "bold"), text_color="#D81B60")
        self.header.pack(pady=20)

        # --- CONTAINER PRINCIPAL (Formulário) ---
        self.form_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=15, border_width=1, border_color="#FFC1D6")
        self.form_frame.pack(pady=10, padx=20, fill="both")

        self.desc = ctk.CTkEntry(self.form_frame, placeholder_text="O que foi realizado?", height=40, border_color="#FFC1D6")
        self.desc.pack(pady=(15, 5), padx=20, fill="x")

        self.cat = ctk.CTkComboBox(self.form_frame, values=["Serviço", "Produtos", "Aluguel Máquina", "Luz", "Outros"], height=40)
        self.cat.pack(pady=5, padx=20, fill="x")
        self.cat.set("Categoria")

        # Troquei Entry por ComboBox para evitar erros no cálculo de comissão
        self.prof = ctk.CTkComboBox(self.form_frame, values=["Leticia", "Outro Profissional"], height=40)
        self.prof.pack(pady=5, padx=20, fill="x")
        self.prof.set("Profissional")

        self.tipo = ctk.CTkSegmentedButton(self.form_frame, values=["Entrada", "Saída"], selected_color="#D81B60", selected_hover_color="#AD1457")
        self.tipo.pack(pady=10, padx=20, fill="x")
        self.tipo.set("Entrada")

        self.valor = ctk.CTkEntry(self.form_frame, placeholder_text="Valor R$ (Ex: 150.00)", height=40, border_color="#FFC1D6")
        self.valor.pack(pady=(5, 15), padx=20, fill="x")

        # --- BOTÕES ---
        self.btn_salvar = ctk.CTkButton(self, text="SALVAR LANÇAMENTO", command=self.salvar_dados, fg_color="#D81B60", hover_color="#AD1457", font=("Arial", 14, "bold"), height=50)
        self.btn_salvar.pack(pady=15, padx=40, fill="x")

        # Frame para botões secundários (lado a lado)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=5, padx=40, fill="x")

        self.btn_relatorio = ctk.CTkButton(self.btn_frame, text="Relatório", command=self.mostrar_relatorio, fg_color="#2d5287", width=120)
        self.btn_relatorio.pack(side="left", padx=5, expand=True)

        self.btn_excluir = ctk.CTkButton(self.btn_frame, text="Excluir Último", command=self.excluir_ultimo, fg_color="#A52A2A", width=120)
        self.btn_excluir.pack(side="right", padx=5, expand=True)

        # --- HISTÓRICO ---
        self.label_hist = ctk.CTkLabel(self, text="Atendimentos Recentes", font=("Arial", 13, "bold"), text_color="#555")
        self.label_hist.pack(pady=(20, 0))
        
        self.txt_historico = ctk.CTkTextbox(self, height=180, corner_radius=10, border_width=1, border_color="#DDD")
        self.txt_historico.pack(pady=10, padx=25, fill="both")
        
        self.atualizar_historico()

    # (As funções salvar_dados, excluir_ultimo e mostrar_relatorio continuam com a mesma lógica do seu código)
    # Apenas certifique-se de usar self.prof.get() e self.valor.get() como você já estava fazendo.
    
    def atualizar_historico(self):
        self.txt_historico.delete("1.0", "end")
        arquivo = 'Gestao_Estetica.xlsx'
        if os.path.exists(arquivo):
            try:
                df = pd.read_excel(arquivo)
                if not df.empty:
                    ultimos = df.tail(5).iloc[::-1]
                    for _, row in ultimos.iterrows():
                        simbolo = "➕" if row['Líquido Estética'] >= 0 else "➖"
                        texto = f"{simbolo} {row['Data']} | {row['Descrição']}\n   Valor: R$ {row['Valor Bruto']:.2f} | {row['Profissional']}\n"
                        texto += "-"*40 + "\n"
                        self.txt_historico.insert("end", texto)
            except:
                self.txt_historico.insert("1.0", "Erro ao carregar histórico.")

    def salvar_dados(self):
        # ... (Sua lógica de salvar original) ...
        # (Lembre-se de adicionar a chamada self.atualizar_historico() no final)
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
