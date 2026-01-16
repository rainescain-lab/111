from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class PriceRange:
    min_price: int
    max_price: int


def split_price_range(price_range: PriceRange) -> Tuple[PriceRange, PriceRange]:
    mid = (price_range.min_price + price_range.max_price) // 2
    left = PriceRange(price_range.min_price, mid)
    right = PriceRange(mid + 1, price_range.max_price)
    return left, right


def should_split(price_range: PriceRange, min_bucket: int) -> bool:
    return (price_range.max_price - price_range.min_price) > min_bucket


def build_initial_ranges(price_min: int, price_max: int) -> List[PriceRange]:
    return [PriceRange(price_min, price_max)]
