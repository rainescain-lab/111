"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import Container from "@/components/Container";
import Button from "@/components/Button";
import { supabase } from "@/lib/supabaseClient";
import type { Product, ProductCard } from "@/lib/rules";

export default function ProductDetailPage() {
  const params = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [card, setCard] = useState<ProductCard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      if (!params?.id) return;
      setLoading(true);
      const [{ data: productData, error: productError }, { data: cardData, error: cardError }] =
        await Promise.all([
          supabase.from("products").select("*").eq("id", params.id).single(),
          supabase.from("product_cards").select("*").eq("product_id", params.id).single()
        ]);

      if (productError || cardError) {
        setError("获取产品失败，请检查 Supabase 数据。");
        setLoading(false);
        return;
      }

      setProduct(productData as Product);
      setCard(cardData as ProductCard);
      setLoading(false);
    };
    load();
  }, [params]);

  if (loading) {
    return (
      <Container>
        <div className="card text-sm text-slate-500">加载产品详情中…</div>
      </Container>
    );
  }

  if (error || !product || !card) {
    return (
      <Container>
        <div className="card space-y-3">
          <p className="text-sm text-red-600">{error ?? "未找到产品"}</p>
          <Link href="/result">
            <Button>返回结果页</Button>
          </Link>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <div className="space-y-6">
        <section className="card space-y-2">
          <h1 className="text-2xl font-semibold text-ink">{product.title}</h1>
          <p className="text-sm text-slate-600">
            {product.category} · {product.price_band} · ${product.price_usd}
          </p>
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
        </section>

        <section className="card space-y-2">
          <h2 className="section-title">为什么适合你</h2>
          <p className="text-sm text-slate-600">{card.why_fit}</p>
        </section>

        <section className="card space-y-2">
          <h2 className="section-title">第一轮怎么测</h2>
          <p className="text-sm text-slate-600">{card.first_test}</p>
        </section>

        <section className="card space-y-2">
          <h2 className="section-title">什么时候该停</h2>
          <p className="text-sm text-slate-600">{card.stop_loss}</p>
        </section>

        <Link href="/result">
          <Button>返回结果页</Button>
        </Link>
      </div>
    </Container>
  );
}
