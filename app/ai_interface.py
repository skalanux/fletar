import os
from datetime import datetime

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from api import API

STORAGE = API()

provider = GoogleProvider(api_key=os.environ.get('GEMINI_API_KEY'))
model = GoogleModel('gemini-1.5-flash', provider=provider)
agent = Agent(model,
    system_prompt="""Sos un asistente que puede registrar gastos hechos en una lista de gastos. 

    Podés:
    - registrar gastos en un archivo de texto:
    - obtener los gastos hechos de un archivo de texto

   Si no te dan un dato intenta inferirlo, sino podés pedilo.
   el medio de pago nunca lo pidas.
    """
)

@agent.instructions  
def add_categories() -> str:
    return f"Las categorias posibles son {STORAGE.get_config().get(API.CATEGORIES_KEY)}"

@agent.instructions  
def add_payment_methods() -> str:
    return f"""Los medios de pago posibles son {STORAGE.get_config().get(API.PAYMENT_METHODS_KEY)}, 
    por defecto asumí qu es cuenta, no hace falta que pidas este dato si no se menciona.
    podes asumir que es cuenta."""

@agent.instructions  
def add_equivalences() -> str:
    return f"""Mercado Pago o mp es cuenta, Cuenta DNI tambien es cuenta.
    Pastas es almuerzo
    Ferreteria es vivienda
    Metrogas, Aysa, Edesur, Alquiler, TSG es vivienda
    """

@agent.instructions 
def add_today() -> str:
    return f"La fecha actual es {datetime.now().strftime('%d/%m/%Y')}"


def run_agent(prompt: str, result=None)-> str:
    if result is not None:
        result = agent.run_sync(prompt, message_history=result.all_messages())
    else:
        result = agent.run_sync(prompt)
    return result

@agent.tool_plain
def registrar_gasto(monto: int, categoria: str, detalle:str, medio: str)-> str:
    """Dado un monto, una categoria, un detalle y un medio de pago, registrar el gasto en un archivo de texto."""
    with open("gastos.txt", "a") as f:
        f.write(f"{monto} - {categoria} - {detalle} - {medio}\n")

    installments = ''
    # Llamada a la función para enviar la nueva fila
    new_entry = STORAGE.build_entry(categoria, detalle, monto, medio, installments)
    try:
        response = STORAGE.insert_row(new_entry)
    except Exception as err:
        print(err)

    return "Gasto registrado"


if __name__ == "__main__":
    result = None
    while True:
        if result is not None:
            question = input(result.output)
        else:
            question = input("¿Qué gasto querés registrar? ")
        result = run_agent(question, result)
        