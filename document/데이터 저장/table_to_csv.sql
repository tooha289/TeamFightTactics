SELECT 'puuid', 'name', 'continent', 'region'
UNION
SELECT puuid, name, continent, region
FROM tftdb.player
INTO OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\data\\player.csv'
FIELDS TERMINATED BY ',' -- 필드 간 구분자
ENCLOSED BY '"' -- 필드 값을 감싸는 문자
LINES TERMINATED BY '\n'; -- 라인 간 구분자

SELECT 'match_id', 'match_date', 'match_length', 'version_major', 'version_minor', 'version_patch', 'version_date', 'tft_set_number'
UNION
SELECT *
FROM tftdb.match
INTO OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\data\\match.csv'
FIELDS TERMINATED BY ',' -- 필드 간 구분자
ENCLOSED BY '"' -- 필드 값을 감싸는 문자
LINES TERMINATED BY '\n'; -- 라인 간 구분자

SELECT 'match_player_id', 'match_id', 'puuid', 'last_round', 'level', 'placement', 'time_eliminated'
UNION
SELECT *
FROM tftdb.match_player
INTO OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\data\\match_player.csv'
FIELDS TERMINATED BY ',' -- 필드 간 구분자
ENCLOSED BY '"' -- 필드 값을 감싸는 문자
LINES TERMINATED BY '\n'; -- 라인 간 구분자

SELECT 'match_player_id', 'sequence', 'name', 'num_units', 'style', 'tier_current', 'tier_total'
UNION
SELECT *
FROM tftdb.match_trait
INTO OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\data\\match_trait.csv'
FIELDS TERMINATED BY ',' -- 필드 간 구분자
ENCLOSED BY '"' -- 필드 값을 감싸는 문자
LINES TERMINATED BY '\n'; -- 라인 간 구분자

SELECT 'match_player_id', 'sequence', 'name', 'rarity', 'tier', 'item1', 'item2', 'item3'
UNION
SELECT *
FROM tftdb.match_unit
INTO OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\data\\match_unit.csv'
FIELDS TERMINATED BY ',' -- 필드 간 구분자
ENCLOSED BY '"' -- 필드 값을 감싸는 문자
LINES TERMINATED BY '\n'; -- 라인 간 구분자

