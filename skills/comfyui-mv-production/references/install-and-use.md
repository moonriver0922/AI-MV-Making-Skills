# Installation and usage

## 1. Install the skill

Send this request in Codex:

```text
Use $skill-installer to install this entire skill directory:
https://github.com/moonriver0922/AI-MV-Making-Skills/tree/master/skills/comfyui-mv-production
```

Alternatively, copy the entire folder into your project's `.agents/skills/comfyui-mv-production/` or your personal `~/.agents/skills/comfyui-mv-production/`. Keep references, scripts, assets, and metadata together. Check for an existing same-name installation first.

```bash
git clone --branch master https://github.com/moonriver0922/AI-MV-Making-Skills.git
mkdir -p .agents/skills
# Run from your target project; replace the clone path below.
test ! -e .agents/skills/comfyui-mv-production && \
  cp -R /path/to/AI-MV-Making-Skills/skills/comfyui-mv-production .agents/skills/
```

These are examples, not an automatic installer. Codex detects local skills; start a new session or restart the client if needed. See [official skill documentation](https://learn.chatgpt.com/docs/build-skills). Other Agent Skills hosts use their own installation/tool permissions.

Commands use Linux/macOS `python3`; on Windows, substitute the installed Python 3 command, such as `py -3`.

## 2. Prepare the production environment

Helpers require Python 3.10+ standard library and FFmpeg/ffprobe for media checks. Inspect `python3 --version`, `ffmpeg -version`, and `ffprobe -version`. Generation additionally requires a working ComfyUI environment, compatible models, and suitable available hardware.

ComfyUI must contain the MiniMax H3 nodes. Consult [ComfyUI](https://github.com/Comfy-Org/ComfyUI) and [Director installation](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director) for supported versions/dependencies. Pin the project environment; do not run unplanned upgrades on an active deadline service.

For continuation, install [H3 Continuum](https://github.com/ukr8b3g-cmyk/ComfyUI-H3-Continuum#install-or-update) according to its upstream instructions in your custom_nodes directory. Director is optional for the core first/last-frame API template. Install optional Spectrum, KJNodes, or LoRAs only when the selected workflow requires and supports them.

Weights are separate:

| Component | Directory | Source |
| --- | --- | --- |
| H3 diffusion model | `ComfyUI/models/diffusion_models/` | [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3) |
| H3 Qwen3-VL text encoder | `ComfyUI/models/text_encoders/` | Same model repository; choose a loader-supported variant |
| H3 video/audio VAE | `ComfyUI/models/vae/` | Same repository, as required by the workflow |
| Optional RealESRGAN_x2plus | `ComfyUI/models/upscale_models/` | [Official inference/model guidance](https://github.com/xinntao/Real-ESRGAN#inference-general-images) |

Choose precision, resolution, steps, and offloading from measured capability. The skill imposes no fixed VRAM gate and does not promise that every model fits every device. Installing dependencies needs the environment's normal authorization.

## 3. Invoke the workflow

Planning only:

```text
Use $comfyui-mv-production with my song, authoritative lyrics, and story.
Prepare cast/set/prop locks, a music-timed shot plan, and a ComfyUI node approach.
Do not generate yet.
```

Revision:

```text
Use $comfyui-mv-production to revise this existing MV.
Keep the approved story baseline and recover the highest approved ComfyUI output
of each same take, preserving the full original composition.
Retain music, subtitles, and cover. Stop/report after two failed attempts per problem.
```

Delivery check:

```text
Use $comfyui-mv-production to inspect my complete export.
Specification: 24fps, 6192x2580, 5112 frames, complete 213-second soundtrack.
Separate technical checks, actual picture review, and pending human audiovisual screening.
```

## 4. Prepare API workflows

Copy `assets/project.example.json` and `shot-manifest.example.json` into your project and replace example paths, models, intervals, receipts, and approvals with real values. Use `scripts/bind_workflow.py` to prepare a new versioned API file, then `scripts/inspect_comfy.py` for read-only node checks. Neither submits generation.

Use the upstream version-matched UI examples for Continuum. The refinement template requires target-size compatible video/audio latents; it is not an automatic first-to-second-pass pipeline. Director's native refine/upscale path is an alternative, as described in [ComfyUI workflows](comfyui.md). SR is a distinct operation. Passing structure checks is not GPU or visual acceptance.

## 5. Update and troubleshoot

Back up the installed skill and project records before replacing the skill directory. Do not delete original footage, models, or production caches as part of a skill update. Missing ffprobe means the media tools need installation; missing nodes require the correct core/extension version. Uncertain submission state requires history inspection before another POST.

When source lineage, compatible latents, hardware capacity, or references are unresolved, report the specific gap and continue independent work. Do not mask it by renaming files, forcing incompatible loaders, weakening acceptance criteria, or claiming unconfigured automatic resumption.
