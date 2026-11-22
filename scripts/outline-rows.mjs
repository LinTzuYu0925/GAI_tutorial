// Print the outline.md slide table (section 3) generated from a deck's slides.md.
// Usage: node scripts/outline-rows.mjs <deck-dir> [--write]
// Columns: # | 標題 | 區塊（eyebrow） | 一句話重點（.takeaway） | ★/○/△ (first mark in the speaker note) | hostOnly
import { readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
const dir = process.argv[2]
const lines = readFileSync(join(dir, 'slides.md'), 'utf8').replace(/\r\n/g, '\n').split('\n')
const slides = []; let cur = []; let fence = false
for (const l of lines) { if (/^```/.test(l)) fence = !fence; if (l === '---' && !fence) { slides.push(cur); cur = [] } else cur.push(l) }
slides.push(cur)
const strip = (s) => s.replace(/<[^>]+>/g, '').replace(/\|/g, '｜').trim()
let n = 0; let hostNext = false
const out = ['| # | 標題 | 區塊 | 一句話重點 | ★/○/△ | 學員看得到 |', '|---|---|---|---|---|---|']
for (const s of slides) {
  const text = s.join('\n')
  if (/^hostOnly: true$/m.test(text) && !s.some((l) => /^# /.test(l))) { hostNext = true; continue }
  const t = s.find((l) => /^# /.test(l)); if (!t) continue
  n++
  const eb = strip(s.find((l) => /class="eyebrow"/.test(l)) || '')
  const tk = strip((text.match(/class="takeaway[^"]*">([\s\S]*?)<\/div>/) || [, ''])[1])
  const note = (text.match(/<!--\s*([★○△])/) || [, '?'])[1]
  out.push(`| ${n} | ${t.replace(/^# /, '')} | ${eb} | ${tk} | ${note} | ${hostNext ? '否（hostOnly）' : '是'} |`)
  hostNext = false
}
const table = out.join('\n')
// --write: replace the block between the slide-table markers in outline.md
if (process.argv.includes('--write')) {
  const f = join(dir, 'outline.md'); const o = readFileSync(f, 'utf8')
  const re = /<!-- slide-table:start -->[\s\S]*?<!-- slide-table:end -->/
  if (!re.test(o)) { console.error('outline.md has no slide-table markers'); process.exit(1) }
  writeFileSync(f, o.replace(re, () => `<!-- slide-table:start -->\n${table}\n<!-- slide-table:end -->`))
  console.log(`outline.md: ${n} slides written`)
} else console.log(table)
