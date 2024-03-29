CREATE DATABASE IF NOT EXISTS db;

USE db;

-- Badge table
CREATE TABLE badge (
    badge_id INT AUTO_INCREMENT,
    badge_name VARCHAR(255) unique,
    PRIMARY KEY (badge_id)
);

-- Card table
CREATE TABLE card (
    card_id INT,
    card_key VARCHAR(50),
    name VARCHAR(255),
    elixir INT,
    type VARCHAR(50),
    rarity VARCHAR(50),
    arena INT,
    description VARCHAR(2000),
    PRIMARY KEY (card_id)
);

-- Player table
CREATE TABLE player (
    player_tag VARCHAR(15) CHECK (player_tag LIKE '#%'),
    name VARCHAR(25),
    exp_level INT,
    total_exp_points INT,
    trophies INT,
    best_trophies INT,
    wins INT,
    losses INT,
    battle_count INT,
    three_crown_wins INT,
    challenge_cards_won INT,
    challenge_max_wins INT,
    tournament_cards_won INT,
    tournament_battle_count INT,
    war_day_wins INT,
    current_favorite_card_id INT,
    PRIMARY KEY (player_tag),
    FOREIGN KEY (current_favorite_card_id) REFERENCES card(card_id)
);

-- Clan table
CREATE TABLE clan (
    clan_tag VARCHAR(15),
    name VARCHAR(255),
    type VARCHAR(20),
    description TEXT(65535),
    clan_score INT,
    clan_war_trophies INT,
    location_id INT,
    required_trophies INT,
    donations_per_week INT,
    PRIMARY KEY (clan_tag)
);

-- War table
CREATE TABLE war (
    clan_tag VARCHAR(15),
    war_id INT,
    standing INT,
    PRIMARY KEY (clan_tag, war_id),
    FOREIGN KEY (clan_tag) REFERENCES clan(clan_tag)
);

-- Achievement table
CREATE TABLE achievement (
    achievement_id INT AUTO_INCREMENT,
    achievement_name VARCHAR(255) unique,
    info TEXT(65535),
    PRIMARY KEY (achievement_id)
);

-- Player Achievement table
CREATE TABLE player_achievement (
    player_tag VARCHAR(15) CHECK (player_tag LIKE '#%'),
    achievement_id INT AUTO_INCREMENT,
    stars INT,
    value INT,
    target INT,
    PRIMARY KEY (player_tag, achievement_id),
    FOREIGN KEY (player_tag) REFERENCES player(player_tag),
    FOREIGN KEY (achievement_id) REFERENCES achievement(achievement_id)
);

-- Clan Member table
CREATE TABLE clan_member (
    player_tag VARCHAR(15) CHECK (player_tag LIKE '#%'),
    clan_tag VARCHAR(15),
    role ENUM('member', 'elder', 'leader', 'coLeader'),
    last_seen DATETIME NULL,
    donations INT, -- represents the number of donations made
    donations_received INT,
    PRIMARY KEY (player_tag, clan_tag),
    FOREIGN KEY (player_tag) REFERENCES player(player_tag),
    FOREIGN KEY (clan_tag) REFERENCES clan(clan_tag)
);


-- Player Card table
CREATE TABLE player_card (
    player_tag VARCHAR(15) CHECK (player_tag LIKE '#%'),
    card_id INT,
    level INT,
    star_level INT NULL,
    PRIMARY KEY (player_tag, card_id),
    FOREIGN KEY (player_tag) REFERENCES player(player_tag),
    FOREIGN KEY (card_id) REFERENCES card(card_id)
);

-- Player Badge table
CREATE TABLE player_badge (
    player_tag VARCHAR(255), 
    badge_id INT AUTO_INCREMENT,
    badge_level INT NULL,
    max_level INT NULL,
    progress INT, -- represents the progress made towards a specific badge level
    target INT, -- represents the target value required to achieve a specific badge level
    PRIMARY KEY (player_tag, badge_id),
    FOREIGN KEY (player_tag) REFERENCES player(player_tag),
    FOREIGN KEY (badge_id) REFERENCES badge(badge_id)
);

-- Deck table
CREATE TABLE deck (
    player_tag VARCHAR(15) CHECK (player_tag LIKE '#%'),
    card1 INT,
    card2 INT,
    card3 INT,
    card4 INT,
    card5 INT,
    card6 INT,
    card7 INT,
    card8 INT,
    PRIMARY KEY (player_tag),
    FOREIGN KEY (player_tag) REFERENCES player(player_tag),
    FOREIGN KEY (card1) REFERENCES card(card_id),
    FOREIGN KEY (card2) REFERENCES card(card_id),
    FOREIGN KEY (card3) REFERENCES card(card_id),
    FOREIGN KEY (card4) REFERENCES card(card_id),
    FOREIGN KEY (card5) REFERENCES card(card_id),
    FOREIGN KEY (card6) REFERENCES card(card_id),
    FOREIGN KEY (card7) REFERENCES card(card_id),
    FOREIGN KEY (card8) REFERENCES card(card_id)
);

-- Log trigger
CREATE TRIGGER db.player_update
AFTER UPDATE ON db.player FOR EACH ROW
    INSERT INTO manual_update_log (update_info)
    VALUES (CONCAT('Updated player record (', OLD.player_tag, ')'));


-- -- Achievement table
-- CREATE TABLE achievement (
--     achievement_id INT,
--     name VARCHAR(255),
--     info TEXT(65535),
--     PRIMARY KEY (achievement_id)
-- );

-- -- Player Achievement table
-- CREATE TABLE player_achievement (
--     player_tag VARCHAR(15) CHECK (player_tag LIKE '#%'),
--     achievement_id INT,
--     stars INT,
--     value INT,
--     target INT,
--     PRIMARY KEY (player_tag, achievement_id),
--     FOREIGN KEY (player_tag) REFERENCES player(player_tag),
--     FOREIGN KEY (achievement_id) REFERENCES achievement(achievement_id)
-- );
