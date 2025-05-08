from flask import Flask, render_template, request, redirect, url_for
import json, os
from datetime import datetime

app = Flask(__name__)

LINKS_FILE = os.path.join(os.path.dirname(__file__), 'links.json')

def carregar_links():
    with open(LINKS_FILE, 'r') as f:
        return json.load(f)
    
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/')
def index():
    setores = list(carregar_links().keys())
    return render_template('index.html', setores=setores)

@app.route('/relatorios')
def relatorios():
    setor = request.args.get('setor')
    dados = carregar_links()

    if not setor or setor not in dados:
        return redirect(url_for('index'))

    links = dados
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return render_template('relatorios.html', setor=setor, links_json=json.dumps(links), timestamp=timestamp)  # JSON como string segura

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)


