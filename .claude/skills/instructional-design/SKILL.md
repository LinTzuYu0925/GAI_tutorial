---
name: instructional-design
description: Design learning objectives, concept sequences, prerequisites, and coherent instructional outlines for technical lectures before slide authoring.
---

# Instructional Design Skill

## Purpose
Turn source material into a coherent learning experience. Optimize for what the audience should understand and be able to explain, not for covering the maximum number of facts.

## When to use
Use this skill before drafting a lecture, tutorial, workshop, or slide deck. Invoke it again when the audience, duration, learning goals, or source material changes.

## Required inputs
Identify, or ask the user for only essential missing details:
- Audience and assumed prior knowledge
- Learning goal or practical outcome
- Available teaching time or approximate slide count
- Source material and any required topics
- Output format and approval requirements

If details are missing but work can proceed, state reasonable assumptions in the outline rather than blocking progress.

## Procedure

### 1. Analyze the source and audience
- Extract the main claims, concepts, examples, and conclusions from the supplied material.
- Separate the source's actual content from useful background knowledge added for teaching.
- Estimate what learners already know and what misconceptions are likely.
- Identify prerequisite knowledge and terms that need plain-language definitions.

### 2. Define measurable learning objectives
Write 3–6 objectives using observable verbs, such as:
- explain
- distinguish
- trace
- apply
- diagnose
- design

Avoid vague objectives such as "understand AI." Prefer "distinguish an LLM from the application that executes its tool calls."

### 3. Build the concept map
For every major concept, record:
- Plain-language definition
- Problem it solves or question it answers
- Prerequisites
- Dependencies and relationships to other concepts
- One example or analogy
- Likely misconception

Represent prerequisite relationships explicitly. Do not imply a strict technical dependency merely because a teaching sequence introduces one concept before another.

### 4. Sequence the lesson
Use a narrative arc:
1. Motivate the topic with a concrete question or problem.
2. Introduce the minimum prerequisites.
3. Explain core concepts in dependency-aware order.
4. Connect concepts into a larger system.
5. Walk through an end-to-end example.
6. Recap the model and check learning.

For each transition, explain why the next concept is needed. Avoid presenting a glossary of disconnected definitions.

### 5. Propose the outline before drafting
For each proposed slide or section, specify:
- Number and title
- Learning objective
- One-sentence takeaway
- Essential content
- Suggested example or visual
- Connection to the previous and next section
- Source or evidence needed

Keep one principal teaching point per slide. If a slide contains multiple independent ideas, split it or justify the combination.

### 6. Respect approval gates
If the user requested approval before production:
- Produce the outline only.
- Save it to the agreed outline file, if file access is available.
- Clearly state assumptions and unresolved questions.
- Stop and ask for explicit approval.
- Do not create the finished deck, slide source, or presentation assets before approval.

Silence, tool availability, or a draft being saved does not count as approval.

### 7. Check instructional quality
Before handing over an outline, verify:
- Objectives are measurable and fit the audience.
- Concepts are introduced after their prerequisites.
- Each section has a clear reason to exist.
- The sequence has meaningful transitions.
- Examples make abstract ideas concrete.
- The ending synthesizes the concepts rather than merely repeating titles.
- The scope fits the requested duration.

## Output format
Use this structure unless the user requests another:
1. Audience assumptions and learning objectives
2. Concept map and prerequisites
3. Proposed lesson or slide sequence
4. End-to-end example
5. Misconceptions to address
6. Knowledge-check questions
7. Sources or evidence still needed
8. Approval request, if required

## Rules
- Teach relationships and reasoning, not just terminology.
- Prefer a smaller number of well-connected ideas over exhaustive coverage.
- Do not invent claims about what a source contains.
- Do not present a pedagogical order as a mandatory technical architecture.
- Keep the learner's practical goal visible throughout.
