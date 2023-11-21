-- Basic select with simple group by clause (with having clause).


SELECT P.exp_level, COUNT() AS playercount
FROM db.player AS P
GROUP BY exp_level
HAVING COUNT() > 6;
