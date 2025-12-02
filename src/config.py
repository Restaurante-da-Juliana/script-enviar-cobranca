import os
from dotenv import load_dotenv

load_dotenv()

EXCEL_PATH = "data/customers.xlsx"

MESSAGE_TEMPLATE = (
    "Olá, tudo bem?\n"
    "\n"
    "Gostaríamos de te lembrar que seu pagamento está pendente:\n"
    "\n"
    "*R$ {amount}*\n"
    "\n"
    "*Realize o pagamento através da Chave PIX Copia-Cola: {link}*\n"
    "\n"
    "Já pagou? Desconsidere!\n"
    "\n"
    "---\n"
    "*Restaurante da Juliana*\n"
    "(44) 98812-9535\n"
)
