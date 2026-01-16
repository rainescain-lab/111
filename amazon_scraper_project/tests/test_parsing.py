import re


def extract_asin(url: str) -> str | None:
    match = re.search(r"/dp/([A-Z0-9]{10})", url)
    return match.group(1) if match else None


def test_extract_asin_from_dp_url() -> None:
    url = "https://www.amazon.com/dp/B08N5WRWNW?ref=abc"
    assert extract_asin(url) == "B08N5WRWNW"


def test_extract_asin_missing() -> None:
    url = "https://www.amazon.com/gp/product/something"
    assert extract_asin(url) is None
