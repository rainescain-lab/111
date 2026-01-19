import Link from "next/link";
import Button from "@/components/Button";
import Container from "@/components/Container";

export default function HomePage() {
  return (
    <Container>
      <div className="flex flex-col gap-10">
        <section className="space-y-4">
          <span className="badge">TikTok 选品决策系统 · MVP</span>
          <h1 className="text-3xl font-bold text-ink md:text-4xl">用最小成本做出靠谱选品决策</h1>
          <p className="text-base text-slate-600">
            不是爆品榜，而是一个「过滤器」：用你的能力与风险偏好，过滤掉不适合的产品池，
            把时间花在更可能成功的方向上。
          </p>
        </section>

        <section className="card space-y-4">
          <h2 className="section-title">反常识解释：这不是爆品榜</h2>
          <p className="text-sm text-slate-600">
            选品失败的原因往往不是没有“热点”，而是人货不匹配。系统只做一件事：
            识别你当前能力下的“可承受风险”，并给出可测试的产品池。
          </p>
        </section>

        <section className="card space-y-4">
          <h2 className="section-title">四维评估</h2>
          <ul className="grid gap-3 text-sm text-slate-600 md:grid-cols-2">
            <li>可复制性：你的内容打法是否能规模化复制。</li>
            <li>情绪牵引：产品是否能触发强情绪或动机。</li>
            <li>放量能力：你有没有能力放大达人/投流。</li>
            <li>风险承受：亏损、合规、供应链波动的承受度。</li>
          </ul>
        </section>

        <section className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h3 className="text-lg font-semibold text-ink">3 分钟生成专属选品池</h3>
            <p className="text-sm text-slate-600">回答 5 个问题，立即看到推荐层级。</p>
          </div>
          <Link href="/quiz">
            <Button>开始测试</Button>
          </Link>
        </section>
      </div>
    </Container>
  );
}
