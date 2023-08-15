use tftdb;

-- 플레이어 데이터 확인 
SELECT count(*) FROM tftdb.player;
SELECT count(*) FROM tftdb.player_statistic;

-- 매치 데이터 확인 
SELECT count(*) FROM tftdb.match;
SELECT count(*) FROM tftdb.match_player;
SELECT count(*) FROM tftdb.match_augment;
SELECT count(*) FROM tftdb.match_trait;
SELECT count(*) FROM tftdb.match_unit;

-- 사용된 증강의 종류
SELECT DISTINCT name
FROM match_augment
ORDER BY name;
-- 사용된 특성의 종류
SELECT DISTINCT name
FROM match_trait
ORDER BY name;
-- 사용된 유닛의 종류
SELECT DISTINCT name
FROM match_unit
ORDER BY name;

-- 각 대륙별 플레이어의 수 
SELECT continent, count(*) num_of_player
FROM player
GROUP BY continent
ORDER BY 2 DESC;

-- 대륙, 지역 별 플레이어 수 및 랭킹
SELECT continent, region,
	   count(*) num_of_player,
       rank() over(order by count(*) DESC) ranking
FROM player
GROUP BY continent, region
ORDER BY 3 DESC;

-- 버전 별, 사용된 유닛의 수를 rarity로 정렬
-- 질문1. Ryze는 동일 유닛인데 합칠 수 있는 방법
SELECT m.version_major, m.version_minor, m.version_patch, mu.name, mu.rarity, count(*) num_of_unit
FROM tftdb.match m INNER JOIN match_player mp ON m.match_id = mp.match_id
				   INNER JOIN match_unit mu ON mp.match_player_id = mu.match_player_id
GROUP BY m.version_major, m.version_minor, m.version_patch, mu.name, mu.rarity
HAVING mu.rarity < 9
ORDER BY 1,2 DESC,3 DESC,mu.rarity DESC;

-- 버전 별, 사용된 유닛들의 순위
CREATE VIEW ranking_of_unit AS
	SELECT m.version_major, m.version_minor, m.version_patch, mu.name, mu.rarity, count(*) num_of_unit,
		   rank() over(partition by m.version_major, m.version_minor, m.version_patch order by count(*) DESC) ranking
	FROM tftdb.match m INNER JOIN match_player mp ON m.match_id = mp.match_id
					   INNER JOIN match_unit mu ON mp.match_player_id = mu.match_player_id
	GROUP BY m.version_major, m.version_minor, m.version_patch, mu.name, mu.rarity
	HAVING mu.rarity < 9
	ORDER BY 1,2 DESC,3 DESC, 6 DESC;

SELECT * FROM ranking_of_unit;

-- 각 match_player 별, rarity * tier의 합과 순위 (heimerdingerTurret은 추가 유닛이므로 제외)

-- 자주 이용되는 유닛(1등 유닛)을 사용한 플레이어들의 각 매치 순위
WITH no_1_units AS
(SELECT version_major, version_minor, version_patch, name
FROM ranking_of_unit
WHERE ranking = 1 AND version_minor > 13)

SELECT m.version_major, m.version_minor, m.version_patch, mu.name,
	   sum(mp.placement) sum_placement, count(*) use_count,
       round(sum(mp.placement) / count(*), 2) avg_placement
FROM tftdb.match m INNER JOIN match_player mp ON m.match_id = mp.match_id
				   INNER JOIN match_unit mu ON mp.match_player_id = mu.match_player_id
WHERE mu.name IN (SELECT name FROM no_1_units)
GROUP BY m.version_major, m.version_minor, m.version_patch, mu.name;

-- 버전 별, 모든 유닛의 평균 순위
SELECT m.version_major, m.version_minor, m.version_patch, mu.name,
	   sum(mp.placement) sum_placement, count(*) use_count,
       round(sum(mp.placement) / count(*), 2) avg_placement
FROM tftdb.match m INNER JOIN match_player mp ON m.match_id = mp.match_id
				   INNER JOIN match_unit mu ON mp.match_player_id = mu.match_player_id
GROUP BY m.version_major, m.version_minor, m.version_patch, mu.name
ORDER BY m.version_major DESC, m.version_minor DESC, m.version_patch DESC, avg_placement;

-- Heimerdinger가 이름에 포함된 유닛의 사용 횟수
SELECT m.version_major, m.version_minor, m.version_patch, mu.name, count(*) num_of_unit
FROM tftdb.match m INNER JOIN match_player mp ON m.match_id = mp.match_id
				   INNER JOIN match_unit mu ON mp.match_player_id = mu.match_player_id
WHERE mu.name LIKE 'TFT9_Heimer%'
GROUP BY m.version_major, m.version_minor, m.version_patch, mu.name;

-- 하이머딩거는 사용했지만 하이머딩거 포탑은 없는 사람들
WITH use_heimerdinger AS(
	SELECT match_player_id
	FROM match_unit mu
	WHERE mu.name = 'TFT9_Heimerdinger'),
use_heimerdinger_turret AS(
	SELECT match_player_id
	FROM match_unit mu
	WHERE mu.name = 'TFT9_HeimerdingerTurret')

SELECT uh.match_player_id
FROM use_heimerdinger uh
WHERE uh.match_player_id NOT IN ( SELECT match_player_id FROM use_heimerdinger_turret);

-- 각 플레이어가 사용한 아이템 리스트
CREATE OR REPLACE VIEW match_player_item(match_player_id, unit_name, item_name) AS
	SELECT match_player_id, name, item1
	FROM match_unit
    WHERE item1 <> ''
UNION ALL
	SELECT match_player_id, name, item2
	FROM match_unit
    WHERE item2 <> ''
UNION ALL
	SELECT match_player_id, name, item3
	FROM match_unit
    WHERE item3 <> '';

SELECT match_player_id, unit_name, item_name FROM match_player_item
GROUP BY match_player_id, unit_name, item_name
ORDER BY match_player_id;

-- 버전 별, 아이템 별 사용 순위

-- 각 유닛 별, 착용한 아이템 순위
SELECT unit_name, item_name, count(*) use_count,
	   dense_rank() over(partition by unit_name order by count(*) desc) ranking
FROM match_player_item
WHERE unit_name <> 'TFT9_HeimerdingerTurret'
GROUP BY unit_name, item_name;
-- 각 유닛 별, 착용한 아이템 순위와 플레이어의 등수
SELECT mpi.unit_name, mpi.item_name,
	   sum(mp.placement) sum_placement, count(mp.placement) count_item,
       round(sum(mp.placement) / count(mp.placement), 2) avg_placement
FROM match_player mp INNER JOIN match_player_item mpi ON mp.match_player_id = mpi.match_player_id
GROUP BY mpi.unit_name, mpi.item_name
ORDER BY mpi.unit_name, count_item DESC;
		
-- 버전 별, 유닛 별 사용 순위
-- 버전 별, 특성 별 사용 순위
-- 버전 별, 각 챔피언이 착용한 아이템 횟수 순위

-- 각 지역 1위 플레이어의 최근 10게임 유닛 조합
-- 각 지역 1위 플레이어의 최근 10게임 특성 조합

-- 각 지역별 게임 시간대 분석

-- 각 플레이어 별 2개 이상 증강이 존재하는 경우
SELECT match_player_id, count(*)
FROM tftdb.match_augment
GROUP BY match_player_id
HAVING count(*) >= 2
ORDER BY match_player_id;
