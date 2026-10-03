from dataclasses import asdict
import json
from pprint import pprint
from argparse import ArgumentParser

from recipe_importer.scraper import scrape_recipe
from recipe_importer.normalizer import normalize_recipe


def main():
    parser = ArgumentParser(
        description="Import a recipe from a url"
    )

    parser.add_argument(
        "url",
        help="URL of the recipe to import"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="./recipes.json",
        help="Output JSON file (default: ./recipes.json)"
    )

    args = parser.parse_args()

    raw_recipe = scrape_recipe(args.url)

    recipe = normalize_recipe(raw_recipe)

    with open(args.output, "w") as file:
        json.dump(asdict(recipe), file, indent=2)

    print(f'Recipe: {recipe.name} imported to {args.output} from {args.url}')


if __name__ == "__main__":
    main()