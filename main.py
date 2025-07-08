# main.py
import customtkinter as ctk
from bot_logic import PokemmoBot
from failsafe import FailSafeListener
import time
import threading
from tkinter import messagebox

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PokéMMO Shiny Hunter")
        self.geometry("600x450")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

        # 1. Cria a instância do Bot e do Fail-Safe
        self.bot = PokemmoBot(update_ui_callback=self.update_ui)
        self.failsafe = FailSafeListener(self.bot)
        self.bot.set_failsafe_listener(self.failsafe)

        # 2. Cria os Widgets
        self.create_widgets()
        
        # 3. Carrega a configuração inicial para mostrar na UI
        self.bot.carregar_config()

    def start_bot_with_delay(self):
        """Inicia uma contagem regressiva em uma nova thread para não travar a UI."""
        
        def countdown_and_start():
            # Desabilita o botão de start para evitar cliques múltiplos
            self.start_button.configure(state="disabled")

            for i in range(6, 0, -1):
                self.update_ui(status=f"Mude para o PokéMMO... {i}s")
                time.sleep(1)
            
            # Após a contagem, inicia o bot
            self.bot.start()

        # Roda a contagem regressiva em uma nova thread
        countdown_thread = threading.Thread(target=countdown_and_start, daemon=True)
        countdown_thread.start()

    def create_widgets(self):
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=10, padx=10, fill="x")
        
        self.start_button = ctk.CTkButton(control_frame, text="Iniciar Bot", command=self.start_bot_with_delay, fg_color="green", hover_color="darkgreen")
        self.start_button.pack(side="left", expand=True, padx=5)
        
        self.stop_button = ctk.CTkButton(control_frame, text="Parar Bot", command=self.bot.stop, fg_color="red", hover_color="darkred", state="disabled")
        self.stop_button.pack(side="left", expand=True, padx=5)
        
        status_frame = ctk.CTkFrame(self)
        status_frame.pack(pady=5, padx=10, fill="x")
        self.status_label = ctk.CTkLabel(status_frame, text="Aguardando início...", font=("Arial", 14))
        self.status_label.pack(side="left", padx=10, pady=5)
        self.encounter_label = ctk.CTkLabel(status_frame, text="Encontros: 0", font=("Arial", 12))
        self.encounter_label.pack(side="right", padx=10, pady=5)

        log_frame = ctk.CTkFrame(self)
        log_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.log_textbox = ctk.CTkTextbox(log_frame, state="disabled", font=("Courier New", 11), wrap="word")
        self.log_textbox.pack(fill="both", expand=True, padx=5, pady=5)

    def update_ui(self, status=None, log=None, encounters=None, toggle_buttons=False):
        if status: self.status_label.configure(text=status)
        if log:
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", f"[{time.strftime('%H:%M:%S')}] {log}\n")
            self.log_textbox.see("end")
            self.log_textbox.configure(state="disabled")
        if encounters is not None: self.encounter_label.configure(text=f"Encontros (aprox.): {encounters}")
        if toggle_buttons:
            is_running = self.bot.running
            self.start_button.configure(state="disabled" if is_running else "normal")
            self.stop_button.configure(state="normal" if is_running else "disabled")

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    # --- MUDANÇA AQUI ---
    # Mostra a mensagem de boas-vindas ANTES de criar a janela principal
    messagebox.showinfo("Bem-vindo!", "O Shiny Hunter foi aberto com sucesso!\n\nLembre-se de executar como administrador.")

    app = App()
    app.mainloop()