-- basic select with where clause
SELECT *
FROM db.clan AS C
WHERE clan_score > 10000;

-- Basic select with simple group by clause (without having clause).
SELECT P.exp_level, COUNT(*) AS playercount
FROM db.player AS P
GROUP BY exp_level;

-- Basic select with simple group by clause (with having clause).
SELECT P.exp_level, COUNT(*) AS playercount
FROM db.player AS P
GROUP BY exp_level
HAVING playercount > 6;

-- Simple join using caresian product and where clause
SELECT P.trophies, CM.clan_tag 
FROM db.player AS P, db.clan_member AS CM
WHERE P.player_tag = CM.player_tag;

-- Join query using ON
SELECT P.trophies, CM.clan_tag
FROM db.player AS P
JOIN db.clan_member AS CM ON P.player_tag = CM.player_tag;


-- Join queries using on (inner, outter left, outter right, full join)
SELECT *
FROM clan c
INNER JOIN war w
ON c.clan_tag = w.clan_tag;

SELECT *
FROM clan c
LEFT JOIN war w
ON c.clan_tag = w.clan_tag;

SELECT *
FROM clan c
RIGHT JOIN war w
ON c.clan_tag = w.clan_tag;

SELECT *
FROM clan c
LEFT JOIN war w ON c.clan_tag = w.clan_tag
UNION
SELECT *
FROM clan c
RIGHT JOIN war w ON c.clan_tag = w.clan_tag;

-- Correlated query
SELECT p.player_tag, p.challenge_max_wins
  FROM db.player p
  WHERE p.challenge_max_wins > (
        SELECT AVG(challenge_max_wins)
        FROM db.player);

 SELECT p.player_tag, p.tournament_battle_count
  FROM db.player p
  WHERE p.tournament_battle_count > (
        SELECT AVG(tournament_battle_count)
        FROM db.player);

-- Set Operations (intersect vs equicalences without set operations)
SELECT p.player_tag, p.three_crown_wins
FROM db.player p
INTERSECT 
SELECT pa.player_tag, pa.achievement_id 
FROM db.player_achievement pa
WHERE pa.achievement_id = 125;

SELECT p.player_tag, p.three_crown_wins
FROM db.player p
WHERE EXISTS ( SELECT *
    FROM db.player_achievement pa
    WHERE pa.player_tag = p.player_tag
    AND pa.achievement_id = 125
);

-- Set Operations (union vs equivalences without set operations)
SELECT p.player_tag, p.three_crown_wins
FROM db.player p
UNION 
SELECT pa.player_tag, pa.achievement_id 
FROM db.player_achievement pa
WHERE pa.achievement_id = 125;

SELECT COALESCE(p.player_tag, pa.player_tag) AS player_tag,
       p.three_crown_wins,
       pa.achievement_id
FROM db.player p
LEFT JOIN db.player_achievement pa
  ON p.player_tag = pa.player_tag AND pa.achievement_id = 125
UNION
SELECT COALESCE(p.player_tag, pa.player_tag) AS player_tag,
       p.three_crown_wins,
       pa.achievement_id
FROM db.player p
RIGHT JOIN db.player_achievement pa
  ON p.player_tag = pa.player_tag AND pa.achievement_id = 125;

-- Set Operations (difference vs equicalences without set operations)
SELECT p.player_tag, p.three_crown_wins
FROM db.player p
EXCEPT 
SELECT pa.player_tag, pa.achievement_id 
FROM db.player_achievement pa
WHERE pa.achievement_id = 125;

SELECT p.player_tag, p.three_crown_wins
FROM db.player p
WHERE NOT EXISTS ( SELECT *
    FROM db.player_achievement pa
    WHERE pa.player_tag = p.player_tag
    AND pa.achievement_id = 125
);

-- View with hard-coded criteria
CREATE VIEW high_exp_players AS
SELECT *
from db.player p
WHERE p.total_exp_points > 1000000

-- Division (regular nested query)
SELECT player_tag, name from player p
WHERE p.player_tag
NOT IN (
SELECT player_tag FROM 
db.player_clan pc
WHERE pc.clan_tag = "LCUYQ0GP"
);

-- Division (Not Exists & Except)
SELECT DISTINCT p.player_tag
FROM db.player p 
WHERE NOT EXISTS (
	(
	SELECT p1.player_tag
	FROM db.player p1
	) 
	EXCEPT 
	(
	SELECT cm.player_tag
	FROM db.clan_member cm 
	WHERE cm.clan_tag <> 'LCUYQ0GP'
	) 
);

-- Queries that demonstrate overlap & covering constraints

