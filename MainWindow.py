import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage

from FilmDetailsWindow import FilmDetailsWindow

from DatabaseService import DatabaseService
from FilmServices import FilmServices
from IsInternetConnected import is_online  # Pour tester si l'utilisateur est online ou pas

from PIL import Image, ImageTk

# WThe following lines should be removed they're here for testing purposes

import requests
from io import BytesIO

color_primary = "#cccccc"


class MainWindow:
    def __init__(self, root, database_service: DatabaseService, film_services: FilmServices):
        self.root = root
        self.root.title("Popular Movies Today")

        self._database_service = database_service
        self._film_services = film_services

        self.photo_images = []
        #  ----------------

        self.root.resizable(width=False, height=False)
        self.root.state("zoomed")

        #  ----------------

        self.main_frame = tk.Frame(self.root, bg=color_primary)
        self.main_frame.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.frame_title = ttk.Label(self.main_frame, text="Popular Movies Today", font=("Helvetica", 24, "bold"),
                                     background=color_primary)
        self.frame_title.grid(row=0, column=1, sticky="ew", pady=10)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=1)

        #  ----------------

        self.film_posters = []

        #  ----------------

        self.image1 = Image.open("image_1.jpg").resize((50, 50))
        self.photo1 = ImageTk.PhotoImage(self.image1)

        # a_response = requests.get("http://localhost:3000/image")  # Testing with a local api endpoint that returns an image
        # image_data = BytesIO(a_response.content)
        #
        # self.image2 = Image.open(image_data).resize((50, 50))
        # self.photo2 = ImageTk.PhotoImage(self.image2)

        # the_url = "http://localhost:3000/image"
        # self.photo2 = self._film_services.get_image_from_url(the_url)

        #  ----------------

        self.style = ttk.Style()
        self.style.configure(
            "Custom.Treeview",
            rowheight=120
        )

        #  ----------------

        self.tree_view = ttk.Treeview(self.main_frame, style="Custom.Treeview")
        self.tree_view.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

        self.tree_view.config(columns=["MOVIE_ID", "IMAGE", "TITRE", "DATE DE SORTIE"])

        for col in self.tree_view["columns"]:
            self.tree_view.column(column=col, anchor=tk.W, width=120, minwidth=80)
            self.tree_view.heading(col, text=col, anchor=tk.W)

        # self.tree_view.column("ID", width=50, minwidth=50)
        # self.tree_view.column("Age", width=50, minwidth=50)
        self.tree_view.column("#0", width=200, minwidth=200, stretch=tk.NO)
        # La colonne movie_id stocke l'id du film pour la navigation vers l'autre fenêtre
        self.tree_view.column("MOVIE_ID", width=0, minwidth=0, stretch=tk.NO)  # On a pas besoin de l'afficher
        self.tree_view.column("IMAGE", width=0, minwidth=0, stretch=tk.NO)
        self.tree_view.column("TITRE", width=400, minwidth=350, stretch=tk.NO)
        self.tree_view.column("DATE DE SORTIE", width=100, minwidth=80, stretch=tk.NO)

        self.tree_view.bind('<Double-1>', self.on_treeview_double_click)

        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        if not is_online():
            self.network_status = ttk.Label(self.main_frame, text="Offline", foreground="red",
                                            font=("Helvetica", 20),
                                            background=color_primary
                                            )
            self.network_status.grid(row=1, column=0, sticky="w")

            # Get data from db

            self.populate_tree_view_if_offline()

        else:
            self.network_status = ttk.Label(self.main_frame, text="Online", foreground="green",
                                            font=("Helvetica", 20)
                                            )
            self.network_status.grid(row=1, column=0, sticky="w")

            # Get data from internet

            self.populate_tree_view_if_online()

    def populate_tree_view_if_offline(self):  # If user is offline
        self.clean_tree_view()
        for film in self._database_service.read_films():
            # poster_image = PhotoImage(file=film.get_poster_path())
            # Si offline, pas d'image ou image generique
            # Testing

            # self.tree_view.insert("", tk.END, image=photo1, values=(
            #     film.get_movie_id(), poster_image, film.get_title(), film.get_release_date()))
            #
            # self.tree_view.image_list = [poster_image, photo1]
            #

            movie_poster = Image.open("movie_placeholder_1.png").resize((100, 100))
            movie_poster = ImageTk.PhotoImage(movie_poster)

            self.film_posters.append(movie_poster)

            self.tree_view.insert("", tk.END,  image=movie_poster, values=(
                film.get_movie_id(), film.get_poster_path(), film.get_title(), film.get_release_date()))
        self.tree_view.image_list = self.film_posters

    def populate_tree_view_if_online(self):  # If user is offline
        self.clean_tree_view()

        for film in self._film_services.get_movie_details():
            self._database_service.insert_film(film=film)

            # Testing
            image1 = Image.open("image_1.jpg").resize((50, 50))
            photo1 = ImageTk.PhotoImage(image1)

            self.film_posters.append(photo1)

            photo2 = self._film_services.get_image_from_url(film.get_poster_path(), size=100)

            self.film_posters.append(photo2)

            self.tree_view.insert("", tk.END, image=photo2, values=(
                film.get_movie_id(), film.get_poster_path(), film.get_title(), film.get_release_date()))

            self.tree_view.image_list = self.film_posters

    def clean_tree_view(self):
        for record in self.tree_view.get_children():
            self.tree_view.delete(record)

    def on_treeview_double_click(self, event):
        # item_id = self.tree.identify('item', event.x, event.y)

        # if item_id:
        #     # Destroy the main window and open the detail window
        #     self.destroy()
        #     # DetailWindow(item_id=item_id)

        selected_item = self.tree_view.selection()[0]

        item_values = self.tree_view.item(selected_item, "values")

        movie_id = item_values[0]

        try:
            # Naviguer vers la nouvelle fenêtre
            self.root.withdraw()
            # FilmDetailsWindow()
            _film_details_window = tk.Toplevel(self.root)
            app = FilmDetailsWindow(movie_id=movie_id,
                                    database_service=self._database_service,
                                    film_services=self._film_services,
                                    root=_film_details_window,
                                    main_window_root=self.root
                                    )
        except Exception:
            messagebox.showerror("ERREUR", f"UNE ERREUR S'EST PRODUITE")

        # messagebox.showinfo("Success", f"FILM avec l'ID #{movie_id} selected")
