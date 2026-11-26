// Build slides.print.md: a copy of slides.md without the slides marked `hostOnly: true`
// in their frontmatter (answer pages and the closing 下一步 preview, which only the hosted deck shows).
import { readFileSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')
let text = readFileSync(join(root, 'slides.md'), 'utf8').replace(/\r\n/g, '\n')
const marker = '\n---\nhostOnly: true\n---\n'
let removed = 0
for (let i = text.indexOf(marker); i >= 0; i = text.indexOf(marker)) {
  const end = text.indexOf('\n---\n', i + marker.length)
  // A hostOnly slide may be the last one (the 下一步 preview): then cut to the end of the file.
  text = end < 0 ? text.slice(0, i) + '\n' : text.slice(0, i) + text.slice(end)
  removed++
}
writeFileSync(join(root, 'slides.print.md'), text)
console.log(`slides.print.md written (${removed} hostOnly slide(s) removed)`)
