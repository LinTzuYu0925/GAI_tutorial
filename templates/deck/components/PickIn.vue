<script setup lang="ts">
import { computed } from 'vue'
import { getAnswer, setAnswer } from './answerStore'

// A drop-down blank for practice pages where students choose instead of type.
// Options that start with a number ("4 · 現成可用") count as a score for <ScoreSum>.
const props = defineProps<{
  id: string
  options: string[]
  hint?: string
}>()

const value = computed({
  get: () => getAnswer(props.id),
  set: v => setAnswer(props.id, v),
})

// Slidev ignores its arrow keys while a control has focus, so give focus back after choosing.
function release(e: Event) {
  (e.target as HTMLElement).blur()
}
</script>

<template>
  <select
    v-model="value"
    class="pick"
    :class="{ empty: !value }"
    :aria-label="hint || '選擇'"
    @change="release"
  >
    <option value="" disabled>
      {{ hint || '選一個……' }}
    </option>
    <option v-for="o in options" :key="o" :value="o">
      {{ o }}
    </option>
  </select>
</template>

<style scoped>
.pick {
  display: block;
  width: 100%;
  height: 28px;
  padding: 0 4px;
  font: inherit;
  font-size: 16px;
  color: var(--text);
  background: var(--soft-blue);
  border: 1px solid transparent;
  border-radius: 4px;
  outline: none;
  cursor: pointer;
}
.pick.empty {
  color: var(--muted-text);
  font-style: italic;
}
.pick:focus {
  background: #fff;
  border-color: var(--primary);
}
.pick option {
  font-style: normal;
  color: var(--text);
}
</style>
