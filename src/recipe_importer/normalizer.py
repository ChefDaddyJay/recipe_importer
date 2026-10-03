from recipe_importer.ingredients import parse_ingredient

from .models import Ingredient, Recipe

UNIT_ALIASES =  {
        'tbsp': 'tablespoon',
        'T': 'tablespoon',
        'tsp': 'teaspoon',
        't': 'teaspoon',
        'lb': 'pound',
        'c': 'cup',
        'C': 'cup',
        'gal': 'gallon',
        'G': 'gallon',
        'l': 'liter',
        'L': 'liter',
        'ml': 'milliliter',
        'mL': 'milliliter',
        'g': 'gram',
        'kg': 'kilogram'
    }

def normalize_ingredient(raw: Ingredient) -> Ingredient:
    normalized = Ingredient(
        name=raw.name,
        amount=raw.amount,
        unit=normalize_unit(raw.unit),
        preparation=raw.preparation,
        form=raw.form
    )

    return normalized

def normalize_unit(raw: str) -> str | None:
    if not raw:
        return None
    
    unit = raw

    if unit.endswith('s') or unit.endswith("S"):
        unit = unit[:-1]

    if unit in UNIT_ALIASES.keys():
        unit = UNIT_ALIASES[unit]

    return unit

def normalize_ingredients(raw: list[str]) -> Ingredient:
    ingredients = [parse_ingredient(ingredient) for ingredient in raw]
    return [normalize_ingredient(ingredient) for ingredient in ingredients]

def normalize_recipe(raw: dict) -> Recipe:
    return Recipe(
        name=raw["title"],
        servings=parse_servings(
            raw["servings"]
        ),
        prep_minutes=raw["prep_time"],
        cook_minutes=raw["cook_time"],
        total_minutes=raw["total_time"],
        ingredients=normalize_ingredients(raw["ingredients"]),
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