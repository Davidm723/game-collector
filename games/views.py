from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Console, Game


# Create your views here.
def about(request):
    return render(request, "about.html")


class ConsoleListView(ListView):
    model: Console
    template_name = "games/console_list.html"
    context_object_name = "console"


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
