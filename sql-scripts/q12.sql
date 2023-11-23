-- One example per set operations: intersect, union, and difference vs. their equivalences without using set operations.

-- UNION WITH UNION KEYWORD
(SELECT p.player_tag
FROM db.player p
WHERE p.total_exp_points < 900000)
UNION
(SELECT p.player_tag
FROM db.player p
WHERE p.total_exp_points > 1500000);

-- UNION WITHOUT UNION KEYWORD
(SELECT p.player_tag
FROM db.player p
WHERE p.total_exp_points < 900000 OR p.total_exp_points > 1500000);


-- INTERSECTION WITH INTERSECT KEYWORD
(SELECT p.player_tag
FROM db.player p
WHERE p.total_exp_points > 900000)
INTERSECT
(SELECT p.player_tag
FROM db.player p
WHERE p.total_exp_points < 1500000);

-- INTERSECTION WITHOUT INTERSECT KEYWORD
(SELECT p.player_tag
FROM db.player p
WHERE p.total_exp_points > 900000 AND p.total_exp_points < 1500000)

-- DIFFERENCE WITH EXCEPT KEYWORD
(SELECT p.player_tag, p.name
FROM db.player p
WHERE p.total_exp_points > 900000)
EXCEPT 
(SELECT p.player_tag, p.name
FROM db.player p
WHERE p.name LIKE 'B%');

-- DIFFERENCE WITHOUT EXCEPT KEYWORD
(SELECT p.player_tag, p.name
FROM db.player p
WHERE p.total_exp_points > 900000 AND p.name NOT LIKE 'B%')
