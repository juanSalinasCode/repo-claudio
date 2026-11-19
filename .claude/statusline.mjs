#!/usr/bin/env node
// Barra de estado de Claude Code: muestra uso y límite disponible tras cada mensaje.
// Claude Code envía un JSON por stdin; este script imprime una línea resumida.

let raw = "";
process.stdin.on("data", (c) => (raw += c));
process.stdin.on("end", () => {
  let d = {};
  try {
    d = JSON.parse(raw);
  } catch {
    console.log("uso: sin datos");
    return;
  }

  const pct = (n) => (typeof n === "number" ? `${Math.round(n)}%` : "?");
  const bar = (n) => {
    if (typeof n !== "number") return "";
    const filled = Math.max(0, Math.min(10, Math.round(n / 10)));
    return "▰".repeat(filled) + "▱".repeat(10 - filled) + " ";
  };
  const color = (n, s) => {
    if (typeof n !== "number") return s;
    const code = n >= 90 ? 31 : n >= 70 ? 33 : 32; // rojo / amarillo / verde
    return `\x1b[${code}m${s}\x1b[0m`;
  };
  const resetIn = (t) => {
    if (!t) return "";
    const ms = (typeof t === "number" ? (t < 1e12 ? t * 1000 : t) : Date.parse(t)) - Date.now();
    if (!(ms > 0)) return "";
    const h = Math.floor(ms / 3.6e6);
    const m = Math.floor((ms % 3.6e6) / 6e4);
    return h >= 24 ? ` (reinicia en ${Math.floor(h / 24)}d ${h % 24}h)` : ` (reinicia en ${h}h ${m}m)`;
  };

  const parts = [];
  if (d.model?.display_name) parts.push(d.model.display_name);

  const rl = d.rate_limits || {};
  const five = rl.five_hour;
  const week = rl.seven_day;
  if (five) {
    const u = five.used_percentage;
    parts.push(color(u, `5h ${bar(u)}${pct(u)} usado`) + resetIn(five.resets_at));
  }
  if (week) {
    const u = week.used_percentage;
    parts.push(color(u, `semana ${pct(u)} usado`) + resetIn(week.resets_at));
  }

  const ctx = d.context_window?.used_percentage;
  if (typeof ctx === "number") parts.push(color(ctx, `contexto ${pct(ctx)}`));

  const cost = d.cost?.total_cost_usd;
  if (typeof cost === "number") parts.push(`sesión ~$${cost.toFixed(2)} equiv.`);

  console.log(parts.join(" │ ") || "uso: sin datos");
});
