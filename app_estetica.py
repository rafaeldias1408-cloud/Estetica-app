import flet as ft
import pandas as pd
from datetime import datetime
import os

def main(page: ft.Page):
    page.title = "Leticia Estética"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 800
    page.padding = 20
    # Cores do tema estética
    cor_principal = "#D81B60" 

    arquivo = 'Gestao_Estetica.xlsx'

    # --- FUNÇÕES DE LÓGICA ---
    def salvar_dados(e):
        if not txt_desc.value or not txt_valor.value:
            page.snack_bar = ft.SnackBar(ft.Text("Preencha a descrição e o valor!"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            bruto = float(txt_valor.value.replace(",", "."))
            profissional = combo_prof.value
            tipo = seg_tipo.value
            categoria = combo_cat.value
            
            comissao_paga = 0
            liquido_empresa = bruto

            if tipo == "Entrada" and categoria == "Serviço":
                if profissional != "Leticia":
                    comissao_paga = bruto * 0.30
                    liquido_empresa = bruto - comissao_paga
            
            if tipo == "Saída":
                liquido_empresa = -bruto

            nova_linha = {
                'Data': datetime.now().strftime("%d/%m %H:%M"),
                'Mes': datetime.now().strftime("%m/%Y"),
                'Descrição': txt_desc.value,
                'Categoria': categoria,
                'Profissional': profissional,
                'Valor Bruto': bruto,
                'Comissão Paga': comissao_paga,
                'Líquido Estética': liquido_empresa
            }
            
            if os.path.exists(arquivo):
                df = pd.read_excel(arquivo)
                df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
            else:
                df = pd.DataFrame([nova_linha])
            
            df.to_excel(arquivo, index=False)
            
            # Limpar campos e atualizar
            txt_desc.value = ""
            txt_valor.value = ""
            atualizar_historico()
            page.snack_bar = ft.SnackBar(ft.Text("✅ Salvo com sucesso!"))
            page.snack_bar.open = True
            page.update()
            
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {ex}"))
            page.snack_bar.open = True
            page.update()

    def atualizar_historico():
        lista_historico.controls.clear()
        if os.path.exists(arquivo):
            df = pd.read_excel(arquivo)
            if not df.empty:
                for _, row in df.tail(5).iloc[::-1].iterrows():
                    cor = ft.colors.GREEN_600 if row['Líquido Estética'] >= 0 else ft.colors.RED_600
                    lista_historico.controls.append(
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.PAYMENT, color=cor),
                            title=ft.Text(f"{row['Descrição']}"),
                            subtitle=ft.Text(f"{row['Data']} - {row['Profissional']}"),
                            trailing=ft.Text(f"R$ {row['Valor Bruto']:.2f}", weight="bold")
                        )
                    )
        page.update()

    # --- COMPONENTES DA INTERFACE ---
    txt_desc = ft.TextField(label="O que foi feito?", border_color=cor_principal)
    combo_cat = ft.Dropdown(
        label="Categoria",
        options=[
            ft.dropdown.Option("Serviço"),
            ft.dropdown.Option("Produtos"),
            ft.dropdown.Option("Aluguel Máquina"),
            ft.dropdown.Option("Luz"),
        ],
        value="Serviço"
    )
    combo_prof = ft.Dropdown(
        label="Profissional",
        options=[ft.dropdown.Option("Leticia"), ft.dropdown.Option("Outro")],
        value="Leticia"
    )
    seg_tipo = ft.SegmentedButton(
        selected={"Entrada"},
        segments=[
            ft.Segment(value="Entrada", label=ft.Text("Entrada"), icon=ft.Icon(ft.icons.ARROW_UPWARD)),
            ft.Segment(value="Saída", label=ft.Text("Saída"), icon=ft.Icon(ft.icons.ARROW_DOWNWARD)),
        ],
    )
    # No iOS, keyboard_type faz o teclado numérico abrir
    txt_valor = ft.TextField(label="Valor R$", keyboard_type=ft.KeyboardType.NUMBER, border_color=cor_principal)
    
    lista_historico = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=200)

    # Montagem da Tela
    page.add(
        ft.Row([ft.Text("✨ Estética Letícia", size=28, weight="bold", color=cor_principal)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        txt_desc,
        ft.Row([combo_cat, combo_prof]),
        ft.Row([seg_tipo], alignment=ft.MainAxisAlignment.CENTER),
        txt_valor,
        ft.ElevatedButton(
            "SALVAR LANÇAMENTO", 
            color=ft.colors.WHITE, 
            bgcolor=cor_principal, 
            height=50, 
            width=400,
            on_click=salvar_dados
        ),
        ft.Text("Últimos Lançamentos", size=16, weight="bold"),
        lista_historico
    )

    atualizar_historico()

ft.app(target=main)
