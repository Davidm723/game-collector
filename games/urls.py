from django.urls import path
from . import views
from .views import ConsoleListView, ConsoleDetailView, GameDetailView

urlpatterns = [
    path('', ConsoleListView.as_view(), name='console-list'),
    path("consoles/<int:pk>/", ConsoleDetailView.as_view(), name="console-detail"),
    path("games/<int:pk>/", GameDetailView.as_view(), name="game-detail"),
    path('about/', views.about, name='about'),
]