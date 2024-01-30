from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)

# Vous devez remplacer 'YOUR_RIOT_API_KEY_HERE' avec votre clé API obtenue de Riot Games.
RIOT_API_KEY = 'RGAPI-6439fe6f-9e4c-4887-aac5-5c1aff6b8f6b'
# Exemple de région, cela peut changer en fonction de la région du joueur.
REGION = 'euw1'


@app.route('/summoner/status/<summoner_name>', methods=['GET'])
def get_summoner_status(summoner_name):
    """Vérifie le statut de réponses pour l'invocateur donné de l'API de Riot."""
    summoner_url = f"https://{
        REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"

    response = requests.get(summoner_url, headers={
                            "X-Riot-Token": RIOT_API_KEY})

    # On retourne juste le code de statut de la réponse
    return jsonify({"status_code": response.status_code})


CORS(app)  # CORS est nécessaire pour que l'application fonctionne sur localhost (ou un autre domaine différent de celui de l'API de Riot Games) car l'API de Riot Games ne permet pas les requêtes cross-origin c'est-à-dire les requêtes provenant d'un autre domaine que celui de l'API de Riot Games.


# Création de la route pour obtenir les matchs récents d'un invocateur donné (10 matchs)
@app.route('/matches/<summoner_name>', methods=['GET'])
def get_recent_matches(summoner_name):
    # Obtenir l'ID invocateur
    summoner_url = f"https://{
        REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    summoner_response = requests.get(
        summoner_url, headers={"X-Riot-Token": RIOT_API_KEY})

    if summoner_response.status_code != 200:
        return jsonify({"error": "Summoner not found"}), summoner_response.status_code

    summoner_data = summoner_response.json()
    account_id = summoner_data['accountId']

    # Récupérer ID des matchs récents
    matches_url = f"https://{REGION}.api.riotgames.com/lol/match/v4/matchlists/by-account/{
        account_id}?endIndex=10"
    matches_response = requests.get(
        matches_url, headers={"X-Riot-Token": RIOT_API_KEY})

    if matches_response.status_code != 200:
        return jsonify({"error": "Matches not found"}), matches_response.status_code

    matches_data = matches_response.json()
    match_ids = [match['gameId'] for match in matches_data['matches']]

    return jsonify({"match_ids": match_ids})


if __name__ == '__main__':
    app.run(debug=True)
