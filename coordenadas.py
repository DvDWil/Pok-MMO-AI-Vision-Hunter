# coordenadas.py
import pyautogui
import time

print("Iniciando o localizador de coordenadas.")
print("Mova o mouse para a posição desejada na tela do jogo.")
print("Pressione Ctrl+C no terminal para parar.")

try:
    while True:
        # Pega a posição atual (X, Y) do mouse
        x, y = pyautogui.position()
        
        # Pega a cor (R, G, B) do pixel sob o mouse
        pixel_color = pyautogui.pixel(x, y)
        
        # Formata a string para exibição
        position_str = f"X: {str(x).rjust(4)}  Y: {str(y).rjust(4)}"
        color_str = f"RGB: ({str(pixel_color[0]).rjust(3)}, {str(pixel_color[1]).rjust(3)}, {str(pixel_color[2]).rjust(3)})"
        
        # Imprime na mesma linha para não poluir o terminal
        print(f"{position_str} | {color_str}", end='\r')
        
        # Pequena pausa para não sobrecarregar a CPU
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nPrograma finalizado.")