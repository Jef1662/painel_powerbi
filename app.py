import logging
from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

# Caminho para o arquivo JSON de links
LINKS_FILE = 'links.json'

# Carregar os dados dos links do arquivo JSON
def carregar_links():
    if os.path.exists(LINKS_FILE):
        with open(LINKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Salvar os dados dos links no arquivo JSON
def salvar_links(dados):
    with open(LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    setor = request.args.get('setor', 'EXTRUSAO')  # valor padrão
    dados = carregar_links()
    relatorios = dados.get(setor.upper(), [])
    logging.info(f"Acessada página inicial - Setor: {setor}")
    return render_template('index.html', setor=setor, relatorios=relatorios)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    senha = request.args.get('senha', '')
    if senha != '1234':  # Senha simples para demonstração
        logging.warning("Tentativa de acesso não autorizado à página de admin")
        return redirect(url_for('index'))

    dados = carregar_links()
    if request.method == 'POST':
        setor = request.form['setor']
        titulo = request.form['titulo']
        url = request.form['url']
        img = request.form['img']
        novo_id = datetime.now().strftime("%Y%m%d%H%M%S")

        if setor not in dados:
            dados[setor] = []

        dados[setor].append({
            "id": novo_id,
            "titulo": titulo,
            "url": url,
            "img": img
        })
        salvar_links(dados)
        logging.info(f"Novo relatório adicionado - Setor: {setor}, Título: {titulo}")
        return redirect(url_for('admin', senha=senha))

    return render_template('admin.html', dados=dados)

@app.route('/excluir/<setor>/<id>', methods=['POST'])
def excluir(setor, id):
    senha = request.args.get('senha', '')
    if senha != '1234':
        logging.warning("Tentativa de exclusão não autorizada")
        return redirect(url_for('index'))

    dados = carregar_links()
    if setor in dados:
        dados[setor] = [link for link in dados[setor] if link['id'] != id]
        salvar_links(dados)
        logging.info(f"Relatório excluído - Setor: {setor}, ID: {id}")
    return redirect(url_for('admin', senha=senha))

if __name__ == '__main__':
    logging.info("Iniciando servidor Flask")
    app.run(debug=False, host='0.0.0.0', port=8050)