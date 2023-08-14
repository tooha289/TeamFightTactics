-- LOAD DATA INFILE을 사용하여 데이터 로드
SHOW VARIABLES LIKE 'FOREIGN_KEY_CHECKS';
SET foreign_key_checks = 0;

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\tft_matches_20230814.csv'
INTO TABLE tft_source.match
FIELDS TERMINATED BY ','
IGNORE 1 LINES;

SET foreign_key_checks = 1;
SHOW VARIABLES LIKE 'FOREIGN_KEY_CHECKS';

-- check count
SELECT count(*) FROM tft_source.match;

-- delete data
DELETE FROM tft_source.match WHERE match_id<>'';

-- insert player table
INSERT INTO tftdb.player (puuid, name, continent, region)
SELECT puuid, name, continent, region
FROM tft_source.player AS source
ON DUPLICATE KEY UPDATE
	name = source.name,
	continent = source.continent,
	region = source.region;
    
-- insert player_statistic table
INSERT INTO tftdb.player_statistic (puuid, ranking, league_point, wins, losses, update_date)
SELECT puuid, ranking, league_point, wins, losses, update_date
FROM tft_source.player_statistic AS source
ON DUPLICATE KEY UPDATE
	ranking = source.ranking,
	league_point = source.league_point,
	wins = source.wins,
	losses = source.losses;
    
-- insert match table
INSERT INTO tftdb.match (match_id, match_date, match_length, version_major, version_minor, version_patch, version_date, tft_set_number)
SELECT match_id, match_date, match_length, version_major, version_minor, version_patch, version_date, tft_set_number
FROM tft_source.match AS source
ON DUPLICATE KEY UPDATE
	match_date = source.match_date,
	match_length = source.match_length,
	version_major = source.version_major,
	version_minor = source.version_minor,
	version_patch = source.version_patch,
	version_date = source.version_date,
	tft_set_number = source.tft_set_number;
    
