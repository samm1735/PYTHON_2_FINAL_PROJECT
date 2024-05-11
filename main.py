import tkinter

# Nom : ISAAC
# Prénom : Sammuel Ramclief
# Cours : PYTHON II
# DEVOIR FINAL
# Informations utiles : Plusieurs classes ont été définies pour faciliter ce travail

from DatabaseService import DatabaseService  # Pour les requêtes sql
from FilmServices import FilmServices  # Pour prendre les données depuis l'API
from MainWindow import MainWindow  # Pour la fenêtre principale

_film_services = FilmServices()
_database_service = DatabaseService()

root = tkinter.Tk()

app = MainWindow(root=root, database_service=_database_service, film_services=_film_services)

# app = MainWindow(root=root, database_service=database_service)

root.mainloop()

#
# for _film in _films_list:
#     print(_film.get_title())
#     print(_film.get_movie_genres())
#     print(_film.get_description())
#
#     print("Adding to DB")
#     _database_service.insert_film(_film)
#     print("Added to DB")
#     # break


# for _film in _films_from_db:
#     print(_film.get_title())
#     print(_film.get_movie_genres())
#     print(_film.get_description())

# print(len(_films_list))
