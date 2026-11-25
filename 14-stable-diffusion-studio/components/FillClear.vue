<script setup lang="ts">
import { clearGroup } from './answerStore'

const props = defineProps<{ group: string, corner?: boolean }>()

function clear(e: Event) {
  if (window.confirm('清除這一頁打的答案？'))
    clearGroup(props.group)
  // A focused button also turns off Slidev's arrow keys.
  ;(e.target as HTMLElement).blur()
}
</script>

<template>
  <div class="fill-clear" :class="{ 'fill-clear--corner': corner }">
    <span>答案只存在這台電腦的瀏覽器，不會傳出去。</span>
    <button type="button" @click="clear">清除這一頁</button>
  </div>
</template>

<style scoped>
.fill-clear {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  margin-top: 4px;
  font-size: 14px;
  color: var(--muted-text);
}
.fill-clear--corner {
  position: absolute;
  top: 38px;
  right: 56px;
  margin-top: 0;
}
.fill-clear button {
  padding: 1px 10px;
  font: inherit;
  color: var(--primary);
  background: #fff;
  border: 1px solid var(--primary);
  border-radius: 4px;
  cursor: pointer;
}
</style>
