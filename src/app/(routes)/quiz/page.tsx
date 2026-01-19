"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Button from "@/components/Button";
import Container from "@/components/Container";
import Stepper from "@/components/Stepper";

const QUESTIONS = [
  {
    id: "q1",
    title: "你能接受“单个产品”最多亏多少？",
    type: "single",
    options: [
      { value: "A", label: "≤ ¥3,000" },
      { value: "B", label: "¥3,000–¥10,000" },
      { value: "C", label: "¥10,000–¥50,000" },
      { value: "D", label: "¥50,000+" }
    ]
  },
  {
    id: "q2",
    title: "你现在最稳定的起量方式是？",
    type: "single",
    options: [
      { value: "A", label: "我自己拍（手机+简单剪辑）" },
      { value: "B", label: "少量达人合作（10–30人）" },
      { value: "C", label: "有稳定达人池 / MCN" },
      { value: "D", label: "主要靠投流放量" }
    ]
  },
  {
    id: "q3",
    title: "你更能接受哪种节奏？",
    type: "single",
    options: [
      { value: "A", label: "慢一点，但稳定" },
      { value: "B", label: "快速测试，能爆就爆" },
      { value: "C", label: "前期亏，后期放大" }
    ]
  },
  {
    id: "q4",
    title: "下面这些情况，你能处理哪些？（可多选）",
    type: "multi",
    options: [
      { value: "退货率偏高", label: "退货率偏高" },
      { value: "客户质疑/负面评论", label: "客户质疑/负面评论" },
      { value: "平台合规审查", label: "平台合规审查" },
      { value: "供应链不稳定", label: "供应链不稳定" }
    ]
  },
  {
    id: "q5",
    title: "你做 TikTok 最核心目标是？",
    type: "single",
    options: [
      { value: "A", label: "稳定赚钱（长期）" },
      { value: "B", label: "快速回本（短期）" },
      { value: "C", label: "榨取流量红利（快进快出）" },
      { value: "D", label: "给达人/账号找内容（内容优先）" }
    ]
  }
] as const;

const STORAGE_KEY = "tiktok-quiz-answers";

export default function QuizPage() {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string | string[]>>({});
  const current = QUESTIONS[step];

  const isValid = useMemo(() => {
    const value = answers[current.id];
    if (current.type === "multi") {
      return Array.isArray(value) && value.length > 0;
    }
    return typeof value === "string" && value.length > 0;
  }, [answers, current]);

  const handleSelect = (value: string) => {
    if (current.type === "multi") {
      const prev = (answers[current.id] as string[]) ?? [];
      const exists = prev.includes(value);
      const updated = exists ? prev.filter((item) => item !== value) : [...prev, value];
      setAnswers((prevState) => ({ ...prevState, [current.id]: updated }));
      return;
    }
    setAnswers((prevState) => ({ ...prevState, [current.id]: value }));
  };

  const handleNext = () => {
    if (!isValid) return;
    if (step < QUESTIONS.length - 1) {
      setStep((prev) => prev + 1);
      return;
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(answers));
    router.push("/result");
  };

  const handleBack = () => {
    if (step === 0) return;
    setStep((prev) => prev - 1);
  };

  return (
    <Container>
      <div className="flex flex-col gap-8">
        <div className="space-y-3">
          <h1 className="text-2xl font-semibold text-ink">5 步生成你的选品画像</h1>
          <Stepper current={step + 1} total={QUESTIONS.length} />
        </div>

        <div className="card space-y-4">
          <h2 className="text-lg font-semibold text-ink">{current.title}</h2>
          <div className="space-y-3">
            {current.options.map((option) => {
              const value = answers[current.id];
              const isChecked = current.type === "multi"
                ? Array.isArray(value) && value.includes(option.value)
                : value === option.value;
              return (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => handleSelect(option.value)}
                  className={
                    isChecked
                      ? "flex w-full items-center justify-between rounded-xl border border-blue-500 bg-blue-50 px-4 py-3 text-left text-sm font-medium text-ink"
                      : "flex w-full items-center justify-between rounded-xl border border-slate-200 bg-white px-4 py-3 text-left text-sm text-slate-600"
                  }
                >
                  <span>{option.label}</span>
                  {isChecked ? <span className="text-xs text-blue-600">已选</span> : null}
                </button>
              );
            })}
          </div>
        </div>

        <div className="flex items-center justify-between">
          <Button onClick={handleBack} className="bg-slate-200 text-slate-700 hover:bg-slate-300">
            上一步
          </Button>
          <Button disabled={!isValid} onClick={handleNext}>
            {step === QUESTIONS.length - 1 ? "生成我的专属选品池" : "下一步"}
          </Button>
        </div>
      </div>
    </Container>
  );
}
