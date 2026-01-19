export default function Stepper({ current, total }: { current: number; total: number }) {
  const items = Array.from({ length: total }, (_, index) => index + 1);
  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-slate-500">
        {current}/{total}
      </span>
      <div className="flex flex-1 items-center gap-1">
        {items.map((step) => (
          <span
            key={step}
            className={
              step <= current
                ? "h-2 flex-1 rounded-full bg-accent"
                : "h-2 flex-1 rounded-full bg-slate-200"
            }
          />
        ))}
      </div>
    </div>
  );
}
