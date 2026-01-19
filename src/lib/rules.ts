import type { ProfileResult } from "./profile";

export type Tier = "forbidden" | "not_recommended" | "testable" | "recommended";

export type RuleCondition = {
  minRisk?: number;
  maxRisk?: number;
  minContent?: number;
  maxContent?: number;
  minScale?: number;
  maxScale?: number;
  minCash?: number;
  maxCash?: number;
  lifecycle?: Array<ProfileResult["vector"]["lifecycle"]>;
  segment?: ProfileResult["segment"][];
};

export type RuleFilter = {
  category?: string[];
  priceBand?: string[];
  contentType?: Array<"template_script" | "human_driven" | "ad_scalable">;
  lifecycleHint?: Array<"short" | "mid" | "long">;
  tagsAny?: string[];
  tagsAll?: string[];
  riskFlagsAny?: string[];
  priceUsdMin?: number;
  priceUsdMax?: number;
};

export type Rule = {
  id: string;
  tier: Tier;
  priority: number;
  condition: RuleCondition;
  filter: RuleFilter;
  public_reason_title: string;
  public_reason_detail: string;
  is_active: boolean;
};

export type Product = {
  id: string;
  is_active: boolean;
  title: string;
  category: string;
  price_usd: number;
  price_band: string;
  tags: string[];
  risk_flags: string[];
  content_type: "template_script" | "human_driven" | "ad_scalable";
  lifecycle_hint: "short" | "mid" | "long";
  supply_chain: {
    cost_usd?: number;
    weight_kg?: number;
    fragile?: boolean;
    battery?: boolean;
    hazmat?: boolean;
    lead_time_days?: number;
    moq?: number;
  } | null;
  content_play: {
    hook_type?: string;
    demo_style?: string;
    emotion_type?: string;
    ugc_difficulty?: string;
    script_template?: string;
  } | null;
};

export type ProductCard = {
  product_id: string;
  why_fit: string;
  first_test: string;
  stop_loss: string;
};

export type TierResult = {
  tier: Tier;
  products: Product[];
  reasons: Array<{ title: string; detail: string; priority: number }>;
};
