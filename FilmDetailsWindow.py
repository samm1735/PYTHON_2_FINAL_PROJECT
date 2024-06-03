import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage

from Cast import Cast
from DatabaseService import DatabaseService
from FilmServices import FilmServices
from IsInternetConnected import is_online

color_primary = "#cccccc"


class FilmDetailsWindow:
    def __init__(self, movie_id: int, database_service: DatabaseService, film_services: FilmServices, root,
                 main_window_root):
        self.root = root

        self.main_window_root = main_window_root

        self.root.title("Popular Movies Today")

        self._database_service = database_service
        self._film_services = film_services
        self.selected_movie_id = movie_id
        #  ----------------

        self.root.resizable(width=False, height=False)
        self.root.state("zoomed")

        #  ----------------

        #  ----------------

        self.main_frame = tk.Frame(self.root, bg=color_primary)
        self.main_frame.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.frame_title = ttk.Label(self.main_frame, text="Popular Movies Today", font=("Helvetica", 24, "bold"),
                                     background=color_primary)
        self.frame_title.grid(row=0, column=1, sticky="ew", pady=10)

        #  ----------------

        #  ----------------

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=1)

        #  ----------------
        #       MOVIE INFORMATIONS
        #  ----------------

        self.movie_title = ttk.Label(self.main_frame, text="...", font=("Helvetica", 35, "bold"))
        self.movie_title.grid(row=2, column=1, sticky="ew", pady=1)

        self.movie_release_date = ttk.Label(self.main_frame, text="...", font=("Helvetica", 12, "italic"))
        self.movie_release_date.grid(row=3, column=3, sticky="ew", pady=1, padx=(0, 20))

        self.movie_description = ttk.Label(self.main_frame, text="...", font=("Helvetica", 12, "normal"),
                                           wraplength=500)
        self.movie_description.grid(row=4, column=1, sticky="ew", pady=20)

        #  ----------------
        #  ----------------

        self.movie_cast_tree_view = ttk.Treeview(self.main_frame)
        self.movie_cast_tree_view.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

        self.movie_cast_tree_view.config(columns=["MOVIE_ID", "ORIGINAL_NAME", "CHARACTER"])

        for col in self.movie_cast_tree_view["columns"]:
            self.movie_cast_tree_view.column(column=col, anchor=tk.W, width=120, minwidth=80)
            self.movie_cast_tree_view.heading(col, text=col, anchor=tk.W)

        self.movie_cast_tree_view.column("#0", width=0, minwidth=0, stretch=tk.NO)
        # La colonne movie_id stocke l'id du film pour la navigation vers l'autre fenêtre
        self.movie_cast_tree_view.column("MOVIE_ID", width=0, minwidth=0, stretch=tk.NO)  # On a pas besoin de l'afficher
        self.movie_cast_tree_view.column("ORIGINAL_NAME", width=500, minwidth=500, stretch=tk.NO)
        self.movie_cast_tree_view.column("CHARACTER", width=400, minwidth=350, stretch=tk.NO)

        # self.populate_movie_cast_tree_view()

        #  ----------------
        #  ----------------

        self.style = ttk.Style()
        self.style.configure(
            "Custom.TButton",
            foreground="black",
            background=color_primary,
            font=("Helvetica", 14, "bold"),
            width=20
        )
        self.get_back_button = ttk.Button(self.main_frame, text="Go Back", style="Custom.TButton",
                                          command=self.go_back_home)
        self.get_back_button.grid(row=0, column=0, padx=10, pady=10)

        #  ----------------

        # Online ou offline, on prend les donnees de la db
        self.populate_window()

        if not is_online():
            self.network_status = ttk.Label(self.main_frame, text="Offline", foreground="red",
                                            font=("Helvetica", 20),
                                            background=color_primary
                                            )
            self.network_status.grid(row=1, column=0, sticky="w")

        else:
            self.network_status = ttk.Label(self.main_frame, text="Online", foreground="green",
                                            font=("Helvetica", 20)
                                            )
            self.network_status.grid(row=1, column=0, sticky="w")

    def go_back_home(self):
        self.root.destroy()
        self.main_window_root.deiconify()
        self.main_window_root.state("zoomed")

    def populate_window(self):  # If user is offline
        # self.clean_window()
        the_film = self._database_service.read_film_by_id(self.selected_movie_id)

        self.movie_title.config(text=the_film.get_title(), background=color_primary)
        self.movie_description.config(text=the_film.get_description())

        genres = " | ".join(the_film.get_movie_genres())

        self.movie_release_date.config(text=f" {the_film.get_release_date()} \t {genres} ")

        self.populate_movie_cast_tree_view(the_film.get_movie_cast())

    def populate_movie_cast_tree_view(self, movie_cast_list: list[Cast]):  # If user is offline
        self.clean_tree_view()
        for individual_cast in movie_cast_list:
            self.movie_cast_tree_view.insert(
                "",
                tk.END,
                values=(
                    self.selected_movie_id,
                    individual_cast.individual_cast_original_name,
                    individual_cast.individual_cast_character
                )
            )

    def clean_window(self):
        self.movie_title.config(text="")
        self.movie_description.config(text="")
        self.movie_release_date.config(text="")

    def clean_tree_view(self):
        for record in self.movie_cast_tree_view.get_children():
            self.movie_cast_tree_view.delete(record)
