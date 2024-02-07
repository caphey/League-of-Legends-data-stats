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
    # collection.insert_one(user_data)
    user_data_for_update = user_data.copy()
    user_data_for_update.pop('_id', None)
    updated_user = collection.find_one_and_update({'game_name': game_name, 'tag_line': tag_line}, {
        '$set': user_data_for_update}, upsert=True, return_document=ReturnDocument.AFTER)
    return updated_user


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

    if existing_user:
        # Si le joueur existe déjà dans la base de données, on récupère ses données
        game_name = request.form.get('game_name')
        tag_line = request.form.get('tag_line')
        puuid = existing_user.get('puuid')
        top_champions = existing_user.get('top_champions')
        icon = existing_user.get('icon')
        level = existing_user.get('level')
        info_match = existing_user.get('info_match')
        win_loss_percentage = existing_user.get('win_loss_percentage')
        stats_three_match = existing_user.get('stats_three_match')
        cs_per_min = existing_user.get('cs_per_min')
    else:
        # Si le joueur n'existe pas dans la base de données, on récupère ses données via l'API et on les sauvegarde
        game_name = request.form.get('game_name')
        tag_line = request.form.get('tag_line')
        puuid = riot.get_puuid(game_name, tag_line)
        top_champions = riot.top_3_champions(puuid)
        icon = riot.get_icon_player(puuid)
        level = riot.get_level_player(puuid)
        info_match = riot.get_info_match_by_puuid(puuid)
        win_loss_percentage = riot.get_win_loss_percentage(puuid)
        stats_three_match = riot.get_stats_last_three_match(puuid)
        cs_per_min = riot.get_cs_per_min(puuid)

    session['game_name'] = game_name
    session['tag_line'] = tag_line
    session['puuid'] = puuid
    session['top_champions'] = top_champions
    session['icon'] = icon
    session['level'] = level
    session['info_match'] = info_match
    session['win_loss_percentage'] = win_loss_percentage
    session['stats_three_match'] = stats_three_match
    session['cs_per_min'] = cs_per_min

    save_user_data(game_name, tag_line, puuid, top_champions, icon, level, info_match,
                   win_loss_percentage, stats_three_match, cs_per_min)

    return redirect(url_for('result'))


@app.route('/result')
def result():
    game_name = session.get('game_name', '')
    tag_line = session.get('tag_line', '')
    puuid = session.get('puuid', '')
    champions = session.get('top_champions', [])
    icon = session.get('icon', '')
    level = session.get('level', '')
    info_match = session.get('info_match', {})
    info_match = session.get('info_match')
    if info_match is None:
        info_match = {}
    win_loss_percentage = session.get('win_loss_percentage', {})
    stats_three_match = session.get('stats_three_match', {})
    cs_per_min = session.get('cs_per_min', {})

    return render_template('result.html', game_name=game_name, tag_line=tag_line, puuid=puuid, champions=champions, icon=icon, level=level, info_match=info_match, win_loss_percentage=win_loss_percentage, stats_three_match=stats_three_match, cs_per_min=cs_per_min)


if __name__ == '__main__':
    app.run(debug=True)
