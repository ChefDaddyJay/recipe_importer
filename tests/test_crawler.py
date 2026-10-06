import requests

from recipe_importer.crawler import crawl_page, extract_links, fetch_page, filter_recipe_urls, filter_same_domain, is_recipe_url, normalize_url, crawl


def test_extract_links():
    html = """
    <html>
        <body>
            <a href="/recipes/chicken">Chicken</a>
            <a href="/recipes/pasta">Pasta</a>
            <a href="/about">About</a>
        </body>
    </html>
    """

    links = extract_links(
        html,
        "https://example.com/recipes/"
    )

    assert links == {
        "https://example.com/recipes/chicken",
        "https://example.com/recipes/pasta",
        "https://example.com/about",
    }

def test_filter_same_domain():
    urls = {
        "https://example.com/recipes/chicken",
        "https://example.com/recipes/pasta",
        "https://other.com/recipe",
        "https://google.com",
    }

    filtered = filter_same_domain(urls, "https://example.com/recipes")

    assert filtered == {
        "https://example.com/recipes/chicken",
        "https://example.com/recipes/pasta",
    }

def test_fetch_page(monkeypatch):
    class FakeResponse:
        text = "<html><body>Just a test</body></html>"

        def raise_for_status(self):
            pass

    def fake_get(url, timeout):
        assert url == "https://example.com"
        assert timeout == 10
        return FakeResponse()

    monkeypatch.setattr(
        "recipe_importer.crawler.requests.get",
        fake_get
    )

    html = fetch_page("https://example.com")

    assert html == "<html><body>Just a test</body></html>"

def test_crawl_page(monkeypatch):
    html = """
    <html>
        <body>
            <a href="/recipes/chicken">Chicken</a>
            <a href="/recipes/pasta">Pasta</a>
            <a href="https://other.com/recipe">Other</a>
        </body>
    </html>
    """

    def fake_fetch_page(url):
        assert url == "https://example.com/recipes/"
        return html

    monkeypatch.setattr(
        "recipe_importer.crawler.fetch_page",
        fake_fetch_page,
    )

    urls = crawl_page(
        "https://example.com/recipes/"
    )

    assert urls == {
        "https://example.com/recipes/chicken",
        "https://example.com/recipes/pasta",
    }

def test_normalize_url_fragment():
    url = "https://example.com/recipes/chicken#ingredients"

    normalized = normalize_url(url)

    assert normalized == "https://example.com/recipes/chicken"

def test_normalize_url_trailing_slash():
    url = "https://example.com/recipes/chicken/"

    normalized = normalize_url(url)

    assert normalized == "https://example.com/recipes/chicken"

def test_normalize_url_args():
    url = "https://example.com/recipes/chicken?user=test"

    normalized = normalize_url(url)

    assert normalized == "https://example.com/recipes/chicken"

def test_normalize_url_complex():
    url = "https://example.com/recipes/chicken/?user=test#ingredients"

    normalized = normalize_url(url)

    assert normalized == "https://example.com/recipes/chicken"

def test_crawl_multiple_pages(monkeypatch):
    pages = {
        "https://example.com/start": """
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
        """,

        "https://example.com/page1": """
            <a href="/page3">Page 3</a>
        """,

        "https://example.com/page2": """
            <a href="/page3">Page 3</a>
        """,

        "https://example.com/page3": """
            <p>Page 3</p>
        """,
    }

    visited = []

    def fake_fetch_page(url):
        visited.append(url)
        return pages[url]

    monkeypatch.setattr(
        "recipe_importer.crawler.fetch_page",
        fake_fetch_page,
    )

    urls = crawl(
        "https://example.com/start",
        max_depth=1,
    )

    assert urls == {
        "https://example.com/start",
        "https://example.com/page1",
        "https://example.com/page2",
    }

    assert set(visited) == {
        "https://example.com/start",
        "https://example.com/page1",
        "https://example.com/page2",
    }

def test_crawl_multiple_pages_no_loops(monkeypatch):
    pages = {
        "https://example.com/start": """
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
        """,

        "https://example.com/page1": """
            <a href="/page3">Page 3</a>
            <a href="/page2">Page 2</a>
        """,

        "https://example.com/page2": """
            <a href="/page3">Page 3</a>
            <a href="start">Start</a>
        """,

        "https://example.com/page3": """
            <p>Page 3</p>
        """,
    }

    visited = []

    def fake_fetch_page(url):
        visited.append(url)
        return pages[url]

    monkeypatch.setattr(
        "recipe_importer.crawler.fetch_page",
        fake_fetch_page,
    )

    urls = crawl(
        "https://example.com/start",
        max_depth=1,
    )

    assert urls == {
        "https://example.com/start",
        "https://example.com/page1",
        "https://example.com/page2",
    }

    assert set(visited) == {
        "https://example.com/start",
        "https://example.com/page1",
        "https://example.com/page2",
    }

def test_crawl_multiple_pages_max_pages(monkeypatch):
    pages = {
        "https://example.com/start": """
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <a href="/page3">Page 3</a>
            <a href="/page4">Page 4</a>
            <a href="/page5">Page 5</a>
            <a href="/page6">Page 6</a>
        """,

        "https://example.com/page1": """
            <a href="/page3">Page 3</a>
            <a href="/page2">Page 2</a>
        """,

        "https://example.com/page2": """
            <a href="/page3">Page 3</a>
            <a href="start">Start</a>
        """,

        "https://example.com/page3": """
            <p>Page 3</p>
        """,

        "https://example.com/page4": """
            <p>Page 3</p>
        """,

        "https://example.com/page5": """
            <p>Page 3</p>
        """,

        "https://example.com/page6": """
            <p>Page 3</p>
        """,
    }

    visited = []

    def fake_fetch_page(url):
        visited.append(url)
        return pages[url]

    monkeypatch.setattr(
        "recipe_importer.crawler.fetch_page",
        fake_fetch_page,
    )

    urls = crawl(
        "https://example.com/start",
        max_depth=1,
        max_pages=3
    )

    assert len(urls) == 3
    assert "https://example.com/start" in urls

    assert len(visited) == 3
    assert "https://example.com/start" in visited

def test_crawl_max_depth_zero(monkeypatch):
    pages = {
        "https://example.com/start": """
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
        """,
    }

    visited = []

    def fake_fetch_page(url):
        visited.append(url)
        return pages[url]

    monkeypatch.setattr(
        "recipe_importer.crawler.fetch_page",
        fake_fetch_page,
    )

    urls = crawl(
        "https://example.com/start",
        max_depth=0,
    )

    assert urls == {
        "https://example.com/start",
    }

    assert visited == [
        "https://example.com/start",
    ]

def test_crawl_skips_failed_pages(monkeypatch):
    pages = {
        "https://example.com/start": """
            <a href="/page1">Page 1</a>
            <a href="/broken">Broken</a>
        """,

        "https://example.com/page1": """
            <p>Page 1</p>
        """,
    }

    def fake_fetch_page(url):
        if url == "https://example.com/broken":
            raise requests.HTTPError("404 Not Found")

        return pages[url]

    monkeypatch.setattr(
        "recipe_importer.crawler.fetch_page",
        fake_fetch_page,
    )

    urls = crawl(
        "https://example.com/start",
        max_depth=1,
    )

    assert urls == {
        "https://example.com/start",
        "https://example.com/page1",
    }

def test_is_recipe_url():
    assert is_recipe_url(
        "https://example.com/recipes/chicken-parmesan"
    )

    assert is_recipe_url(
        "https://example.com/recipe/chicken-parmesan"
    )

    assert is_recipe_url(
            "https://example.com/Recipe/chicken-parmesan"
        )

    assert not is_recipe_url(
        "https://example.com/about"
    )

    assert not is_recipe_url(
        "https://example.com/contact"
    )

def test_filter_recipe_urls():
    urls = {
        "https://example.com/recipes/chicken",
        "https://example.com/recipes/pasta",
        "https://example.com/about",
        "https://example.com/contact",
        "https://example.com/recipe/soup",
    }

    filtered = filter_recipe_urls(urls)

    assert filtered == {
        "https://example.com/recipes/chicken",
        "https://example.com/recipes/pasta",
        "https://example.com/recipe/soup",
    }