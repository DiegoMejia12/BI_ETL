import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import psycopg2
import datetime

# Press the green button in the gutter to run the script.


client_id = '371971522439457f83f82326d20c4876'
client_secret = '2bd8ddfa6e504c6d8bb4ef2439d16868'

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
        "INSERT INTO artists (nombre_artista, id_artista, tipo, uri, popularidad, cantidad_followers, origin ,"
        "fecha_consulta) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id_artista) DO NOTHING",
        (info_artist))

    connection.commit()


def insertdB_track(info_track, cursor, connection):

    cursor.execute(
        "INSERT INTO tracks (nombre_track, tipo_track, album, track_number, id_track, nombre_artista, id_artista, "
        "fecha_lanzamiento, generos, "
        "uri, origin ,fecha_consulta) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id_track) DO NOTHING",
        (info_track))

    connection.commit()


def search_artist(artist, cursor, conecction):
    artist_search = sp.search(q='artist:'+artist, type='artist')
    artist_info = artist_search['artists']['items'][0]
    artist_id = artist_info['id']

    info_artist = artist_info['name'], artist_info['id'], artist_info['type'], artist_info['uri'], artist_info['popularity'], int(
        artist_info['followers']['total']), artist_info['href'], datetime.datetime.now()

    insertdB_artist(info_artist, cursor, conecction)

    albums_search = sp.artist_albums(artist_id)
    albums_info = albums_search['items']

    for album in albums_info:
        album_id = album['id']

        tracks_search = sp.album_tracks(album_id)
        tracks_info = tracks_search['items']

        for track in tracks_info:
            info = track['name'], track['type'], album['name'], track['track_number'], track['id'], artist_info['name'], artist_info['id'], album[
                'release_date'], artist_info['genres'], track['uri'], track['href'], datetime.datetime.now()
            insertdB_track(info, cursor, conecction)


print("Conectando a Base de Datos")

cursor, connection = conection_bd("postgres", "12345", "localhost", "2020", "Spotify")

print("Cargando Metalica")

search_artist('Metalica', cursor=cursor, conecction=connection)

print("Cargando Black Sabbath")

search_artist('Black Sabbath', cursor=cursor, conecction=connection)

print("Cargando Led Zeppelin")

search_artist('Led Zeppelin', cursor=cursor, conecction=connection)

print("Cargando Grupo Niche")

search_artist('Grupo Niche', cursor=cursor, conecction=connection)

print("Cargando Bod Dylan")

search_artist('Bod Dylan', cursor=cursor, conecction=connection)

print("Cargando Michael Jackson")

search_artist('Michael Jackson', cursor=cursor, conecction=connection)

print("Cargando Eminem")

search_artist('Eminem', cursor=cursor, conecction=connection)

print("Cargando Red Hot Chili Peppers")

search_artist('Red Hot Chili Peppers', cursor=cursor, conecction=connection)

print("Completado")

close_conection_db(cursor, connection)
