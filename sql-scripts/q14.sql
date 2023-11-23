-- Two implementations of the division operator using a) a regular nested query using
-- NOT IN and b) a correlated nested query using NOT EXISTS and EXCEPT (See [4]).


SELECT player_tag, name from player p
WHERE p.player_tag
NOT IN (
SELECT player_tag FROM 
db.player_clan pc
WHERE pc.clan_tag = "LCUYQ0GP"
)