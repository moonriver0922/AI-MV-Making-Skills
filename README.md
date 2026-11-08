# AI MV Making Skills

Reusable skills for planning, producing, and reviewing AI-assisted music videos. The workflow starts with the song and the director's intent, then turns those decisions into editable shots.

## Available skills

| Skill | Use it for |
| --- | --- |
| [AI Music Video Production](skills/ai-music-video-production/SKILL.md) | A complete music video or a revision that must preserve lyric timing, character continuity, and the delivery specifications. |

## Install and use the skill

### Paste the link into Codex

Send this request to Codex:

```text
Use $skill-installer to install this skill:
https://github.com/moonriver0922/AI-MV-Making-Skills/tree/master/skills/ai-music-video-production
```

If you use another assistant that supports Agent Skills, send it the same link and ask it to install the entire skill directory using that assistant's supported setup. Keep the supporting files together with `SKILL.md`.

### Install from a terminal

If you have the Codex CLI, run:

```bash
codex 'Use $skill-installer to install the skill from https://github.com/moonriver0922/AI-MV-Making-Skills/tree/master/skills/ai-music-video-production'
```

### Run it on a project

After installing, ask Codex in a new turn:

```text
Use $ai-music-video-production to plan and produce a music video
from my audio, lyrics, and creative brief. Start with the story,
characters, locations, and a shot plan tied to the music.
```

Provide the audio, verified lyrics if available, and delivery specs. If your setup requires manual installation, download the full skill directory into your project's `.agents/skills/` directory.

## Add another skill

Create a separate folder under `skills/`. Put a `SKILL.md` with `name` and `description` in its YAML frontmatter at the root of that folder. Keep supporting references alongside the skill, and add the new entry to the table above.
