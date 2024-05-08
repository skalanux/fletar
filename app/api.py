import os
from datetime import datetime

import gspread


CREDENTIALS = 'credentials.json'
print(os.environ)
SPREADSHEET_URL=os.environ['SPREADSHEET_URL']

class API:  
    CATEGORIES_KEY = 'categories'
    PAYMENT_METHODS_KEY = 'payment_methods'

    def __init__(self):
        self.sa = gspread.service_account(filename=CREDENTIALS)
        self.spreadsheet = self.sa.open_by_url(SPREADSHEET_URL)

    def get_config(self):
        wks = self.spreadsheet.worksheet('Configuraciones')
        all_values = wks.get_all_values()[1:]
        categories = [k[0] for k in all_values]
        payment_methods = [k[1] for k in all_values]
        return {self.CATEGORIES_KEY: categories, 
                self.PAYMENT_METHODS_KEY: payment_methods}

    def insert_row(self, spent_entry):
        worksheet = self.spreadsheet.worksheet('Gastos')
        # Agregar la fila a la hoja de cálculo
        worksheet.append_row(spent_entry, value_input_option='USER_ENTERED')

    def build_entry(self, category, detail, price, payment_method, installments):
        today = datetime.now().strftime('%d/%m/%Y')
        
        return ( 
            category,
            today,
            detail,
            price,
            payment_method,
            installments
        )

def main():
    com = API()
    print(com.get_config())


if __name__ == "__main__":
    main()
