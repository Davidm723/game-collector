from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Console, Game, Genre
from .forms import GameSearchForm
from .services.rawg import search_games, import_game


# Create your views here.
def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


class ConsoleListView(ListView):
    model = Console
    template_name = "games/console_list.html"
    context_object_name = "consoles"

    def get_queryset(self):
        return Console.objects.filter(games__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        console_images = {
            "3DO": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/3DO-FZ1-Console-Set.jpg/500px-3DO-FZ1-Console-Set.jpg",
            "3DS": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Nintendo-3DS-AquaOpen.png/500px-Nintendo-3DS-AquaOpen.png",
            "Android": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Android_robot_%282014-2019%29.svg/250px-Android_robot_%282014-2019%29.svg.png",
            "Atari 2600": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Atari-2600-Wood-4Sw-Set.png/500px-Atari-2600-Wood-4Sw-Set.png",
            "Game Boy": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Game-Boy-FL.png/500px-Game-Boy-FL.png",
            "Genesis": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Sega-Genesis-Mk2-6button.jpg/500px-Sega-Genesis-Mk2-6button.jpg",
            "NES": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/NES-Console-Set.png/500px-NES-Console-Set.png",
            "PC": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/IBM_PC-IMG_7271_%28transparent%29.png/500px-IBM_PC-IMG_7271_%28transparent%29.png",
            "PlayStation 5": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Black_and_white_Playstation_5_base_edition_with_controller.png/330px-Black_and_white_Playstation_5_base_edition_with_controller.png",
            "SEGA Master System": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Sega-Master-System-Set.jpg/500px-Sega-Master-System-Set.jpg",
        }

        for console in context["consoles"]:
            console.display_image = console_images.get(
                console.name, "placeholder" + console.name.replace(" ", "+")
            )

        return context


class ConsoleDetailView(DetailView):
    model = Console
    template_name = "games/console_detail.html"
    context_object_name = "console"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = Game.objects.filter(console=self.object)
        console_images = {
            "3DO": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/3DO-FZ1-Console-Set.jpg/500px-3DO-FZ1-Console-Set.jpg",
            "3DS": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Nintendo-3DS-AquaOpen.png/500px-Nintendo-3DS-AquaOpen.png",
            "Android": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Android_robot_%282014-2019%29.svg/250px-Android_robot_%282014-2019%29.svg.png",
            "Atari 2600": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Atari-2600-Wood-4Sw-Set.png/500px-Atari-2600-Wood-4Sw-Set.png",
            "Game Boy": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Game-Boy-FL.png/500px-Game-Boy-FL.png",
            "Genesis": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Sega-Genesis-Mk2-6button.jpg/500px-Sega-Genesis-Mk2-6button.jpg",
            "NES": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/NES-Console-Set.png/500px-NES-Console-Set.png",
            "PC": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/IBM_PC-IMG_7271_%28transparent%29.png/500px-IBM_PC-IMG_7271_%28transparent%29.png",
            "PlayStation 5": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Black_and_white_Playstation_5_base_edition_with_controller.png/330px-Black_and_white_Playstation_5_base_edition_with_controller.png",
            "SEGA Master System": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Sega-Master-System-Set.jpg/500px-Sega-Master-System-Set.jpg",
        }

        self.object.display_image = console_images.get(
            self.object.name, "https://placehold.co/600x400?text=No+Image"
        )

        return context


class GameDetailView(DetailView):
    model = Game
    template_name = "games/game_detail.html"
    context_object_name = "game"


class GameSearchView(View):
    template_name = "games/game_search.html"

    def get(self, request):
        form = GameSearchForm()
        return render(request, self.template_name, {"form": form, "games": []})

    def post(self, request):
        form = GameSearchForm(request.POST)
        games = []

        if form.is_valid():
            query = form.cleaned_data["query"]
            rawg_results = search_games(query)

            for game in rawg_results:
                platforms = [p["platform"]["name"] for p in game.get("platforms", [])]
                if platforms:
                    games.append(
                        {
                            "id": game["id"],
                            "name": game["name"],
                            "image": game.get("background_image", ""),
                            "platforms": platforms,
                        }
                    )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "games": games,
            },
        )


class GameImportView(View):
    def post(self, request):
        from .services.rawg import import_game

        game_ids = request.POST.getlist("game_ids")
        console_names = request.POST.getlist("console_name")

        for rawg_id, console_name in zip(game_ids, console_names):
            console, _ = Console.objects.get_or_create(name=console_name)
            import_game(rawg_id=rawg_id, console=console)

        return redirect("console-list")


class GenreListView(ListView):
    model = Genre
    template_name = "games/genre_list.html"


class GenreDetailView(DetailView):
    model = Genre
    template_name = "games/genre_detail.html"
