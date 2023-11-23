-- A couple of examples to demonstrate correlated queries. 
 
 
 SELECT p.player_tag, p.tournament_battle_count
  FROM db.player p
  WHERE p.tournament_battle_count > (
        SELECT AVG(tournament_battle_count)
        FROM db.player);