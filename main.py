import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import psycopg2
import datetime

# Press the green button in the gutter to run the script.


client_id = ''
client_secret = ''

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def conection_bd(user, password, host, port, database):
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


def insertdB_artist(info_artist, cursor, connection):
    cursor.execute(
        "INSERT INTO artist (nombre_artista, tipo, uri, popularidad, cantidad_followers, origin ,fecha_consulta) "
        "values (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (uri) DO NOTHING",
        (info_artist, datetime.datetime.now()))

    connection.commit()


def insertdB_track(info_track, cursor, connection):
    cursor.execute(
        "INSERT INTO tracks (nombre_track, tipo_track, album, track_number, id_track, fecha_lanzamiento, generos, "
        "uri, origin ,fecha_consulta) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (uri) DO NOTHING",
        (info_track, datetime.datetime.now()))

    connection.commit()


def search_artist(artist, cursor, conecction):
    artist_search = sp.search(artist, 'artist')
    artist_info = artist_search['artists']['items'][0]
    artist_id = artist_info['id']

    info_artist = artist_info['name'], artist_info['type'], artist_info['uri'], artist_info['popularity'], int(
        artist_info['followers']['total']), artist_info['href']

    insertdB_artist(info_artist, cursor, conecction)

    albums_search = sp.artist_albums(artist_id)
    albums_info = albums_search['items']

    for album in albums_info:
        album_id = album['id']

        tracks_search = sp.album_tracks(artist_id)
        tracks_info = tracks_search['items']

        for track in tracks_info:
            info = track['name'], track['type'], album['name'], track['track_number'], track['id'], album[
                'release_date'], artist_info['genres'], track['uri'], track['href']
            insertdB_track(info, cursor, conecction)

cursor, connection = conection_bd("postgres", "12345", "localhost", "2020", "Spotify")

search_artist('Metalica', cursor=cursor, conecction=connection)

search_artist('Black Sabbath', cursor=cursor, conecction=connection)

search_artist('Led Zeppelin', cursor=cursor, conecction=connection)

search_artist('Grupo Niche', cursor=cursor, conecction=connection)

search_artist('Bod Dylan', cursor=cursor, conecction=connection)

search_artist('Michael Jackson', cursor=cursor, conecction=connection)

close_conection_db(cursor, connection)
