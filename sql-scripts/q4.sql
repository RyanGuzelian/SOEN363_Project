-- A simple join select query using cartesian product and where clause 

SELECT p.trophies, cm.clan_tag 
FROM db.player p, db.clan_member cm
WHERE p.player_tag = cm.player_tag
