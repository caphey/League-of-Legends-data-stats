import requests
from datetime import datetime

# API key provenant de la plateforme Riot Games
api_key = "RGAPI-8afd6d0b-95ee-42b6-91dd-21a5aa5f501e"

platform_api = ["BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2",
                "NA1", "OC1", "TR1", "RU", "PH2", "SG2", "TH2", "TW2", "VN2"]
region_api = ["americas", "asia", "europe", "sea"]
startTime = "1705705200"  # 20 janvier 2024 00:00:00
endTime = "1706569200"  # 30 janvier 2024 00:00:00
# puuid = "P0CtqteOnbBAXVwPMTnlKo6a_L2JxZjdeFOflppDPGMUFZLUSl917s2xPfmR3fSa79WZJu9cDTxZJQ"


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
        region_api[2], puuid, startTime, endTime, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        match_data = response.json()
        url_first_match = "https://{}.api.riotgames.com/lol/match/v5/matches/{}/timeline?api_key={}".format(region_api[2], match_data[0], api_key)
        response = requests.get(url_first_match)
        if response.status_code == 200:
            match_info = response.json()
            did_win = match_info["metadata"]["participants"][0]["win"]
            if did_win:
                did_win = "Victoire"
            else:
                did_win = "Défaite"
            kills = match_info["info"]["participants"][0]["kills"]
            deaths = match_info["info"]["participants"][0]["deaths"]
            assists = match_info["info"]["participants"][0]["assists"]
            champ_level = match_info["info"]["participants"][0]["champLevel"]
            gold_earned = match_info["info"]["participants"][0]["goldEarned"]
            total_damage_dealt_to_champions = match_info["info"]["participants"][0]["totalDamageDealtToChampions"]
            champions = match_info["info"]["participants"][0]["championName"]
            id_champions = match_info["info"]["participants"][0]["championId"]
            kda = (kills + assists) / deaths
            return did_win, kills, deaths, assists, champ_level, gold_earned, total_damage_dealt_to_champions, champions, id_champions, kda
        else:
            return None
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


def get_icon_player():
    url = "https://cdn.communitydragon.org/11.20.1/profile-icon/29"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
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

# print(get_info_match_by_puuid(get_puuid("Cig", "ImYou")))