from recipe_scrapers import scrape_me


def scrape_recipe(url: str):
    scraper = scrape_me(url)

    return {
        "title": scraper.title(),
        "ingredients": scraper.ingredients(),
        "instructions": scraper.instructions(),
        "prep_time": scraper.prep_time(),
        "cook_time": scraper.cook_time(),
        "total_time": scraper.total_time(),
        "servings": scraper.yields(),
        "image": scraper.image(),
        "url": url,
    }