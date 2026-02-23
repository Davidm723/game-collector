from django.urls import path
from .views import (
    ConsoleListView,
    ConsoleDetailView,
    GameDetailView,
    GameSearchView,
    GameImportView,
    about,
)

urlpatterns = [
    path("", ConsoleListView.as_view(), name="console-list"),
    path("console/<int:pk>/", ConsoleDetailView.as_view(), name="console-detail"),
    path("game/<int:pk>/", GameDetailView.as_view(), name="game-detail"),
    path("add-games/", GameSearchView.as_view(), name="game-search"),
    path("import-games/", GameImportView.as_view(), name="game-import"),
    path("about/", about, name="about"),
]
