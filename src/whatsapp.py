import webbrowser
from config import MESSAGE_TEMPLATE

def generate_link_wa(phone_number, amount, description, customer_name, date):
    msg = MESSAGE_TEMPLATE.format(amount=amount, description=description, name=customer_name, date=date)
    msg = msg.replace("\n", "%0A")

    return f"https://wa.me/55{phone_number}?text={msg}"

def open_whatsapp(phone_number, amount, description, customer_name, date):
    url = generate_link_wa(phone_number, amount, description, customer_name, date)
    webbrowser.open(url)
