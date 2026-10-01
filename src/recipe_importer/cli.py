from pprint import pprint
import sys

from recipe_importer.scraper import scrape_recipe
from recipe_importer.normalizer import normalize_recipe


def main():
    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python -m recipe_importer <recipe-url>"
        )
        return

    url = sys.argv[1]

    raw_recipe = scrape_recipe(url)

    recipe = normalize_recipe(raw_recipe)

    pprint(recipe)


if __name__ == "__main__":
    main()