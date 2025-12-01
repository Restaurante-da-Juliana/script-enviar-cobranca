import webbrowser
from config import MESSAGE_TEMPLATE

def generate_link_wa(number, value, link_pix):
    msg = MESSAGE_TEMPLATE.format(value=value, link=link_pix)
    msg = msg.replace("\n", "%0A")

    return f"https://wa.me/55{number}?text={msg}"

def open_whatsapp(number, value, link_pix):
    url = generate_link_wa(number, value, link_pix)
    webbrowser.open(url)
