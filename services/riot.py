import requests
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import contextlib
from config import Config

# Constants
BASE_URL = "https://{}.api.riotgames.com"
API_VERSION = "14.2.1"
PLATFORM_API = ["BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2",
                "NA1", "OC1", "TR1", "RU", "PH2", "SG2", "TH2", "TW2", "VN2"]
REGION_API = ["americas", "asia", "europe", "sea"]
GAME_RESULT = {True: "Victoire", False: "Défaite"}

# Configuration
api_key = Config.RIOT_API_KEY
region = REGION_API[2]  # Europe
platform = PLATFORM_API[2]  # EUW1

# Time constants
START_TIME = "1623974400"  # 18 juin 2021
TODAY = datetime.now()
TEN_DAYS_AGO = TODAY - timedelta(days=10)
TODAY_TIMESTAMP = int(TODAY.timestamp())
TEN_DAYS_AGO_TIMESTAMP = int(TEN_DAYS_AGO.timestamp())


@dataclass
class MatchInfo:
    url_icon: str
    result: str
    kills: int
    deaths: int
    assists: int
    champ_level: int
    gold_earned: int
    total_damage: int
    champion_name: str
    kda: float
    date: str
    type: str


@contextlib.contextmanager
def api_session():
    session = requests.Session()
    try:
        yield session
    finally:
        session.close()


def make_api_request(url: str, params: Optional[Dict] = None) -> Dict:
    """Make an API request and return the JSON response."""
    params = params or {}
    params['api_key'] = api_key
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_puuid(game_name: str, tag_line: str) -> Optional[str]:
    """Get the PUUID for a given game name and tag line."""
    url = f"{BASE_URL.format(
        region)}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    try:
        player_info = make_api_request(url)
        return player_info["puuid"]
    except requests.exceptions.RequestException:
        return None


def get_match_details(match_id: str, puuid: str) -> Tuple[Dict, int]:
    """Get details for a specific match."""
    url = f"{BASE_URL.format(region)}/lol/match/v5/matches/{match_id}"
    match_info = make_api_request(url)
    part_index = match_info["metadata"]["participants"].index(puuid)
    return match_info, part_index


def calculate_kda(kills: int, deaths: int, assists: int) -> float:
    """Calculate KDA ratio."""
    return round((kills + assists) / max(deaths, 1), 2)


def get_info_match_by_puuid(puuid: str) -> List[MatchInfo]:
    """Get information for recent matches of a player."""
    url = f"{BASE_URL.format(
        region)}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "startTime": TEN_DAYS_AGO_TIMESTAMP,
        "endTime": TODAY_TIMESTAMP
    }
    list_match = make_api_request(url, params)

    all_matches_info = []
    with api_session() as session:
        for match_id in list_match:
            match_info, part_index = get_match_details(match_id, puuid)
            participant = match_info["info"]["participants"][part_index]

            match_data = MatchInfo(
                url_icon=f"https://ddragon.leagueoflegends.com/cdn/{
                    API_VERSION}/img/champion/{participant['championName']}.png",
                result=GAME_RESULT[participant["win"]],
                kills=participant["kills"],
                deaths=participant["deaths"],
                assists=participant["assists"],
                champ_level=participant["champLevel"],
                gold_earned=participant["goldEarned"],
                total_damage=participant["totalDamageDealtToChampions"],
                champion_name=participant["championName"],
                kda=calculate_kda(
                    participant["kills"], participant["deaths"], participant["assists"]),
                date=datetime.fromtimestamp(
                    match_info["info"]["gameCreation"] / 1000).strftime("%d/%m/%Y"),
                type=match_info["info"]["gameMode"]
            )
            all_matches_info.append(match_data)

    return all_matches_info


def top_3_champions(puuid: str) -> List[str]:
    """Get the top 3 champions for a player."""
    url = f"{BASE_URL.format(
        platform)}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top"
    champions_player = make_api_request(url)

    data_champions_url = f"https://ddragon.leagueoflegends.com/cdn/{
        API_VERSION}/data/en_US/champion.json"
    data_champions = make_api_request(data_champions_url)

    top_champions = []
    for champ in champions_player[:3]:
        for value in data_champions["data"].values():
            if champ["championId"] == int(value["key"]):
                top_champions.append(value["name"])
                break

    return top_champions


def get_level_player(puuid: str) -> Optional[int]:
    """Get the summoner level of a player."""
    url = f"{BASE_URL.format(
        platform)}/lol/summoner/v4/summoners/by-puuid/{puuid}"
    try:
        summoner_info = make_api_request(url)
        return summoner_info["summonerLevel"]
    except requests.exceptions.RequestException:
        return None


def get_icon_player(puuid: str) -> Optional[str]:
    """Get the icon of a player."""
    url = f"{BASE_URL.format(
        platform)}/lol/summoner/v4/summoners/by-puuid/{puuid}"
    try:
        summoner_info = make_api_request(url)
        summoner_icon_id = summoner_info["profileIconId"]

        url_data_icon = f"https://ddragon.leagueoflegends.com/cdn/{
            API_VERSION}/data/en_US/profileicon.json"
        data_icon = make_api_request(url_data_icon)

        for key, value in data_icon["data"].items():
            if summoner_icon_id == int(key):
                return value["image"]["full"]
        return None
    except requests.exceptions.RequestException:
        return None


def get_win_loss_percentage(puuid: str) -> Optional[Dict[str, int]]:
    """Get the win/loss percentage for a player's recent matches."""
    url = f"{BASE_URL.format(
        region)}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "startTime": TEN_DAYS_AGO_TIMESTAMP,
        "endTime": TODAY_TIMESTAMP,
        "count": 20
    }
    try:
        list_match = make_api_request(url, params)
        win_loss = {"wins": 0, "losses": 0}

        for match_id in list_match:
            match_info, part_index = get_match_details(match_id, puuid)
            if match_info["info"]["participants"][part_index]["win"]:
                win_loss["wins"] += 1
            else:
                win_loss["losses"] += 1

        return win_loss
    except requests.exceptions.RequestException:
        return None


def get_stats_last_three_match(puuid: str) -> List[Dict]:
    """Get stats for the last three matches of a player."""
    url = f"{BASE_URL.format(
        region)}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "startTime": TEN_DAYS_AGO_TIMESTAMP,
        "endTime": TODAY_TIMESTAMP,
        "count": 3
    }
    try:
        list_match = make_api_request(url, params)
        all_matches_info = []

        for match_id in list_match:
            match_info, part_index = get_match_details(match_id, puuid)
            participant = match_info["info"]["participants"][part_index]

            match_info_dict = {
                "champion_name": participant["championName"],
                "kills": participant["kills"],
                "deaths": participant["deaths"],
                "assists": participant["assists"],
                "champ_level": participant["champLevel"],
                "gold_earned": round(participant["goldEarned"] / 1000, 2),
                "total_damage_dealt_to_champions": round(participant["totalDamageDealtToChampions"] / 1000, 2),
                "kda": calculate_kda(participant["kills"], participant["deaths"], participant["assists"])
            }
            all_matches_info.append(match_info_dict)

        return all_matches_info
    except requests.exceptions.RequestException:
        return None


def get_cs_per_min(puuid: str) -> Optional[Dict]:
    """Get CS per minute stats for recent matches of a player."""
    url = f"{BASE_URL.format(
        region)}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "startTime": TEN_DAYS_AGO_TIMESTAMP,
        "endTime": TODAY_TIMESTAMP,
        "count": 20
    }
    try:
        list_match = make_api_request(url, params)
        list_cs_per_min = []

        for match_id in list_match:
            match_info, part_index = get_match_details(match_id, puuid)
            participant = match_info["info"]["participants"][part_index]

            total_minions_killed = participant["totalMinionsKilled"]
            duree = match_info["info"]["gameDuration"]
            cs_per_min = round(total_minions_killed / (duree / 60), 2)
            list_cs_per_min.append(cs_per_min)

        mean_cs_per_min = round(sum(list_cs_per_min) / len(list_cs_per_min), 2)
        return {
            "cs_per_min": list_cs_per_min,
            "mean_cs": mean_cs_per_min
        }
    except requests.exceptions.RequestException:
        return None


def get_user_data(game_name: str, tag_line: str) -> Dict:
    """Get all user data for a given player."""
    puuid = get_puuid(game_name, tag_line)
    if puuid is None:
        return {}

    return {
        'game_name': game_name,
        'tag_line': tag_line,
        'puuid': puuid,
        'top_champions': top_3_champions(puuid),
        'icon': get_icon_player(puuid),
        'level': get_level_player(puuid),
        'info_match': get_info_match_by_puuid(puuid),
        'win_loss_percentage': get_win_loss_percentage(puuid),
        'stats_three_match': get_stats_last_three_match(puuid),
        'cs_per_min': get_cs_per_min(puuid)
    }
