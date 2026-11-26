<script setup lang="ts">
import { computed } from 'vue'
import { getAnswer, setAnswer } from './answerStore'

// One clickable multiple-choice question for 隨堂檢核.
// `answer` is the index of the correct option; `why[i]` explains option i
// (shown when it is chosen); `explain` is shown once the right answer is chosen.
const props = defineProps<{
  id: string
  n?: number
  options: string[]
  answer: number
  why?: string[]
  explain?: string
}>()

const letters = ['A', 'B', 'C', 'D', 'E']
const chosen = computed(() => {
  const v = getAnswer(props.id)
  return v === '' ? -1 : Number(v)
})
const correct = computed(() => chosen.value === props.answer)

function pick(i: number, e: Event) {
  setAnswer(props.id, String(i))
  ;(e.currentTarget as HTMLElement).blur()
}
</script>

<template>
  <div class="mcq-q">
    <div class="stem">
      <span v-if="n" class="qn">{{ n }}.</span><slot />
    </div>
    <div class="opts">
      <button
        v-for="(o, i) in options"
        :key="i"
        type="button"
        class="opt"
        :class="{
          right: chosen !== -1 && i === answer && correct,
          wrong: i === chosen && !correct,
        }"
        @click="pick(i, $event)"
      >
        <b>{{ letters[i] }}</b> {{ o }}
        <span v-if="i === chosen" class="mark">{{ correct ? '✓' : '✗' }}</span>
      </button>
    </div>
    <div v-if="chosen !== -1" class="fb" :class="correct ? 'fb-right' : 'fb-wrong'">
      <template v-if="correct">
        <b>答對了！</b>{{ explain }}
      </template>
      <template v-else>
        <b>再想想：</b>{{ why?.[chosen] ?? '這個選項不對。' }}
      </template>
    </div>
  </div>
</template>

<style scoped>
.mcq-q { margin-bottom: 18px; }
.stem { font-size: 19px; line-height: 1.4; }
.qn { font-weight: 700; margin-right: 6px; }
.opts { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 10px; margin-top: 6px; }
.opt {
  text-align: left;
  font: inherit;
  font-size: 17px;
  line-height: 1.3;
  padding: 5px 10px;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  background: #fff;
  color: var(--text);
  cursor: pointer;
}
.opt:hover { border-color: var(--primary); }
.opt b { color: var(--primary); margin-right: 4px; }
.opt.right { border-color: var(--secondary); background: var(--soft-teal); }
.opt.wrong { border-color: var(--warm-accent); background: var(--soft-amber); }
.mark { float: right; font-weight: 700; }
.opt.right .mark { color: var(--secondary); }
.opt.wrong .mark { color: var(--warm-accent); }
.fb { margin-top: 6px; font-size: 16px; line-height: 1.4; padding: 4px 10px; border-radius: 6px; }
.fb-right { background: var(--soft-teal); }
.fb-wrong { background: var(--soft-amber); }
.fb b { margin-right: 4px; }
</style>
