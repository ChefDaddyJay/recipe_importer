import re

from .models import Ingredient

UNITS = {
    "cup",
    "cups",
    "tbsp",
    "tablespoon",
    "tablespoons",
    "tsp",
    "teaspoon",
    "teaspoons",
    "clove",
    "cloves",
    "pound",
    "pounds",
    "ounce",
    "ounces",
}

def parse_amount(value: str) -> float | None:
    parts = value.split()

    if len(parts) == 2 and "/" in parts[1]:
        try:
            whole = parts[0]
            numerator, denominator = parts[1].split("/", 1)

            return float(whole) + float(numerator) / float(denominator)
        except ValueError:
            return None

    if "/" in value:
        try:
            numerator, denominator = value.split("/", 1)

            return float(numerator) / float(denominator)
        except ValueError:
            return None

    try:
        return float(value)
    except ValueError:
        return None

def extract_preparation(value: str) -> tuple[str, str | None]:
    if ',' not in value:
        return value, None

    name, preparation = value.split(',', 1)
    return name.strip(), preparation.strip()

def extract_container(value: str) -> tuple[str | None, str]:
    match = re.match(r"^\((.+)\)\s*(.*)$", value)

    if not match:
        return None, value

    container = match.group(1)
    remainder = match.group(2)

    return container, remainder

def parse_container(value: str) -> tuple[float | None, str | None, str | None]:
    parts = value.split()

    if len(parts) != 3:
        return None, None, None

    amount = parse_amount(parts[0])

    if amount is None:
        return None, None, None

    unit = parts[1]
    form = parts[2]

    return amount, unit, form

def parse_ingredient(value: str) -> Ingredient:
    match = re.match(
        r"^(\d+\s+\d+/\d+|\d+(?:\.\d+)?|\d+/\d+)\s+(.+)$",
        value,
    )

    if not match:
        return Ingredient(name=value)

    amount = parse_amount(match.group(1))

    remainder = match.group(2)

    unit = None
    form = None

    container, remainder = extract_container(remainder)

    if container is not None:
        container_amount, unit, form = parse_container(container)

        if container_amount is not None:
            amount *= container_amount

    else:
        parts = remainder.split()
        possible_unit = parts[0]

        if possible_unit in UNITS:
            unit = possible_unit 
            remainder = " ".join(parts[1:])
        else:
            unit = None

    name, preparation = extract_preparation(remainder)

    if amount is not None and amount.is_integer():
        amount = int(amount)

    return Ingredient(
        name=name,
        amount=amount,
        unit=unit,
        preparation=preparation,
        form=form
    )