# failsafe.py
import keyboard
import threading

class FailSafeListener:
    def __init__(self, bot_instance):
        self.bot = bot_instance
        self.is_running = False
        self.paused = False # Novo estado para controlar a pausa

    def _keyboard_callback(self, event):
        if self.paused: return # Se estiver pausado, ignora o evento
        if event.name not in ['shift', 'ctrl', 'alt']:
            self.bot.update_ui(status=f"FAIL-SAFE: Tecla '{event.name}' pressionada!", log="Parando o bot por segurança.")
            self.bot.stop()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.paused = False
            keyboard.on_press(self._keyboard_callback)
            self.bot.update_ui(log="[INFO] Fail-safe de teclado ativado.")

    def stop(self):
        if self.is_running:
            self.is_running = False
            keyboard.unhook_all()
            self.bot.update_ui(log="[INFO] Fail-safe de teclado desativado.")

    def pause(self):
        """Pausa o listener do teclado."""
        if self.is_running and not self.paused:
            self.paused = True
            self.bot.update_ui(log="[INFO] Fail-safe pausado para sequência de ações.")

    def resume(self):
        """Retoma o listener do teclado."""
        if self.is_running and self.paused:
            self.paused = False
            self.bot.update_ui(log="[INFO] Fail-safe retomado.")