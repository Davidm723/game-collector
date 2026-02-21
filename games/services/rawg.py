import requests
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


def import_consoles():
    data = rawg_get("platforms", {"page_size": 40})

    for item in data["results"]:
        Console.objects.get_or_create(
            name=item["name"],
            defaults={
                "release_year": item.get("year_start"),
                "manufacturer": item.get("platform", {}).get("name", ""),
            },
        )


def import_genres():
    data = rawg_get("genres")

    for item in data["results"]:
        Genre.objects.get_or_create(name=item["name"])


def import_games(search, console_name, page_size=10):
    data = rawg_get(
        "games",
        {
            "search": search,
            "page_size": page_size,
        },
    )

    console = Console.objects.get(name=console_name)

    for item in data["results"]:
        game, created = Game.objects.get_or_create(
            rawg_id=item["id"],
            defaults={
                "title": item["name"],
                "console": console,
                "released": (
                    datetime.strptime(item["released"], "%Y-%m-%d").date()
                    if item.get("released")
                    else None
                ),
                "image": item.get("background_image", ""),
            },
        )

        for g in item.get("genres", []):
            genre, _ = Genre.objects.get_or_create(name=g["name"])
            game.genres.add(genre)
