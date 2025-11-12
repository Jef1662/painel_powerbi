import os
import time
import json
from datetime import datetime
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# ===================== CONFIGURAÇÕES GERAIS =====================

# A partir do Selenium 4.6+, o Selenium Manager gerencia o ChromeDriver automaticamente.
# Não é mais necessário definir o caminho manualmente.
# CHROME_DRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
# if not CHROME_DRIVER_PATH or not os.path.exists(CHROME_DRIVER_PATH):
#     raise FileNotFoundError(f"ChromeDriver não encontrado no caminho: {CHROME_DRIVER_PATH}")
# Tempo de espera para o carregamento da página (em segundos)
WAIT_TIME = int(os.getenv("SCREENSHOT_WAIT_TIME", 30))

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
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--disk-cache-size=0")
chrome_options.add_argument("--media-cache-size=0")
# Suprime logs de erro irrelevantes do console
chrome_options.add_argument('--log-level=3')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# O Selenium Manager encontrará e usará o driver correto automaticamente.
# service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(options=chrome_options)

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
        url = rel.get('url', '').strip()
        id_ = rel['id']
        nome_arquivo = f"{setor}_{id_}.png"
        caminho_arquivo = os.path.join(OUTPUT_DIR, nome_arquivo)

        if not url:
            registrar_log(f"URL vazia para {setor} - ID: {id_}. Ignorando captura.")
            continue

        try:
            registrar_log(f"Acessando: {url}")
            
            # Navega para a URL
            driver.get(url)

            # Aguarda o carregamento do relatório do Power BI e limpa o cache
            wait = WebDriverWait(driver, WAIT_TIME)
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.report-container, report-embed")))

            # Adiciona uma espera fixa para garantir que os dados do PBI sejam carregados
            registrar_log("Aguardando 15 segundos para o carregamento completo do Power BI...")
            time.sleep(15)
            
            driver.save_screenshot(caminho_arquivo)
            cortar_imagem(caminho_arquivo)

            registrar_log(f"Screenshot salvo: {caminho_arquivo}")

        except Exception as e:
            # Captura qualquer erro (timeout, elemento não encontrado, etc.), registra e continua
            error_message = str(e).split('\n')[0] # Pega apenas a primeira linha do erro
            registrar_log(f"ERRO ao processar {url}: {error_message}")

driver.quit()
registrar_log("Script finalizado com sucesso.")
print("Capturas finalizadas.")
