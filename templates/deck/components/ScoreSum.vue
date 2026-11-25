<script setup lang="ts">
import { computed } from 'vue'
import { getAnswer } from './answerStore'

// Adds up the scores chosen in <PickIn> blanks: each answer's leading number counts.
const props = defineProps<{
  ids: string[]
  max?: number
}>()

const picked = computed(() => props.ids
  .map(id => Number.parseFloat(getAnswer(id)))
  .filter(n => !Number.isNaN(n)))
const total = computed(() => picked.value.reduce((a, b) => a + b, 0))
const missing = computed(() => props.ids.length - picked.value.length)
</script>

<template>
  <span class="score-sum">
    <b>{{ total }}</b><span v-if="max">／{{ max }}</span>
    <small v-if="missing">（缺 {{ missing }} 項）</small>
  </span>
</template>

<style scoped>
.score-sum { font-size: 18px; white-space: nowrap; }
.score-sum b { color: var(--primary); font-size: 22px; }
.score-sum small { color: var(--muted-text); font-size: 14px; margin-left: 6px; }
</style>
