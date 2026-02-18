import PyInstaller.__main__
import os
import shutil

def build():
    print("Iniciando build do executável...")
    
    # Clean previous build
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        
    # PyInstaller arguments
    args = [
        'interface.py',                 # Script principal
        '--name=RestauranteCobranca',   # Nome do executável
        '--onefile',                    # Arquivo único
        '--windowed',                   # Sem console (GUI apenas)
        '--noconfirm',                  # Não pedir confirmação para sobrescrever
        '--collect-all=customtkinter',  # Coletar arquivos do customtkinter
        '--add-data=src:src',           # Incluir pasta src (para imports funcionarem)
        '--paths=src',                  # Adiciona src ao path de busca do PyInstaller
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
    ]
    
    PyInstaller.__main__.run(args)
    
    print("\nBUILD CONCLUÍDO COM SUCESSO!")
    print(f"O executável está na pasta: {os.path.abspath('dist/RestauranteCobranca.exe')}")

if __name__ == "__main__":
    build()
