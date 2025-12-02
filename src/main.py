from sheet import loading_sheet
from whatsapp import open_whatsapp

def process():
    df = loading_sheet()

    for idx, row in df.iterrows():
        name = row["customer_name"]
        phone_number = row["phone_number"]
        amount = row["amount_due"]
        date = row['date']
        description = row['description']

        print(f"Gerando cobrança para {name} ({phone_number})...")

        open_whatsapp(phone_number, amount, description, name, date)

        if idx < len(df) - 1:
            input("\n⏸️  Pressione ENTER para continuar para o próximo contato...\n")

    print("Processo concluído!")

if __name__ == "__main__":
    process()
