// Usage: node check-order.cjs <deck-dir>
// Prints slide order, eyebrow labels, chain/grid/table orders, and outline.md titles.
const fs = require("fs");
const path = require("path");
const dir = process.argv[2];
if (!dir) { console.error("usage: node check-order.cjs <deck-dir>"); process.exit(1); }
const read = (f) => fs.readFileSync(path.join(dir, f), "utf8");
const text = read("slides.md");
const lines = text.split("\n");

// split into slides (first block is global frontmatter + first slide frontmatter)
const slides = [];
let cur = [], inFence = false;
for (const l of lines) {
  if (/^```/.test(l)) inFence = !inFence;
  if (l === "---" && !inFence) { slides.push(cur); cur = []; } else cur.push(l);
}
slides.push(cur);
const real = slides.filter((s) => s.some((l) => /^# /.test(l)));

console.log("== Slides (number | eyebrow | title) ==");
const titles = [];
real.forEach((s, i) => {
  const eb = (s.find((l) => /class="eyebrow"/.test(l)) || "").replace(/<[^>]+>/g, "").trim();
  const title = (s.find((l) => /^# /.test(l)) || "").replace(/^# /, "");
  titles.push(title);
  console.log(String(i + 1).padStart(2), "|", eb.padEnd(34), "|", title);
});
const ebNums = real.map((s) => (s.find((l) => /class="eyebrow"/.test(l)) || "").replace(/<[^>]+>/g, "").trim().match(/^(\d\d) ·/)?.[1]).filter(Boolean);
let prev = -1, warn = [];
for (const n of ebNums) { const v = +n; if (v < prev) warn.push(`eyebrow number goes backwards: ${n} after ${prev}`); prev = v; }
console.log(warn.length ? "WARN " + warn.join("; ") : "eyebrow numbers: non-decreasing");

console.log("\n== Cover chain chips ==");
const chain = text.match(/<div class="chain[\s\S]*?<\/div>/);
if (chain) console.log([...chain[0].matchAll(/<span class="chip[^"]*">([^<]+)</g)].map((m) => m[1]).join(" -> "));

console.log("\n== Overview grid nodes ==");
const grid = text.match(/<div class="grid grid-cols-4[\s\S]*?<\/div>\n<\/div>|<div class="grid grid-cols-4[\s\S]*?\n<\/div>/);
if (grid) console.log([...grid[0].matchAll(/<div class="node">([^<]+)</g)].map((m) => m[1].trim()).join(" | "));

console.log("\n== Tables (first-column order) ==");
[...text.matchAll(/<table[\s\S]*?<\/table>/g)].forEach((t, i) => {
  const rows = [...t[0].matchAll(/<tr>\s*<td>(?:<strong>)?([^<]+)/g)].map((m) => m[1].trim());
  if (rows.length) console.log(`table ${i + 1}:`, rows.join(" | "));
});

if (fs.existsSync(path.join(dir, "outline.md"))) {
  console.log("\n== outline.md vs slides ==");
  const rows = read("outline.md").split("\n").filter((l) => /^\| \d+ \|/.test(l)).map((l) => l.split("|").map((c) => c.trim()));
  rows.forEach((r, i) => console.log(r[1].padStart(2), r[2] === (titles[i] || "") ? "ok      " : "MISMATCH", r[2]));
  if (rows.length !== titles.length) console.log(`WARN outline has ${rows.length} rows, slides has ${titles.length}`);
}
