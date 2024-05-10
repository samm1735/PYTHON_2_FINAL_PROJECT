from FilmServices import FilmServices


_film_services = FilmServices()
_films_list = _film_services.popular_films

for _film in _films_list:
    print(_film.get_title())
    print(_film.get_movie_genres())

# print(len(_films_list))
