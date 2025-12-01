from sheet import loading_sheet, save_sheet, get_pendings
from infinitepay import generate_bill
from whatsapp import open_whatsapp

def process():
    df = loading_sheet()
    pendings = get_pendings(df)

    if pendings.empty:
        print("Nenhuma cobrança pendente!")
        return

    for idx, row in pendings.iterrows():
        nome = row["nome"]
        numero = row["telefone"]
        valor = row["valor"]

        print(f"Gerando cobrança para {nome} ({numero})...")

        try:
            link_pix = generate_bill(valor, f"Cobrança para {nome}")
        except Exception as e:
            print(f"Erro ao gerar cobrança: {e}")
            continue

        open_whatsapp(numero, valor, link_pix)

        df.loc[idx, "status"] = "enviado"
        df.loc[idx, "link_pix"] = link_pix

    save_sheet(df)
    print("Processo concluído!")

if __name__ == "__main__":
    process()
