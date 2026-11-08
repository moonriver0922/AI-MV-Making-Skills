# Production reference

## Shot sheet

| Field | What to capture |
|---|---|
| Cue | Exact audio source, section, and measured time range |
| Words | Authoritative text, translated subtitle, and review status |
| Story | Emotional beat, visible action, and what changes before the next cut |
| Continuity | Cast, wardrobe, set state, prop holder, entry and exit directions |
| Camera | Shot size, angle, movement, focal action, and caption-safe area |
| Implementation | Reusable assets, key poses, frame range, transition, and version |
| Review | Evidence at the critical timestamp and open issues |

Start with the hard shots. Test a handoff or a moving camera, a recurring character at two sizes, and an English line with a long reading load. This prevents a beautiful still or short demo from hiding production problems.

## Choose the tool by the job

| Job | Common route |
|---|---|
| Creative options, continuity notes, and targeted code changes | A conversational AI or coding assistant |
| Original visual exploration | Image generation followed by inspection, selection, and asset cleanup |
| Audio and lyric timing | Local audio analysis, a transcription or alignment model, then human listening |
| Precise recurring action | An editable 2D engine, compositing tool, or script-based renderer |
| Compositing and delivery | A timeline editor or FFmpeg, with a separate subtitle layer and a decode check |

Treat a route as optional until tested against the brief. A generator can be useful for an isolated texture or a bounded insert, while a repeatable renderer is easier to revise for recurring casts. Match the method to the production constraints.

## Provenance example from a completed production

The human director chose the adult friendship story and supervised the emotional arc. Codex helped organize the work and implement timestamped changes. ImageGen was used for concept exploration and sprite experiments. Local faster-whisper provided draft timing against supplied lyrics. Godot was used for early pixel-animation tests. The final pixel frames were produced with Python and Pillow, and FFmpeg composed separately rendered bilingual subtitles, encoded the original music, and exported the review and 6K versions. FFprobe and decode checks verified technical delivery. This is an example toolchain, not a dependency of the skill.

The most consequential revisions came from reviewing action and continuity in context. A football-to-suitcase match cut needed direction, physical contact, and a reason to move the story forward. Repeated seasonal lyrics needed different actions. A photo had to sit between the characters' sightlines, and the camera had to let the fireworks decay before resting on it. Fixing these issues in editable shots was more dependable than regenerating the complete video.
