from datetime import datetime
from enum import Enum
from pprint import pprint
import json

import gspread
array = ['Gastos', 'Prueba']
final = []
finaldict = {'Name':[],'Expenditure':[]}
cred = 'credentials.json'
url = 'https://docs.google.com/spreadsheets/d/1r6ZceccaTBeK7ftDVy8kESbFNGL69T3AYN2sr8pEzOY/edit?usp=sharing'


class Concept(Enum):
    SERVICIOS = "Servicios"
    ALIMENTOS_E_HIGIENE = "Alimentos e higiene"
    OCIO = "Ocio"

class PaymentType(Enum):
    CREDIT_CARD = "Tarjeta de crédito"
    MERCADO_PAGO = "Mercado Pago"
    DEBITO = "Debito"
    CUENTA_DNI = "Cuenta DNI"
    EFECTIVO = "Cash"


class API:  
    final = []
    CATEGORIES_KEY = 'categories'
    PAYMENT_METHODS_KEY = 'payment_methods'

    def __init__(self):
        #name = 'Fruitas'
        # Initialization of the Strings
        self.sa = gspread.service_account(filename = cred)
        self.spreadsheet = self.sa.open_by_url(url)

    def get_config(self):
        counter = 0
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
    concept = Concept.SERVICIOS.value
    detail = 'Pago Gas'
    price = 1200
    payment_type = PaymentType.MERCADO_PAGO.value
    installments = ''
    print(com.get_config())
    #new_entry = com.build_entry(concept, detail, price, payment_type, installments)
    #com.insert_row(new_entry)


if __name__ == "__main__":
    main()
