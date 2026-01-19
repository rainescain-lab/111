import type { ProfileResult } from "./profile";
import type { Product, Rule, Tier, TierResult } from "./rules";

const tierWeight: Record<Tier, number> = {
  forbidden: 4,
  not_recommended: 3,
  testable: 2,
  recommended: 1
};

const matchCondition = (profile: ProfileResult, condition: Rule["condition"]) => {
  const { vector, segment } = profile;
  if (condition.minRisk !== undefined && vector.risk < condition.minRisk) return false;
  if (condition.maxRisk !== undefined && vector.risk > condition.maxRisk) return false;
  if (condition.minContent !== undefined && vector.content < condition.minContent) return false;
  if (condition.maxContent !== undefined && vector.content > condition.maxContent) return false;
  if (condition.minScale !== undefined && vector.scale < condition.minScale) return false;
  if (condition.maxScale !== undefined && vector.scale > condition.maxScale) return false;
  if (condition.minCash !== undefined && vector.cash < condition.minCash) return false;
  if (condition.maxCash !== undefined && vector.cash > condition.maxCash) return false;
  if (condition.lifecycle && !condition.lifecycle.includes(vector.lifecycle)) return false;
  if (condition.segment && !condition.segment.includes(segment)) return false;
  return true;
};

const matchFilter = (product: Product, filter: Rule["filter"]) => {
  if (!product.is_active) return false;
  if (filter.category && !filter.category.includes(product.category)) return false;
  if (filter.priceBand && !filter.priceBand.includes(product.price_band)) return false;
  if (filter.contentType && !filter.contentType.includes(product.content_type)) return false;
  if (filter.lifecycleHint && !filter.lifecycleHint.includes(product.lifecycle_hint)) return false;
  if (filter.priceUsdMin !== undefined && product.price_usd < filter.priceUsdMin) return false;
  if (filter.priceUsdMax !== undefined && product.price_usd > filter.priceUsdMax) return false;
  if (filter.tagsAny && !filter.tagsAny.some((tag) => product.tags?.includes(tag))) return false;
  if (filter.tagsAll && !filter.tagsAll.every((tag) => product.tags?.includes(tag))) return false;
  if (filter.riskFlagsAny && !filter.riskFlagsAny.some((flag) => product.risk_flags?.includes(flag))) {
    return false;
  }
  return true;
};

export function runRecommendation(
  profile: ProfileResult,
  rules: Rule[],
  products: Product[]
): TierResult[] {
  const tiers: Record<Tier, TierResult> = {
    forbidden: { tier: "forbidden", products: [], reasons: [] },
    not_recommended: { tier: "not_recommended", products: [], reasons: [] },
    testable: { tier: "testable", products: [], reasons: [] },
    recommended: { tier: "recommended", products: [], reasons: [] }
  };

  const productTier = new Map<string, Tier>();
  const sortedRules = [...rules].filter((rule) => rule.is_active).sort((a, b) => a.priority - b.priority);

  sortedRules.forEach((rule) => {
    if (!matchCondition(profile, rule.condition)) return;
    const matchedProducts = products.filter((product) => matchFilter(product, rule.filter));

    if (matchedProducts.length === 0) return;

    tiers[rule.tier].reasons.push({
      title: rule.public_reason_title,
      detail: rule.public_reason_detail,
      priority: rule.priority
    });

    matchedProducts.forEach((product) => {
      const existingTier = productTier.get(product.id);
      if (!existingTier || tierWeight[rule.tier] > tierWeight[existingTier]) {
        productTier.set(product.id, rule.tier);
      }
    });
  });

  productTier.forEach((tier, productId) => {
    const product = products.find((item) => item.id === productId);
    if (!product) return;
    tiers[tier].products.push(product);
  });

  (Object.keys(tiers) as Tier[]).forEach((tier) => {
    tiers[tier].products.sort((a, b) => a.title.localeCompare(b.title, "zh-Hans-CN"));
    tiers[tier].reasons.sort((a, b) => a.priority - b.priority);
  });

  return Object.values(tiers);
}
