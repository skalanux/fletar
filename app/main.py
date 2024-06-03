import flet as ft
from api import API


STORAGE = API()

def save_spent(price, detail, category, payment_method):
    """Save spent into the spreadsheet."""
    installments = ''
    # Llamada a la función para enviar la nueva fila
    new_entry = STORAGE.build_entry(category, detail, price, payment_method, installments)
    try:
        response = STORAGE.insert_row(new_entry)
    except Exception as err:
        print(err)


def main(page: ft.Page):
    async def add_clicked(e):
        spent_view.controls.append(
            ft.Text(
                f'{spent.value} {spent_detail.value}',
                size=14,
                color=ft.colors.INDIGO_500,
                weight=ft.FontWeight.W_100,
            ))

        save_spent(spent.value, spent_detail.value, spent_category.value, spent_payment_method.value)
        spent.value = ""
        spent_detail.value = ""
        spent.focus()
        main_column.update()

    CONFIGURATION = STORAGE.get_config()
    spent = ft.TextField(hint_text="Cuánto?", expand=True)
    spent_detail = ft.TextField(hint_text="En qué?", expand=True)
    spent_category = ft.Dropdown(hint_text='Y que es eso?',
        options=[ft.dropdown.Option(k) for k in CONFIGURATION.get(API.CATEGORIES_KEY)]
    )
    spent_category.value = spent_category.options[0]
    spent_payment_method= ft.Dropdown(hint_text='Cómo pagaste?',
        options=[ft.dropdown.Option(k) for k in CONFIGURATION.get(API.PAYMENT_METHODS_KEY) if k!='']
    )
    
    app_title = ft.Text(
            "Fletar",
            size=40,
            color=ft.colors.INDIGO_500,
            weight=ft.FontWeight.W_100,
        )

    spent_view = ft.Column()

    spent_row = ft.ResponsiveRow(
            [
                ft.Container(
                    spent,
                    padding=5,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
                ft.Container(
                    spent_detail,
                    padding=5,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
                ft.Container(
                    spent_category,
                    padding=5,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
                ft.Container(
                    spent_payment_method,
                    padding=5,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),
                ft.Container(
                    ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_clicked),
                    padding=5,
                    col={"sm": 6, "md": 4, "xl": 2},
                ),


            ],
            run_spacing={"xs": 10},
    )

    main_column = ft.Column(
        controls=[
            ft.Row(controls=[app_title]),
            spent_row,
            ft.Container(
                spent_view,
                padding=5,
                col={"sm": 6, "md": 4, "xl": 2},
            ),


        ],
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Fletar(al presiduende)"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme = ft.Theme(color_scheme_seed="blue")
    page.theme_mode = "light"
    page.add(
        main_column
    )
    spent.focus()
 
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
