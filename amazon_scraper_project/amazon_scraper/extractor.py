from __future__ import annotations

from typing import Any, Dict, List

from playwright.sync_api import Error as PlaywrightError, Page


CARD_JS = """
() => {
  const cards = Array.from(
    document.querySelectorAll(
      'div.s-main-slot div[data-component-type="s-search-result"][data-asin]:not([data-asin=""])'
    )
  );
  const cleanText = (value) => value.replace(/\\s+/g, " ").trim();
  const scrubAdText = (value) =>
    value
      .replace(/sponsored/gi, "")
      .replace(/you['’]re seeing this ad/gi, "")
      .replace(/leave ad feedback/gi, "")
      .replace(/learn more/gi, "")
      .replace(/why this ad\\??/gi, "")
      .replace(/report this ad\\??/gi, "")
      .replace(/\\s+/g, " ")
      .trim();

  return cards.map((el, index) => {
    const pickText = (node) => node ? node.textContent.trim() : "";
    const primaryTitleNode = el.querySelector("h2 a span");
    const fallbackTitleNodes = Array.from(
      el.querySelectorAll(
        "span.a-size-base-plus.a-color-base.a-text-normal, " +
          "span.a-size-medium.a-color-base.a-text-normal, " +
          "[data-cy='title-recipe'] span, " +
          "h2"
      )
    );
    const titleCandidates = [];
    if (primaryTitleNode && primaryTitleNode.textContent) {
      titleCandidates.push(primaryTitleNode.textContent);
    }
    for (const node of fallbackTitleNodes) {
      if (node && node.textContent) {
        titleCandidates.push(node.textContent);
      }
    }
    const cleanedCandidates = titleCandidates
      .map((text) => scrubAdText(cleanText(text || "")))
      .filter((text) => text.length > 0);
    const title =
      cleanedCandidates.find((text) => text.length >= 8) ||
      cleanedCandidates.sort((a, b) => b.length - a.length)[0] ||
      "";

    const linkEl =
      el.querySelector("a[href*='/dp/']") ||
      el.querySelector("a[href*='/gp/']");
    const allLinks = linkEl ? [linkEl] : Array.from(el.querySelectorAll("a[href]"));
    const hrefMatch = allLinks.find((node) => {
      const href = node.getAttribute("href") || "";
      return href.includes("/dp/") || href.includes("/gp/");
    });

    const priceEl = el.querySelector(".a-price .a-offscreen");
    const ratingEl = el.querySelector("span.a-icon-alt");
    const reviewsEl =
      el.querySelector("span.s-underline-text") ||
      el.querySelector("a[href*='customerReviews'] span") ||
      el.querySelector("span[aria-label$='ratings'], span[aria-label$='rating']");
    const asin = el.getAttribute("data-asin") || "";
    const url = hrefMatch ? hrefMatch.href : "";
    const sponsoredLabel =
      el.querySelector("[aria-label*='Sponsored'], [aria-label*='sponsored']") ||
      Array.from(el.querySelectorAll("span")).find(
        (node) => cleanText(node.textContent || "") === "Sponsored"
      );

    return {
      rank_in_page: index + 1,
      asin,
      title,
      url,
      price_text: pickText(priceEl),
      rating_text: pickText(ratingEl),
      reviews_text: pickText(reviewsEl),
      is_sponsored: Boolean(sponsoredLabel),
    };
  });
}
"""


def extract_cards(page: Page) -> List[Dict[str, Any]]:
    try:
        return page.evaluate(CARD_JS)
    except PlaywrightError:
        return []
