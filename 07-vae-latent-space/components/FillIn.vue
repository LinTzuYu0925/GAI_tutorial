<script setup lang="ts">
import { computed } from 'vue'
import { getAnswer, setAnswer } from './answerStore'

const props = defineProps<{
  id: string
  hint?: string
  check?: boolean
}>()

const text = computed({
  get: () => getAnswer(props.id),
  set: value => setAnswer(props.id, value),
})

const checked = computed({
  get: () => getAnswer(props.id) === '1',
  set: value => setAnswer(props.id, value ? '1' : ''),
})

// Slidev ignores its arrow keys while an input has focus, so give focus back when the student is done.
function release(e: Event) {
  (e.target as HTMLElement).blur()
}

// Enter also confirms a word in Chinese input methods; that must not leave the cell.
function onEnter(e: KeyboardEvent) {
  if (!e.isComposing)
    release(e)
}
</script>

<template>
  <input
    v-if="check"
    v-model="checked"
    class="fill-check"
    type="checkbox"
    aria-label="完成"
    @change="release"
  >
  <input
    v-else
    v-model="text"
    class="fill-text"
    type="text"
    autocomplete="off"
    spellcheck="false"
    :placeholder="hint"
    :aria-label="hint || '答案'"
    @keydown.enter="onEnter"
    @keydown.esc="release"
  >
</template>

<style scoped>
.fill-text {
  display: block;
  width: 100%;
  height: 26px;
  padding: 0 6px;
  font: inherit;
  font-size: 16px;
  color: var(--text);
  background: var(--soft-blue);
  border: 1px solid transparent;
  border-radius: 4px;
  outline: none;
}
.fill-text::placeholder {
  color: var(--muted-text);
  font-style: italic;
  font-size: 14px;
  opacity: 1;
}
.fill-text:focus {
  background: #fff;
  border-color: var(--primary);
}
.fill-check {
  display: block;
  width: 20px;
  height: 20px;
  margin: 0 auto;
  cursor: pointer;
  accent-color: var(--primary);
}
</style>
