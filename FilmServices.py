import requests
import json

from io import BytesIO

from urllib.request import urlopen

from Cast import Cast
from Constants import Constants
from Film import Film

from PIL import Image, ImageTk


class FilmServices:
    def __init__(self):
        # self.popular_movies_response = self.get_popular_movies_response()
        self.popular_movies_data = None
        self.movie_details_data = None
        self.movie_credits_data = None

        self.popular_films: list[Film] = []  # À stocker dans une variable pour avoir la liste des films
        # self.get_movie_details()

    @staticmethod
    def get_image_from_url(url: str):
        response = requests.get(url)

        image_data = BytesIO(response.content)
        return ImageTk.PhotoImage(Image.open(image_data).resize((100,100)))

        # return Image.open(BytesIO(image_data))

    @staticmethod
    def get_image_from_url_2(url: str):
        u = urlopen(url)
        raw_data = u.read()
        u.close()
        return raw_data

    @staticmethod
    def get_popular_movies_response():
        return requests.get(Constants.tmdb_api_popular_movies_url, headers=Constants.headers)

    @staticmethod
    def get_movie_details_url(movie_id):
        return f"{Constants.tmdb_api_base_url}{movie_id}?language=en-US"

    @staticmethod
    def get_movie_details_response(movie_details_url):
        return requests.get(movie_details_url, headers=Constants.headers)

    @staticmethod
    def get_movie_credits_url(movie_id):
        return f"{Constants.tmdb_api_base_url}{movie_id}/credits?language=en-US"

    @staticmethod
    def get_movie_credits_response(movie_credits_url):
        return requests.get(movie_credits_url, headers=Constants.headers)

    def get_movie_details(self):
        self.popular_movies_data = json.loads(self.get_popular_movies_response().text)

        movies = self.popular_movies_data["results"]

        for movie in movies:
            movie_id = int(movie["id"])
            movie_title = movie["title"]
            movie_description = movie["overview"]
            movie_poster_path = Constants.tmdb_original_files_link + movie["poster_path"]
            movie_backdrop_path = movie["backdrop_path"]
            movie_backdrop_path = f"{Constants.tmdb_original_files_link}{movie_backdrop_path}"
            movie_release_date = movie["release_date"]

            # Movie details - Pour les genres, car le premier response a l'id des genres
            #                                                           pas les strings correspondants
            movie_details_url = self.get_movie_details_url(movie_id)
            movie_details_response = self.get_movie_details_response(movie_details_url)

            self.movie_details_data = json.loads(movie_details_response.text)

            movie_genres = self.movie_details_data["genres"]

            movie_genres_list = []

            for movie_genre in movie_genres:
                movie_genres_list.append(movie_genre["name"])

            # Movie credits
            movie_credits_url = self.get_movie_credits_url(movie_id)
            movie_credits_response = self.get_movie_credits_response(movie_credits_url)

            self.movie_credits_data = json.loads(movie_credits_response.text)

            movie_credits = self.movie_credits_data["cast"]

            movie_cast_list: list[Cast] = []

            for movie_credit in movie_credits:
                movie_cast = Cast(
                    individual_cast_original_name=movie_credit["original_name"],
                    individual_cast_character=movie_credit["character"]
                )
                movie_cast_list.append(movie_cast)

            self.popular_films.append(
                Film(
                    movie_id=movie_id,
                    title=movie_title,
                    description=movie_description,
                    poster_path=movie_poster_path,
                    backdrop_path=movie_backdrop_path,
                    release_date=movie_release_date,
                    movie_genres=movie_genres_list[:],
                    movie_cast=movie_cast_list[:]
                )
            )

        return self.popular_films
