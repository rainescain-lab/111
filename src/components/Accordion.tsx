"use client";

import { useState } from "react";

export default function Accordion({
  title,
  defaultOpen = false,
  children
}: {
  title: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="rounded-2xl border border-slate-200 bg-white">
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="flex w-full items-center justify-between px-5 py-4 text-left"
      >
        <span className="text-base font-semibold text-ink">{title}</span>
        <span className="text-sm text-slate-500">{open ? "收起" : "展开"}</span>
      </button>
      {open ? <div className="border-t border-slate-200 px-5 py-4">{children}</div> : null}
    </div>
  );
}
