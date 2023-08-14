from datetime import date
import json
import os
from os.path import join
import time
from team_fight_tactics import RiotApiAdaptor, TftDataHandler, REGIONS_INFO
import csv_utilities
import logging
from tft_models import Player
from utility import create_directories

if __name__ == "__main__":
    riot_api_adaptor = RiotApiAdaptor("")
    tft_data_handler = TftDataHandler(riot_api_adaptor)

    LOGGING_FORMAT = "%(asctime)s %(levelname)-8s %(name)-15s %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)

    # Define debug filter
    debug_filter = lambda record: record.levelno == logging.DEBUG

    # Create a file handler
    debug_file_handler = logging.FileHandler("./logs/debug_logfile.log")
    debug_file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    debug_file_handler.addFilter(debug_filter)

    warn_file_handler = logging.FileHandler("./logs/warn_logfile.log")
    warn_file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    warn_file_handler.setLevel(logging.WARN)

    loggers = [riot_api_adaptor.logger, tft_data_handler.logger]

    for logger in loggers:
        logger.addHandler(debug_file_handler)
        logger.addHandler(warn_file_handler)

    # load existing player list
    players_json_path = "./product/results/tft_players.json"
    existing_players = set()
    if os.path.exists(players_json_path):
        with open(players_json_path, "r") as file:
            data = json.load(file)
        for item in data:
            player = Player(**item)
            existing_players.add(player)

    regions = REGIONS_INFO.keys()

    # slected_region = list(regions)[]
    slected_region = ["TH2"]

    # Format string arguments for the path.
    relative_path = "./product"
    match_tables = {
        "matches": [],
        "match_players": [],
        "match_augments": [],
        "match_traits": [],
        "match_units": [],
    }
    player_table = {"players": set(), "player_statistics": []}
    total_table_names = [*match_tables] + [*player_table]

    # Create product directories
    directory_paths = [join(relative_path, dir) for dir in total_table_names]
    create_directories(directory_paths)

    for region in slected_region:
        start_ranking = 1
        end_ranking = 10

        challenger_league_json = riot_api_adaptor.get_challenger_league(region).json()

        (
            player_table["players"],
            player_table["player_statistics"],
        ) = tft_data_handler.get_player_classes_from(
            challenger_league_json,
            region,
            start_ranking,
            end_ranking,
        )
        player_table["players"] = set(player_table["players"])

        matches_json = []
        match_ids = set()
        continent = next(iter(player_table["players"])).continent

        start_index = 0
        match_count = 20

        for player in player_table["players"]:
            response = riot_api_adaptor.get_match_ids_by_puuid(
                player.continent, player.puuid, start_index, match_count
            )
            match_ids.update(response.json())
        # clear players
        player_table["players"].clear()

        for match_id in match_ids:
            response = riot_api_adaptor.get_matches_by_match_id(continent, match_id)
            matches_json.append(response.json())

        for match_json in matches_json:
            players = tft_data_handler.get_players_from(match_json)
            player_table["players"].update(
                [player for player in players if player not in existing_players]
            )
            match_tables["matches"].append(
                tft_data_handler.get_matches_from(match_json)
            )
            match_tables["match_players"].extend(
                tft_data_handler.get_match_players_from(match_json)
            )
            match_tables["match_augments"].extend(
                tft_data_handler.get_match_augments_from(match_json)
            )
            match_tables["match_traits"].extend(
                tft_data_handler.get_match_traits_from(match_json)
            )
            match_tables["match_units"].extend(
                tft_data_handler.get_match_units_from(match_json)
            )

        # add name information
        for player in player_table["players"]:
            if player.name != "":
                continue
            player_json = riot_api_adaptor.get_player_by_player_puuid(
                region, player.puuid
            ).json()
            player_name = player_json["name"]
            player.name = player_name

        # store player data
        for table_name, table in player_table.items():
            if table_name == "players":
                path = f"{relative_path}/results/tft_{table_name}.csv"
                mode = "w"
                is_header = True
                if os.path.exists(path):
                    mode = "a"
                    is_header = False
                csv_utilities.save_class_list_to_csv(
                    path, table, with_header=is_header, header_strip_str="_", mode=mode
                )
            csv_utilities.save_class_list_to_csv(
                f"{relative_path}/{table_name}/tft_{table_name}_{region}.csv",
                table,
                with_header=True,
                header_strip_str="_",
            )

        # stroe Match, MatchPlayer, MatchAugment, MatchTrait, MatchUnit data
        for table_name, table in match_tables.items():
            csv_utilities.save_class_list_to_csv(
                f"{relative_path}/{table_name}/tft_{table_name}_{region}.csv",
                table,
                with_header=True,
                header_strip_str="_",
            )

        # list initialization
        match_tables = {key: [] for key in match_tables}
        player_table = {"players": set(), "player_statistics": []}

    directory_file_dict = {
        f"{relative_path}/{table_name}": f"tft_{table_name}_{str(date.today().strftime('%Y%m%d'))}.csv"
        for table_name in total_table_names
    }

    # merge csv files
    for directory, file_name in directory_file_dict.items():
        lines = csv_utilities.merge_csv_files_in_directory(directory, with_header=True)
        csv_utilities.save_csv_file(join(relative_path, "results", file_name), lines)

    # csv to json
    directory_path = "./product/results"
    csv_file_list = [
        join(directory_path, file)
        for file in os.listdir(directory_path)
        if file.endswith(".csv")
    ]
    json_file_list = [file.replace("csv", "json") for file in csv_file_list]
    file_path_list = zip(csv_file_list, json_file_list)
    for csv_file, json_file in file_path_list:
        csv_utilities.csv_to_json(csv_file, json_file)
    print()
