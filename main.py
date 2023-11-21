import requests
import json
import mysql.connector
import time

start = time.time()
# Connect to the database
cnx = mysql.connector.connect(user='root', password='admin',
                              host='localhost', port=3307, database='db')
cursor = cnx.cursor(buffered=True)


# api2_url = 'https://royaleapi.github.io/cr-api-data/json/cards.json'
#
# response = requests.get(api2_url)
# data = json.loads(response.text)
#
# for card in data:
#     card_id = card['id']
#     key = card['key']
#     name = card['name']
#     elixir = card['elixir']
#     card_type = card['type']
#     rarity = card['rarity']
#     arena = card['arena']
#     description = card['description']
#
#     add_card = ("INSERT IGNORE INTO card"
#                 "(card_id, card_key, name, elixir, type, rarity, arena, description)"
#                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)")
#     data_card = (card_id, key, name, elixir, card_type, rarity, arena, description)
#
#     cursor.execute(add_card, data_card)

# Define the API endpoint and parameters
api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImQ2NDcyZDk4LWEwMWEtNDliMi05ZGY0LWQxZjQxYjU0OWZlOSIsImlhdCI6MTcwMDU4MzMwMCwic3ViIjoiZGV2ZWxvcGVyLzU5NmQ3MWE1LWEwOTItZmJjNy03Njc1LThiYjUxN2Q4MTZmMCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMzIuMjA1LjIyOS4yMCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.h68R8UIHq3HDYKoweIoBbB5Iz2TwHTYefjwwl_BUyBOFOM3whzrFdcXTOEPJw4Vn0qmdViF6eijsa_WMjzgcgw'
api_url = 'https://api.clashroyale.com/v1/'
clan_tags = []
headers = {'Authorization': f'Bearer {api_token}'}

#Add clans to clan_tags
tag_url = api_url + "clans?name=mexico&limit=1000"#done the, aaa, russia, pol, mexico
tag_response = requests.get(tag_url, headers)
tag_data = json.loads(tag_response.text)
whole_clan_data = tag_data['items']
for clan_data in whole_clan_data:
    clan_tags.append(clan_data['tag'][1:])

# Loop through the clan tags
for clan_tag in clan_tags:
    clan_url = api_url + "clans/%23" + clan_tag
    clan_response = requests.get(clan_url, headers)
    clan_data = json.loads(clan_response.text)

    new_clan_tag = '#' + clan_tag

    war_url = clan_url + "/riverracelog?limit=3"
    war_response = requests.get(war_url, headers)
    war_data = json.loads(war_response.text)
    # Extract the relevant data from the JSON response for the clan
    name = clan_data['name']  # VARCHAR
    type = clan_data['type']  # ENUM {open, closed, invite only}?
    description = clan_data['description']  # text
    badge_id = clan_data['badgeId']  # int, might remove if the badges are not found in the api
    clan_score = clan_data['clanScore']  # int
    clan_war_trophies = clan_data['clanWarTrophies']  # int
    location = clan_data['location']  # holds id, name, isCountry, and countrycode, maybe do a location table?
    required_trophies = clan_data[
        'requiredTrophies']  # int, can make a query to check all players that are eligible to join, with the minimum of their trophies being this number
    donations_per_week = clan_data['donationsPerWeek']

    members = clan_data[
        'memberList']  # holds players and their respective data relating to the clan (tag, name, role, lastSeen, expLevel, arena{id, name}, donations, donationsReceived)
    # Insert the clan data into the clan table
    add_clan = ("INSERT IGNORE INTO clan "
                "(clan_tag, name, type, description, clan_score, clan_war_trophies, location_id, required_trophies, donations_per_week) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data_clan = (
        new_clan_tag, name, type, description, clan_score, clan_war_trophies, location['id'],
        required_trophies,
        donations_per_week)
    cursor.execute(add_clan, data_clan)

    location_id = location['id']
    location_name = location['name']
    location_is_country = location['isCountry']
    if 'countryCode' in location:
        location_code = location['countryCode']
    else :
        location_code = None

    add_location = ("INSERT IGNORE INTO location"
                    "(location_id, location_name, location_code, isCountry)"
                    "VALUES(%s, %s, %s, %s)")
    data_location = (location_id, location_name, location_code, location_is_country)
    cursor.execute(add_location, data_location)

    # add war data to war table

    wars = war_data.get('items', [])
    for i, war in enumerate(wars, start=1):
        standings = war.get('standings', [])
        for standing in standings:
            if standing['clan']['tag'][1:] == clan_tag:
                add_war = ("INSERT IGNORE INTO war"
                           "(clan_tag, war_id, standing)"
                           "VALUES (%s, %s, %s)")
                data_war = (new_clan_tag, i, standing['rank'])
                cursor.execute(add_war, data_war)

    # Extract the data for the members
    for member in members:
        player_tag = member['tag']
        print(clan_tag + ', ' + player_tag)

        player_url = api_url + "players/%23" + player_tag[1:]
        player_response = requests.get(player_url, headers)
        player_data = json.loads(player_response.text)

        name = player_data['name']  # VARCHAR
        exp_level = player_data['expLevel']  # int
        if 'lastSeen' in member:
            last_seen = member['lastSeen']
        else:
            last_seen = None
        role = player_data['role']
        total_exp_points = player_data['totalExpPoints']  # int
        trophies = player_data['trophies']  # int
        best_trophies = player_data['bestTrophies']  # int
        wins = player_data['wins']  # int
        losses = player_data['losses']  # int
        battle_count = player_data['battleCount']  # int
        three_crown_wins = player_data['threeCrownWins']  # int
        challenge_cards_won = player_data['challengeCardsWon']  # int
        challenge_max_wins = player_data['challengeMaxWins']  # int
        tournament_cards_won = player_data['tournamentCardsWon']  # int
        tournament_battle_count = player_data['tournamentBattleCount']  # int
        donations = player_data['donations']  # int
        donations_received = player_data['donationsReceived']  # int
        cards = player_data['cards']  # holds level and starLevel of each card
        deck = player_data['currentDeck']  # holds card entities
        current_favorite_card = player_data['currentFavouriteCard']['id']  # int
        arena = player_data['arena']
        badges = player_data['badges']
        achievements = player_data['achievements']
        star_points = player_data['starPoints']
        exp_points = player_data['expPoints']

        add_player = ("INSERT IGNORE INTO player"
                      "(player_tag, name, exp_level, total_exp_points, trophies, best_trophies, wins, losses, battle_count, three_crown_wins, challenge_cards_won, challenge_max_wins, tournament_cards_won, tournament_battle_count, current_favorite_card_id)"
                      "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data_player = (
            player_tag, name, exp_level, total_exp_points, trophies, best_trophies, wins, losses, battle_count,
            three_crown_wins, challenge_cards_won, challenge_max_wins, tournament_cards_won, tournament_battle_count,
            current_favorite_card)
        cursor.execute(add_player, data_player)

        add_clan_member = ("INSERT IGNORE INTO clan_member "
                           "(clan_tag, player_tag, role, last_seen, donations, donations_received)"
                           "VALUES(%s, %s, %s, %s, %s, %s)")
        data_clan_member = (new_clan_tag, player_tag, role, last_seen, donations, donations_received)
        cursor.execute(add_clan_member, data_clan_member)



        # Adding player cards to player_card
        for card in cards:
            card_id = card['id']  # int pour tout le reste dans cartes
            card_level = card['level']
            if 'starLevel' in card:
                card_star_level = card['starLevel']
            else:
                card_star_level = None
            # print(f'{card_id}, {card_star_level}')
            add_player_card = ("INSERT IGNORE INTO player_card"
                               "(player_tag, card_id, level, star_level)"
                               "VALUES (%s, %s, %s, %s)")
            # Assuming card_star_level is the variable you want to insert into star_level
            if card_star_level is not None:
                data_player_card = (player_tag, card_id, card_level, card_star_level)
            else:
                data_player_card = (player_tag, card_id, card_level, None)  # Setting star_level to NULL
            cursor.execute(add_player_card, data_player_card)

        # adding deck to player_deck
        deck_card_ids = []
        for card in deck:
            deck_card_ids.append(card['id'])
        add_player_deck = ("INSERT IGNORE INTO deck"
                           "(player_tag, card1, card2, card3, card4, card5, card6, card7, card8)"
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        data_player_deck = (
            player_tag, deck_card_ids[0], deck_card_ids[1], deck_card_ids[2], deck_card_ids[3], deck_card_ids[4],
            deck_card_ids[5], deck_card_ids[6], deck_card_ids[7])
        cursor.execute(add_player_deck, data_player_deck)

        # adding badges to badge and player_badge
        for badge in badges:

            badge_name = badge['name']
            # print(f'{badge_name}')
            if 'level' in badge:
                badge_level = badge['level']
            else:
                badge_level = None
            if 'maxLevel' in badge:
                badge_max_level = badge['maxLevel']
            else:
                badge_max_level = None
            badge_progress = badge['progress']
            if 'target' in badge:
                badge_target = badge['target']
            else:
                badge_target = None

            # add_badge = ("INSERT IGNORE INTO badge"
            #              "(badge_name)"
            #              "VALUES(%s)")
            data_badge = (badge_name)
            # cursor.execute(add_badge, (data_badge,))

            # Retrieve the badge_id (whether inserted or already exists)
            get_badge_id = "SELECT badge_id FROM badge WHERE badge_name = %s"
            cursor.execute(get_badge_id, (data_badge,))
            result = cursor.fetchone()
            if result:
                badge_id = result[0]
            else:
                # Person was just inserted, get the last inserted ID
                cursor.execute("SELECT LAST_INSERT_ID()")
                badge_id = cursor.fetchone()[0]

            add_player_badge = ("INSERT IGNORE INTO player_badge"
                                "(player_tag, badge_id, badge_level, max_level, progress, target)"
                                "VALUES(%s, %s, %s, %s, %s, %s)")
            data_player_badge = (player_tag, badge_id, badge_level, badge_max_level, badge_progress, badge_target)
            cursor.execute(add_player_badge, data_player_badge)

        for achievement in achievements:
            achievement_name = achievement['name']
            achievement_info = achievement['info']
            achievement_stars = achievement['stars']
            achievement_value = achievement['value']
            achievement_target = achievement['target']

            # add_achievement = ("INSERT IGNORE INTO achievement"
            #                    "(achievement_name, info)"
            #                    "VALUES (%s, %s)")
            # data_achievement = (achievement_name, achievement_info)
            # cursor.execute(add_achievement, data_achievement)

            # Retrieve the badge_id (whether inserted or already exists)
            get_achievement_id = "SELECT achievement_id FROM achievement WHERE achievement_name = %s"
            data_achievement_name = (achievement_name)
            cursor.execute(get_achievement_id, (data_achievement_name,))
            result = cursor.fetchone()
            if result:
                achievement_id = result[0]
            else:
                # Person was just inserted, get the last inserted ID
                cursor.execute("SELECT LAST_INSERT_ID()")
                achievement_id = cursor.fetchone()[0]

            add_player_achievement = ("INSERT IGNORE INTO player_achievement"
                                      "(player_tag, achievement_id, stars, value, target)"
                                      "VALUES(%s, %s, %s, %s, %s)")
            data_player_achievement = (
                player_tag, achievement_id, achievement_stars, achievement_value, achievement_target)
            cursor.execute(add_player_achievement, data_player_achievement)
    cnx.commit()
# Commit the changes and close the connection

cursor.close()
cnx.close()
end = time.time()
print(end - start)
