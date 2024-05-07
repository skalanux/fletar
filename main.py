import flet as ft
from api import Concept, PaymentType, API


STORAGE = API()

def save_spent(price, detail, category, payment_method):
    """Save spent into the spreadsheet."""
    installments = ''
    # Llamada a la función para enviar la nueva fila
    new_entry = STORAGE.build_entry(category, detail, price, payment_method, installments)
    try:
        response=STORAGE.insert_row(new_entry)
    except Exception as err:
        print(err)


def main(page: ft.Page):
    async def add_clicked(e):
        spent_view.controls.append(ft.Checkbox(label=spent.value))
        save_spent(spent.value, spent_detail.value, spent_category.value, spent_payment_method.value)
        spent.value = ""
        spent_detail.value = ""
        view.update()

    CONFIGURATION = STORAGE.get_config()

    spent = ft.TextField(hint_text="Cuánto?", expand=True)
    spent_detail = ft.TextField(hint_text="En qué?", expand=True)
    spent_category = ft.Dropdown(
        width=150,
        options=[ft.dropdown.Option(k) for k in CONFIGURATION.get(API.CATEGORIES_KEY)]
    )
    spent_payment_method= ft.Dropdown(
        width=150,
        options=[ft.dropdown.Option(k) for k in CONFIGURATION.get(API.PAYMENT_METHODS_KEY)]
    )

    spent_view = ft.Column()
    view=ft.Column(
        width=800,
        controls=[
            ft.Row(
                controls=[
                    spent,
                    spent_detail,
                    spent_category,
                    spent_payment_method,
                    ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked),
                ],
            ),
            spent_view,
        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Fletar(al presiduende)"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme = ft.Theme(color_scheme_seed="green")
    page.add(view)
 
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
