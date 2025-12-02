import webbrowser
from config import MESSAGE_TEMPLATE

def generate_link_wa(phone_number, amount, payment_link):
    msg = MESSAGE_TEMPLATE.format(amount=amount, link=payment_link)
    msg = msg.replace("\n", "%0A")

    return f"https://wa.me/55{phone_number}?text={msg}"

def open_whatsapp(phone_number, amount, payment_link):
    url = generate_link_wa(phone_number, amount, payment_link)
    webbrowser.open(url)
