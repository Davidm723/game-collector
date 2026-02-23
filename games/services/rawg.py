import requests
from datetime import datetime
from django.conf import settings
from games.models import Console, Genre, Game

BASE_URL = "https://api.rawg.io/api"


def rawg_get(endpoint, params=None):
    if params is None:
        params = {}

    params["key"] = settings.RAWG_API_KEY

    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    response.raise_for_status()
    return response.json()


def search_games(query, page_size=10):
    data = rawg_get(
        "games",
        {
            "search": query,
            "page_size": page_size,
        },
    )
    return data.get("results", [])


def import_consoles():
    data = rawg_get("platforms", {"page_size": 40})

    for item in data.get("results", []):
        Console.objects.get_or_create(
            name=item["name"],
            defaults={
                "release_year": item.get("year_start"),
                "manufacturer": item.get("platform", {}).get("name", ""),
                "image": item.get("image_background", ""),
            },
        )


def import_genres():
    data = rawg_get("genres")

    for item in data.get("results", []):
        Genre.objects.get_or_create(name=item["name"])


def import_game(rawg_id, console):
    data = rawg_get(f"games/{rawg_id}")

    game, created = Game.objects.get_or_create(
        rawg_id=data["id"],
        defaults={
            "title": data["name"],
            "console": console,
            "released": (
                datetime.strptime(data["released"], "%Y-%m-%d").date()
                if data.get("released")
                else None
            ),
            "image": data.get("background_image") or "",
        },
    )

    for g in data.get("genres", []):
        genre, _ = Genre.objects.get_or_create(name=g["name"])
        game.genres.add(genre)

    return game
