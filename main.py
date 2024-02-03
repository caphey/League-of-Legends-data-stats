from flask import Flask, render_template, request, session, redirect, url_for
import riot

app = Flask(__name__)
app.secret_key = 'dasitathon'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
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
    session['top_champions'] = top_champions
    session['icon'] = icon
    session['level'] = level
    session['info_match'] = info_match
    session['win_loss_percentage'] = win_loss_percentage
    session['stats_three_match'] = stats_three_match
    session['cs_per_min'] = cs_per_min
    return redirect(url_for('result'))


@app.route('/result')
def result():
    game_name = session.get('game_name', '')
    tag_line = session.get('tag_line', '')
    champions = session.get('top_champions', [])
    icon = session.get('icon', '')
    level = session.get('level', '')
    info_match = session.get('info_match', {})
    win_loss_percentage = session.get('win_loss_percentage', {})
    stats_three_match = session.get('stats_three_match', {})
    cs_per_min = session.get('cs_per_min', {})
    return render_template('result.html', game_name=game_name, tag_line=tag_line, champions=champions, icon=icon, level=level, info_match=info_match, win_loss_percentage=win_loss_percentage, stats_three_match=stats_three_match, cs_per_min=cs_per_min)


if __name__ == '__main__':
    app.run(debug=True)
