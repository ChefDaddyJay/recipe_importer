from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup
import requests

def fetch_page(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def extract_links(html: str, base_url: str) -> set[str]:
    soup = BeautifulSoup(html, "html.parser")

    links = set()

    for anchor in soup.find_all("a", href=True):
        url = urljoin(base_url, anchor["href"])
        url = normalize_url(url)
        links.add(url)

    return links

def normalize_url(url: str) -> str:
    parsed = urlparse(url)

    normalized_path = parsed.path.strip('/')

    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            normalized_path,
            "", "", ""
        )
    )

def filter_same_domain(urls: set[str], base_url: str) -> set[str]:
    base_domain = urlparse(base_url).netloc

    return {
        url
        for url in urls
        if urlparse(url).netloc == base_domain
    }

def crawl_page(url: str) -> set[str]:
    html = fetch_page(url)

    links = extract_links(
        html,
        url,
    )

    return filter_same_domain(
        links,
        url,
    )

def crawl(start_url: str, max_depth: int = 1, max_pages: int = 100) -> set[str]:
    start_url = normalize_url(start_url)

    to_visit = [(start_url, 0)]
    visited = set()

    while to_visit:
        url, depth = to_visit.pop(0)

        if url in visited:
            continue

        if len(visited) >= max_pages:
            break

        try:
            links = crawl_page(url)
        except requests.RequestException:
            continue

        visited.add(url)

        if depth >= max_depth:
            continue

        for link in links:
            if link not in visited:
                to_visit.append((link, depth + 1))

    return visited

def is_recipe_url(url: str) -> bool:
    path = urlparse(url).path.lower()
    print(f'PATH: {path}')
    print(f'recipes {'/recipes/' in path}')
    print(f'recipe {'/recipe/' in path}')
    print(f'OR: {'/recipes/' in path or '/recipe/' in path}')

    return (
        '/recipe/' in path
        or '/recipes/' in path
    )

def filter_recipe_urls(urls: set[str]) -> set[str]:
    return {
        url 
        for url in urls 
        if is_recipe_url(url)
    }