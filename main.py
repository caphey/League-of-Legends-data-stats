from flask import Flask, render_template, request, session, redirect, url_for
from config import Config
from services import riot
from database import save_user_data, get_user_data

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    game_name = request.form.get('game_name')
    tag_line = request.form.get('tag_line')

    # try:
    existing_user = get_user_data(game_name, tag_line)
    new_user_data = riot.get_user_data(game_name, tag_line)

    # if existing_user != new_user_data:
    #     user_data = save_user_data(new_user_data)
    # else:
    #     user_data = existing_user

    session['user_data'] = new_user_data
    return redirect(url_for('result'))
    # except Exception as e:
    #     # Log l'erreur
    #     return render_template('error.html', message="Une erreur s'est produite. Veuillez réessayer plus tard.")


@app.route('/result')
def result():
    user_data = session.get('user_data', {})
    if not user_data:
        return redirect(url_for('index'))
    return render_template('result.html', **user_data)


if __name__ == '__main__':
    app.run(debug=Config.DEBUG)
