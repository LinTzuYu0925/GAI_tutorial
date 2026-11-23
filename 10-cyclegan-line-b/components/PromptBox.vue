<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ inline?: boolean }>()

const body = ref<HTMLElement>()
const label = ref('複製')

// The clipboard API needs a secure page; fall back for anything else.
async function write(text: string) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  }
  catch {
    const area = document.createElement('textarea')
    area.value = text
    document.body.appendChild(area)
    area.select()
    const ok = document.execCommand('copy')
    area.remove()
    return ok
  }
}

// Text as the student sees it, with blanks replaced by what they typed. Line breaks in the source are written as <br>.
function read(node: Node): string {
  if (node.nodeType === Node.TEXT_NODE)
    return (node.textContent ?? '').replace(/[ \t\r\n]+/g, ' ')
  if (node instanceof HTMLBRElement)
    return '\n'
  if (node instanceof HTMLInputElement)
    return node.value.trim()
  return [...node.childNodes].map(read).join('')
}

function show(text: string) {
  label.value = text
  setTimeout(() => label.value = '複製', 1500)
}

async function copy(e: Event) {
  // A focused button also turns off Slidev's arrow keys.
  ;(e.currentTarget as HTMLElement).blur()
  if (!body.value)
    return
  const empty = [...body.value.querySelectorAll('input')].find(i => !i.value.trim())
  if (empty) {
    empty.focus()
    show('先填空格')
    return
  }
  const text = read(body.value).replace(/^ +| +$/gm, '').trim()
  if (await write(text))
    show('已複製 ✓')
}
</script>

<template>
  <div class="prompt-box" :class="{ 'prompt-box--inline': inline }">
    <div class="prompt-box__head">
      <span v-if="!inline">貼給 Agent</span>
      <button type="button" @click="copy">{{ label }}</button>
    </div>
    <div ref="body" class="prompt-box__body"><slot /></div>
  </div>
</template>

<style scoped>
.prompt-box {
  text-indent: 0;
  border: 1.5px solid var(--primary);
  border-radius: 8px;
  background: var(--soft-blue);
  overflow: hidden;
}
.prompt-box__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2px 4px 2px 10px;
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  background: var(--primary);
}
.prompt-box__head button {
  min-width: 76px;
  padding: 0 10px;
  font: inherit;
  color: var(--text);
  background: #fff;
  border: 0;
  border-radius: 4px;
  cursor: pointer;
}
.prompt-box__body {
  padding: 5px 10px;
  font-size: 15px;
  line-height: 1.45;
}
.prompt-box--inline {
  display: flex;
  flex-direction: row-reverse;
  align-items: center;
}
.prompt-box--inline .prompt-box__head {
  background: transparent;
}
.prompt-box--inline .prompt-box__head button {
  color: #fff;
  background: var(--primary);
}
.prompt-box--inline .prompt-box__body {
  flex: 1;
  padding: 2px 10px;
}
</style>
