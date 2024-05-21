from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import instaloader
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/download', methods=['POST'])
def download_post():
    url = request.form['url']
    shortcode = url.split("/")[-2]

    L = instaloader.Instaloader()

    # Baixar o post
    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        owner_username = post.owner_username  # Guarda o nome do usuário dono do post
        os.makedirs(owner_username, exist_ok=True)
        L.download_post(post, target=owner_username)
    except Exception as e:
        return f"Erro ao baixar o post: {str(e)}"

    # Encontrar o arquivo correto para servir
    for file in os.listdir(owner_username):
        if file.endswith('.jpg') or file.endswith('.mp4'):
            return redirect(url_for('serve_file', filename=os.path.join(owner_username, file)))

    return "Arquivo não encontrado"

@app.route('/files/<path:filename>')
def serve_file(filename):
    # O diretório principal do projeto é usado diretamente
    directory = os.getcwd()
    try:
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        return "Arquivo não encontrado", 404

#if __name__ == '__main__':
    #app.run(debug=True)
