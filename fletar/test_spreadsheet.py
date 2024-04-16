from datetime import datetime
from enum import Enum
from pprint import pprint
import json

import httpx


TOKEN = 'xxx'


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


def get_data():
    url = "https://api.zerosheets.com/v1/irl"
    headers = {
        "Authorization": f'Bearer {TOKEN}'
    }

    with httpx.Client() as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

    return data


def add_entry(new_entry):
    url = "https://api.zerosheets.com/v1/irl"
    headers = {
        "Authorization": f'Bearer {TOKEN}'
    }

    with httpx.Client() as client:
        response = client.post(url, json=json.dumps(new_entry), headers=headers)
        response.raise_for_status()
        data = response.json()

    return data

def build_entry(concept, detail, price, payment_type, installments):
    today = datetime.now().strftime('%d/%m/%Y')

    return {
        "Concepto": concept,
        "Fecha": today,
        "Detalle": detail,
        "Precio": price,
        "Medio de pago": payment_type,
        "Cuotas": installments
    }

def main():
    data = get_data()
    concept = Concept.SERVICIOS.value
    detail = 'Pago internet'
    price = '20000'
    payment_type = PaymentType.CUENTA_DNI.value
    installments = ''
    # Llamada a la función para enviar la nueva file
    new_entry = build_entry(concept, detail, price, payment_type, installments)
    try:
        response=add_entry(new_entry)
    except Exception as err:
        print(err)

    data = get_data()
    pprint(data)


if __name__ == "__main__":
    main()
