:param {
  // Define the file path root and the individual file names required for loading.
  // https://neo4j.com/docs/operations-manual/current/configuration/file-locations/
  file_path_root: 'file:///', // Change this to the folder your script can access the files at.
  file_0: 'location_202312031610.csv',
  file_1: 'clan_202312031610.csv',
  file_2: 'war_202312031610.csv',
  file_3: 'player_202312031610.csv',
  file_4: 'badge_202312031610.csv',
  file_5: 'achievement_202312031610.csv',
  file_6: 'deck_202312031610.csv',
  file_7: 'card_202312031610.csv',
  file_8: 'player_achievement_202312031610.csv',
  file_9: 'player_badge_202312031610.csv',
  file_10: 'clan_member_202312031610.csv',
  file_11: 'player_card_202312031610.csv'
};

// CONSTRAINT creation
// -------------------
//
// Create node uniqueness constraints, ensuring no duplicates for the given node label and ID property exist in the database. This also ensures no duplicates are introduced in future.
//
// NOTE: If your database version is below (not including) 4.4.0, please use the constraint creation syntax below:
// CREATE CONSTRAINT `imp_uniq_Achievement_achievement_id_` IF NOT EXISTS
// ON (n: `Achievement`)
// ASSERT n.`achievement_id ` IS UNIQUE;
// CREATE CONSTRAINT `imp_uniq_Badge_badge_id` IF NOT EXISTS
// ON (n: `Badge`)
// ASSERT n.`badge_id` IS UNIQUE;
// CREATE CONSTRAINT `imp_uniq_Card_card_id` IF NOT EXISTS
// ON (n: `Card`)
// ASSERT n.`card_id` IS UNIQUE;
// CREATE CONSTRAINT `imp_uniq_Player_player_tag_` IF NOT EXISTS
// ON (n: `Player`)
// ASSERT n.`player_tag ` IS UNIQUE;
// CREATE CONSTRAINT `imp_uniq_Clan_clan_tag` IF NOT EXISTS
// ON (n: `Clan`)
// ASSERT n.`clan_tag` IS UNIQUE;
// CREATE CONSTRAINT `imp_uniq_War_war_id` IF NOT EXISTS
// ON (n: `War`)
// ASSERT n.`war_id` IS UNIQUE;
// CREATE CONSTRAINT `imp_uniq_Deck_player_tag` IF NOT EXISTS
// ON (n: `Deck`)
// ASSERT n.`player_tag` IS UNIQUE;
// CREATE CONSTRAINT `imp_uniq_Location_location_id` IF NOT EXISTS
// ON (n: `Location`)
// ASSERT n.`location_id` IS UNIQUE;
//
// NOTE: The following constraint creation syntax is generated based on the current connected database version 5.14-aura.
CREATE CONSTRAINT `imp_uniq_Achievement_achievement_id_` IF NOT EXISTS
FOR (n: `Achievement`)
REQUIRE (n.`achievement_id `) IS UNIQUE;
CREATE CONSTRAINT `imp_uniq_Badge_badge_id` IF NOT EXISTS
FOR (n: `Badge`)
REQUIRE (n.`badge_id`) IS UNIQUE;
CREATE CONSTRAINT `imp_uniq_Card_card_id` IF NOT EXISTS
FOR (n: `Card`)
REQUIRE (n.`card_id`) IS UNIQUE;
CREATE CONSTRAINT `imp_uniq_Player_player_tag_` IF NOT EXISTS
FOR (n: `Player`)
REQUIRE (n.`player_tag `) IS UNIQUE;
CREATE CONSTRAINT `imp_uniq_Clan_clan_tag` IF NOT EXISTS
FOR (n: `Clan`)
REQUIRE (n.`clan_tag`) IS UNIQUE;
CREATE CONSTRAINT `imp_uniq_War_war_id` IF NOT EXISTS
FOR (n: `War`)
REQUIRE (n.`war_id`) IS UNIQUE;
CREATE CONSTRAINT `imp_uniq_Deck_player_tag` IF NOT EXISTS
FOR (n: `Deck`)
REQUIRE (n.`player_tag`) IS UNIQUE;
CREATE CONSTRAINT `imp_uniq_Location_location_id` IF NOT EXISTS
FOR (n: `Location`)
REQUIRE (n.`location_id`) IS UNIQUE;

:param {
  idsToSkip: []
};

// NODE load
// ---------
//
// Load nodes in batches, one node label at a time. Nodes will be created using a MERGE statement to ensure a node with the same label and ID property remains unique. Pre-existing nodes found by a MERGE statement will have their other properties set to the latest values encountered in a load file.
//
// NOTE: Any nodes with IDs in the 'idsToSkip' list parameter will not be loaded.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_5) AS row
WITH row
WHERE NOT row.`achievement_id` IN $idsToSkip AND NOT toInteger(trim(row.`achievement_id`)) IS NULL
CALL {
  WITH row
  MERGE (n: `Achievement` { `achievement_id `: toInteger(trim(row.`achievement_id`)) })
  SET n.`achievement_id ` = toInteger(trim(row.`achievement_id`))
  SET n.`achievement_name ` = row.`achievement_name`
  SET n.`info` = row.`info`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_4) AS row
WITH row
WHERE NOT row.`badge_id` IN $idsToSkip AND NOT toInteger(trim(row.`badge_id`)) IS NULL
CALL {
  WITH row
  MERGE (n: `Badge` { `badge_id`: toInteger(trim(row.`badge_id`)) })
  SET n.`badge_id` = toInteger(trim(row.`badge_id`))
  SET n.`badge_name` = row.`badge_name`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_7) AS row
WITH row
WHERE NOT row.`card_id` IN $idsToSkip AND NOT toInteger(trim(row.`card_id`)) IS NULL
CALL {
  WITH row
  MERGE (n: `Card` { `card_id`: toInteger(trim(row.`card_id`)) })
  SET n.`card_id` = toInteger(trim(row.`card_id`))
  SET n.`card_key` = row.`card_key`
  SET n.`name` = row.`name`
  SET n.`elixir` = toInteger(trim(row.`elixir`))
  SET n.`type` = row.`type`
  SET n.`rarity` = row.`rarity`
  SET n.`arena` = toInteger(trim(row.`arena`))
  SET n.`description` = row.`description`
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_3) AS row
WITH row
WHERE NOT row.`player_tag` IN $idsToSkip AND NOT row.`player_tag` IS NULL
CALL {
  WITH row
  MERGE (n: `Player` { `player_tag `: row.`player_tag` })
  SET n.`player_tag ` = row.`player_tag`
  SET n.`name` = row.`name`
  SET n.`exp_level` = toInteger(trim(row.`exp_level`))
  SET n.`total_exp_points` = toInteger(trim(row.`total_exp_points`))
  SET n.`trophies` = toInteger(trim(row.`trophies`))
  SET n.`best_trophies` = toInteger(trim(row.`best_trophies`))
  SET n.`wins` = toInteger(trim(row.`wins`))
  SET n.`losses` = toInteger(trim(row.`losses`))
  SET n.`battle_count` = toInteger(trim(row.`battle_count`))
  SET n.`three_crown_wins` = toInteger(trim(row.`three_crown_wins`))
  SET n.`challenge_cards_won` = toInteger(trim(row.`challenge_cards_won`))
  SET n.`challenge_max_wins` = toInteger(trim(row.`challenge_max_wins`))
  SET n.`tournament_cards_won` = toInteger(trim(row.`tournament_cards_won`))
  SET n.`tournament_battle_count` = toInteger(trim(row.`tournament_battle_count`))
  SET n.`war_day_wins` = toInteger(trim(row.`war_day_wins`))
  SET n.`current_favorite_card_id` = toInteger(trim(row.`current_favorite_card_id`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row
WHERE NOT row.`clan_tag` IN $idsToSkip AND NOT row.`clan_tag` IS NULL
CALL {
  WITH row
  MERGE (n: `Clan` { `clan_tag`: row.`clan_tag` })
  SET n.`clan_tag` = row.`clan_tag`
  SET n.`name` = row.`name`
  SET n.`type` = row.`type`
  SET n.`description` = row.`description`
  SET n.`clan_score` = toInteger(trim(row.`clan_score`))
  SET n.`clan_war_trophies` = toInteger(trim(row.`clan_war_trophies`))
  SET n.`location_id` = toInteger(trim(row.`location_id`))
  SET n.`required_trophies` = toInteger(trim(row.`required_trophies`))
  SET n.`donations_per_week` = toInteger(trim(row.`donations_per_week`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_2) AS row
WITH row
WHERE NOT row.`war_id` IN $idsToSkip AND NOT toInteger(trim(row.`war_id`)) IS NULL
CALL {
  WITH row
  MERGE (n: `War` { `war_id`: toInteger(trim(row.`war_id`)) })
  SET n.`war_id` = toInteger(trim(row.`war_id`))
  SET n.`clan_tag` = row.`clan_tag`
  SET n.`standing` = toInteger(trim(row.`standing`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row
WHERE NOT row.`player_tag` IN $idsToSkip AND NOT row.`player_tag` IS NULL
CALL {
  WITH row
  MERGE (n: `Deck` { `player_tag`: row.`player_tag` })
  SET n.`player_tag` = row.`player_tag`
  SET n.`card1` = toInteger(trim(row.`card1`))
  SET n.`card2` = toInteger(trim(row.`card2`))
  SET n.`card3` = toInteger(trim(row.`card3`))
  SET n.`card4` = toInteger(trim(row.`card4`))
  SET n.`card5` = toInteger(trim(row.`card5`))
  SET n.`card6` = toInteger(trim(row.`card6`))
  SET n.`card7` = toInteger(trim(row.`card7`))
  SET n.`card8` = toInteger(trim(row.`card8`))
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_0) AS row
WITH row
WHERE NOT row.`location_id` IN $idsToSkip AND NOT toInteger(trim(row.`location_id`)) IS NULL
CALL {
  WITH row
  MERGE (n: `Location` { `location_id`: toInteger(trim(row.`location_id`)) })
  SET n.`location_id` = toInteger(trim(row.`location_id`))
  SET n.`location_name` = row.`location_name`
  SET n.`location_code` = row.`location_code`
  SET n.`isCountry` = toLower(trim(row.`isCountry`)) IN ['1','true','yes']
} IN TRANSACTIONS OF 10000 ROWS;


// RELATIONSHIP load
// -----------------
//
// Load relationships in batches, one relationship type at a time. Relationships are created using a MERGE statement, meaning only one relationship of a given type will ever be created between a pair of nodes.
LOAD CSV WITH HEADERS FROM ($file_path_root + $file_8) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Player` { `player_tag `: row.`player_tag` })
  MATCH (target: `Achievement` { `achievement_id `: toInteger(trim(row.`achievement_id`)) })
  MERGE (source)-[r: `HAS_ACHIEVEMENT`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Player` { `player_tag `: row.`player_tag` })
  MATCH (target: `Deck` { `player_tag`: row.`player_tag` })
  MERGE (source)-[r: `USES`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Deck` { `player_tag`: row.`player_tag` })
  MATCH (target: `Card` { `card_id`: toInteger(trim(row.`card1`)) })
  MERGE (source)-[r: `INCLUDES_1`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_11) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Player` { `player_tag `: row.`player_tag` })
  MATCH (target: `Card` { `card_id`: toInteger(trim(row.`card_id`)) })
  MERGE (source)-[r: `HAS_CARD`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_9) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Player` { `player_tag `: row.`player_tag` })
  MATCH (target: `Badge` { `badge_id`: toInteger(trim(row.`badge_id`)) })
  MERGE (source)-[r: `HAS_BADGE`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_10) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Player` { `player_tag `: row.`player_tag` })
  MATCH (target: `Clan` { `clan_tag`: row.`clan_tag` })
  MERGE (source)-[r: `IS_IN`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_1) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Clan` { `clan_tag`: row.`clan_tag` })
  MATCH (target: `Location` { `location_id`: toInteger(trim(row.`location_id`)) })
  MERGE (source)-[r: `LOCATED_IN`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Deck` { `player_tag`: row.`player_tag` })
  MATCH (target: `Card` { `card_id`: toInteger(trim(row.`card2`)) })
  MERGE (source)-[r: `INCLUDES_2`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Deck` { `player_tag`: row.`player_tag` })
  MATCH (target: `Card` { `card_id`: toInteger(trim(row.`card3`)) })
  MERGE (source)-[r: `INCLUDES_3`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Deck` { `player_tag`: row.`player_tag` })
  MATCH (target: `Card` { `card_id`: toInteger(trim(row.`card4`)) })
  MERGE (source)-[r: `INCLUDES_4`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Deck` { `player_tag`: row.`player_tag` })
  MATCH (target: `Card` { `card_id`: toInteger(trim(row.`card5`)) })
  MERGE (source)-[r: `INCLUDES_5`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Deck` { `player_tag`: row.`player_tag` })
  MATCH (target: `Card` { `card_id`: toInteger(trim(row.`card6`)) })
  MERGE (source)-[r: `INCLUDES_6`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Deck` { `player_tag`: row.`player_tag` })
  MATCH (target: `Card` { `card_id`: toInteger(trim(row.`card7`)) })
  MERGE (source)-[r: `INCLUDES_7`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;

LOAD CSV WITH HEADERS FROM ($file_path_root + $file_6) AS row
WITH row 
CALL {
  WITH row
  MATCH (source: `Deck` { `player_tag`: row.`player_tag` })
  MATCH (target: `Card` { `card_id`: toInteger(trim(row.`card8`)) })
  MERGE (source)-[r: `INCLUDES_8`]->(target)
} IN TRANSACTIONS OF 10000 ROWS;
