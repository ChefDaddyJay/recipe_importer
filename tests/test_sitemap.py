import requests

from recipe_importer.sitemap import discover_sitemap_urls, extract_sitemap_locations, get_sitemap_type

def test_extract_sitemap_locations():
    xml = """
    <?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>https://example.com/recipe/chicken</loc>
        </url>
        <url>
            <loc>https://example.com/recipe/pasta</loc>
        </url>
        <url>
            <loc>https://example.com/about</loc>
        </url>
    </urlset>
    """.strip()

    urls = extract_sitemap_locations(xml)

    assert urls == {
        "https://example.com/recipe/chicken",
        "https://example.com/recipe/pasta",
        "https://example.com/about",
    }

def test_extract_sitemap_index_locations():
    xml = """
    <?xml version="1.0" encoding="UTF-8"?>
    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <sitemap>
            <loc>https://example.com/sitemap_1.xml</loc>
        </sitemap>
        <sitemap>
            <loc>https://example.com/sitemap_2.xml</loc>
        </sitemap>
        <sitemap>
            <loc>https://example.com/sitemap_3.xml</loc>
        </sitemap>
    </sitemapindex>
    """.strip()

    urls = extract_sitemap_locations(xml)

    assert urls == {
        "https://example.com/sitemap_1.xml",
        "https://example.com/sitemap_2.xml",
        "https://example.com/sitemap_3.xml",
    }

def test_get_sitemap_type_urlset():
    xml = """
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    </urlset>
    """.strip()

    assert get_sitemap_type(xml) == "urlset"

def test_get_sitemap_type_index():
    xml = """
    <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    </sitemapindex>
    """.strip()

    assert get_sitemap_type(xml) == "sitemapindex"

def test_discover_sitemap_urls(monkeypatch):
    sitemaps = {
        "https://example.com/sitemap.xml": """
            <sitemapindex
                xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <sitemap>
                    <loc>https://example.com/sitemap_1.xml</loc>
                </sitemap>
                <sitemap>
                    <loc>https://example.com/sitemap_2.xml</loc>
                </sitemap>
            </sitemapindex>
        """,

        "https://example.com/sitemap_1.xml": """
            <urlset
                xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://example.com/recipe/chicken</loc>
                </url>
                <url>
                    <loc>https://example.com/recipe/pasta</loc>
                </url>
            </urlset>
        """,

        "https://example.com/sitemap_2.xml": """
            <urlset
                xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://example.com/recipe/soup</loc>
                </url>
            </urlset>
        """,
    }

    def fake_fetch_sitemap(url):
        return sitemaps[url]

    monkeypatch.setattr(
        "recipe_importer.sitemap.fetch_sitemap",
        fake_fetch_sitemap,
    )

    urls = discover_sitemap_urls(
        "https://example.com/sitemap.xml"
    )

    assert urls == {
        "https://example.com/recipe/chicken",
        "https://example.com/recipe/pasta",
        "https://example.com/recipe/soup",
    }

def test_discover_sitemap_urls_duplicates(monkeypatch):
    sitemaps = {
        "https://example.com/sitemap.xml": """
            <sitemapindex
                xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <sitemap>
                    <loc>https://example.com/sitemap_1.xml</loc>
                </sitemap>
                <sitemap>
                    <loc>https://example.com/sitemap_2.xml</loc>
                </sitemap>
            </sitemapindex>
        """,

        "https://example.com/sitemap_1.xml": """
            <urlset
                xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://example.com/recipe/chicken</loc>
                </url>
                <url>
                    <loc>https://example.com/recipe/pasta</loc>
                </url>
            </urlset>
        """,

        "https://example.com/sitemap_2.xml": """
            <urlset
                xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://example.com/recipe/soup</loc>
                </url>
                <url>
                    <loc>https://example.com/recipe/pasta</loc>
                </url>
            </urlset>
        """,
    }

    def fake_fetch_sitemap(url):
        return sitemaps[url]

    monkeypatch.setattr(
        "recipe_importer.sitemap.fetch_sitemap",
        fake_fetch_sitemap,
    )

    urls = discover_sitemap_urls(
        "https://example.com/sitemap.xml"
    )

    assert urls == {
        "https://example.com/recipe/chicken",
        "https://example.com/recipe/pasta",
        "https://example.com/recipe/soup",
    }

def test_discover_sitemap_urls_skips_failed_sitemap(monkeypatch):
    sitemaps = {
        "https://example.com/sitemap.xml": """
            <sitemapindex
                xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <sitemap>
                    <loc>https://example.com/sitemap_1.xml</loc>
                </sitemap>
                <sitemap>
                    <loc>https://example.com/sitemap_2.xml</loc>
                </sitemap>
            </sitemapindex>
        """,

        "https://example.com/sitemap_1.xml": """
            <urlset
                xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                <url>
                    <loc>https://example.com/recipe/chicken</loc>
                </url>
            </urlset>
        """,
    }

    def fake_fetch_sitemap(url):
        if url == "https://example.com/sitemap_2.xml":
            raise requests.HTTPError("402 Payment Required")

        return sitemaps[url]

    monkeypatch.setattr(
        "recipe_importer.sitemap.fetch_sitemap",
        fake_fetch_sitemap,
    )

    urls = discover_sitemap_urls(
        "https://example.com/sitemap.xml"
    )

    assert urls == {
        "https://example.com/recipe/chicken",
    }