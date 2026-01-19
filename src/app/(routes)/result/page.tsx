"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import Container from "@/components/Container";
import Accordion from "@/components/Accordion";
import ProductCard from "@/components/ProductCard";
import Button from "@/components/Button";
import { buildProfile, type QuizAnswers } from "@/lib/profile";
import { supabase } from "@/lib/supabaseClient";
import { runRecommendation } from "@/lib/recommend";
import type { Product, Rule, Tier, TierResult } from "@/lib/rules";

const STORAGE_KEY = "tiktok-quiz-answers";

const tierMeta: Record<Tier, { title: string; description: string }> = {
  recommended: {
    title: "推荐池",
    description: "与你当前能力匹配度最高，优先关注。"
  },
  testable: {
    title: "可测试池",
    description: "可控风险内值得小批量测试。"
  },
  not_recommended: {
    title: "不推荐池",
    description: "可能会拖慢节奏或消耗资源。"
  },
  forbidden: {
    title: "强劝退池",
    description: "风险过高或不适合当前阶段。"
  }
};

export default function ResultPage() {
  const [answers, setAnswers] = useState<QuizAnswers | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [rules, setRules] = useState<Rule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      setLoading(false);
      return;
    }
    try {
      const parsed = JSON.parse(stored) as QuizAnswers;
      if (!parsed.q1 || !parsed.q2 || !parsed.q3 || !parsed.q4 || !parsed.q5 || !Array.isArray(parsed.q4)) {
        setError("答题结果不完整，请重新填写问卷。");
        setLoading(false);
        return;
      }
      setAnswers(parsed);
    } catch (err) {
      setError("答题结果解析失败，请重新填写问卷。");
    }
  }, []);

  useEffect(() => {
    const load = async () => {
      if (!answers) return;
      setLoading(true);
      const [{ data: productData, error: productError }, { data: ruleData, error: ruleError }] =
        await Promise.all([
          supabase.from("products").select("*").eq("is_active", true),
          supabase.from("rules").select("*").eq("is_active", true)
        ]);

      if (productError || ruleError) {
        setError("数据加载失败，请检查 Supabase 配置。");
        setLoading(false);
        return;
      }

      setProducts((productData as Product[]) ?? []);
      setRules((ruleData as Rule[]) ?? []);
      setLoading(false);
    };
    load();
  }, [answers]);

  const profile = useMemo(() => (answers ? buildProfile(answers) : null), [answers]);
  const tiers = useMemo<TierResult[]>(() => {
    if (!profile) return [];
    return runRecommendation(profile, rules, products);
  }, [profile, rules, products]);

  if (loading) {
    return (
      <Container>
        <div className="card text-sm text-slate-500">正在生成结果…</div>
      </Container>
    );
  }

  if (error) {
    return (
      <Container>
        <div className="card space-y-3">
          <p className="text-sm text-red-600">{error}</p>
          <Link href="/quiz">
            <Button>重新答题</Button>
          </Link>
        </div>
      </Container>
    );
  }

  if (!answers) {
    return (
      <Container>
        <div className="card space-y-3">
          <h2 className="text-lg font-semibold text-ink">还没有答题记录</h2>
          <p className="text-sm text-slate-600">请先完成 5 个问题，生成你的选品画像。</p>
          <Link href="/quiz">
            <Button>去答题</Button>
          </Link>
        </div>
      </Container>
    );
  }

  if (products.length === 0 || rules.length === 0) {
    return (
      <Container>
        <div className="card space-y-3">
          <h2 className="text-lg font-semibold text-ink">暂无数据</h2>
          <p className="text-sm text-slate-600">
            Supabase 暂无产品或规则，请导入 seed 数据后刷新页面。
          </p>
          <Link href="/">
            <Button>返回首页</Button>
          </Link>
        </div>
      </Container>
    );
  }

  return (
    <Container>
      <div className="flex flex-col gap-8">
        <section className="card space-y-3">
          <h1 className="text-2xl font-semibold text-ink">你的选品画像已生成</h1>
          <p className="text-sm text-slate-600">
            风险承受度 {profile?.vector.risk} · 内容能力 {profile?.vector.content} · 放量能力{" "}
            {profile?.vector.scale} · 现金流 {profile?.vector.cash}
          </p>
          <div className="flex flex-wrap gap-2">
            <span className="badge">生命周期：{profile?.vector.lifecycle}</span>
            <span className="badge-muted">Segment：{profile?.segment}</span>
          </div>
        </section>

        {tiers.map((tier) => {
          const meta = tierMeta[tier.tier];
          const defaultOpen = tier.tier === "recommended" || tier.tier === "testable";
          const reasons = tier.reasons;
          const mainReason = reasons[0];
          const extraReasons = reasons.slice(1);
          return (
            <Accordion key={tier.tier} title={`${meta.title} (${tier.products.length})`} defaultOpen={defaultOpen}>
              <div className="space-y-4">
                <p className="text-sm text-slate-600">{meta.description}</p>
                {mainReason ? (
                  <div className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm">
                    <p className="font-medium text-ink">{mainReason.title}</p>
                    <p className="text-slate-600">{mainReason.detail}</p>
                    {extraReasons.length > 0 ? (
                      <details className="mt-2 text-slate-500">
                        <summary className="cursor-pointer text-xs">还有 {extraReasons.length} 条原因</summary>
                        <ul className="mt-2 space-y-1 text-xs">
                          {extraReasons.map((reason) => (
                            <li key={reason.title + reason.priority}>
                              <span className="font-medium text-slate-700">{reason.title}：</span>
                              {reason.detail}
                            </li>
                          ))}
                        </ul>
                      </details>
                    ) : null}
                  </div>
                ) : (
                  <p className="text-xs text-slate-400">暂无规则原因。</p>
                )}
                {tier.products.length === 0 ? (
                  <p className="text-sm text-slate-500">暂无产品匹配。</p>
                ) : (
                  <div className="grid gap-4 md:grid-cols-2">
                    {tier.products.map((product) => (
                      <ProductCard key={product.id} product={product} />
                    ))}
                  </div>
                )}
              </div>
            </Accordion>
          );
        })}
      </div>
    </Container>
  );
}
