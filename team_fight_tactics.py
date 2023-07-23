"""
This module contains classes that collect TFT data, and handlers.

Author: Chung seop, Shin
Date Created: 2023/07/17
"""
from tft_models import *
from utility import pad_list
from pprint import pprint
from typing import Iterable, Optional
from bs4 import BeautifulSoup
import logging
import requests
import random
import time

REGIONS_INFO = {
    "BR": ["AMERICAS", "BR1"],
    "EUNE": ["EUROPE", "EUN1"],
    "EUW": ["EUROPE", "EUW1"],
    "JP": ["ASIA", "JP1"],
    "KR": ["ASIA", "KR"],
    "LAN": ["AMERICAS", "LA1"],
    "LAS": ["AMERICAS", "LA2"],
    "NA": ["AMERICAS", "NA1"],
    "OCE": ["SEA", "OC1"],
    "PH": ["SEA", "PH2"],
    "RU": ["EUROPE", "RU"],
    "SG": ["SEA", "SG2"],
    "TH": ["SEA", "TH2"],
    "TR": ["EUROPE", "TR1"],
    "TW": ["SEA", "TW2"],
    "VN": ["SEA", "VN2"],
}


class TftScraper(object):
    def __init__(self) -> None:
        self._logger = logging.getLogger("team_fight_tactics.TftScraper")
        self._lolchessgg_url = "https://lolchess.gg/leaderboards"
        self._header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Whale/3.21.192.18 Safari/537.36"
        }
        self._ssesion = requests.Session()
        self._ssesion.headers.update(self._header)

    @property
    def logger(self):
        return self._logger

    def get_top_players_without_puuid(self, start, end, *regions):
        """Get player info from "lolchess.gg" site. However, no puuid information is provided.

        Args:
            start: The starting rank of the range of players to get. The minimum value is 1.
            end: The last rank of the range of players to get. The maximum value is 100.
            regions: A variable parameter of the player region to get.
            example> BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, TR, RU, PH, SG, TH, TW, VN
        """
        players = []
        params = {"mode": "ranked"}
        selector_table_rows = (
            "#wrapper > div.leaderboards.container > table > tbody > tr > td.summoner"
        )
        for region in regions:
            region = region.upper()
            params["region"] = region
            response = self._ssesion.get(self._lolchessgg_url, params=params)
            self._logger.debug(f"get_top_players_without_puuid: {response.status_code}")

            bs = BeautifulSoup(response.content, "html.parser")
            table_rows = bs.select(selector_table_rows)
            table_rows = table_rows[start - 1 : end]

            for table_row in table_rows:
                player_name = table_row.select_one("a").get_text().strip()
                player_rank = (
                    table_row.select_one("span.rank")
                    .get_text()
                    .strip()
                    .replace("#", "")
                )
                player = Player("", player_name, *REGIONS_INFO[region], player_rank)
                players.append(player)

            time.sleep(random.randint(1, 3))

        return players

    def __repr__(self) -> str:
        return super.__repr__()

    def __str__(self) -> str:
        return self.__repr__()


class RiotApiAdaptor(object):
    def __init__(self, api_key) -> None:
        self._logger = logging.getLogger("team_fight_tactics.RiotApiAdaptor")

        self._api_key = api_key
        self._url_get_player_by_name = "https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{name}"
        self._url_get_match_ids_by_puuid = "https://{continent}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids"
        self._url_get_matches_by_match_id = (
            "https://{continent}.api.riotgames.com/tft/match/v1/matches/{match_id}"
        )
        self._headers = {"X-Riot-Token": self._api_key}

    @property
    def logger(self):
        return self._logger

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def get_player_by_player_name(self, region, name) -> requests.models.Response:
        """Get player info by name.

        Args:
            region: This is the region information of the server the player belongs to.
            example> BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU, PH2, SG2, TH2, TW2, VN2
            name: This is the player's name.
        """
        url = self._url_get_player_by_name.format(region=region, name=name)
        try:
            response = requests.get(url, headers=self._headers)
            self._logger.debug(f"get_player_by_player_name: {response.status_code}")
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return None

        time.sleep(2)
        return response

    def get_match_ids_by_puuid(
        self, continent, puuid, start=0, count=20, *, start_time="", end_time=""
    ) -> requests.models.Response:
        """Get a list of match ids by PUUID

        Args:
            continent: This is the continent information of the server the player belongs to.
            example> AMERICAS, ASIA, EUROPE, SEA
            puuid: Encrypted PUUID. Exact length of 78 characters.
            start_time: Epoch timestamp in seconds. The matchlist started storing timestamps on June 16th, 2021. Any matches played before June 16th, 2021 won't be included in the results if the startTime filter is set. start_time is optional.
            end_time: Epoch timestamp in seconds. end_time is optional.
            start: Defaults to 0. Start index.
            end: Defaults to 20. Number of match ids to return.
        """
        url = self._url_get_match_ids_by_puuid.format(continent=continent, puuid=puuid)
        params = {
            "start": start,
            "count": count,
            "start_time": start_time,
            "end_time": end_time,
        }
        try:
            response = requests.get(url, params=params, headers=self._headers)
            self._logger.debug(f"get_match_ids_by_puuid: {response.status_code}")
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return None

        time.sleep(2)
        return response

    def get_matches_by_match_id(self, continent, match_id) -> requests.models.Response:
        """Get a match by match id

        Args:
            continent: This is the continent information of the server the player belongs to.
            example> AMERICAS, ASIA, EUROPE, SEA
            match_id: Match id.
        """
        url = self._url_get_matches_by_match_id.format(
            continent=continent, match_id=match_id
        )
        try:
            response = requests.get(url, headers=self._headers)
            self._logger.debug(f"get_matches_by_match_id: {response.status_code}")
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return None

        time.sleep(2)
        return response

    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return self.__repr__()


class TftDataHandler(object):
    def __init__(self, riot_api_adaptor: RiotApiAdaptor) -> None:
        self._logger = logging.getLogger(f"team_fight_tactics.TftDataBuilder")
        self._riot_api_adaptor = riot_api_adaptor

    @property
    def logger(self):
        return self._logger

    def get_players_with_puuid(self, players: Iterable[Player]) -> Iterable[Player]:
        try:
            new_players = []
            for player in players:
                response = self._riot_api_adaptor.get_player_by_player_name(
                    player.region, player.name
                )
                puuid = response.json()["puuid"]
                player.puuid = puuid
                new_players.append(player)

            return new_players
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return []

    def get_matches_from(self, match_json) -> Optional[Match]:
        try:
            metadata = match_json["metadata"]
            info = match_json["info"]

            instance_value = {
                "match_id": metadata["match_id"],
                "match_datetime": info["game_datetime"],
                "match_length": info["game_length"],
                "tft_set_number": info["tft_set_number"],
            }
            match = Match(**instance_value)

            return match
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return None

    def get_match_players_from(self, match_json) -> Iterable[MatchPlayer]:
        try:
            metadata = match_json["metadata"]
            info = match_json["info"]
            participants = info["participants"]

            match_id = metadata["match_id"]
            match_players = []
            for participant in participants:
                instance_value = {
                    "puuid": participant["puuid"],
                    "last_round": participant["last_round"],
                    "level": participant["level"],
                    "placement": participant["placement"],
                    "time_eliminated": participant["time_eliminated"],
                }
                match_player = MatchPlayer(match_id=match_id, **instance_value)
                match_players.append(match_player)

            return match_players

        except Exception as e:
            print(e)
            self._logger.exception(e)
            return []

    def get_match_augments_from(self, match_json) -> Iterable[MatchAugment]:
        try:
            metadata = match_json["metadata"]
            info = match_json["info"]
            participants = info["participants"]

            match_id = metadata["match_id"]
            match_augments = []
            for participant in participants:
                puuid = participant["puuid"]
                augments = participant["augments"]
                for i, augment in enumerate(augments):
                    instance_value = {
                        "match_id": match_id,
                        "puuid": puuid,
                        "name": augment,
                        "sequence": i,
                    }
                    match_augment = MatchAugment(**instance_value)
                    match_augments.append(match_augment)

            return match_augments

        except Exception as e:
            print(e)
            self._logger.exception(e)
            return []

    def get_match_traits_from(self, match_json) -> Iterable[MatchTrait]:
        try:
            metadata = match_json["metadata"]
            info = match_json["info"]
            participants = info["participants"]

            match_id = metadata["match_id"]
            match_traits = []
            for participant in participants:
                puuid = participant["puuid"]
                traits = participant["traits"]
                for i, trait in enumerate(traits):
                    instance_value = {
                        "match_id": match_id,
                        "puuid": puuid,
                        "name": trait["name"],
                        "num_units": trait["num_units"],
                        "style": trait["style"],
                        "tier_current": trait["tier_current"],
                        "tier_total": trait["tier_total"],
                        "sequence": i,
                    }
                    match_trait = MatchTrait(**instance_value)
                    match_traits.append(match_trait)

            return match_traits

        except Exception as e:
            print(e)
            self._logger.exception(e)
            return []

    def get_match_units_from(self, match_json) -> Iterable[MatchUnit]:
        try:
            metadata = match_json["metadata"]
            info = match_json["info"]
            participants = info["participants"]

            match_id = metadata["match_id"]
            match_units = []
            for participant in participants:
                puuid = participant["puuid"]
                units = participant["units"]
                for i, unit in enumerate(units):
                    items = unit["itemNames"]
                    item1, item2, item3 = pad_list(items, 3, "")
                    instance_value = {
                        "match_id": match_id,
                        "puuid": puuid,
                        "unit_id": unit["character_id"],
                        "rarity": unit["rarity"],
                        "tier": unit["tier"],
                        "sequence": i,
                        "item1": item1,
                        "item2": item2,
                        "item3": item3,
                    }
                    match_unit = MatchUnit(**instance_value)
                    match_units.append(match_unit)

            return match_units

        except Exception as e:
            print(e)
            self._logger.exception(e)
            return []

    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return self.__repr__()
