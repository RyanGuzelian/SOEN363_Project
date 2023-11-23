-- A couple of examples to demonstrate correlated queries. 
 
 
SELECT p.player_tag, p.three_crown_wins
FROM db.player p
WHERE EXISTS ( SELECT *
	FROM db.player_achievement pa
	WHERE pa.player_tag = p.player_tag
	AND pa.achievement_id = 125
);