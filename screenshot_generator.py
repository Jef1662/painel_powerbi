import os
import time
import json
from datetime import datetime
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ===================== CONFIGURAÇÕES GERAIS =====================

# Caminho para o ChromeDriver via variável de ambiente
CHROME_DRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
if not CHROME_DRIVER_PATH or not os.path.exists(CHROME_DRIVER_PATH):
    raise FileNotFoundError(f"ChromeDriver não encontrado no caminho: {CHROME_DRIVER_PATH}")

# Caminho para o arquivo de links
LINKS_FILE = os.path.join(os.path.dirname(__file__), 'links.json')

# Pasta de saída dos screenshots
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'screenshots')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Caminho para salvar o log (apenas se a pasta existir)
LOG_DIR = r"C:\Users\powerbi\Desktop\Pagina_web_alternante_II\painel_powerbi\logs"
LOG_FILE = os.path.join(LOG_DIR, 'log_screenshots.txt')
def registrar_log(mensagem):
    try:
        if os.path.exists(LOG_DIR):
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] {mensagem}\n")
    except:
        pass  # Ignora falhas no log

registrar_log("Script iniciado com sucesso.")
registrar_log(f"Salvando screenshots em: {OUTPUT_DIR}")

# ===================== CONFIGURAÇÃO DO NAVEGADOR =====================

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=2560,1440")

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# ===================== FUNÇÃO DE CORTE DE IMAGEM =====================

def cortar_imagem(caminho_arquivo):
    with Image.open(caminho_arquivo) as img:
        largura, altura = img.size
        img_cortada = img.crop((0, 0, largura, altura - 75))
        img_cortada.save(caminho_arquivo)

# ===================== EXECUÇÃO PRINCIPAL =====================

with open(LINKS_FILE, 'r', encoding='utf-8') as f:
    dados = json.load(f)

for setor, relatorios in dados.items():
    for rel in relatorios:
        url = rel['url']
        id_ = rel['id']
        nome_arquivo = f"{setor}_{id_}.png"
        caminho_arquivo = os.path.join(OUTPUT_DIR, nome_arquivo)

        registrar_log(f"Acessando: {url}")
        driver.get(url)

        time.sleep(10)  # Aguarda carregamento

        driver.save_screenshot(caminho_arquivo)
        cortar_imagem(caminho_arquivo)

        registrar_log(f"Screenshot salvo: {caminho_arquivo}")

driver.quit()
registrar_log("Script finalizado com sucesso.")
print("Capturas finalizadas.")
