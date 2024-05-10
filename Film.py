from Cast import Cast


class Film:
    def __init__(self, movie_id: int, title: str, description: str, poster_path: str, backdrop_path: str, release_date: str, movie_genres: list, movie_cast: list[Cast]):
        self.__movie_id = movie_id
        self.__title = title
        self.__description = description
        self.__poster_path = poster_path
        self.__backdrop_path = backdrop_path
        self.__release_date = release_date
        self.__movie_genres = movie_genres
        self.__movie_cast = movie_cast

#     Nous n'allons pas modifier les films, pas besoin de setters

    def get_movie_id(self):
        return self.__movie_id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_poster_path(self):
        return self.__poster_path

    def get_backdrop_path(self):
        return self.__backdrop_path

    def get_release_date(self):
        return self.__release_date

    def get_movie_genres(self):
        return self.__movie_genres

    def get_movie_cast(self):
        return self.__movie_cast
