# bot_logic.py
import pyautogui
import time
import pytesseract
from PIL import Image, ImageGrab
import winsound
import json
import threading
import requests # IMPORT NECESSÁRIO PARA AS NOTIFICAÇÕES

class PokemmoBot:
    def __init__(self, update_ui_callback):
        self.update_ui = update_ui_callback
        pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        self.running = False
        self.thread = None
        self.encontros = 0
        self.pp_restantes = 0
        self.config = {}
        self.failsafe_listener = None
        self.lock = threading.Lock()

    def set_failsafe_listener(self, listener):
        self.failsafe_listener = listener

    def carregar_config(self):
        with open('config.json', 'r') as f:
            config_data = json.load(f)
        perfil_ativo_nome = config_data['perfil_ativo']
        self.config = config_data['perfis'][perfil_ativo_nome]
        self.pp_restantes = self.config.get('pp_total_aroma_doce', 0)
        self.update_ui(status=f"Perfil carregado: {perfil_ativo_nome}")

    # --- FUNÇÃO DE NOTIFICAÇÃO RESTAURADA ---
    def send_mobile_notification(self, title, message):
        topic = "shiny-hunt-dvd22"
        try:
            requests.post(f"https://ntfy.sh/{topic}",
                          data=message.encode('utf-8'),
                          headers={
                              "Title": title.encode('utf-8'),
                              "Priority": "urgent",
                              "Tags": "tada,partying_face"
                          })
            self.update_ui(log="[INFO] Notificação enviada para o celular!")
        except Exception as e:
            self.update_ui(log=f"[ERRO] Falha ao enviar notificação: {e}")

    def is_in_battle(self):
        try:
            config_batalha = self.config['verificacao_batalha']
            bbox = config_batalha['bbox_botao_fugir']
            texto_esperado = config_batalha['texto_esperado']
            img = ImageGrab.grab(bbox=bbox).convert('L')
            texto_lido = pytesseract.image_to_string(img, lang='por').strip()
            self.update_ui(log=f"Verificando botão de batalha. Leu: '{texto_lido}'")
            return texto_esperado.lower() in texto_lido.lower()
        except Exception:
            return False

    def usar_aroma_doce(self):
        self.update_ui(status="Usando Aroma Doce (hotkey)...")
        hotkey = self.config['hotkeys']['aroma_doce']
        
        if self.failsafe_listener: self.failsafe_listener.pause()
        try:
            pyautogui.press(hotkey)
        finally:
            if self.failsafe_listener: self.failsafe_listener.resume()

        self.update_ui(log=f"Apertou '{hotkey}'. Aguardando {self.config['tempo_espera_batalha']}s para a batalha.")
        time.sleep(self.config['tempo_espera_batalha'])

    def fugir_batalha_horda(self):
        botao_fugir_coord = self.config['verificacao_batalha']['bbox_botao_fugir']
        x = (botao_fugir_coord[0] + botao_fugir_coord[2]) // 2
        y = (botao_fugir_coord[1] + botao_fugir_coord[3]) // 2
        self.update_ui(status="Não é shiny. Fugindo da horda...")
        
        if self.failsafe_listener: self.failsafe_listener.pause()
        try:
            pyautogui.click(x, y)
        finally:
            if self.failsafe_listener: self.failsafe_listener.resume()
            
        time.sleep(4)

    def usar_fruta_ciema(self):
        self.update_ui(status="PPs acabaram. Usando Fruta Ciema...")
        hotkey_fruta = self.config['hotkeys']['menu_frutas']
        coords = self.config['coords_fruta']
        
        if self.failsafe_listener: self.failsafe_listener.pause()
        try:
            pyautogui.press(hotkey_fruta); time.sleep(2)
            pyautogui.moveTo(*coords['pokemon_para_usar_fruta'], duration=0.2); pyautogui.click(); time.sleep(2)
            pyautogui.moveTo(*coords['habilidade_para_restaurar'], duration=0.2); pyautogui.click(); time.sleep(2)
            pyautogui.moveTo(*coords['botao_maximo_frutas'], duration=0.2); pyautogui.click(); time.sleep(2)
            pyautogui.moveTo(*coords['botao_usar_frutas'], duration=0.2); pyautogui.click(); time.sleep(2)
        finally:
            if self.failsafe_listener: self.failsafe_listener.resume()
        
        self.update_ui(log="PP restaurado com sucesso!")
        self.pp_restantes = self.config.get('pp_total_aroma_doce', 0)
        self.update_ui(log=f"PP resetado para {self.pp_restantes}.")

    def verificar_shiny(self):
        whitelist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ. 0123456789'
        tesseract_config = f'--psm 7 -c tessedit_char_whitelist="{whitelist}"'
        for slot in self.config['bbox_nome_pokemon']:
            bbox, posicao = slot['bbox'], slot['posicao']
            img = ImageGrab.grab(bbox=bbox)
            width, height = img.size
            img = img.resize((width * 3, height * 3), Image.Resampling.LANCZOS)
            img = img.convert('L')
            img = img.point(lambda p: 0 if p < 150 else 255)
            texto = pytesseract.image_to_string(img, lang='eng', config=tesseract_config).strip()
            if len(texto) < 5: continue
            self.update_ui(log=f"Slot '{posicao}': Leu '{texto}'")
            texto_lower = texto.lower()
            if "shiny" in texto_lower and any(alvo.lower() in texto_lower for alvo in self.config['pokemon_alvo']):
                self.update_ui(log=f"[!!!] SHINY ENCONTRADO NO SLOT '{posicao}': '{texto}'")
                # ENVIA A NOTIFICAÇÃO REAL QUANDO O SHINY É ENCONTRADO
                self.send_mobile_notification("SHINY ENCONTRADO!", f"Pokémon: {texto}")
                return True
        self.update_ui(log="Nenhum shiny encontrado na horda.")
        return False

    def tocar_alerta(self):
        for _ in range(5): winsound.Beep(1500, 500); time.sleep(0.1)

    def loop_de_farm(self):
        self.encontros = 0
        self.pp_restantes = self.config.get('pp_total_aroma_doce', 0)
        self.update_ui(status="Iniciando ciclo com hotkeys...")
        
        while self.running:
            if not self.running: break
            
            if self.pp_restantes < 5:
                self.usar_fruta_ciema()
                if not self.running: break
            
            self.update_ui(status=f"PP Restante: {self.pp_restantes}", encounters=self.encontros)
            self.usar_aroma_doce()
            self.pp_restantes -= 5
            self.encontros += 5

            if not self.running: break
            
            if self.is_in_battle():
                self.update_ui(status="Batalha detectada. Verificando shiny...")
                time.sleep(1.5)
                if self.verificar_shiny():
                    self.tocar_alerta()
                    self.update_ui(status=">>> SHINY ENCONTRADO! BOT PARADO! <<<")
                    self.stop()
                    break
                else:
                    self.fugir_batalha_horda()
            else:
                self.update_ui(log="[AVISO] Batalha não iniciou. Continuando...")
            
            time.sleep(1)

    def start(self):
        with self.lock:
            if not self.running:
                self.running = True
                
                # --- NOTIFICAÇÃO DE TESTE / INÍCIO ---
                self.send_mobile_notification("Shiny Hunter", "O farm foi iniciado!")
                
                if self.failsafe_listener: self.failsafe_listener.start()
                self.thread = threading.Thread(target=self.loop_de_farm, daemon=True)
                self.thread.start()
                self.update_ui(status="Bot iniciado!", toggle_buttons=True)

    def stop(self):
        with self.lock:
            if self.running:
                self.running = False
                if self.failsafe_listener:
                    self.failsafe_listener.stop()
                self.update_ui(status="Bot parado.", toggle_buttons=True)