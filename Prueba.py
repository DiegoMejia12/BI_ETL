import json
import psycopg2
import datetime


def conectarBD(user, password, host, port, database):
    try:

        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        return cursor, connection
    except(Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def close_conection_db(cursor, connection):
    cursor.close()
    connection.close()


def abrir_json(ruta):
    with open(ruta) as f:
        file = f.read().lower()
        return json.loads(file)


def insertdB_artist(json, cursor, connection):
    cursor.execute(
        "INSERT INTO artist (nombre_artista, tipo, uri, popularidad, cantidad_followers, origin ,fecha_consulta) "
        "values (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (uri) DO NOTHING",
        (json['name'], json['type'], json['uri'], json['popularity'], int(json['followers']['total']), json['href'],
         datetime.datetime.now()))

    connection.commit()


cursor, connection = conectarBD("postgres", "12345", "localhost", "2020", "Spotify")

black_sabbath = abrir_json('src/black_sabbath_artist.json')
grupo_niche = abrir_json('src/grupo_niche_artist.json')

insertdB_artist(black_sabbath, cursor=cursor, connection=connection)
insertdB_artist(grupo_niche, cursor=cursor, connection=connection)

close_conection_db(cursor, connection)

