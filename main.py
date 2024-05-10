from DatabaseService import DatabaseService
from FilmServices import FilmServices


_film_services = FilmServices()
_films_list = _film_services.popular_films
_database_service = DatabaseService()

for _film in _films_list:
    print(_film.get_title())
    print(_film.get_movie_genres())
    print(_film.get_description())

    print("Adding to DB")
    _database_service.insert_film(_film)
    print("Added to DB")
    # break

# print(len(_films_list))
