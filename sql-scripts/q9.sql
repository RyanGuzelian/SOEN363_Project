-- A couple of examples to demonstrate correlated queries. 
 
 
 SELECT p.player_tag, p.challenge_max_wins
  FROM db.player p
  WHERE p.challenge_max_wins > (
        SELECT AVG(challenge_max_wins)
        FROM db.player);