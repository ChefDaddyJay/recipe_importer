from .models import Recipe


def normalize_recipe(raw: dict) -> Recipe:
    return Recipe(
        name=raw["title"],
        servings=parse_servings(
            raw["servings"]
        ),
        prep_minutes=raw["prep_time"],
        cook_minutes=raw["cook_time"],
        total_minutes=raw["total_time"],
        ingredients=raw["ingredients"],
        instructions=raw["instructions"],
        source_url=raw["url"],
        image_url=raw["image"],
    )


def parse_servings(value: str | None) -> int | None:
    if not value:
        return None

    # Example:
    # "6 servings" -> 6

    first_word = value.split()[0]

    try:
        return int(first_word)
    except ValueError:
        return None