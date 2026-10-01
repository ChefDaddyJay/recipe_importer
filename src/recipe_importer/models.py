from dataclasses import dataclass, field


@dataclass
class Ingredient:
    name: str
    amount: float | None = None
    unit: str | None = None
    preparation: str | None = None
    form: str | None = None


@dataclass
class Recipe:
    name: str
    servings: int | None = None

    prep_minutes: int | None = None
    cook_minutes: int | None = None
    total_minutes: int | None = None

    ingredients: list[Ingredient] = field(
        default_factory=list
    )

    instructions: str = ""

    notes: str | None = None
    tags: list[str] = field(
        default_factory=list
    )

    source_url: str | None = None
    image_url: str | None = None