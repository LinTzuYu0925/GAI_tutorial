import { configs } from '@slidev/client'
import { reactive } from 'vue'

// Students' answers on practice pages. They stay in this browser and are never sent anywhere.
// All decks share one site origin, so the key includes the deck name.
const prefix = `fill:${configs.exportFilename}:`
const answers = reactive<Record<string, string>>({})

// Reading or writing storage can throw (private window, blocked site data); typing still works, it just isn't kept.
try {
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i)
    if (key?.startsWith(prefix))
      answers[key.slice(prefix.length)] = localStorage.getItem(key) ?? ''
  }
  window.addEventListener('storage', (e) => {
    if (e.key?.startsWith(prefix))
      answers[e.key.slice(prefix.length)] = e.newValue ?? ''
  })
}
catch {}

export function getAnswer(id: string) {
  return answers[id] ?? ''
}

export function setAnswer(id: string, value: string) {
  answers[id] = value
  try {
    if (value)
      localStorage.setItem(prefix + id, value)
    else
      localStorage.removeItem(prefix + id)
  }
  catch {}
}

// Ids look like `group.item`; clears every answer in one group.
export function clearGroup(group: string) {
  for (const id of Object.keys(answers)) {
    if (id.startsWith(`${group}.`))
      setAnswer(id, '')
  }
}
