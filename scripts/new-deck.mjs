// Create a new deck from templates/deck.  Usage: npm run new-deck -- 03-vae "VAE 標題" "單元 03"
// Copies the template (CLAUDE.md: decks never import from each other, so each deck gets its own copy),
// then fills __DECK__, __TITLE__ and __UNIT__. Run `npm install` at the root afterwards so the
// workspace picks the deck up.
import { cpSync, existsSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const [deck, title = '標題', unit = '單元'] = process.argv.slice(2)
if (!deck || !/^\d\d[a-z]?-[a-z0-9-]+$/.test(deck)) {
  console.error('usage: npm run new-deck -- NN-kebab-topic ["標題"] ["單元 NN"]')
  process.exit(1)
}
const dest = join(root, deck)
if (existsSync(dest)) { console.error(`${deck} already exists`); process.exit(1) }
cpSync(join(root, 'templates', 'deck'), dest, { recursive: true })
const walk = (d) => readdirSync(d).flatMap((f) => (statSync(join(d, f)).isDirectory() ? walk(join(d, f)) : [join(d, f)]))
for (const f of walk(dest).filter((f) => /\.(md|json|mjs)$/.test(f))) {
  const t = readFileSync(f, 'utf8')
  const u = t.replaceAll('__DECK__', deck).replaceAll('__TITLE__', title).replaceAll('__UNIT__', unit)
  if (u !== t) writeFileSync(f, u)
}
console.log(`${deck}/ created. Next: npm install (root), then cd ${deck} && npm run dev`)
