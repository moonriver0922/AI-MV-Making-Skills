# AI MV Making Skills

Reusable Agent Skills for planning, producing, repairing, and delivering AI-assisted music videos. Start with the song and the director's intent, then turn those decisions into traceable, editable shots.

## Available skills

| Skill | Best suited to |
| --- | --- |
| [ComfyUI MV Production](skills/comfyui-mv-production/SKILL.md) | Narrative MVs made with ComfyUI, MiniMax H3, Continuum, reference frames, recurring characters and sets, and delivery deadlines. |
| [AI Music Video Production](skills/ai-music-video-production/SKILL.md) | General MV planning, animation, lyric timing, continuity, and delivery across different visual toolchains. |

The original general-production skill is retained. The dedicated ComfyUI skill adds native-source auditing, first/second-pass workflows, motion review, bounded retries, bilingual karaoke, and complete-film verification.

## Install the ComfyUI skill

Send this request to Codex:

```text
Use $skill-installer to install this entire skill directory:
https://github.com/moonriver0922/AI-MV-Making-Skills/tree/master/skills/comfyui-mv-production
```

For manual installation, copy the entire `skills/comfyui-mv-production` directory into your project's `.agents/skills/` directory or your personal `~/.agents/skills/` directory. Keep its references, scripts, and assets together. Check for an existing version before copying.

Installing the skill does not install ComfyUI, download model weights, or start GPU generation. See the [installation and usage guide](skills/comfyui-mv-production/references/install-and-use.md) for prerequisites, model/node sources, examples, and troubleshooting. Local skill discovery follows the [official Codex documentation](https://learn.chatgpt.com/docs/build-skills).

## Use it

For a new production:

```text
Use $comfyui-mv-production with my song, authoritative lyrics, and creative brief.
First prepare the story, cast/set/prop locks, and a shot plan tied to the music.
Generate only after the agreed planning stage. Preserve approved full-frame outputs.
Keep a complete fallback; report a problem after two failed attempts and move on.
```

For an existing film:

```text
Use $comfyui-mv-production to repair this MV.
Trace every shot to the highest approved ComfyUI output of the same take.
Preserve the original full composition, song, lyric clock, and approved story.
Identify previews, baked crops, and composited intermediates before choosing sources.
Deliver a complete review copy and the specified master, with remaining issues disclosed.
```

## Workflow and resources

- [Production pipeline](skills/comfyui-mv-production/references/pipeline.md): story, cast, sets, props, eras, musical cues, and shot planning.
- [ComfyUI workflows](skills/comfyui-mv-production/references/comfyui.md): MiniMax H3 first/second pass, whole-frame SR, Continuum, and reference frames.
- [Source integrity](skills/comfyui-mv-production/references/source-integrity.md): approved takes, parent stages, real dimensions, and full-frame lineage.
- [Review and recovery](skills/comfyui-mv-production/references/review-and-recovery.md): blur, identity changes, sliding feet, door hinges, paper, retries, and resumption.
- [Subtitles and delivery](skills/comfyui-mv-production/references/delivery.md): bilingual karaoke, year cues, cover, complete music, encoded masters, and remote viewing.
- [API templates](skills/comfyui-mv-production/assets/workflows/): first/last-frame generation, compatible-latent refinement, and whole-frame 2x SR. These are API examples, not frontend canvas workflows or a promise of immediate execution.

Prepare a workflow from the repository root:

```bash
cp skills/comfyui-mv-production/assets/project.example.json my-project.json
# Edit your models, references, frame count, and output settings first.
python3 skills/comfyui-mv-production/scripts/bind_workflow.py \
  skills/comfyui-mv-production/assets/workflows/minimax-h3-first-last.api.json \
  my-project.json --output shot001.prepared.api.json
python3 skills/comfyui-mv-production/scripts/inspect_comfy.py \
  shot001.prepared.api.json --server http://127.0.0.1:8188
```

These commands prepare and inspect files; they do not submit generation. Audit source choices and verify actual exports:

```bash
python3 skills/comfyui-mv-production/scripts/audit_sources.py \
  my-shot-manifest.json --probe --output source-audit.json
python3 skills/comfyui-mv-production/scripts/verify_delivery.py \
  final.mp4 --width 6192 --height 2580 --fps 24 --frames 5112 \
  --decode --output delivery-check.json
```

The dimensions and frame count above are example project settings. Replace them with the actual delivery specification. Technical checks do not establish correct identity, motion, story, or human audiovisual acceptance. Model weights, music, lyrics, portraits, and film footage are not included.

## Validate this package

Python 3.10+ and FFmpeg/ffprobe are required for all tests:

```bash
python3 -m unittest discover -s tests -v
```

Tests cover source lineage, cropped ancestors, parent cycles, frame coverage, parameter types, missing nodes/assets, and truncated audio. [Validation notes](VALIDATION.md) separate code/structure checks, behavioral dry runs, and GPU/visual acceptance.

## Install the original general-production skill

```text
Use $skill-installer to install this entire skill directory:
https://github.com/moonriver0922/AI-MV-Making-Skills/tree/master/skills/ai-music-video-production
```

With Codex CLI:

```bash
codex 'Use $skill-installer to install the skill from https://github.com/moonriver0922/AI-MV-Making-Skills/tree/master/skills/ai-music-video-production'
```

After installation, invoke `$ai-music-video-production` with your audio, verified lyrics, creative brief, and delivery requirements. Other assistants supporting Agent Skills should use their own installation mechanism and retain the entire directory.

## Add another skill

Create a directory under `skills/` with a `SKILL.md` containing YAML `name` and `description` fields. Keep supporting resources alongside it and add the skill to the table above.
