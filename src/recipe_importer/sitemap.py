import xml.etree.ElementTree as ET

import requests

def extract_sitemap_locations(xml: str) -> set[str]:
    root = ET.fromstring(xml)

    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"

    urls = set()

    for loc in root.findall(f'.//{{{namespace}}}loc'):
        if loc.text:
            urls.add(loc.text.strip())

    return urls

def get_sitemap_type(xml: str) -> str:
    root = ET.fromstring(xml)

    return root.tag.split("}", 1)[-1]

def discover_sitemap_urls(sitemap_url: str) -> set[str]:
    try:
        xml = fetch_sitemap(sitemap_url)
    except requests.RequestException:
        return set()

    sitemap_type = get_sitemap_type(xml)
    locations = extract_sitemap_locations(xml)

    if sitemap_type == "urlset":
        return locations

    if sitemap_type == "sitemapindex":
        urls = set()

        for child_sitemap in locations:
            urls.update(
                discover_sitemap_urls(child_sitemap)
            )

        return urls

    raise ValueError(
        f"Unsupported sitemap type: {sitemap_type}"
    )

def fetch_sitemap(url: str) -> str:
    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    return response.text