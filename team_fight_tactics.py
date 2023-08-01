"""
This module contains classes that collect TFT data, and handlers.

Author: Chung seop, Shin
Date Created: 2023/07/17
"""
from datetime import datetime
from tft_models import *
from utility import pad_list
from typing import Iterable, Optional, Tuple
import logging
import requests
import time

REGIONS_INFO = {
    "BR1": "AMERICAS",
    "EUN1": "EUROPE",
    "EUW1": "EUROPE",
    "JP1": "ASIA",
    "KR": "ASIA",
    "LA1": "AMERICAS",
    "LA2": "AMERICAS",
    "NA1": "AMERICAS",
    "OC1": "SEA",
    "PH2": "SEA",
    "RU": "EUROPE",
    "SG2": "SEA",
    "TH2": "SEA",
    "TR1": "EUROPE",
    "TW2": "SEA",
    "VN2": "SEA",
}


class RiotApiAdaptor(object):
    def __init__(self, api_key) -> None:
        self._logger = logging.getLogger("team_fight_tactics.RiotApiAdaptor")

        self._api_key = api_key
        self._url_get_challenger_leauge = (
            "https://{region}.api.riotgames.com/tft/league/v1/challenger"
        )
        self._url_get_player_by_puuid = "https://{region}.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}"
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

    def get_challenger_league(self, region) -> requests.models.Response:
        """Get the challenger league.

        Args:
            region: This is the region information of the server the player belongs to.
            example> BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU, PH2, SG2, TH2, TW2, VN2
        """
        url = self._url_get_challenger_leauge.format(region=region)
        try:
            response = requests.get(url, headers=self._headers)
            self._logger.debug(f"get_challenger_league: {response.status_code}")
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return None

        time.sleep(2)
        return response

    def get_player_by_player_puuid(self, region, puuid) -> requests.models.Response:
        """Get player info by puuid.

        Args:
            region: This is the region information of the server the player belongs to.
            example> BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU, PH2, SG2, TH2, TW2, VN2
            name: This is the player's name.
        """
        url = self._url_get_player_by_puuid.format(region=region, puuid=puuid)
        try:
            response = requests.get(url, headers=self._headers)
            self._logger.debug(f"get_player_by_player_puuid: {response.status_code}")
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return None

        time.sleep(2)
        return response

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
        self._logger = logging.getLogger(f"team_fight_tactics.TftDataHandler")
        self._riot_api_adaptor = riot_api_adaptor

    @property
    def logger(self):
        return self._logger

    def get_players_with_puuid(self, players: Iterable[Player]) -> Iterable[Player]:
        """Get a list of players with puuid.

        Returns:
            Iterable[Player]: If puuid cannot be found by name, a list excluding the player is returned.
        """
        new_players = []
        for player in players:
            try:
                response = self._riot_api_adaptor.get_player_by_player_name(
                    player.region, player.name
                )
                puuid = response.json()["puuid"]
                player.puuid = puuid
                new_players.append(player)

            except KeyError as e:
                print(e)
                self._logger.exception(e)
            except Exception as e:
                print(e)
                self._logger.exception(e)

        return new_players

    def get_player_classes_from(
        self, league_json, region, start=1, end=10
    ) -> Tuple[Iterable[Player], Iterable[PlayerStatistic]]:
        """Get players and player statistics via league info in json format.
        Args:
            league_json: This is the league_json containing information about the league participants.
            region: This is the region information of the server the player belongs to.
            example> BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, TR1, RU, PH2, SG2, TH2, TW2, VN2
            start:The first rank in the league for the player you want to return.
            end:The last rank in the league for the player you want to return.
        """
        try:
            entries = league_json["entries"]

            entries = sorted(entries, key=lambda x: x["leaguePoints"], reverse=True)
            entries = entries[start - 1 : end]
            players = []
            player_statistics = []
            update_date = int(time.time())
            update_date = str(datetime.fromtimestamp(update_date))

            for ranking, entry in enumerate(entries):
                name = entry["summonerName"]
                response = self._riot_api_adaptor.get_player_by_player_name(
                    region, name
                )
                puuid = response.json()["puuid"]

                instance_value = {
                    "puuid": puuid,
                    "name": name,
                    "continent": REGIONS_INFO[region],
                    "region": region,
                }
                player = Player(**instance_value)
                players.append(player)

                instance_value = {
                    "puuid": puuid,
                    "ranking": ranking + 1,
                    "league_point": entry["leaguePoints"],
                    "wins": entry["wins"],
                    "losses": entry["losses"],
                    "update_date": str(update_date),
                }
                player_statistic = PlayerStatistic(**instance_value)
                player_statistics.append(player_statistic)

            return players, player_statistics
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return None

    def get_players_from(self, match_json) -> Iterable[Player]:
        try:
            metadata = match_json["metadata"]
            match_id = metadata["match_id"]
            region = match_id.split("_")[0]
            participants = metadata["participants"]

            players = []
            for puuid in participants:
                player = Player(puuid, "", REGIONS_INFO[region], region)
                players.append(player)

            return players
        except Exception as e:
            print(e)
            self._logger.exception(e)
            return None

    def get_matches_from(self, match_json) -> Optional[Match]:
        try:
            metadata = match_json["metadata"]
            info = match_json["info"]
            match_timestamp = info["game_datetime"]
            match_date = str(datetime.fromtimestamp(match_timestamp // 1000))

            instance_value = {
                "match_id": metadata["match_id"],
                "match_date": str(match_date),
                "match_length": info["game_length"],
                "match_version": info["game_version"],
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
                placement = participant["placement"]
                match_player_id = f"{match_id}_{placement}"

                instance_value = {
                    "match_player_id": match_player_id,
                    "match_id": match_id,
                    "puuid": participant["puuid"],
                    "last_round": participant["last_round"],
                    "level": participant["level"],
                    "placement": placement,
                    "time_eliminated": participant["time_eliminated"],
                }
                match_player = MatchPlayer(**instance_value)
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
                placement = participant["placement"]
                augments = participant["augments"]
                match_player_id = f"{match_id}_{placement}"

                for i, augment in enumerate(augments):
                    instance_value = {
                        "match_player_id": match_player_id,
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
                placement = participant["placement"]
                traits = participant["traits"]
                match_player_id = f"{match_id}_{placement}"

                for i, trait in enumerate(traits):
                    instance_value = {
                        "match_player_id": match_player_id,
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
                placement = participant["placement"]
                units = participant["units"]
                match_player_id = f"{match_id}_{placement}"

                for i, unit in enumerate(units):
                    items = unit["itemNames"]
                    item1, item2, item3 = pad_list(items, 3, "")
                    instance_value = {
                        "match_player_id": match_player_id,
                        "name": unit["character_id"],
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
