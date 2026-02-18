import customtkinter as ctk
import subprocess
import threading
import sys
import os
from dotenv import load_dotenv

# Configuração da aparência
ctk.set_appearance_mode("Dark")  # Modos: "System" (padrão), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue" (padrão), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.title("Automação de Cobrança - Restaurante da Juliana")
        self.geometry("700x500")

        # Configuração do grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Área de log expande

        # Título
        self.label_title = ctk.CTkLabel(self, text="Painel de Controle de Cobranças", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Frame de Entrada
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.label_url = ctk.CTkLabel(self.input_frame, text="URL da Planilha (Excel):", font=ctk.CTkFont(size=14))
        self.label_url.grid(row=0, column=0, padx=15, pady=15)

        self.entry_url = ctk.CTkEntry(self.input_frame, placeholder_text="Cole o link da planilha aqui...", height=35)
        self.entry_url.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        self.btn_save = ctk.CTkButton(self.input_frame, text="Salvar Configuração", command=self.save_env, width=150, height=35)
        self.btn_save.grid(row=0, column=2, padx=15, pady=15)

        # Carregar valor atual do .env
        self.load_env()

        # Área de Log
        self.textbox_log = ctk.CTkTextbox(self, width=600, height=200, font=ctk.CTkFont(family="Courier New", size=12))
        self.textbox_log.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.textbox_log.insert("0.0", "O log de execução aparecerá aqui...\n\n")
        self.textbox_log.configure(state="disabled")

        # Botão de Ação Principal
        self.btn_run = ctk.CTkButton(self, text="EXECUTAR ENVIOS", command=self.start_process_thread, height=60, 
                                     font=ctk.CTkFont(size=18, weight="bold"), fg_color="#2CC985", hover_color="#229964", text_color="white")
        self.btn_run.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        # Texto de rodapé
        self.footer = ctk.CTkLabel(self, text="Desenvolvido para automação eficiente", text_color="gray")
        self.footer.grid(row=4, column=0, pady=5)

    def load_env(self):
        """Carrega a variável de ambiente EXCEL_URL para o campo de texto."""
        load_dotenv()
        url = os.getenv("EXCEL_URL")
        if url:
            self.entry_url.delete(0, "end")
            self.entry_url.insert(0, url)

    def save_env(self):
        """Salva a URL digitada no arquivo .env."""
        url = self.entry_url.get().strip()
        if not url:
            self.log("ERRO: O campo de URL não pode estar vazio!")
            return
        
        env_file = ".env"
        try:
            # Lê o conteúdo atual para preservar outras variáveis (se houver)
            lines = []
            if os.path.exists(env_file):
                with open(env_file, "r") as f:
                    lines = f.readlines()
            
            # Atualiza ou adiciona EXCEL_URL
            found = False
            new_lines = []
            for line in lines:
                if line.startswith("EXCEL_URL="):
                    new_lines.append(f"EXCEL_URL={url}\n")
                    found = True
                else:
                    new_lines.append(line)
            
            if not found:
                new_lines.append(f"EXCEL_URL={url}\n")
            
            with open(env_file, "w") as f:
                f.writelines(new_lines)
            
            self.log(f"Configuração salva com sucesso! URL atualizada.")
            # Recarrega as variáveis de ambiente no processo atual
            os.environ["EXCEL_URL"] = url
            
        except Exception as e:
            self.log(f"ERRO ao salvar configuração: {e}")

    def log(self, message):
        """Adiciona uma mensagem à área de log."""
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert("end", f"> {message}\n")
        self.textbox_log.see("end")
        self.textbox_log.configure(state="disabled")

    def start_process_thread(self):
        """Inicia o processo em uma thread separada para não travar a GUI."""
        if not self.entry_url.get().strip():
             self.log("ERRO: Configure a URL da planilha antes de executar!")
             return

        self.btn_run.configure(state="disabled", text="Executando... (Aguarde)")
        self.save_env()  # Garante que está salvo antes de rodar
        
        thread = threading.Thread(target=self.run_process)
        thread.daemon = True # Thread morre se o app fechar
        thread.start()

    def run_process(self):
        """Executa o script main.py e captura sua saída."""
        self.log("-" * 40)
        self.log("INICIANDO PROCESSO DE COBRANÇA...")
        
        try:
            # Usa o mesmo executável python que está rodando a interface
            python_exec = sys.executable 
            script_path = os.path.join("src", "main.py")

            if not os.path.exists(script_path):
                 self.log(f"ERRO CRÍTICO: Script não encontrado em {script_path}")
                 return

            # Executa o script. 'bufsize=0' e '-u' para tentar saída sem buffer
            process = subprocess.Popen(
                [python_exec, "-u", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd(), # Executa a partir da pasta raiz
                bufsize=1, # Line buffered
                universal_newlines=True
            )

            # Lê a saída linha por linha em tempo real
            with process.stdout:
                for line in iter(process.stdout.readline, ''):
                    if line:
                        # Schedule updating the GUI in the main thread ideally, 
                        # but tkinter handles simple updates from threads usually okay-ish 
                        # or we should use after(). Let's keep it simple.
                        self.log(line.strip())
            
            # Captura erros se houver
            stderr = process.stderr.read()
            if stderr:
                self.log(f"ERRO NO SCRIPT: {stderr}")

            rc = process.wait()
            if rc == 0:
                self.log("PROCESSO FINALIZADO COM SUCESSO! ✅")
            else:
                self.log(f"O processo terminou com erro (código {rc}). ❌")

        except Exception as e:
            self.log(f"ERRO DE EXECUÇÃO: {e}")
        finally:
            # Restaura o botão na thread principal (pode precisar de .after se der erro de thread)
            self.btn_run.configure(state="normal", text="EXECUTAR ENVIOS")

if __name__ == "__main__":
    app = App()
    app.mainloop()
