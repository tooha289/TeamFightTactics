"""
This module contains classes that TFT entities.

Author: Chung seop, Shin
Date Created: 2023/07/17
"""


class Player(object):
    def __init__(self, puuid, name, continent, region) -> None:
        self._puuid = puuid
        self._name = name
        self._continent = continent
        self._region = region

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

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __str__(self) -> str:
        return self.__repr__()

    def __hash__(self):
        return hash(self._puuid)

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self._puuid == other._puuid and self._name == other._name 


class PlayerStatistic(object):
    def __init__(self, puuid, ranking, league_point, wins, losses, update_date) -> None:
        self._puuid = puuid
        self._ranking = ranking
        self._league_point = league_point
        self._wins = wins
        self._losses = losses
        self._update_date = update_date

    @property
    def puuid(self):
        return self._puuid

    @puuid.setter
    def puuid(self, value):
        self._puuid = value

    @property
    def ranking(self):
        return self._ranking

    @ranking.setter
    def ranking(self, value):
        self._ranking = value

    @property
    def league_point(self):
        return self._league_point

    @league_point.setter
    def league_point(self, value):
        self._league_point = value

    @property
    def wins(self):
        return self._wins

    @wins.setter
    def wins(self, value):
        self._wins = value

    @property
    def losses(self):
        return self._losses

    @losses.setter
    def losses(self, value):
        self._losses = value

    @property
    def update_date(self):
        return self._update_date

    @update_date.setter
    def update_date(self, value):
        self._update_date = value

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __str__(self) -> str:
        return self.__repr__()


class Match(object):
    def __init__(
        self,
        match_id,
        match_date,
        match_length,
        version_major,
        version_minor,
        version_patch,
        version_date,
        tft_set_number,
    ) -> None:
        self._match_id = match_id
        self._match_date = match_date
        self._match_length = match_length
        self._version_major = version_major
        self._version_minor = version_minor
        self._version_patch = version_patch
        self._version_date = version_date
        self._tft_set_number = tft_set_number

    @property
    def match_id(self):
        return self._match_id

    @match_id.setter
    def match_id(self, value):
        self._match_id = value

    @property
    def match_date(self):
        return self._match_date

    @match_date.setter
    def match_date(self, value):
        self._match_date = value

    @property
    def match_length(self):
        return self._match_length

    @match_length.setter
    def match_length(self, value):
        self._match_length = value

    @property
    def version_major(self):
        return self._version_major

    @version_major.setter
    def version_major(self, value):
        self._version_major = value

    @property
    def version_minor(self):
        return self._version_minor

    @version_minor.setter
    def version_minor(self, value):
        self._version_minor = value

    @property
    def version_patch(self):
        return self._version_patch

    @version_patch.setter
    def version_patch(self, value):
        self._version_patch = value

    @property
    def version_date(self):
        return self._version_date

    @version_date.setter
    def version_date(self, value):
        self._version_date = value

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


class Version(object):
    def __init__(self, version_id, major, minor, patch, build, release, update_date):
        self._version_id = version_id
        self._major = major
        self._minor = minor
        self._patch = patch
        self._build = build
        self._release = release
        self._update_date = update_date

    @property
    def version_id(self):
        return self._version_id

    @version_id.setter
    def version_id(self, value):
        self._version_id = value

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, value):
        self._major = value

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, value):
        self._minor = value

    @property
    def patch(self):
        return self._patch

    @patch.setter
    def patch(self, value):
        self._patch = value

    @property
    def build(self):
        return self._build

    @build.setter
    def build(self, value):
        self._build = value

    @property
    def release(self):
        return self._release

    @release.setter
    def release(self, value):
        self._release = value

    @property
    def update_date(self):
        return self._update_date

    @update_date.setter
    def update_date(self, value):
        self._update_date = value

    def __repr__(self) -> str:
        return f"{vars(self)}"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Version):
            return False
        return self._version_id == other._version_id


class MatchPlayer(object):
    def __init__(
        self,
        match_player_id,
        match_id,
        puuid,
        last_round,
        level,
        placement,
        time_eliminated,
    ) -> None:
        self._match_player_id = match_player_id
        self._match_id = match_id
        self._puuid = puuid
        self._last_round = last_round
        self._level = level
        self._placement = placement
        self._time_eliminated = time_eliminated

    @property
    def match_player_id(self):
        return self._match_player_id

    @match_player_id.setter
    def match_player_id(self, value):
        self._match_player_id = value

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
    def __init__(self, match_player_id, sequence, name) -> None:
        self._match_player_id = match_player_id
        self._sequence = sequence
        self._name = name

    @property
    def match_player_id(self):
        return self._match_player_id

    @match_player_id.setter
    def match_player_id(self, value):
        self._match_player_id = value

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
        match_player_id,
        sequence,
        name,
        num_units,
        style,
        tier_current,
        tier_total,
    ) -> None:
        self._match_player_id = match_player_id
        self._sequence = sequence
        self._name = name
        self._num_units = num_units
        self._style = style
        self._tier_current = tier_current
        self._tier_total = tier_total

    @property
    def match_player_id(self):
        return self._match_player_id

    @match_player_id.setter
    def match_player_id(self, value):
        self._match_player_id = value

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
        self,
        match_player_id,
        sequence,
        name,
        rarity,
        tier,
        item1,
        item2,
        item3,
    ) -> None:
        self._match_player_id = match_player_id
        self._sequence = sequence
        self._name = name
        self._rarity = rarity
        self._tier = tier
        self._item1 = item1
        self._item2 = item2
        self._item3 = item3

    @property
    def match_player_id(self):
        return self._match_player_id

    @match_player_id.setter
    def match_player_id(self, value):
        self._match_player_id = value

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
