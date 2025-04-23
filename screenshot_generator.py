from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import os
from PIL import Image  # Importando Pillow para manipulação de imagens

# Caminho para o ChromeDriver
CHROME_DRIVER_PATH = r"C:\Users\jeferson.s\OneDrive - INPLAC SA\Ambientes_virtuais\Ambiente_2\painel_web\chromedriver.exe"

# Caminho para links.json
LINKS_FILE = os.path.join(os.path.dirname(__file__), 'links.json')

# Pasta de saída para os screenshots
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'screenshots')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configurações do navegador
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Executar em segundo plano
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=2560,1440")  # Altíssima resolução

# Inicializa o navegador
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Lê o JSON
with open(LINKS_FILE, 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Função para cortar a imagem (exemplo: cortar uma parte do topo)
def cortar_imagem(caminho_arquivo):
    with Image.open(caminho_arquivo) as img:
        # Defina as coordenadas para cortar (exemplo: cortando 100px do topo)
        largura, altura = img.size
        # Corte a imagem (aqui, cortamos 100px do topo e mantemos a largura inteira)
        img_cortada = img.crop((0, 0, largura, altura - 75))
        img_cortada.save(caminho_arquivo)  # Sobrescreve o arquivo com a imagem cortada

# Processa cada link
for setor, relatorios in dados.items():
    for rel in relatorios:
        url = rel['url']
        id_ = rel['id']
        nome_arquivo = f"{setor}_{id_}.png"
        caminho_arquivo = os.path.join(OUTPUT_DIR, nome_arquivo)

        print(f"Acessando: {url}")
        driver.get(url)

        time.sleep(10)  # Espera o carregamento (ajuste se necessário)

        print(f"Salvando screenshot: {caminho_arquivo}")
        driver.save_screenshot(caminho_arquivo)

        # Aplica o corte na imagem
        cortar_imagem(caminho_arquivo)

driver.quit()
print("Capturas finalizadas.")
