---
name: technical-research-fact-checking
description: Verify technical explanations against authoritative sources, distinguish evidence from inference, and provide accurate citations for educational material.
---

# Technical Research & Fact-Checking Skill

## Purpose
Make technical learning materials accurate, traceable, and appropriately qualified. This skill supports research and verification; it does not replace instructional design or visual design.

## When to use
Use when preparing technical slides, tutorials, documentation, or explanations that make claims about software, protocols, AI systems, APIs, research, or current capabilities.

## Source hierarchy
Prefer sources in this order, depending on the claim:
1. Official specifications and standards
2. Official product or project documentation
3. Original research papers or official project repositories
4. Reputable technical books or established educational sources
5. Secondary articles, discussions, and commentary

Use secondary sources to discover context, not as the sole evidence for important technical claims when primary sources are available.

## Procedure

### 1. Extract claims
List claims that materially affect understanding. Prioritize:
- Definitions and distinctions
- How a system or protocol works
- Requirements, limitations, and dependencies
- Version-specific behavior
- Security, privacy, performance, and cost claims
- Claims attributed to a video, author, or paper

Do not spend disproportionate effort verifying obvious framing or harmless illustrative examples.

### 2. Find evidence
- Search official documentation, specifications, repositories, or primary papers.
- Prefer the version relevant to the user's tools and timeframe.
- Open and inspect sources rather than relying only on search snippets.
- For videos, use a transcript or directly accessible chapter/source material when available.
- If the original source cannot be accessed, disclose that limitation. Do not invent quotations, timestamps, or statements attributed to the source.

### 3. Maintain a claim ledger
For each important claim, record:
- Claim
- Source title and URL
- Relevant section, page, heading, or timestamp
- Evidence summary
- Status: verified, partially verified, disputed, or unverified
- Necessary qualification

### 4. Check definitions and boundaries
For generative-AI topics, explicitly check distinctions such as:
- Likelihood versus probability; MLE versus minimizing cross-entropy / KL (state which direction of KL)
- ELBO versus the true log-likelihood; what each VAE loss term really is
- What the diffusion network predicts (ε, x₀ or v) in the specific library/scheduler used
- DDPM versus DDIM versus a distilled/adversarial sampler (SDXL-Turbo / ADD); steps and quality claims per paper
- GAN loss variants (original minimax, non-saturating, hinge, WGAN): which one the lab uses
- Pretraining versus instruction tuning versus preference tuning (SFT, DPO); LoRA versus full fine-tuning
- Model weights versus a hosted API; open weights versus open source; model license terms
- Quantization format (8-bit, 4-bit NF4, GGUF) and what a memory number refers to (weights only or peak)
- Library API names and defaults by version (`transformers`, `diffusers`, `peft`, `trl` change often)
- A paper's reported result versus what our T4 lab reproduces

Do not assume that every product uses the same architecture or terminology.

### 5. Handle uncertainty and conflicting sources
- Prefer primary sources for normative behavior and official capabilities.
- Note version differences when relevant.
- If sources disagree, explain the disagreement and its likely cause.
- Mark claims that cannot be verified instead of silently treating them as facts.
- Separate source claims from your own explanation, analogy, or inference.

### 6. Cite responsibly
- Place citations close to the claim they support.
- Use links that lead to the relevant source, not a generic homepage when a deep link is available.
- Include source titles and access dates when useful for changing documentation.
- Never fabricate URLs, page numbers, quotations, or timestamps.
- Paraphrase in your own words; quote only when wording itself matters.
- Ensure the final source list contains only sources actually consulted.

### 7. Final verification pass
Before delivery:
- Re-check all high-impact claims.
- Confirm the cited source supports the precise wording.
- Remove unsupported superlatives and absolute claims.
- Verify commands, API names, code examples, and version assumptions.
- Label illustrative scenarios as examples, not evidence.
- List unresolved uncertainties transparently.

## Output format
When useful, provide:
1. Key claims checked
2. Claim-to-source ledger
3. Corrections or qualifications
4. Citation-ready source list
5. Unverified claims and limitations

For slide work, save source notes to the agreed research file (for example, `research/sources.md`) and use short citations on slides with a fuller reference list at the end.

## Rules
- Never fabricate evidence.
- Do not claim a source was read if only its search snippet was seen.
- Do not attribute your inference to a source.
- Do not present a time-sensitive feature as current without checking current documentation.
- Do not state a VRAM figure, runtime or sample quality as fact unless it was measured in our own Colab run (`research/lab-runs.md`) or comes from a cited source.
- If verification is impossible, say so and continue only with clearly labeled assumptions.
