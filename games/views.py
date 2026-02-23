from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Console, Game, Genre
from .forms import GameSearchForm
from .services.rawg import search_games, import_game


# Create your views here.
def about(request):
    return render(request, "about.html")


class ConsoleListView(ListView):
    model = Console
    template_name = "games/console_list.html"
    context_object_name = "consoles"

    def get_queryset(self):
        return Console.objects.filter(games__isnull=False).distinct()


class ConsoleDetailView(DetailView):
    model = Console
    template_name = "games/console_detail.html"
    context_object_name = "console"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = Game.objects.filter(console=self.object)
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
                    games.append({
                        "id": game["id"],
                        "name": game["name"],
                        "image": game.get("background_image", ""),
                        "platforms": platforms,
                    })

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
