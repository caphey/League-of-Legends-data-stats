import requests
import time
from datetime import datetime, timedelta

# API key provenant de la plateforme Riot Games
api_key = "RGAPI-beeb6a08-d5f6-4bfb-9ce6-d3e3c1f1c1a6"

platform_api = ["BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2",
                "NA1", "OC1", "TR1", "RU", "PH2", "SG2", "TH2", "TW2", "VN2"]
region_api = ["americas", "asia", "europe", "sea"]

# Timestamp de la date de début de la recherche des matchs (18 juin 2021)
startTime = "1623974400"
# Timestamp de la date de fin de la recherche des matchs (date actuelle)
today_timestamp = round(time.time())
# Timestamp de la date d'il y a 10 jours
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
        list_cs_per_min = []
        for match_id in list_match:
            url_match = "https://{}.api.riotgames.com/lol/match/v5/matches/{}?api_key={}".format(
                region_api[2], match_id, api_key)
            response = requests.get(url_match)
            if response.status_code == 200:
                match_info = response.json()
                part_index = match_info["metadata"]["participants"].index(
                    puuid)

                did_win = match_info["info"]["participants"][part_index]["win"]
                if did_win:
                    did_win = "Victoire"
                else:
                    did_win = "Défaite"
                date_match = datetime.fromtimestamp(
                    match_info["info"]["gameCreation"] / 1000).strftime("%d/%m/%Y")
                type_match = match_info["info"]["gameMode"]
                kills = match_info["info"]["participants"][part_index]["kills"]
                deaths = match_info["info"]["participants"][part_index]["deaths"]
                assists = match_info["info"]["participants"][part_index]["assists"]
                champ_level = match_info["info"]["participants"][part_index]["champLevel"]
                gold_earned = match_info["info"]["participants"][part_index]["goldEarned"]
                total_damage_dealt_to_champions = match_info["info"][
                    "participants"][part_index]["totalDamageDealtToChampions"]
                champions_name = match_info["info"]["participants"][part_index]["championName"]
                url_icon = "https://ddragon.leagueoflegends.com/cdn/14.2.1/img/champion/{}.png".format(
                    champions_name)
                total_minions_killed = match_info["info"]["participants"][part_index]["totalMinionsKilled"]
                duree = match_info["info"]["gameDuration"]
                cs_per_min = round(total_minions_killed / (duree / 60), 2)
                list_cs_per_min.append(cs_per_min)
                if deaths == 0:
                    kda = (kills + assists)
                else:
                    kda = (kills + assists) / deaths

                match_info_list = [url_icon, did_win, kills, deaths, assists, champ_level,
                                   gold_earned, total_damage_dealt_to_champions, champions_name, round(kda, 2), date_match, type_match]
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
    url = "https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?startTime={}&endTime={}&count=20&api_key={}".format(
        region_api[2], puuid, ten_days_ago_timestamp, today_timestamp, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        list_match = response.json()
        win_loss = {"wins": 0, "losses": 0}
        for match_id in list_match:
            url_match = "https://{}.api.riotgames.com/lol/match/v5/matches/{}?api_key={}".format(
                region_api[2], match_id, api_key)
            response = requests.get(url_match)
            if response.status_code == 200:
                match_info = response.json()
                part_index = match_info["metadata"]["participants"].index(
                    puuid)
                if match_info["info"]["participants"][part_index]["win"]:
                    win_loss["wins"] += 1
                else:
                    win_loss["losses"] += 1
            else:
                return None
        return win_loss
    else:
        return None


def get_stats_last_three_match(puuid):
    # puuid : identifiant unique du joueur
    url = "https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?startTime={}&endTime={}&api_key={}".format(
        region_api[2], puuid, ten_days_ago_timestamp, today_timestamp, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        list_match = response.json()
        all_matches_info = []
        for match_id in list_match[:3]:
            url_match = "https://{}.api.riotgames.com/lol/match/v5/matches/{}?api_key={}".format(
                region_api[2], match_id, api_key)
            response = requests.get(url_match)
            if response.status_code == 200:
                match_info = response.json()
                part_index = match_info["metadata"]["participants"].index(
                    puuid)

                kills = match_info["info"]["participants"][part_index]["kills"]
                deaths = match_info["info"]["participants"][part_index]["deaths"]
                assists = match_info["info"]["participants"][part_index]["assists"]
                champ_level = match_info["info"]["participants"][part_index]["champLevel"]
                gold_earned = round(
                    match_info["info"]["participants"][part_index]["goldEarned"] / 1000, 2)
                total_damage_dealt_to_champions = round(match_info["info"][
                    "participants"][part_index]["totalDamageDealtToChampions"] / 1000, 2)
                champions_name = match_info["info"]["participants"][part_index]["championName"]
                if deaths == 0:
                    kda = (kills + assists)
                else:
                    kda = (kills + assists) / deaths

                match_info_dict = {
                    "champion_name": champions_name,
                    "kills": kills,
                    "deaths": deaths,
                    "assists": assists,
                    "champ_level": champ_level,
                    "gold_earned": gold_earned,
                    "total_damage_dealt_to_champions": total_damage_dealt_to_champions,
                    "kda": round(kda, 2)
                }
                all_matches_info.append(match_info_dict)
            else:
                return None
        return all_matches_info
    else:
        return None


def get_cs_per_min(puuid):
    # puuid : identifiant unique du joueur
    url = "https://{}.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?startTime={}&endTime={}&api_key={}".format(
        region_api[2], puuid, ten_days_ago_timestamp, today_timestamp, api_key)
    response = requests.get(url)
    if response.status_code == 200:
        list_match = response.json()
        list_cs_per_min = []
        for match_id in list_match[:21]:
            url_match = "https://{}.api.riotgames.com/lol/match/v5/matches/{}?api_key={}".format(
                region_api[2], match_id, api_key)
            response = requests.get(url_match)
            if response.status_code == 200:
                match_info = response.json()
                part_index = match_info["metadata"]["participants"].index(
                    puuid)

                total_minions_killed = match_info["info"]["participants"][part_index]["totalMinionsKilled"]
                duree = match_info["info"]["gameDuration"]
                cs_per_min = round(total_minions_killed / (duree / 60), 2)
                list_cs_per_min.append(cs_per_min)
            else:
                return None
        mean_cs_per_min = round(
            sum(list_cs_per_min) / len(list_cs_per_min), 2)
        dict_cs_per_min = {"cs_per_min": list_cs_per_min,
                           "mean_cs": mean_cs_per_min}

        return dict_cs_per_min
    else:
        return None
