from os.path import join
import time
from team_fight_tactics import RiotApiAdaptor, TftDataHandler, REGIONS_INFO
import csv_utilities
import logging
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

    regions = REGIONS_INFO.keys()

    slected_region = regions

    # Format string arguments for the path.
    relative_path = "./product"
    match_tables = {
        "matches": [],
        "match_players": [],
        "match_augments": [],
        "match_traits": [],
        "match_units": [],
    }
    player_table = {"players": [], "player_statistics": []}
    total_table_names = [*match_tables] + [*player_table]

    # Create product directories
    directory_paths = [join(relative_path, dir) for dir in total_table_names]
    create_directories(directory_paths)

    for region in slected_region:
        start_ranking = 1
        end_ranking = 10

        (
            player_table["players"],
            player_table["player_statistics"],
        ) = tft_data_handler.get_player_classes_from(
            riot_api_adaptor.get_challenger_league(region).json(),
            region,
            start_ranking,
            end_ranking,
        )
        # store player data
        for table_name, table in player_table.items():
            csv_utilities.save_class_list_to_csv(
                f"{relative_path}/{table_name}/tft_{table_name}_{region}.csv",
                table,
                with_header=True,
                header_strip_str="_",
            )

        matches_json = []
        match_ids = set()
        continent = player_table["players"][0].continent
        start_index = 0
        match_count = 20

        for player in player_table["players"]:
            response = riot_api_adaptor.get_match_ids_by_puuid(
                player.continent, player.puuid, start_index, match_count
            )
            match_ids.update(response.json())

        for match_id in match_ids:
            response = riot_api_adaptor.get_matches_by_match_id(continent, match_id)
            matches_json.append(response.json())

        for match_json in matches_json:
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

        # stroe Match, MatchPlayer, MatchAugment, MatchTrait, MatchUnit data
        for table_name, table in match_tables.items():
            csv_utilities.save_class_list_to_csv(
                f"{relative_path}/{table_name}/tft_{table_name}_{region}.csv",
                table,
                with_header=True,
                header_strip_str="_",
            )

    directory_file_dict = {
        f"{relative_path}/{table_name}": f"tft_{table_name}_{int(time.time())}.csv"
        for table_name in total_table_names
    }

    # merge csv files
    for directory, file_name in directory_file_dict.items():
        lines = csv_utilities.merge_csv_files_in_directory(directory, with_header=True)
        csv_utilities.save_csv_file(join(relative_path, "results", file_name), lines)
