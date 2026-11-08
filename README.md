# AI MV Making Skills

Reusable skills for planning, producing, and reviewing AI-assisted music videos. The workflow starts with the song and the director's intent, then turns those decisions into editable shots.

## Available skills

| Skill | Use it for |
| --- | --- |
| [AI Music Video Production](skills/ai-music-video-production/SKILL.md) | A complete music video or a revision that must preserve lyric timing, character continuity, and the delivery specifications. |

## Use a skill in Codex

1. Clone or download this repository.
2. Copy the entire `skills/ai-music-video-production` folder into your project's `.agents/skills/` directory. Keep `SKILL.md`, `references/`, and `agents/` together.
3. Open the project in Codex and ask for the skill by name. Provide the song, verified lyrics if available, creative brief, and delivery specs.

```text
Use $ai-music-video-production to plan and produce a music video
from my audio, lyrics, and creative brief. Start with the story,
characters, locations, and a shot plan tied to the music.
```

Start with a representative test shot and agree on how to review the full cut. The skill works with different songs, visual styles, and toolchains.

## Add another skill

Create a separate folder under `skills/`. Put a `SKILL.md` with `name` and `description` in its YAML frontmatter at the root of that folder. Keep supporting references alongside the skill, and add the new entry to the table above.
