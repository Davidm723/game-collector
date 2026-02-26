from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Console, Game, Genre
from .forms import GameSearchForm
from .services.rawg import search_games, import_game


# Create your views here.
class Home(LoginView):
    template_name = "home.html"


def about(request):
    return render(request, "about.html")


class ConsoleListView(LoginRequiredMixin, ListView):
    model = Console
    template_name = "games/console_list.html"
    context_object_name = "consoles"

    def get_queryset(self):
        return Console.objects.filter(games__user=self.request.user).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        console_images = {
            "3DO": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/3DO-FZ1-Console-Set.jpg/500px-3DO-FZ1-Console-Set.jpg",
            "Nintendo 3DS": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Nintendo-3DS-AquaOpen.png/500px-Nintendo-3DS-AquaOpen.png",
            "Android": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Android_robot_%282014-2019%29.svg/250px-Android_robot_%282014-2019%29.svg.png",
            "Atari 2600": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Atari-2600-Wood-4Sw-Set.png/500px-Atari-2600-Wood-4Sw-Set.png",
            "Dreamcast": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Dreamcast-Console-Set.png/500px-Dreamcast-Console-Set.png",
            "Nintendo DS": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Nintendo-DS-Fat-Blue.png/330px-Nintendo-DS-Fat-Blue.png",
            "Game Boy": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Game-Boy-FL.png/500px-Game-Boy-FL.png",
            "Game Boy Advance": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Nintendo-Game-Boy-Advance-Purple-FL.png/500px-Nintendo-Game-Boy-Advance-Purple-FL.png",
            "Game Boy Color": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Nintendo_Game_Boy_Color.png/500px-Nintendo_Game_Boy_Color.png",
            "GameCube": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/GameCube-Console-Set.png/500px-GameCube-Console-Set.png",
            "Game Gear": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Sega-Game-Gear-WB.png/500px-Sega-Game-Gear-WB.png",
            "Genesis": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Sega-Genesis-Mk2-6button.jpg/500px-Sega-Genesis-Mk2-6button.jpg",
            "iOS": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/250px-Apple_logo_black.svg.png",
            "Jaguar": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Atari-Jaguar-Console-Set.png/500px-Atari-Jaguar-Console-Set.png",
            "Neo Geo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Neo-Geo-AES-Console-Set.png/500px-Neo-Geo-AES-Console-Set.png",
            "NES": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/NES-Console-Set.png/500px-NES-Console-Set.png",
            "Nintendo 64": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/N64-Console-Set.png/500px-N64-Console-Set.png",
            "Nintendo Switch": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Nintendo-Switch-wJoyCons-BlRd-Standing-FL.jpg/960px-Nintendo-Switch-wJoyCons-BlRd-Standing-FL.jpg",
            "PC": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/IBM_PC-IMG_7271_%28transparent%29.png/500px-IBM_PC-IMG_7271_%28transparent%29.png",
            "PlayStation": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/PlayStation-SCPH-1000-with-Controller.png/500px-PlayStation-SCPH-1000-with-Controller.png",
            "PlayStation 2": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/PS2-Versions.png/500px-PS2-Versions.png",
            "PlayStation 3": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/PS3-Fat-Console-Vert.jpg/330px-PS3-Fat-Console-Vert.jpg",
            "PlayStation 4": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/PS4-Console-wDS4.jpg/500px-PS4-Console-wDS4.jpg",
            "PlayStation 5": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Black_and_white_Playstation_5_base_edition_with_controller.png/330px-Black_and_white_Playstation_5_base_edition_with_controller.png",
            "PS Vita": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/PlayStation-Vita-1101-FL.jpg/500px-PlayStation-Vita-1101-FL.jpg",
            "PSP": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Psp-1000.jpg/500px-Psp-1000.jpg",
            "SEGA Master System": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Sega-Master-System-Set.jpg/500px-Sega-Master-System-Set.jpg",
            "SEGA Saturn": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Sega-Saturn-Console-Set-Mk2.png/500px-Sega-Saturn-Console-Set-Mk2.png",
            "SEGA 32X": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Sega-Genesis-Model2-32X.jpg/500px-Sega-Genesis-Model2-32X.jpg",
            "SEGA CD": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Sega-CD-Model2-Set.jpg/500px-Sega-CD-Model2-Set.jpg",
            "SNES": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/SNES-Mod1-Console-Set.png/500px-SNES-Mod1-Console-Set.png",
            "Wii": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Wii-Console.png/500px-Wii-Console.png",
            "Wii U": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Wii_U_Console_and_Gamepad.png/500px-Wii_U_Console_and_Gamepad.png",
            "Xbox": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Xbox-Console-wDuke-L.jpg/500px-Xbox-Console-wDuke-L.jpg",
            "Xbox 360": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Xbox-360-Pro-wController.jpg/250px-Xbox-360-Pro-wController.jpg",
            "Xbox One": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Microsoft-Xbox-One-Console-Set-wKinect.jpg/250px-Microsoft-Xbox-One-Console-Set-wKinect.jpg",
            "Xbox Series S/X": "https://cms-assets.xboxservices.com/assets/bc/40/bc40fdf3-85a6-4c36-af92-dca2d36fc7e5.png?n=642227_Hero-Gallery-0_A1_857x676.png",
        }

        for console in context["consoles"]:
            console.display_image = console_images.get(
                console.name, "placeholder" + console.name.replace(" ", "+")
            )

        return context


class ConsoleDetailView(LoginRequiredMixin, DetailView):
    model = Console
    template_name = "games/console_detail.html"
    context_object_name = "console"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = Game.objects.filter(
            console=self.object, user=self.request.user
        )
        console_images = {
            "3DO": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/3DO-FZ1-Console-Set.jpg/500px-3DO-FZ1-Console-Set.jpg",
            "Nintendo 3DS": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Nintendo-3DS-AquaOpen.png/500px-Nintendo-3DS-AquaOpen.png",
            "Android": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Android_robot_%282014-2019%29.svg/250px-Android_robot_%282014-2019%29.svg.png",
            "Atari 2600": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Atari-2600-Wood-4Sw-Set.png/500px-Atari-2600-Wood-4Sw-Set.png",
            "Dreamcast": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Dreamcast-Console-Set.png/500px-Dreamcast-Console-Set.png",
            "Nintendo DS": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Nintendo-DS-Fat-Blue.png/330px-Nintendo-DS-Fat-Blue.png",
            "Game Boy": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Game-Boy-FL.png/500px-Game-Boy-FL.png",
            "Game Boy Advance": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Nintendo-Game-Boy-Advance-Purple-FL.png/500px-Nintendo-Game-Boy-Advance-Purple-FL.png",
            "Game Boy Color": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Nintendo_Game_Boy_Color.png/500px-Nintendo_Game_Boy_Color.png",
            "GameCube": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/GameCube-Console-Set.png/500px-GameCube-Console-Set.png",
            "Game Gear": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Sega-Game-Gear-WB.png/500px-Sega-Game-Gear-WB.png",
            "Genesis": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Sega-Genesis-Mk2-6button.jpg/500px-Sega-Genesis-Mk2-6button.jpg",
            "iOS": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/250px-Apple_logo_black.svg.png",
            "Jaguar": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Atari-Jaguar-Console-Set.png/500px-Atari-Jaguar-Console-Set.png",
            "Neo Geo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Neo-Geo-AES-Console-Set.png/500px-Neo-Geo-AES-Console-Set.png",
            "NES": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/NES-Console-Set.png/500px-NES-Console-Set.png",
            "Nintendo 64": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/N64-Console-Set.png/500px-N64-Console-Set.png",
            "Nintendo Switch": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Nintendo-Switch-wJoyCons-BlRd-Standing-FL.jpg/960px-Nintendo-Switch-wJoyCons-BlRd-Standing-FL.jpg",
            "PC": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/IBM_PC-IMG_7271_%28transparent%29.png/500px-IBM_PC-IMG_7271_%28transparent%29.png",
            "PlayStation": "https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/PlayStation-SCPH-1000-with-Controller.png/500px-PlayStation-SCPH-1000-with-Controller.png",
            "PlayStation 2": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/PS2-Versions.png/500px-PS2-Versions.png",
            "PlayStation 3": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/PS3-Fat-Console-Vert.jpg/330px-PS3-Fat-Console-Vert.jpg",
            "PlayStation 4": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/PS4-Console-wDS4.jpg/500px-PS4-Console-wDS4.jpg",
            "PlayStation 5": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Black_and_white_Playstation_5_base_edition_with_controller.png/330px-Black_and_white_Playstation_5_base_edition_with_controller.png",
            "PS Vita": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/PlayStation-Vita-1101-FL.jpg/500px-PlayStation-Vita-1101-FL.jpg",
            "PSP": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Psp-1000.jpg/500px-Psp-1000.jpg",
            "SEGA Master System": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Sega-Master-System-Set.jpg/500px-Sega-Master-System-Set.jpg",
            "SEGA Saturn": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Sega-Saturn-Console-Set-Mk2.png/500px-Sega-Saturn-Console-Set-Mk2.png",
            "SEGA 32X": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Sega-Genesis-Model2-32X.jpg/500px-Sega-Genesis-Model2-32X.jpg",
            "SEGA CD": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Sega-CD-Model2-Set.jpg/500px-Sega-CD-Model2-Set.jpg",
            "SNES": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/SNES-Mod1-Console-Set.png/500px-SNES-Mod1-Console-Set.png",
            "Wii": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Wii-Console.png/500px-Wii-Console.png",
            "Wii U": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Wii_U_Console_and_Gamepad.png/500px-Wii_U_Console_and_Gamepad.png",
            "Xbox": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Xbox-Console-wDuke-L.jpg/500px-Xbox-Console-wDuke-L.jpg",
            "Xbox 360": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Xbox-360-Pro-wController.jpg/250px-Xbox-360-Pro-wController.jpg",
            "Xbox One": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Microsoft-Xbox-One-Console-Set-wKinect.jpg/250px-Microsoft-Xbox-One-Console-Set-wKinect.jpg",
            "Xbox Series S/X": "https://cms-assets.xboxservices.com/assets/bc/40/bc40fdf3-85a6-4c36-af92-dca2d36fc7e5.png?n=642227_Hero-Gallery-0_A1_857x676.png",
        }

        self.object.display_image = console_images.get(
            self.object.name, "https://placehold.co/600x400?text=No+Image"
        )

        return context


class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = "games/game_detail.html"
    context_object_name = "game"

    def get_queryset(self):
        return Game.objects.filter(user=self.request.user)


class GameUpdate(LoginRequiredMixin, UpdateView):
    model = Game
    fields = ["console"]
    template_name = "games/game_form.html"

    def get_queryset(self):
        return Game.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("game-detail", kwargs={"pk": self.object.pk})


class GameDelete(LoginRequiredMixin, DeleteView):
    model = Game
    success_url = reverse_lazy("console-list")
    template_name = "games/game_confirm_delete.html"

    def get_queryset(self):
        return Game.objects.filter(user=self.request.user)


class GameSearchView(LoginRequiredMixin, View):
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


class GameImportView(LoginRequiredMixin, View):
    login_url = "login"

    def post(self, request):
        game_ids = request.POST.getlist("game_ids")

        for rawg_id in game_ids:
            console_name = request.POST.get(f"console_name_{rawg_id}")

            if not console_name:
                continue

            console, _ = Console.objects.get_or_create(name=console_name)

            import_game(
                rawg_id=rawg_id,
                console=console,
                user=request.user
            )

        return redirect("console-list")


class GenreListView(LoginRequiredMixin, ListView):
    model = Genre
    template_name = "games/genre_list.html"
    context_object_name = "genres"
    login_url = "login"

    def get_queryset(self):
        return Genre.objects.filter(games__user=self.request.user).distinct()


class GenreDetailView(LoginRequiredMixin, DetailView):
    model = Genre
    template_name = "games/genre_detail.html"
    context_object_name = "genre"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = self.object.games.filter(user=self.request.user)
        return context


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('console-list')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
