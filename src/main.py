from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicializar o Flask
app = Flask(__name__)

def scrape_google_trends():
    """Scrape Google Trends trending topics and search volumes using Selenium and return as JSON."""

    # Configurar o ChromeDriver
    service = Service("/usr/local/bin/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executar em modo headless
    options.add_argument("--disable-dev-shm-usage")  # Resolver problemas de espaço compartilhado
    options.add_argument("--no-sandbox")  # Necessário para rodar no Docker
    options.add_argument("--disable-gpu")  # Evitar problemas com renderização
    options.add_argument("--disable-dev-tools")  # Desabilitar DevTools
    options.add_argument("--remote-debugging-port=9222")  # Depuração remota (opcional)
    driver = webdriver.Chrome(service=service, options=options)

    trends = []

    try:
        # Acessar a URL
        url = "https://trends.google.com.br/trending?geo=US&hl=pt-BR&category=3"
        driver.get(url)

        # Aguarde os elementos principais carregarem
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.enOdEe-wZVHld-aOtOmf.jvkLtd"))
        )

        rows = driver.find_elements(By.CSS_SELECTOR, "td.enOdEe-wZVHld-aOtOmf.jvkLtd")

        for row in rows:
            try:
                # Capturar título
                title = row.find_element(By.CSS_SELECTOR, "div.mZ3RIc").text.strip()

                # Capturar volume de pesquisa
                search_volume = row.find_element(By.CSS_SELECTOR, "div.qNpYPd").get_attribute("textContent").strip()

                # Adicionar ao resultado
                trends.append({"title": title, "search_volume": search_volume})
            except Exception:
                continue
    finally:
        driver.quit()

    return trends

@app.route('/', methods=['GET'])
def home():
    """Endpoint para a página inicial."""
    return jsonify({
        "message": "Bem-vindo à API de Google Trends!",
        "endpoints": {
            "/trends": "Retorna as trends em JSON"
        }
    })

@app.route('/trends', methods=['GET'])
def get_trends():
    """Endpoint para retornar as trends em JSON."""
    try:
        trends = scrape_google_trends()
        return jsonify(trends)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
