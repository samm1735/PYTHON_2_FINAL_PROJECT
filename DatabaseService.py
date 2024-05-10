# Cette classe a été créée pour rendre le code plus facile à maintenir
import json
import sqlite3


from Cast import Cast
from Constants import Constants
from Film import Film


class DatabaseService:
    def __init__(self):
        self.conn = sqlite3.connect(Constants.DB_NAME)
        self.cursor = self.conn.cursor()

        self.table_name = Film.__name__  # Cette variable sera utilisée pour le nom de la table
        self.create_table_if_not_exists()  # Crée la table dès l'initialisation

    def create_table_if_not_exists(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            movie_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            poster_path TEXT,
            backdrop_path TEXT,
            release_date TEXT,
            movie_cast TEXT,
            movie_genres TEXT
        )""")

    def insert_film(self, film: Film):
        self.cursor.execute(f"""
                INSERT INTO {self.table_name} 
                (movie_id, title, description, poster_path, backdrop_path, release_date, movie_genres, movie_cast)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (film.get_movie_id(), film.get_title(), film.get_description(),
              film.get_poster_path(), film.get_backdrop_path(), film.get_release_date(),
              json.dumps(film.get_movie_genres())),
              json.dumps([cast.__dict__ for cast in film.get_movie_cast()])
                            )
        self.commit()

    def read_films(self):
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        films_data = self.cursor.fetchall()
        films = []
        for film_data in films_data:
            film = self._parse_film_data(film_data)
            films.append(film)
        return films

    def read_film_by_id(self, film_id):
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE movie_id = ?", (film_id,))
        film_data = self.cursor.fetchone()
        if film_data:
            return self._parse_film_data(film_data)
        return None

    @staticmethod
    def _parse_film_data(self, film_data):
        # Assuming the schema matches the Film class attributes
        movie_id, title, description, poster_path, backdrop_path, release_date, movie_cast_json, movie_genres_json = film_data
        movie_cast = [Cast(**cast_data) for cast_data in json.loads(movie_cast_json)]
        movie_genres = json.loads(movie_genres_json)
        return Film(movie_id, title, description, poster_path, backdrop_path, release_date, movie_genres, movie_cast)

    def commit(self):
        self.conn.commit()
