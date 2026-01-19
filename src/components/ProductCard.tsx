import Link from "next/link";
import type { Product } from "@/lib/rules";

export default function ProductCard({ product }: { product: Product }) {
  return (
    <Link
      href={`/product/${product.id}`}
      className="card flex flex-col gap-4 transition hover:border-blue-200"
    >
      <div className="space-y-1">
        <h3 className="text-lg font-semibold text-ink">{product.title}</h3>
        <p className="text-sm text-slate-500">
          {product.category} · {product.price_band} · ${product.price_usd}
        </p>
      </div>
      <div className="space-y-2 text-sm text-slate-600">
        <div>
          <span className="font-medium text-slate-700">内容打法：</span>
          {product.content_play?.hook_type ?? "未定义"} / {product.content_play?.demo_style ?? "未定义"}
        </div>
        <div>
          <span className="font-medium text-slate-700">供应链要点：</span>
          成本 ${product.supply_chain?.cost_usd ?? "-"} · 重量 {product.supply_chain?.weight_kg ?? "-"}
          kg · MOQ {product.supply_chain?.moq ?? "-"}
        </div>
      </div>
      <div className="flex flex-wrap gap-2">
        {product.tags?.map((tag) => (
          <span key={tag} className="badge-muted">
            {tag}
          </span>
        ))}
        {product.risk_flags?.map((flag) => (
          <span key={flag} className="badge-danger">
            {flag}
          </span>
        ))}
      </div>
    </Link>
  );
}
