from django.urls import path
from .views import (
    ConsoleListView,
    ConsoleDetailView,
    GameDetailView,
    GameUpdate,
    GameDelete,
    GameSearchView,
    GameImportView,
    GenreListView,
    GenreDetailView,
    about,
    Home,
    signup,
)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path("console/", ConsoleListView.as_view(), name="console-list"),
    path("console/<int:pk>/", ConsoleDetailView.as_view(), name="console-detail"),
    path("game/<int:pk>/", GameDetailView.as_view(), name="game-detail"),
    path("games/<int:pk>/edit/", GameUpdate.as_view(), name="game-update"),
    path("games/<int:pk>/delete/", GameDelete.as_view(), name="game-delete"),
    path("add-games/", GameSearchView.as_view(), name="game-search"),
    path("import-games/", GameImportView.as_view(), name="game-import"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("genres/<int:pk>/", GenreDetailView.as_view(), name="genre-detail"),
    path("about/", about, name="about"),
    path('accounts/signup/', signup, name='signup'),
]
