import os
from dotenv import load_dotenv

load_dotenv()

EXCEL_PATH = os.getenv("EXCEL_PATH")

INFINITEPAY_CLIENT_ID = os.getenv("INFINITEPAY_CLIENT_ID")
INFINITEPAY_SECRET = os.getenv("INFINITEPAY_SECRET")

MESSAGE_TEMPLATE = (
    "Olá! Sou do restaurante. Sua cobrança está pronta.\n"
    "Valor: R$ {valor}\n"
    "Link para pagar: {link}\n"
)
