import requests
from config import INFINITEPAY_CLIENT_ID, INFINITEPAY_SECRET

def generate_token():
    url = "https://api.infinitepay.io/oauth/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": INFINITEPAY_CLIENT_ID,
        "client_secret": INFINITEPAY_SECRET
    }

    r = requests.post(url, data=payload)
    r.raise_for_status()
    return r.json()["access_token"]


def generate_bill(value, description):
    token = generate_token()

    url = "https://api.infinitepay.io/v2/invoice"

    payload = {
        "amount": float(value),
        "description": description,
        "payment_method": "pix"
    }

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()

    data = r.json()
    return data["payment_info"]["pix"]["copy_paste"]
