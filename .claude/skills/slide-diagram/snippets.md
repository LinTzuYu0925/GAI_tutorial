# Snippets for slide-diagram

Copy into the deck that needs them. Colors are the deck tokens (`style.css`). Replace labels with Traditional Chinese content.

## 1. Arrow markers that do not scale with the stroke

```html
<svg width="868" height="300" viewBox="0 0 868 300" role="img" aria-label="describe the diagram in words">
  <defs>
    <marker id="uniq-gray" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto">
      <path d="M0,1 L11,6 L0,11 z" fill="#4b5563"/>
    </marker>
  </defs>
  <line x1="85" y1="62" x2="325" y2="62" stroke="#4b5563" stroke-width="1.8" marker-end="url(#uniq-gray)"/>
</svg>
```

Rename `uniq-` per slide (ids are global in the page). Make one marker per color (gray `#4b5563`, blue `#2457c5`, green `#16847a`, orange `#b85c20`, dark `#172033`).

## 2. Thick "repeat" arrow with a separate head

```html
<path d="M618,256 V288 H290 V272" fill="none" stroke="#172033" stroke-width="4.5" stroke-linejoin="round"/>
<polygon points="290,259 280,273 300,273" fill="#172033"/>
```

The line ends at the head's base; the head touches the box edge without covering any label.

## 3. Sequence diagram generator (Node)

Generate the SVG from data, then paste into the slide. Columns are lifelines; rows are arrows.

```js
const cx = [85, 325, 565, 785];                      // user, platform (Agent), model, tool
const rows = [                                       // [from, to, label, tone]
  [0, 1, "1　幫我看 app.py 為什麼壞了", "gray"],
  [1, 2, "2　問題＋可用工具清單", "gray"],
  [2, 1, "3　呼叫 read_file（app.py）", "blue"],     // model only outputs a call
  [1, 3, "4　真正執行 read_file", "green"],          // the platform really executes
  [3, 1, "5　結果：app.py 的內容", "gray"],
  [1, 2, "6　工具的執行結果", "gray"],
  [2, 1, "7　整理成一句話", "blue"],
  [1, 0, "8　第 12 行少了冒號", "gray"],
];
// y = 62 + 31 * i; label above the line, centered, white halo:
// <text ... stroke="#fff" stroke-width="4" paint-order="stroke" style="font-size:14px">
```

Header boxes: orange user, green platform, blue model, gray tool. Dashed lifelines in each role's color.

## 4. Windows-style chat window (HTML)

```html
<div style="border:1px solid #9aa5b4; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(23,32,51,0.18); background:#fff">
  <div style="display:flex; align-items:center; justify-content:space-between; background:#f3f3f3; border-bottom:1px solid var(--border); height:30px; padding-left:10px; font-size:14px">
    <span style="display:flex; align-items:center; gap:6px"><span style="display:inline-block; width:12px; height:12px; border-radius:6px; background:var(--primary)"></span>AI 助理</span>
    <svg width="138" height="30" viewBox="0 0 138 30" aria-hidden="true"><g stroke="#172033" stroke-width="1.2" fill="none"><path d="M18,15 H28"/><rect x="65" y="10" width="10" height="10"/><path d="M111,10 L121,20 M121,10 L111,20"/></g></svg>
  </div>
  <div class="flex flex-col gap-2" style="padding:10px 12px; font-size:18px; line-height:1.4">
    <div style="align-self:flex-end; background:var(--soft-blue); border-radius:16px; padding:4px 14px">user message</div>
    <div>AI reply as plain text on the left</div>
  </div>
</div>
```

For an agent work log add a muted line `Worked for 47s ∧` and one row per tool call: icon, English log text from the real product, and the model's thought in blue on the right.

## 5. Context cup component (`components/ContextCup.vue`)

Props: `blocks` (`{ text, tone, h }`, bottom block first), `width`, `height`, `fontSize`, `caption`. Tones: `gray`, `teal`, `blue`, `warm`, `ghost` (dashed). The cup is open at the top; blocks stack upward; leave headroom to show the limit. Never rename a tone key to `text`.

```html
<ContextCup :blocks="[{text:'AGENTS.md（規則檔）',tone:'gray',h:30},{text:'前面每一輪的對話',tone:'teal',h:30},{text:'你這次的 prompt',tone:'blue',h:30}]" :width="290" :height="150" :fontSize="14" caption="規則檔放在 Context 最前面" />
```

## 6. Equal-width output column

When rows have inputs on the left and outputs on the right, give every output box the same fixed width, for example `style="width:300px"`, and keep the input boxes `flex-1`.
