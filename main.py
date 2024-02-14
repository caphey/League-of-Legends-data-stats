from flask import Flask, render_template, request, session, redirect, url_for
import riot
from pymongo import MongoClient, ReturnDocument

app = Flask(__name__)
app.secret_key = 'dasitathon'

# Connexion à la base de données
client = MongoClient('localhost', 27017)
db = client['api-project']
collection = db['riot']


def save_user_data(game_name, tag_line, puuid, top_champions, icon, level, info_match, win_loss_percentage, stats_three_match, cs_per_min):
    user_data = {
        'game_name': game_name,
        'tag_line': tag_line,
        'puuid': puuid,
        'top_champions': top_champions,
        'icon': icon,
        'level': level,
        'info_match': info_match,
        'win_loss_percentage': win_loss_percentage,
        'stats_three_match': stats_three_match,
        'cs_per_min': cs_per_min
    }
    user_data_for_update = user_data.copy()
    user_data_for_update.pop('_id', None)
    updated_user = collection.find_one_and_update({'game_name': game_name, 'tag_line': tag_line}, {
        '$set': user_data_for_update}, upsert=True, return_document=ReturnDocument.AFTER)

    return updated_user


def get_user_data(game_name, tag_line):
    # Récupére les données de l'utilisateur
    puuid = riot.get_puuid(game_name, tag_line)
    top_champions = riot.top_3_champions(puuid)
    icon = riot.get_icon_player(puuid)
    level = riot.get_level_player(puuid)
    info_match = riot.get_info_match_by_puuid(puuid)
    win_loss_percentage = riot.get_win_loss_percentage(puuid)
    stats_three_match = riot.get_stats_last_three_match(puuid)
    cs_per_min = riot.get_cs_per_min(puuid)

    user_data = {
        'game_name': game_name,
        'tag_line': tag_line,
        'puuid': puuid,
        'top_champions': top_champions,
        'icon': icon,
        'level': level,
        'info_match': info_match,
        'win_loss_percentage': win_loss_percentage,
        'stats_three_match': stats_three_match,
        'cs_per_min': cs_per_min
    }

    return user_data


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    game_name = request.form.get('game_name')
    tag_line = request.form.get('tag_line')

    # Check si le joueur existe déjà dans la base de données
    existing_user = collection.find_one(
        {'game_name': game_name, 'tag_line': tag_line})

    # Récupére les nouvelles données de l'API
    new_user_data = get_user_data(game_name, tag_line)

    if existing_user:
        # Si l'utilisateur existe déjà, compare les nouvelles données avec les données existantes
        if new_user_data == existing_user:
            # Si les données sont les mêmes, utilise les données existantes
            user_data = existing_user
        else:
            # Si les données sont différentes, utilise les nouvelles données et mettez à jour la base de données
            user_data = new_user_data
            user_data_for_update = user_data.copy()
            user_data_for_update.pop('_id', None)
            collection.find_one_and_update({'game_name': game_name, 'tag_line': tag_line}, {
                '$set': user_data_for_update}, upsert=True, return_document=ReturnDocument.AFTER)
    else:
        # Si l'utilisateur n'existe pas, utilise les nouvelles données et enregistrez-les dans la base de données
        user_data = new_user_data
        user_data_for_update = user_data.copy()
        user_data_for_update.pop('_id', None)
        collection.find_one_and_update({'game_name': game_name, 'tag_line': tag_line}, {
            '$set': user_data_for_update}, upsert=True, return_document=ReturnDocument.AFTER)

    # Stocke les données dans la session
    session['user_data'] = user_data
    return redirect(url_for('result'))

@app.route('/result')
def result():
    user_data = session.get('user_data', {})
    game_name = user_data.get('game_name', '')
    tag_line = user_data.get('tag_line', '')
    puuid = user_data.get('puuid', '')
    champions = user_data.get('top_champions', [])
    icon = user_data.get('icon', '')
    level = user_data.get('level', '')
    info_match = user_data.get('info_match', {})
    win_loss_percentage = user_data.get('win_loss_percentage', {})
    stats_three_match = user_data.get('stats_three_match', {})
    cs_per_min = user_data.get('cs_per_min', {})

    return render_template('result.html', game_name=game_name, tag_line=tag_line, puuid=puuid, champions=champions, icon=icon, level=level, info_match=info_match, win_loss_percentage=win_loss_percentage, stats_three_match=stats_three_match, cs_per_min=cs_per_min)

if __name__ == '__main__':
    app.run(debug=True)
