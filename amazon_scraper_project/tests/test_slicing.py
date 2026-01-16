from amazon_scraper.slicer import PriceRange, should_split, split_price_range


def test_should_split() -> None:
    assert should_split(PriceRange(0, 100), 10) is True
    assert should_split(PriceRange(0, 5), 10) is False


def test_split_price_range() -> None:
    left, right = split_price_range(PriceRange(0, 100))
    assert left.min_price == 0
    assert left.max_price <= right.min_price
