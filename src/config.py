import os
from dotenv import load_dotenv

load_dotenv()

# EXCEL_URL = os.getenv("EXCEL_URL") # Moved to dynamic loading

MESSAGE_TEMPLATE = (
    "Olá {name}, tudo bem?\n"
    "\n"
    "Gostaríamos de te lembrar que seu pagamento está pendente:\n"
    "\n"
    "*R$ {amount}*\n"
    "\n"
    "*Descrição:* {description}\n"
    "*Data:* {date}\n"
    "\n"
    "*Realize o pagamento e envie o comprovante através da Chave PIX: 03085367977*\n"
    "\n"
    "Já pagou? Desconsidere!\n"
    "\n"
    "---\n"
    "*Restaurante da Juliana*\n"
    "(44) 98812-9535"
)
