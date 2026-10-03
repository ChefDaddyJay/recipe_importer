from recipe_importer.models import Ingredient
from recipe_importer.normalizer import normalize_ingredient, normalize_recipe


def test_normalize_cup():
    ingredient = Ingredient(
        name="flour",
        amount=2,
        unit="cups",
    )

    normalized = normalize_ingredient(ingredient)

    assert normalized.unit == "cup"


def test_normalize_tablespoon():
    ingredient = Ingredient(
        name="olive oil",
        amount=3,
        unit="tbsp",
    )

    normalized = normalize_ingredient(ingredient)

    assert normalized.unit == "tablespoon"


def test_normalize_teaspoon():
    ingredient = Ingredient(
        name="salt",
        amount=1,
        unit="tsp",
    )

    normalized = normalize_ingredient(ingredient)

    assert normalized.unit == "teaspoon"


def test_normalize_cloves():
    ingredient = Ingredient(
        name="garlic",
        amount=4,
        unit="cloves",
    )

    normalized = normalize_ingredient(ingredient)

    assert normalized.unit == "clove"


def test_normalize_ounces():
    ingredient = Ingredient(
        name="cream cheese",
        amount=8,
        unit="ounces",
    )

    normalized = normalize_ingredient(ingredient)

    assert normalized.unit == "ounce"


def test_normalize_unknown_unit():
    ingredient = Ingredient(
        name="something",
        amount=1,
        unit="whatever",
    )

    normalized = normalize_ingredient(ingredient)

    assert normalized.unit == "whatever"


def test_normalize_no_unit():
    ingredient = Ingredient(
        name="eggs",
        amount=2,
        unit=None,
    )

    normalized = normalize_ingredient(ingredient)

    assert normalized.unit is None

def test_normalize_preserves_ingredient_data():
    ingredient = Ingredient(
        name="garlic",
        amount=2,
        unit="cloves",
        preparation="minced",
        form=None,
    )

    normalized = normalize_ingredient(ingredient)

    assert normalized.name == "garlic"
    assert normalized.amount == 2
    assert normalized.unit == "clove"
    assert normalized.preparation == "minced"
    assert normalized.form is None

def test_normalize_recipe_ingredients():
    raw_recipe = {
        "title": "Garlic Bread",
        "servings": "4 servings",
        "prep_time": 10,
        "cook_time": 15,
        "total_time": 25,
        "ingredients": [
            "2 cloves garlic, minced",
            "1/2 cup butter",
            "3 tablespoons parsley",
        ],
        "instructions": "Mix and bake.",
        "url": "https://example.com/garlic-bread",
        "image": "https://example.com/image.jpg",
    }

    recipe = normalize_recipe(raw_recipe)

    assert len(recipe.ingredients) == 3

    assert recipe.ingredients[0].name == "garlic"
    assert recipe.ingredients[0].amount == 2
    assert recipe.ingredients[0].unit == "clove"
    assert recipe.ingredients[0].preparation == "minced"

    assert recipe.ingredients[1].name == "butter"
    assert recipe.ingredients[1].amount == 0.5
    assert recipe.ingredients[1].unit == "cup"

    assert recipe.ingredients[2].name == "parsley"
    assert recipe.ingredients[2].amount == 3
    assert recipe.ingredients[2].unit == "tablespoon"