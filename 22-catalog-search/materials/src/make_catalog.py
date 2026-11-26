"""Generate the course's synthetic product-photo catalog (40 images, 8 categories) with SD1.5 + LCM-LoRA.

Usage (repo root): python -X utf8 22-catalog-search/materials/src/make_catalog.py
Why generated: Wikimedia Commons refused bulk downloads (HTTP 429) on 2026-11-26, and generated images have a
single, known licence (SD1.5 CreativeML OpenRAIL-M; LCM-LoRA openrail++). Slides label them as AI-generated.
Writes materials/data/catalog/*.jpg (320 px) and catalog.csv (file, category, prompt, seed).
"""
import csv, time
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline, LCMScheduler

OUT = Path(__file__).resolve().parents[1] / "data" / "catalog"
OUT.mkdir(parents=True, exist_ok=True)
CATS = {
    "耳機": "wireless headphones",
    "行動電源": "portable power bank battery pack",
    "智慧手錶": "smartwatch with a round screen",
    "掃地機器人": "round robot vacuum cleaner on a floor",
    "電熱水壺": "electric kettle",
    "筆電": "laptop computer, open",
    "背包": "backpack",
    "馬克杯": "ceramic coffee mug",
}
VARIANTS = [
    "black, on a white background, studio product photo",
    "white, on a wooden table, soft daylight, product photo",
    "blue, on a pastel background, minimal product photo",
    "silver, on a dark background, dramatic lighting, product photo",
    "red, lifestyle photo in a cozy living room",
]
pipe = StableDiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5",
                                               torch_dtype=torch.float32, safety_checker=None)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")
pipe.set_progress_bar_config(disable=True)
rows = []
for i, (zh, obj) in enumerate(CATS.items()):
    for j, var in enumerate(VARIANTS):
        prompt = f"a {var.split(',')[0]} {obj}, {', '.join(var.split(', ')[1:])}, high quality"
        seed = 100 * i + j
        t0 = time.time()
        img = pipe(prompt, num_inference_steps=4, guidance_scale=1.0, height=512, width=512,
                   generator=torch.Generator().manual_seed(seed)).images[0]
        name = f"c{i}_{j}.jpg"
        img.resize((320, 320)).save(OUT / name, quality=88)
        rows.append({"file": name, "category": zh, "prompt": prompt, "seed": seed})
        print(zh, name, f"{time.time()-t0:.0f}s", prompt, flush=True)
with open(OUT.parent / "catalog.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "images")
