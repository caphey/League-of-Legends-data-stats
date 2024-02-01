import requests
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

# API key provenant de la plateforme Riot Games
api_key = "RGAPI-08f13e20-7c65-4b94-9af7-cb3c7fcff42b"

platform_api = ["BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2",
                "NA1", "OC1", "TR1", "RU", "PH2", "SG2", "TH2", "TW2", "VN2"]
region_api = ["americas", "asia", "europe", "sea"]
# startTime = "1706221916"
# endTime = "1706741999"

# date_created = "01/01/2009"
# date_format = "%d/%m/%Y"
# date_created_timestamp = round(datetime.strptime(
#     date_created, date_format).timestamp())

startTime = "1623974400"

today_timestamp = round(time.time())

today = datetime.now()
ten_days_ago = today - timedelta(days=10)
ten_days_ago_timestamp = round(ten_days_ago.timestamp())


# Fonction qui permet de récupérer les informations du joueur
def get_puuid(gameName, tagLine):
    # gameName : nom du joueur
    # tagLine : tag du joueur
    url = "https://{}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}?api_key={}".format(
        region_api[2], gameName, tagLine, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        player_info = response.json()
        puuid = player_info["puuid"]
        return puuid

    else:
        return None


# Fonction qui permet de récupérer la liste des matchs du joueur
def get_info_match_by_puuid(puuid):
    # puuid : identifiant unique du joueur
    url = "https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?startTime={}&endTime={}&api_key={}".format(
        region_api[2], puuid, ten_days_ago_timestamp, today_timestamp, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        list_match = response.json()
        match_info_list = []
        all_matches_info = []
        for match_id in list_match:
            url_match = "https://{}.api.riotgames.com/lol/match/v5/matches/{}?api_key={}".format(
                region_api[2], match_id, api_key)
            response = requests.get(url_match)
            if response.status_code == 200:
                match_info = response.json()
                part_index = match_info["metadata"]["participants"].index(
                    puuid)

                champion_name = match_info["info"]["participants"][part_index]["championName"]
                url_icon = "https://ddragon.leagueoflegends.com/cdn/14.2.1/img/champion/{}.png".format(
                    champion_name)
                did_win = match_info["info"]["participants"][part_index]["win"]
                if did_win:
                    did_win = "Victoire"
                else:
                    did_win = "Défaite"
                date_match = datetime.fromtimestamp(
                    match_info["info"]["gameCreation"] / 1000).strftime("%d/%m/%Y")
                kills = match_info["info"]["participants"][part_index]["kills"]
                deaths = match_info["info"]["participants"][part_index]["deaths"]
                assists = match_info["info"]["participants"][part_index]["assists"]
                champ_level = match_info["info"]["participants"][part_index]["champLevel"]
                gold_earned = match_info["info"]["participants"][part_index]["goldEarned"]
                total_damage_dealt_to_champions = match_info["info"][
                    "participants"][part_index]["totalDamageDealtToChampions"]
                champions = match_info["info"]["participants"][part_index]["championName"]
                if deaths == 0:
                    kda = (kills + assists)
                else:
                    kda = (kills + assists) / deaths
                match_info_list = [url_icon, did_win, kills, deaths, assists, champ_level,
                                   gold_earned, total_damage_dealt_to_champions, champions, round(kda, 2), date_match]
                all_matches_info.append(match_info_list)
            else:
                return None
        return all_matches_info
    else:
        return None


# Fonction qui permet de récupérer les 3 champions les plus joués
def top_3_champions(puuid):
    # champions : liste des champions joués
    champions_player_url = "https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{}/top?api_key={}".format(
        platform_api[2], puuid, api_key)
    response = requests.get(champions_player_url)
    if response.status_code == 200:
        champions_player = response.json()
        data_champions_url = "https://ddragon.leagueoflegends.com/cdn/14.2.1/data/en_US/champion.json"
        response = requests.get(data_champions_url)
        if response.status_code == 200:
            data_champions = response.json()
            top_champions = []
            # On parcourt la liste des champions du joueur pour trouver le nom du champion correspondant à l'id
            for i in range(len(champions_player)):
                # On parcourt la liste de tous les champions pour trouver le nom du champion correspondant à l'id
                for key, value in data_champions["data"].items():
                    # Si l'id du champion du joueur correspond à l'id du champion de la liste de tous les champions
                    if champions_player[i]["championId"] == int(value["key"]):
                        # On ajoute le nom du champion à la liste des champions les plus joués
                        top_champions.append(value["name"])
            return top_champions
        else:
            return None
    else:
        return None


def get_level_player(puuid):
    url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}?api_key={}".format(
        platform_api[2], puuid, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        summoner_level = response.json()["summonerLevel"]
        return summoner_level
    else:
        return None


def get_icon_player(puuid):
    url = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}?api_key={}".format(
        platform_api[2], puuid, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        summoner_icon_id = response.json()["profileIconId"]
        url_data_icon = "https://ddragon.leagueoflegends.com/cdn/14.2.1/data/en_US/profileicon.json"
        response = requests.get(url_data_icon)
        if response.status_code == 200:
            data_icon = response.json()
            for key, value in data_icon["data"].items():
                if summoner_icon_id == int(key):
                    summoner_icon = value["image"]["full"]
                    return summoner_icon
        else:
            return None
    else:
        return None


def get_icon_champion(champion_name):
    url = "https://ddragon.leagueoflegends.com/cdn/14.2.1/img/champion/{}.png".format(
        champion_name)
    return url


def get_win_loss_percentage(puuid):
    champions_player_url = "https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{}/top?count=5&api_key={}".format(
        platform_api[2], puuid, api_key)
    response = requests.get(champions_player_url)
    if response.status_code == 200:
        champions_player = response.json()
        data_champions_url = "https://ddragon.leagueoflegends.com/cdn/14.2.1/data/en_US/champion.json"
        response = requests.get(data_champions_url)
        if response.status_code == 200:
            data_champions = response.json()
            top_champions = []
            win_loss_percentage = {}
            # On parcourt la liste des champions du joueur pour trouver le nom du champion correspondant à l'id
            for i in range(len(champions_player)):
                # On parcourt la liste de tous les champions pour trouver le nom du champion correspondant à l'id
                for key, value in data_champions["data"].items():
                    # Si l'id du champion du joueur correspond à l'id du champion de la liste de tous les champions
                    if champions_player[i]["championId"] == int(value["key"]):
                        # On ajoute le nom du champion à la liste des champions les plus joués
                        top_champions.append(value["name"])
                        win_loss_percentage[value["name"]] = {
                            "wins": 0, "losses": 0}
            # On peut seulement récupérer les données des champions concernant les 20 derniers matchs car l'API permet seulement 100 requêtes toutes les 2 minutes
            matchs_url = "https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?startTime={}&endTime={}&api_key={}".format(
                region_api[2], puuid, startTime, today_timestamp, api_key)
            response = requests.get(matchs_url)
            if response.status_code == 200:
                list_match = response.json()
                for match_id in list_match:
                    url_match = "https://{}.api.riotgames.com/lol/match/v5/matches/{}?api_key={}".format(
                        region_api[2], match_id, api_key)
                    response = requests.get(url_match)
                    if response.status_code == 200:
                        match_info = response.json()
                        part_index = match_info["metadata"]["participants"].index(
                            puuid)
                        champion_name = match_info["info"]["participants"][part_index]["championName"]
                        if champion_name in top_champions:
                            if match_info["info"]["participants"][part_index]["win"]:
                                win_loss_percentage[champion_name]["wins"] += 1
                            else:
                                win_loss_percentage[champion_name]["losses"] += 1
            else:
                return None
            return win_loss_percentage
        else:
            return None
    else:
        return None


def plot_win_loss_percentage(win_loss_percentage):
    champions = []
    wins = []
    losses = []

    for champion, stats in win_loss_percentage.items():
        if stats["wins"] != 0 or stats["losses"] != 0:
            champions.append(champion)
            wins.append(stats["wins"])
            losses.append(stats["losses"])

    if champions:
        fig, ax = plt.subplots()

        ax.pie(wins, losses, labels=champions, autopct='%1.1f%%', startangle=90)
        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')

        ax.set_title('Win-Loss Percentage by Champion')

        plt.show()


print(plot_win_loss_percentage(get_win_loss_percentage(get_puuid("Cig", "ImYou"))))

# print(get_win_loss_percentage(get_puuid("27o", "euw27")))
