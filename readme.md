# PokéMMO AI Vision Hunter

<p align="center">
  <img src="https://imgur.com/gallery/pok-mmo-ai-vision-hunter-JUVGDkW" alt="Interface do Bot" width="600"/>
</p>

## 🌟 Sobre o Projeto

**PokéMMO AI Vision Hunter** não é apenas um bot de automação, é um assistente de caça inteligente que utiliza **Inteligência Artificial** para encontrar Pokémon Shiny no PokéMMO. Em vez de seguir cliques cegos, este projeto emprega um motor de **Reconhecimento Óptico de Caracteres (OCR)** para ler e interpretar a tela do jogo em tempo real.

O bot "vê" quando uma batalha começa, "lê" o nome de cada Pokémon na horda para identificar a palavra "Shiny" e gerencia de forma autônoma o uso de itens para farmar por horas, sem interrupção. Quando o tão esperado shiny aparece, ele te notifica imediatamente no celular.

**Aviso Legal:** O uso de bots e automação pode ser contra os Termos de Serviço do PokéMMO. Este projeto foi desenvolvido para fins educacionais e para o estudo de Visão Computacional e IA aplicada. Use por sua conta e risco.

---

## ✨ Funcionalidades Principais

*   **Visão de IA (OCR):** Utiliza Tesseract para ler a tela, detectando o início de batalhas e a presença de Pokémon Shiny.
*   **Farm Autônomo:** Executa o ciclo completo de usar `Aroma Doce` (Sweet Scent), verificar a horda e fugir da batalha.
*   **Gerenciamento Inteligente de PP:** Controla o gasto de PP e utiliza `Fruta Ciema` (Leppa Berry) para restaurá-lo, permitindo sessões de farm prolongadas.
*   **Notificação Instantânea no Celular:** Envia uma notificação push urgente (via `ntfy.sh`) assim que um shiny é detectado.
*   **Interface Gráfica Amigável:** Criada com `customtkinter` para exibir status, logs detalhados e controles de Iniciar/Parar.
*   **Fail-Safe de Segurança:** O bot pode ser parado imediatamente a qualquer momento pressionando uma tecla do teclado.

---

## 🚀 Como a IA é Utilizada

O "cérebro" do bot está na sua capacidade de transformar pixels em informação útil.

1.  **Detecção de Estado:** Em vez de depender de pausas fixas, o bot tira um "screenshot" da área do botão de batalha e usa a IA do **Tesseract** para ler o texto. Se ele lê "FUGIR", ele sabe que está em batalha.
2.  **Verificação de Shiny:** Esta é a parte mais crítica. Para cada Pokémon na horda, o bot:
    *   Isola a região do nome do Pokémon.
    *   **Aplica técnicas de pré-processamento de imagem:** redimensiona a imagem e a converte para preto e branco puro para maximizar a legibilidade.
    *   Envia a imagem tratada para a IA do Tesseract, que foi treinada em milhões de textos para reconhecer os caracteres.
    *   O bot então analisa a "tradução" do Tesseract, procurando pela palavra-chave "shiny".
3.  **Tomada de Decisão:** Com base na informação extraída pela IA, a automação (o resto do código com `pyautogui`) entra em ação, seja para fugir da batalha ou para parar tudo e alertar o usuário.

Este ciclo de **Ver -> Ler -> Entender -> Agir** é o que diferencia este projeto de um simples macro.

---
## 🛠️ Configuração e Instalação

Para rodar este projeto, você precisará do Python 3 e de algumas dependências.

### 1. Instale o Tesseract-OCR

Este bot depende do motor de OCR do Tesseract.
*   Baixe o instalador para Windows na [página oficial do Tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
*   Durante a instalação, certifique-se de marcar os pacotes de idioma adicionais para **"English" (eng)** e **"Portuguese" (por)**.

### 2. Prepare o Ambiente Python

É altamente recomendado usar um ambiente virtual (`venv`).

```bash
# Navegue até a pasta do projeto
cd /caminho/para/o/projeto

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
# source venv/bin/activate
```

### 3. Instale as Bibliotecas Python

Com o ambiente virtual ativado, instale todas as dependências com um único comando:

```bash
pip install -r requirements.txt
```

### 4. Configure o `config.json`

Este é o passo mais importante.
*   Abra o PokéMMO e use o script `coordenadas.py` para encontrar as coordenadas (X, Y) e as áreas de tela (bbox) para todas as ações.
*   Atualize os valores no arquivo `config.json` para corresponderem à sua resolução de tela e layout do jogo.

### 5. (Opcional) Configure as Notificações no Celular

*   Baixe o aplicativo **ntfy** (para [Android](https://play.google.com/store/apps/details?id=io.heckel.ntfy) ou [iOS](https://apps.apple.com/us/app/ntfy/id1625396347)).
*   No app, inscreva-se em um "tópico" com um nome secreto e único (ex: `shiny-alert-meu-nome-9876`).
*   Abra o arquivo `bot_logic.py` e atualize a variável `topic` na função `send_mobile_notification` com o mesmo nome.

---

## 🏃 Como Executar

1.  Certifique-se de que seu ambiente virtual está ativado.
2.  **Execute o script `main.py` como Administrador** (no Windows, abra o PowerShell/CMD como Admin, navegue até a pasta e execute o comando). Isso é necessário para que o `pyautogui` possa controlar a janela do jogo.

    ```bash
    python main.py
    ```
3.  Uma caixa de diálogo de boas-vindas aparecerá. Clique em "OK".
4.  A interface do bot será aberta. Clique em **"Iniciar Bot"**.
5.  Você terá 6 segundos para clicar na janela do PokéMMO e torná-la a janela ativa.
6.  Sente-se, relaxe e espere o seu shiny!

---
## 📜 Requirements

As dependências do projeto estão listadas no arquivo `requirements.txt`:

*   `customtkinter`
*   `pyautogui`
*   `pytesseract`
*   `Pillow`
*   `keyboard`
*   `requests`
