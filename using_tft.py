from os.path import join
from team_fight_tactics import TftScraper, RiotApiAdaptor, TftDataHandler
import csv_utilities
import logging

if __name__ == "__main__":
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

    root_logger = logging.getLogger()
    root_logger.addHandler(debug_file_handler)

    scraper = TftScraper()
    riot_api_adaptor = RiotApiAdaptor("")
    tft_data_handler = TftDataHandler(riot_api_adaptor)

    loggers = [scraper.logger, riot_api_adaptor.logger, tft_data_handler.logger]
    for logger in loggers:
        logger.addHandler(warn_file_handler)
        logger.setLevel(logging.WARN)

    regions = [
        "BR",
        "EUNE",
        "EUW",
        "JP",
        "KR",
        "LAN",
        "LAS",
        "NA",
        "OCE",
        "PH",
        "RU",
        "SG",
        "TH",
        "TR",
        "TW",
        "VN",
    ]

    slected_region = ["KR"]

    # Format string arguments for the path.
    relative_path = "./product"
    match_table_names = [
        "matches",
        "match_players",
        "match_augments",
        "match_traits",
        "match_units",
    ]
    table_name = "players"

    for region in slected_region:
        start_ranking = 1
        end_ranking = 2

        players = tft_data_handler.get_players_with_puuid(
            scraper.get_top_players_without_puuid(start_ranking, end_ranking, region)
        )
        # store player data
        csv_utilities.save_class_list_to_csv(
            f"{relative_path}/{table_name}/tft_{table_name}_{region}.csv",
            players,
            with_header=True,
            header_strip_str="_",
        )

        matches_json = []
        match_ids = set()
        matches, match_players, match_augments, match_traits, match_units = (
            [],
            [],
            [],
            [],
            [],
        )
        continent = players[0].continent
        start_index = 0
        match_count = 2

        for player in players:
            response = riot_api_adaptor.get_match_ids_by_puuid(
                player.continent, player.puuid, start_index, match_count
            )
            match_ids.update(response.json())

        for match_id in match_ids:
            response = riot_api_adaptor.get_matches_by_match_id(continent, match_id)
            matches_json.append(response.json())

        for match_json in matches_json:
            matches.append(tft_data_handler.get_matches_from(match_json))
            match_players.extend(tft_data_handler.get_match_players_from(match_json))
            match_augments.extend(tft_data_handler.get_match_augments_from(match_json))
            match_traits.extend(tft_data_handler.get_match_traits_from(match_json))
            match_units.extend(tft_data_handler.get_match_units_from(match_json))

        path_strings = [
            f"{relative_path}/{match_table}/tft_{match_table}_{region}.csv"
            for match_table in match_table_names
        ]

        # stroe Match, MatchPlayer, MatchAugment, MatchTrait, MatchUnit data
        for path in path_strings:
            csv_utilities.save_class_list_to_csv(
                path,
                matches,
                with_header=True,
                header_strip_str="_",
            )

    directory_file_dict = {
        f"{relative_path}/{match_table}": f"tft_{match_table}.csv"
        for match_table in match_table_names
    }

    # merge csv files
    for directory, file_name in directory_file_dict.items():
        lines = csv_utilities.merge_csv_files_in_directory(directory, with_header=True)
        csv_utilities.save_csv_file(join(directory, file_name), lines)
