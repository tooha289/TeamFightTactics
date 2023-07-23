"""
This module contains classes that collect TFT data, TFT-related entities, and handlers.

Author: Chung seop, Shin
Date Created: 2023/07/17
"""
from pprint import pprint
from typing import Iterable, Optional
from bs4 import BeautifulSoup
import logging
import requests
import random
import time
from utility import pad_list

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


class Player(object):
    def __init__(self, puuid, name, continent, region, ranking) -> None:
        self._puuid = puuid
        self._name = name
        self._continent = continent
        self._region = region
        self._ranking = ranking

    @property
    def puuid(self):
        return self._puuid

    @puuid.setter
    def puuid(self, value):
        self._puuid = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def continent(self):
        return self._continent

    @continent.setter
    def continent(self, value):
        self._continent = value

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        self._region = value

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        self._ranking = value

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __str__(self) -> str:
        return self.__repr__()


class Match(object):
    def __init__(self, match_id, match_datetime, match_length, tft_set_number) -> None:
        self._match_id = match_id
        self._match_datetime = match_datetime
        self._match_length = match_length
        self._tft_set_number = tft_set_number

    @property
    def match_id(self):
        return self._match_id

    @match_id.setter
    def match_id(self, value):
        self._match_id = value

    @property
    def match_datetime(self):
        return self._match_datetime

    @match_datetime.setter
    def match_datetime(self, value):
        self._match_datetime = value

    @property
    def match_length(self):
        return self._match_length

    @match_length.setter
    def match_length(self, value):
        self._match_length = value

    @property
    def tft_set_number(self):
        return self._tft_set_number

    @tft_set_number.setter
    def tft_set_number(self, value):
        self._tft_set_number = value

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __str__(self) -> str:
        return self.__repr__()


class MatchPlayer(object):
    def __init__(
        self, match_id, puuid, last_round, level, placement, time_eliminated
    ) -> None:
        self._match_id = match_id
        self._puuid = puuid
        self._last_round = last_round
        self._level = level
        self._placement = placement
        self._time_eliminated = time_eliminated

    @property
    def match_id(self):
        return self._match_id

    @match_id.setter
    def match_id(self, value):
        self._match_id = value

    @property
    def puuid(self):
        return self._puuid

    @puuid.setter
    def puuid(self, value):
        self._puuid = value

    @property
    def last_round(self):
        return self._last_round

    @last_round.setter
    def last_round(self, value):
        self._last_round = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def time_eliminated(self):
        return self._time_eliminated

    @time_eliminated.setter
    def time_eliminated(self, value):
        self._time_eliminated = value

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, value):
        self._placement = value

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __str__(self) -> str:
        return self.__repr__()


class MatchAugment(object):
    def __init__(self, match_id, puuid, name, sequence) -> None:
        self._match_id = match_id
        self._puuid = puuid
        self._name = name
        self._sequence = sequence

    @property
    def match_id(self):
        return self._match_id

    @match_id.setter
    def match_id(self, value):
        self._match_id = value

    @property
    def puuid(self):
        return self._puuid

    @puuid.setter
    def puuid(self, value):
        self._puuid = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        self._sequence = value

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __str__(self) -> str:
        return self.__repr__()


class MatchTrait(object):
    def __init__(
        self,
        match_id,
        puuid,
        name,
        num_units,
        style,
        tier_current,
        tier_total,
        sequence,
    ) -> None:
        self._match_id = match_id
        self._puuid = puuid
        self._name = name
        self._num_units = num_units
        self._style = style
        self._tier_current = tier_current
        self._tier_total = tier_total
        self._sequence = sequence

    @property
    def match_id(self):
        return self._match_id

    @match_id.setter
    def match_id(self, value):
        self._match_id = value

    @property
    def puuid(self):
        return self._puuid

    @puuid.setter
    def puuid(self, value):
        self._puuid = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def num_units(self):
        return self._num_units

    @num_units.setter
    def num_units(self, value):
        self._num_units = value

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style = value

    @property
    def tier_current(self):
        return self._tier_current

    @tier_current.setter
    def tier_current(self, value):
        return self._tier_current

    @property
    def tier_total(self):
        return self._tier_total

    @tier_total.setter
    def tier_total(self, value):
        self._tier_total = value

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        self._sequence = value

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __str__(self) -> str:
        return self.__repr__()


class MatchUnit(object):
    def __init__(
        self, match_id, puuid, unit_id, rarity, tier, sequence, item1, item2, item3
    ) -> None:
        self._match_id = match_id
        self._puuid = puuid
        self._unit_id = unit_id
        self._rarity = rarity
        self._tier = tier
        self._sequence = sequence
        self._item1 = item1
        self._item2 = item2
        self._item3 = item3

    @property
    def match_id(self):
        return self._match_id

    @match_id.setter
    def match_id(self, value):
        self._match_id = value

    @property
    def puuid(self):
        return self._puuid

    @puuid.setter
    def puuid(self, value):
        self._puuid = value

    @property
    def unit_id(self):
        return self._unit_id

    @unit_id.setter
    def unit_id(self, value):
        self._unit_id = value

    @property
    def rarity(self):
        return self._rarity

    @rarity.setter
    def rarity(self, value):
        self._rarity = value

    @property
    def tier(self):
        return self._tier

    @tier.setter
    def tier(self, value):
        self._tier = value

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        self._sequence = value

    @property
    def item1(self):
        return self._item1

    @item1.setter
    def item1(self, value):
        self._item1 = value

    @property
    def item2(self):
        return self._item2

    @item2.setter
    def item2(self, value):
        self._item2 = value

    @property
    def item3(self):
        return self._item3

    @item3.setter
    def item3(self, value):
        self._item3 = value

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __str__(self) -> str:
        return self.__repr__()


class TftScraper(object):
    def __init__(self) -> None:
        self._logger = logging.getLogger("team_fight_tactics.TftScraper")
        self._lolchessgg_url = "https://lolchess.gg/leaderboards"
        self._header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Whale/3.21.192.18 Safari/537.36"
        }
        self._ssesion = requests.Session()
        self._ssesion.headers.update(self._header)

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

    def get_players_with_puuid(self, players: Iterable[Player]) -> Iterable[Player]:
        new_players = []
        for player in players:
            response = self._riot_api_adaptor.get_player_by_player_name(
                player.region, player.name
            )
            puuid = response.json()["puuid"]
            player.puuid = puuid
            new_players.append(player)

        return new_players

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
            return []

    def __repr__(self) -> str:
        return ""

    def __str__(self) -> str:
        return self.__repr__()
