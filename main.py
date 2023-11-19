import requests
import json
import mysql.connector
import time

start = time.time()
# Connect to the database
cnx = mysql.connector.connect(user='root', password='admin',
                              host='localhost', port=3307, database='db')
cursor = cnx.cursor(buffered=True)

# Define the API endpoint and parameters
api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjMzMjJiZjQwLWZiYjYtNGFjOS1iYzI1LTM3NWQ2MjU5NjVhOCIsImlhdCI6MTcwMDQyNTA4NCwic3ViIjoiZGV2ZWxvcGVyLzU5NmQ3MWE1LWEwOTItZmJjNy03Njc1LThiYjUxN2Q4MTZmMCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NS41OC4xMDAuMjE0Il0sInR5cGUiOiJjbGllbnQifV19.0L2oSwax4ewkqusycn30_xbcnBL4CiR5GAuB3gO6EbRWeWszoBUd1e-L5PRbpE-WbOZgLuOGLtmDAqnN3wM7vQ'
api_url = 'https://api.clashroyale.com/v1/'
clan_tags = ["LCUYQ0GP", "9CPV098R", "28RR9L0Y", "LUV2PUC2", "9GUCJRL0", "QR889RG0", "QVUJPU9Q", "QPY22Q0L", "QYU08YU9", "QYRY02LQ", "Q82P2JCJ", "8L9Y9UP0", "890C9RJV", "8902RQR", "82V9V", "GP9GRQ", "8LUR0C0Y", "8CRR000P", "QC9Y9V", "Q2YU2RCG", "80G9JYP", "GGU8QY", "LLCCRCL0", "8G2YPC", "QLJ9CJUL", "9J2U8GU", "Q0R08YLJ", "P88PGYP", "QYGL80RR", "LJCVV8P0", "2GR2GQRC", "PJ9PGCC9", "9VVPR2R8", "QUR0GLQC", "CP22UC", "G8YL9CLU", "Q8CRCR2P", "PQYR0C2C", "8Y08VVC", "Q82QU2L9", "QCG29C9C", "Q2CU82VC", "LJGG89QY", "GL008G8P", "L28V902R", "PQUC20", "8GQGUJ", "Q28QQG08", "G00G2R29", "889YVPYR", "9JJRCUUY", "YQPGYRLV", "LJP9VPJR", "GU8G9QQQ", "90UUC92Y", "U92J2C", "YLYJ8", "QY9V0QJ0", "8UJ2UUJ8", "LGQCCJU9", "89JQ02Q9", "P90C9YUJ", "9JCLGG9G", "PUVY2PUY", "QPGUGJQY", "QYRY02LQ"]
headers={'Authorization': f'Bearer {api_token}'}
# Loop through the clan tags
for clan_tag in clan_tags:
    clan_url = api_url + "clans/%23" + clan_tag
    clan_response = requests.get(clan_url, headers)
    clan_data = json.loads(clan_response.text)

    # Extract the relevant data from the JSON response for the clan
    name = clan_data['name'] # VARCHAR
    type = clan_data['type'] # ENUM {open, closed, invite only}?
    description = clan_data['description'] # text
    badge_id = clan_data['badgeId'] #int, might remove if the badges are not found in the api
    clan_score = clan_data['clanScore'] # int
    clan_war_trophies = clan_data['clanWarTrophies'] #int
    location = clan_data['location'] # holds id, name, isCountry, and countrycode, maybe do a location table?
    required_trophies = clan_data['requiredTrophies'] # int, can make a query to check all players that are eligible to join, with the minimum of their trophies being this number
    donations_per_week = clan_data['donationsPerWeek']

    members = clan_data['memberList'] # holds players and their respective data relating to the clan (tag, name, role, lastSeen, expLevel, arena{id, name}, donations, donationsReceived)
    # Insert the clan data into the clan table
    add_clan = ("INSERT IGNORE INTO clan "
                "(clan_tag, name, type, description, badge_id, clan_score, clan_war_trophies, location_id, required_trophies, donations_per_week) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    data_clan = (
    clan_tag, name, type, description, badge_id, clan_score, clan_war_trophies, location['id'], required_trophies,
    donations_per_week)
    cursor.execute(add_clan, data_clan)
    #Extract the data for the members
    for member in members:
        player_tag = member['tag']

        player_url = api_url + "players/%23" + player_tag[1:]
        player_response = requests.get(player_url, headers)
        player_data = json.loads(player_response.text)

        name = player_data['name'] #VARCHAR
        exp_level = player_data['expLevel'] #int
        total_exp_points = player_data['totalExpPoints']#int
        trophies = player_data['trophies'] #int
        best_trophies = player_data['bestTrophies'] #int
        wins = player_data['wins'] #int
        losses = player_data['losses']#int
        battle_count = player_data['battleCount']#int
        three_crown_wins = player_data['threeCrownsWins']#int
        challenge_cards_won = player_data['challengeCardsWon']#int
        challenge_max_wins = player_data['challengeMaxWins']#int
        tournament_cards_won = player_data['tournamentCardsWon']#int
        tournament_battle_count = player_data['tournamentBattleCount']#int
        donations = player_data['donations']#int
        donations_received = player_data['donationsReceived']#int
        total_donations = player_data['totalDonations']#int
        war_day_wins = player_data['warDayWins']#int
        clan_cards_collected = player_data['clanCardsCollected']#int
        cards = player_data['cards']#holds level and starLevel of each card
        deck = player_data['currentDeck']#holds card entities
        current_favorite_card = player_data['currentFavoriteCard']#holds favorite card (name, id, maxLevel, maxEvolutionLevel, elixirCost), we could only keep the id of the card with the player, and add FK to cards table






# IGNORE EVERYTHING UNDER THIS LINE



    # Adding actors into person and actor
    for actor in actors:
        add_person = ("INSERT IGNORE INTO person "
                      "(name) "
                      "VALUES (%s)")
        data_person = (actor['node']['name']['nameText']['text'])
        cursor.execute(add_person, (data_person,))

        # Retrieve the person_id (whether inserted or already exists)
        get_person_id = "SELECT person_id FROM person WHERE name = %s"
        cursor.execute(get_person_id, (data_person,))
        result = cursor.fetchone()
        if result:
            person_id = result[0]
        else:
            # Person was just inserted, get the last inserted ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            person_id = cursor.fetchone()[0]
        for character in actor['node']['characters']:
            add_actor = ("INSERT IGNORE INTO actor "
                         "(imdb_id, person_id, character_name) "
                         "VALUES (%s, %s, %s)")

            data_actor = (clan_tag, person_id, character['name'])

            cursor.execute(add_actor, data_actor)

    # Adding creators into creator and person
    for creator in creators:
        if creator['@type'] == 'Person':
            add_person = ("INSERT IGNORE INTO person "
                          "(name) "
                          "VALUES (%s)")
            data_person = (creator['name'])
            cursor.execute(add_person, (data_person,))

            # Retrieve the person_id (whether inserted or already exists)
            get_person_id = "SELECT person_id FROM person WHERE name = %s"
            cursor.execute(get_person_id, (data_person,))
            result = cursor.fetchone()
            if result:
                person_id = result[0]
            else:
                # Person was just inserted, get the last inserted ID
                cursor.execute("SELECT LAST_INSERT_ID()")
                person_id = cursor.fetchone()[0]

            add_creator = ("INSERT IGNORE INTO creator"
                           "(person_id, imdb_id)"
                           "VALUES (%s, %s)")
            data_creator = (person_id, clan_tag)
            cursor.execute(add_creator, data_creator)

    # Adding directors into director and person
    for director in directors:
        if director['@type'] == 'Person':
            add_person = ("INSERT IGNORE INTO person "
                          "(name) "
                          "VALUES (%s)")
            data_person = (director['name'])
            cursor.execute(add_person, (data_person,))

            # Retrieve the person_id (whether inserted or already exists)
            get_person_id = "SELECT person_id FROM person WHERE name = %s"
            cursor.execute(get_person_id, (data_person,))
            result = cursor.fetchone()
            if result:
                person_id = result[0]
            else:
                # Person was just inserted, get the last inserted ID
                cursor.execute("SELECT LAST_INSERT_ID()")
                person_id = cursor.fetchone()[0]

            add_director = ("INSERT IGNORE INTO director"
                            "(person_id, imdb_id)"
                            "VALUES (%s, %s)")
            data_director = (person_id, clan_tag)
            cursor.execute(add_director, data_director)

    # Adding content rating to content_rating
    add_content_rating = ("INSERT IGNORE INTO content_rating"
                          "(content_rating_name)"
                          "VALUES (%s)")
    data_content_rating = (content_rating)
    cursor.execute(add_content_rating, (data_content_rating,))

    # Adding relation of movie id and content rating id
    get_content_rating_id = "SELECT content_rating_id FROM content_rating WHERE content_rating_name = %s"
    cursor.execute(get_content_rating_id, (data_content_rating,))
    result = cursor.fetchone()
    if result:
        content_rating_id = result[0]
    else:
        # Person was just inserted, get the last inserted ID
        cursor.execute("SELECT LAST_INSERT_ID()")
        content_rating_id = cursor.fetchone()[0]

    add_movie_content_rating = ("INSERT INTO movie_content_rating"
                                "(imdb_id, content_rating_id)"
                                "VALUES (%s, %s)")
    data_movie_content_rating = (clan_tag, content_rating_id)
    cursor.execute(add_movie_content_rating, data_movie_content_rating)

    # Adding genre to genre db and relating to movie
    for genre in genres:
        add_genre = ("INSERT IGNORE INTO genre"
                     "(genre)"
                     "VALUES (%s)")
        data_genre = (genre)
        cursor.execute(add_genre, (data_genre,))

        get_genre_id = "SELECT genre_id FROM genre WHERE genre = %s"
        cursor.execute(get_genre_id, (data_genre,))
        result = cursor.fetchone()
        if result:
            genre_id = result[0]
        else:
            # Person was just inserted, get the last inserted ID
            cursor.execute("SELECT LAST_INSERT_ID()")
            genre_id = cursor.fetchone()[0]

        add_movie_genre = ("INSERT INTO movie_genre"
                           "(imdb_id, genre_id)"
                           "VALUES (%s, %s)")
        data_movie_genre = (clan_tag, genre_id)
        cursor.execute(add_movie_genre, data_movie_genre)

    # Relating akas to movie
    akaCounter = 1
    for aka in akas:
        if aka['node']['__typename'] == 'Aka':
            add_aka = ("INSERT INTO movie_aka"
                       "(imdb_id, aka_id, text)"
                       "VALUES (%s, %s, %s)")
            data_aka = (clan_tag, akaCounter, aka['node']['text'])
            cursor.execute(add_aka, data_aka)
            akaCounter += 1

    # Adding keywords to keyword db and relating to movie
    for keyword in keywords:
        add_keyword = ("INSERT IGNORE INTO keyword"
                       "(keyword_text)"
                       "VALUES (%s)")
        data_keyword = (keyword)
        cursor.execute(add_keyword, (data_keyword,))

        get_keyword_id = "SELECT keyword_id FROM keyword WHERE keyword_text = %s"
        cursor.execute(get_keyword_id, (data_keyword,))
        result = cursor.fetchone()
        if result:
            keyword_id = result[0]
        else:
            cursor.execute("SELECT LAST_INSERT_ID()")
            keyword_id = cursor.fetchone()[0]

        add_movie_keyword = ("INSERT INTO movie_keyword"
                             "(imdb_id, keyword_id)"
                             "VALUES (%s, %s)")
        data_movie_keyword = (clan_tag, keyword_id)
        cursor.execute(add_movie_keyword, data_movie_keyword)

    # Adding language to language db and relating to movie
    for language in languages:
        add_language = ("INSERT IGNORE INTO language"
                        "(language_text)"
                        "VALUES (%s)")
        data_language = (language['text'])
        cursor.execute(add_language, (data_language,))

        get_language_id = "SELECT language_id FROM language WHERE language_text = %s"
        cursor.execute(get_language_id, (data_language,))
        result = cursor.fetchone()
        if result:
            language_id = result[0]
        else:
            cursor.execute("SELECT LAST_INSERT_ID()")
            language_id = cursor.fetchone()[0]

        add_movie_language = ("INSERT INTO movie_language"
                              "(imdb_id, language_id)"
                              "VALUES (%s, %s)")
        data_movie_language = (clan_tag, language_id)
        cursor.execute(add_movie_language, data_movie_language)

    # Relating country to movie
    for country in countries:
        add_country = ("INSERT IGNORE INTO movie_country"
                       "(imdb_id, country_iso_code)"
                       "VALUES (%s, %s)")
        data_country = (clan_tag, country['id'])
        cursor.execute(add_country, data_country)

# Commit the changes and close the connection
cnx.commit()
cursor.close()
cnx.close()
end = time.time()
print(end - start)