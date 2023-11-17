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
url = 'https://search.imdbot.workers.dev/?tt='
imdb_ids = ['tt0111161', 'tt0068646', 'tt0468569', 'tt0208092', 'tt0050083',
            'tt0108052', 'tt0167260', 'tt0110912', 'tt0060196', 'tt0137523',
            'tt0120737', 'tt0109830', 'tt1375666', 'tt0167261', 'tt0080684',
            'tt0133093', 'tt0099685', 'tt0073486', 'tt0047478', 'tt0114369',
            'tt0317248', 'tt0114814', 'tt0102926', 'tt0038650', 'tt0110413',
            'tt0120689', 'tt0816692', 'tt0246578', 'tt0120586', 'tt0054215',
            'tt0021749', 'tt0027977', 'tt0076759', 'tt0120915', 'tt0034583',
            'tt0064116', 'tt0032553', 'tt0078788', 'tt0082971', 'tt0047396',
            'tt0986264', 'tt0209144', 'tt0078748', 'tt0033467', 'tt0043014',
            'tt4154796', 'tt4633694', 'tt0090605', 'tt1187043', 'tt0435761',
            'tt1194238', 'tt6644200']

# Loop through the IMDb IDs and retrieve the data
for imdb_id in imdb_ids:
    response = requests.get(url + imdb_id)
    data = json.loads(response.text)

    # Extract the relevant data from the JSON response
    title = data['short']['name']
    print(title + ' ' + imdb_id)

    release_year = data['top']['releaseYear']['year']
    rating = data['short']['aggregateRating']['ratingValue']
    description = data['short']['description']
    runtime = data['short']['duration']
    content_rating = data['short']['contentRating']
    directors = data['short']['director']
    actors = data['main']['cast']['edges']
    creators = data['short']['creator']
    number_of_reviews = data['short']['aggregateRating']['ratingCount']
    genres = data['short']['genre']
    akas = data['main']['akas']['edges']
    keywords = data['short']['keywords'].split(',')
    languages = data['main']['spokenLanguages']['spokenLanguages']
    countries = data['top']['countriesOfOrigin']['countries']

    # Insert the data into the database
    add_movie = ("INSERT IGNORE INTO movie "
                 "(imdb_id, title, description, rating, runtime, release_year, number_of_reviews) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    data_movie = (imdb_id, title, description, rating, runtime, release_year, number_of_reviews)
    cursor.execute(add_movie, data_movie)

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

            data_actor = (imdb_id, person_id, character['name'])

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
            data_creator = (person_id, imdb_id)
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
            data_director = (person_id, imdb_id)
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
    data_movie_content_rating = (imdb_id, content_rating_id)
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
        data_movie_genre = (imdb_id, genre_id)
        cursor.execute(add_movie_genre, data_movie_genre)

    # Relating akas to movie
    akaCounter = 1
    for aka in akas:
        if aka['node']['__typename'] == 'Aka':
            add_aka = ("INSERT INTO movie_aka"
                       "(imdb_id, aka_id, text)"
                       "VALUES (%s, %s, %s)")
            data_aka = (imdb_id, akaCounter, aka['node']['text'])
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
        data_movie_keyword = (imdb_id, keyword_id)
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
        data_movie_language = (imdb_id, language_id)
        cursor.execute(add_movie_language, data_movie_language)

    # Relating country to movie
    for country in countries:
        add_country = ("INSERT IGNORE INTO movie_country"
                       "(imdb_id, country_iso_code)"
                       "VALUES (%s, %s)")
        data_country = (imdb_id, country['id'])
        cursor.execute(add_country, data_country)

# Commit the changes and close the connection
cnx.commit()
cursor.close()
cnx.close()
end = time.time()
print(end - start)