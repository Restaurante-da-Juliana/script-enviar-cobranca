import customtkinter as ctk
import threading
import sys
import os
import io
import time
from dotenv import load_dotenv

# Ensure we can import from src
if getattr(sys, 'frozen', False):
    # Running as compiled exe
    base_path = sys._MEIPASS
else:
    # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

src_path = os.path.join(base_path, "src")
if src_path not in sys.path:
    sys.path.append(src_path)

try:
    # Try importing as top-level if src is in path
    import main
except ImportError:
    # Fallback to package import
    from src import main

# Configuração da aparência
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class RedirectText(io.StringIO):
    """Class to redirect stdout/stderr to the Text widget."""
    def __init__(self, text_widget, tag="stdout"):
        super().__init__()
        self.text_widget = text_widget
        self.tag = tag

    def write(self, string):
        if string:
            # Schedule the update on the main thread
            self.text_widget.after(0, lambda: self._insert(string))

    def _insert(self, string):
        try:
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", string)
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")
        except Exception:
            pass
            
    def flush(self):
        pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Automação de Cobrança - Restaurante da Juliana")
        self.geometry("700x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # UI Elements
        self.label_title = ctk.CTkLabel(self, text="Painel de Controle de Cobranças", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        self.label_url = ctk.CTkLabel(self.input_frame, text="URL da Planilha (Excel):", font=ctk.CTkFont(size=14))
        self.label_url.grid(row=0, column=0, padx=15, pady=15)

        self.entry_url = ctk.CTkEntry(self.input_frame, placeholder_text="Cole o link da planilha aqui...", height=35)
        self.entry_url.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        self.btn_save = ctk.CTkButton(self.input_frame, text="Salvar Configuração", command=self.save_env, width=150, height=35)
        self.btn_save.grid(row=0, column=2, padx=15, pady=15)

        self.load_env()

        self.textbox_log = ctk.CTkTextbox(self, width=600, height=200, font=ctk.CTkFont(family="Courier New", size=12))
        self.textbox_log.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.textbox_log.insert("0.0", "O log de execução aparecerá aqui...\n\n")
        self.textbox_log.configure(state="disabled")

        self.btn_run = ctk.CTkButton(self, text="EXECUTAR ENVIOS", command=self.start_process_thread, height=60, 
                                     font=ctk.CTkFont(size=18, weight="bold"), fg_color="#2CC985", hover_color="#229964", text_color="white")
        self.btn_run.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        self.footer = ctk.CTkLabel(self, text="Desenvolvido para automação eficiente", text_color="gray")
        self.footer.grid(row=4, column=0, pady=5)

    def load_env(self):
        env_path = ".env"
        # Try to load from current directory first (where exe is)
        if os.path.exists(env_path):
             load_dotenv(env_path)
             
        url = os.getenv("EXCEL_URL")
        if url:
            self.entry_url.delete(0, "end")
            self.entry_url.insert(0, url)

    def save_env(self):
        url = self.entry_url.get().strip()
        if not url:
            self.log_message("ERRO: O campo de URL não pode estar vazio!")
            return False
            
        try:
            env_file = ".env"
            lines = []
            if os.path.exists(env_file):
                with open(env_file, "r") as f:
                    lines = f.readlines()
            
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
            
            os.environ["EXCEL_URL"] = url # Update immediately for current process
            self.log_message(f"Configuração salva com sucesso!")
            return True
            
        except Exception as e:
            self.log_message(f"ERRO ao salvar configuração: {e}")
            return False

    def log_message(self, message):
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert("end", f"> {message}\n")
        self.textbox_log.see("end")
        self.textbox_log.configure(state="disabled")

    def start_process_thread(self):
        if not self.entry_url.get().strip():
             self.log_message("ERRO: Configure a URL da planilha antes de executar!")
             return

        if not self.save_env():
             return

        self.btn_run.configure(state="disabled", text="Executando... (Aguarde)")
        
        thread = threading.Thread(target=self.run_process)
        thread.daemon = True
        thread.start()

    def run_process(self):
        # Redirect stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        sys.stdout = RedirectText(self.textbox_log, "stdout")
        sys.stderr = RedirectText(self.textbox_log, "stderr")

        try:
            print("-" * 40)
            print("INICIANDO PROCESSO...", flush=True)
            
            # Reload loading_sheet logic is dynamic now, so just calling main.process() works
            # provided os.environ is set (which save_env does)
            
            try:
                # We re-import or use the imported module
                # Direct call
                main.process()
            except Exception as e_inner:
                print(f"ERRO DURANTE EXECUÇÃO: {e_inner}")
                import traceback
                traceback.print_exc()

        except Exception as e:
            self.log_message(f"ERRO GERAL: {e}")
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            self.after(0, lambda: self.btn_run.configure(state="normal", text="EXECUTAR ENVIOS"))

if __name__ == "__main__":
    app = App()
    app.mainloop()
