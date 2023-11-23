-- A few queries to demonstrate various join types on the same tables: inner vs. outer
-- (left and right) vs. full join. Use of null values in the database to show the differences
-- is required.

SELECT *
FROM clan c
LEFT JOIN war w
ON c.clan_tag = w.clan_tag;
