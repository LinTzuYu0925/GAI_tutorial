<script setup lang="ts">
import { computed } from 'vue'
import { getAnswer, setAnswer } from './answerStore'

const props = defineProps<{
  id: string
  hint: string
}>()

const text = computed({
  get: () => getAnswer(props.id),
  set: value => setAnswer(props.id, value),
})

// Wide enough for the hint, and grows with what the student types.
const width = computed(() => `calc(${Math.max(props.hint.length, text.value.length + 1)}em + 14px)`)

// Slidev ignores its arrow keys while an input has focus, so give focus back when the student is done.
function release(e: Event) {
  (e.target as HTMLElement).blur()
}

// Enter also confirms a word in Chinese input methods; that must not leave the blank.
function onEnter(e: KeyboardEvent) {
  if (!e.isComposing)
    release(e)
}
</script>

<template>
  <input
    v-model="text"
    class="prompt-blank"
    type="text"
    autocomplete="off"
    spellcheck="false"
    :placeholder="hint"
    :aria-label="hint"
    :style="{ width }"
    @keydown.enter="onEnter"
    @keydown.esc="release"
  >
</template>

<style scoped>
.prompt-blank {
  display: inline-block;
  max-width: 100%;
  height: 22px;
  margin: 0 2px;
  padding: 0 6px;
  font: inherit;
  color: var(--text);
  vertical-align: baseline;
  background: #fff;
  border: 1px dashed var(--primary);
  border-radius: 4px;
  outline: none;
}
.prompt-blank::placeholder {
  color: var(--muted-text);
  font-style: italic;
  font-size: 13px;
  opacity: 1;
}
.prompt-blank:focus {
  border-style: solid;
}
</style>
