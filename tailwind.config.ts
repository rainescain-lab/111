import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0f172a",
        mute: "#64748b",
        canvas: "#f8fafc",
        accent: "#2563eb",
        accentSoft: "#dbeafe",
        success: "#16a34a",
        warning: "#f97316",
        danger: "#dc2626"
      }
    }
  },
  plugins: []
};

export default config;
