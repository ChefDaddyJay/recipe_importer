from recipe_importer.ingredients import extract_container, extract_preparation, parse_container, parse_ingredient


def test_parse_simple_ingredient():
    ingredient = parse_ingredient("2 cups flour")

    assert ingredient.name == "flour"
    assert ingredient.amount == 2
    assert ingredient.unit == "cups"

def test_parse_decimal_amount():
    ingredient = parse_ingredient("2.5 cups sugar")

    assert ingredient.name == "sugar"
    assert ingredient.amount == 2.5
    assert ingredient.unit == "cups"

def test_parse_multi_word_ingredients():
    ingredient = parse_ingredient("1 tsp olive oil")

    assert ingredient.name == "olive oil"
    assert ingredient.amount == 1
    assert ingredient.unit == "tsp"

def test_parse_no_units():
    ingredients = parse_ingredient("2 eggs")

    assert ingredients.name == "eggs"
    assert ingredients.amount == 2
    assert ingredients.unit is None

def test_parse_no_units_name():
    ingredients = parse_ingredient("1 onion")

    assert ingredients.name == "onion"
    assert ingredients.amount == 1
    assert ingredients.unit is None

def test_parse_unusual_units():
    ingredients = parse_ingredient("4 cloves garlic")

    assert ingredients.name == "garlic"
    assert ingredients.amount == 4
    assert ingredients.unit == "cloves"

def test_parse_fraction():
    ingredient = parse_ingredient("1/2 cup milk")

    assert ingredient.name == "milk"
    assert ingredient.amount == 0.5
    assert ingredient.unit == "cup"


def test_parse_three_quarters():
    ingredient = parse_ingredient("3/4 teaspoon salt")

    assert ingredient.name == "salt"
    assert ingredient.amount == 0.75
    assert ingredient.unit == "teaspoon"

def test_parse_mixed_fraction():
    ingredient = parse_ingredient("1 1/2 tbsp butter")

    assert ingredient.name == "butter"
    assert ingredient.amount == 1.5
    assert ingredient.unit == "tbsp"

def test_parse_fraction_two():
    ingredient = parse_ingredient("2 3/4 pounds ground beef")

    assert ingredient.name == "ground beef"
    assert ingredient.amount == 2.75
    assert ingredient.unit == "pounds"

def test_parse_preparation():
    ingredient = parse_ingredient("2 cloves garlic, minced")

    assert ingredient.name == "garlic"
    assert ingredient.amount == 2
    assert ingredient.unit == "clove"
    assert ingredient.preparation == "minced"

def test_parse_preparation_chopped():
    ingredient = parse_ingredient("1 onion, chopped")

    assert ingredient.name == "onion"
    assert ingredient.amount == 1
    assert ingredient.unit is None
    assert ingredient.preparation == "chopped"
    assert ingredient.form is None

def test_parse_container_amount():
    ingredient = parse_ingredient("1 (14.5 oz can) diced tomatoes")

    assert ingredient.name == "diced tomatoes"
    assert ingredient.amount == 14.5
    assert ingredient.unit == "oz"
    assert ingredient.preparation is None
    assert ingredient.form == "can"

def test_extract_preparation():
    name, preparation = extract_preparation(
        "garlic, minced"
    )

    assert name == "garlic"
    assert preparation == "minced"

def test_extract_no_preparation():
    name, preparation = extract_preparation(
        "garlic"
    )

    assert name == "garlic"
    assert preparation is None

def test_extract_multiple_preparations():
    name, preparation = extract_preparation(
        "tomatoes, diced, drained"
    )

    assert name == "tomatoes"
    assert preparation == "diced, drained"

def test_parse_preparation():
    ingredient = parse_ingredient("2 cloves garlic, minced")

    assert ingredient.name == "garlic"
    assert ingredient.amount == 2
    assert ingredient.unit == "cloves"
    assert ingredient.preparation == "minced"

def test_parse_preparation():
    ingredient = parse_ingredient("1 onion, chopped")

    assert ingredient.name == "onion"
    assert ingredient.amount == 1
    assert ingredient.unit is None
    assert ingredient.preparation == "chopped"

def test_parse_container():
    amount, unit, form = parse_container("14.5 oz can")

    assert amount == 14.5
    assert unit == "oz"
    assert form == "can"

def test_extract_container():
    container, remainder = extract_container("(14.5 oz can) diced tomatoes")

    assert container == "14.5 oz can"
    assert remainder == "diced tomatoes"

def test_parse_multiple_containers():
    ingredient = parse_ingredient(
        "2 (15 oz cans) black beans"
    )

    assert ingredient.name == "black beans"
    assert ingredient.amount == 30
    assert ingredient.unit == "oz"
    assert ingredient.preparation is None
    assert ingredient.form == "cans"


def test_parse_multiple_packages():
    ingredient = parse_ingredient(
        "3 (8 oz packages) cream cheese"
    )

    assert ingredient.name == "cream cheese"
    assert ingredient.amount == 24
    assert ingredient.unit == "oz"
    assert ingredient.preparation is None
    assert ingredient.form == "packages"

def test_parse_partial_package():
    ingredient = parse_ingredient("1/2 (8 oz package) cream cheese")

    assert ingredient.name == "cream cheese"
    assert ingredient.amount == 4
    assert ingredient.unit == "oz"
    assert ingredient.form == "package"

def test_parse_mixed_fraction_bag_with_prep():
    ingredient = parse_ingredient("1 1/2 (5 lb bag) sugar, divided")

    assert ingredient.name == "sugar"
    assert ingredient.amount == 7.5
    assert ingredient.unit == "lb"
    assert ingredient.form == "bag"
    assert ingredient.preparation == "divided"