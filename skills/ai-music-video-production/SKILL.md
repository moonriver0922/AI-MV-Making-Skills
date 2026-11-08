---
name: ai-music-video-production
description: Plan, prototype, animate, revise, and deliver a human-directed music video using AI-assisted production. Use for a complete MV or a revision that must respect the song, shot timeline, recurring cast, continuity, subtitles, or delivery specs. For an isolated image request, use the relevant image workflow instead.
---

# AI Music Video Production

Build an editable film around a song. Keep the user in charge of story, performance, emotional progression, and final creative decisions. Use AI to develop options, generate candidate assets, implement shots, and make targeted revisions.

## 1. Establish the source and brief

- Inventory the exact audio master, authoritative lyrics, reference materials, intended audience, and delivery requirements. Distinguish verified rules from assumptions. Check permissions for music, fonts, footage, generated imagery, and real likenesses. Record missing inputs and continue on work they do not block.
- Analyze the supplied audio. Mark sung lines, repeated lines, instrumental gaps, musical turns, and the final decay. Use transcription or forced alignment for a draft where useful. Keep the authoritative lyric text separate from recognition output. Label machine timing and uncertain syllables, and listen-check them before claiming manual alignment. Leave unknown words and times blank.
- Agree on the visual language, a one-sentence premise, character relationships, and the emotional turn at each section. If the user has already approved the direction, carry it forward.

## 2. Direct the story before generating shots

- Make a timeline with source in and out, lyric or musical cue, story purpose, visible action, set, cast, camera, transition, and continuity dependencies. Use [the production reference](references/production.md) for an adaptable shot sheet and review procedure.
- Assign repeated lyrics a progression. The same idea can move from a shared routine to a test of the relationship to its payoff. Recur to a prop or location when its meaning has changed.
- Design transitions around a visible or audible relationship, such as shared motion direction, a matched object, or a recurring gesture. Stage the ending against the music, including the time needed for the last action to settle.
- Lock character turnarounds, identifying silhouettes and colours, recurring sets, props, lighting states, and the intended camera scale. Make a continuity map for entrances, exits, held props, travel direction, and look direction. Treat references as inspiration and build original assets.

## 3. Prototype, then build editable shots

- Make a short proof with a representative action, cut, and subtitle at the intended playback scale. Test whether motion, legibility, texture, and character consistency survive the delivery format.
- Use a deterministic layered renderer for recurring characters, props, precise handoffs, or work that needs frame-level revision. Use AI image generation for concepts or candidate plates and sprites where helpful. For a generative-video shot, lock reference frames and generate a bounded action, then review the whole clip before acceptance.
- Keep the timeline, character assets, animation, camera, captions, and source audio editable. Render by frame index on a single clock. Preserve the original audio master unless the user authorizes a change.
- For pixel art, choose a logical grid on purpose and test it at target display size. Preserve hard edges with nearest-neighbour scaling where appropriate. Render text separately at the actual delivery resolution. Other visual styles can use different filtering.

## 4. Assemble and revise against the music

- Assemble the complete film before judging the emotional arc. Give each repeated section a distinct visible action or change in stakes. Review continuous motion through cuts as well as still frames.
- Translate captions by meaning and reading time. Keep repeated lines consistent where the meaning is stable. For karaoke, use the source timing to drive highlighting and label approximate word-to-word mapping in translated lines.
- Use timestamped feedback to identify the first point where continuity, framing, or emotional intent breaks. Repair the narrowest affected asset, shot, or timing range, then check both adjoining shots. Keep versioned previews so approved decisions can be restored and compared.
- Check hand and prop contact, foot placement, screen direction, door and wheel geometry, object ownership, character identity, prop continuity, lighting, camera direction, and caption readability. Verify motion by playing the shot.

## 5. Deliver and document

- Export a review copy and the specified master. Check dimensions, aspect ratio, frame rate, frame count, duration, audio streams, start and end, and complete decode. Compare the audio with a reference encode from the supplied master if the song should be the only soundtrack.
- Spot-check frames at native size and normal viewing size. Check cover text, credits, and caption-safe areas in the encoded files. Distinguish technical checks from human listening or screening still pending.
- Record the actual tools used, model or workflow where known, what the user decided, asset provenance, and limitations. Separate concepts and prototypes from the production pipeline. Deliver the editable project, finished media, and any requested process notes or reflection. Follow the user's authorization boundaries for uploads and submissions.
