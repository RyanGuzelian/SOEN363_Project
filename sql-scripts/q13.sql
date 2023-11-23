-- An example of a view that has a hard-coded criteria, by which the content of the view
-- may change upon changing the hard-coded value (see L09 slide 24).

CREATE VIEW high_exp_players AS
SELECT *
from db.player p
WHERE p.total_exp_points > 1000000
