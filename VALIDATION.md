# Validation record - 2026-11-09

The added skill is `comfyui-mv-production`. The original `ai-music-video-production` files remain at their existing paths.

## Executed checks

- Skill Creator `quick_validate.py` passed naming, frontmatter, and entry-point checks.
- Standard-library unit tests: **9/9 passed**. Cases cover same-take highest full-frame selection, cropped ancestors, missing/cyclic parents, source interval coverage, typed binding, missing parameters/nodes, modern COMBO asset options, truncated audio, and full decode. Missing implementations initially failed; the modern COMBO check also reproduced an actual false-ready result before a regression fix passed.
- All three API templates bind against the example project while preserving numeric types. Existing prepared files are protected against overwrite.
- Read-only `/object_info` checks found all required node classes on the available ComfyUI server. Missing example images, latents, and video prevent asset readiness. No POST, queuing, cancellation, model download, or service change was performed for package validation.
- An independent forward dry run copied the complete skill to a temporary `.agents/skills/` directory, prepared templates, audited sources, and tested FFmpeg fixtures. A 0.5-second/12-frame picture with a 0.25-second audio stream correctly failed; the complete 0.5-second counterpart passed and decoded all 12 frames. `visual_acceptance` remained false.
- Feedback led to Python 3 interpreter guidance, the modern COMBO missing-video fix, and clearer latent prerequisites/Director upscale instructions.

The simple no-skill baseline judgment scenario already passed. No fabricated baseline failure or claim of guaranteed behavioral improvement is made. Dry-run success establishes usability and checked failure handling, not universal video quality.

## Limits

- No new GPU generation/refinement was run to validate this publication. API graphs are de-identified, parameterized references derived from completed local workflows; the parameterized copies have not received new GPU acceptance.
- Models, references, music, lyrics, portraits, footage, and private machine paths are excluded. Real source files, node versions, and model compatibility must be established in the target environment.
- `minimax-h3-refine.api.json` is a sampling tail after compatible target-size video and matching audio latents exist. It does not enlarge a latent automatically. Use a compatible upstream Director/Continuum preparation route; renaming a first-pass latent is not preparation.
- Source approvals and ancestry are declarations. `--probe` cannot prove truthful lineage or absence of baked compositing; compare real workflow receipts and pictures.
- Media checks do not prove original-song content, listening-based lyric alignment, exact foot contact, stable identities, or completed human audiovisual screening.
- Temporary directory copying was tested. New-session discovery, other-machine installation, GPU performance, and any actual 09:00 film deadline remain outside this package's acceptance.

## Reproduce

```bash
python3 -m unittest discover -s tests -v
```

Python 3.10+ and FFmpeg/ffprobe are needed for all checks. Without FFmpeg, media tests are skipped; a skip is not a pass. Skill Creator's separate validator is optional for consumers and is not required to run the bundled helpers.
