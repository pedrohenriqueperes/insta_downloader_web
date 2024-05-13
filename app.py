from flask import Flask, render_template, request, redirect, url_for
import instaloader
import os
from flask_cors import CORS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/download', methods=['POST'])
def download_post():
    url = request.form['url']
    username = request.form['username']
    password = request.form['password']
    shortcode = url.split("/")[-2]

    L = instaloader.Instaloader()

    session_filename = f"{username}_session"
    # Checando se o arquivo de sessão existe
    if os.path.exists(session_filename):
        L.load_session_from_file(username, filename=session_filename)
    else:
        try:
            L.login(username, password)
            L.save_session_to_file(filename=session_filename)
        except instaloader.exceptions.TwoFactorAuthRequiredError:
            return "Autenticação de dois fatores requerida, por favor verifique seu dispositivo."
        except instaloader.exceptions.BadCredentialsException:
            return "Falha no login: verifique seu nome de usuário e senha."
        except Exception as e:
            return f"Erro ao fazer login: {str(e)}"

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target=post.owner_username)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao baixar o post: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
