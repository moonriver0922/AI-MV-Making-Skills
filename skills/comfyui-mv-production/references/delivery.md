# Subtitles, cover, and complete delivery

## Project specification

Take fps, aspect ratio, dimensions, and total frames from the user's requirements. Example: 5112 frames at 24fps is 213 seconds. A separate three-second cover adds 72 frames, producing 216 seconds/5184 frames. Keep the no-intro version; do not sacrifice story or music for a cover.

Separate original footage, highest approved ComfyUI outputs, working edits, and delivery encodes. Check source color tags before normalization rather than assigning one matrix to every file. Scale or pad whole frames without silently changing composition.

## Lyrics and dates

Use authoritative lyric text and acoustic timing. Label machine-derived or unlistened boundaries. Translate by meaning and reading time; keep repeated meanings consistent.

When two lower-left rows are requested, put the original language above English and check that long lines do not wrap into a third row. Choose size/position at actual viewing scale. ASS `\kf` with yellow PrimaryColour and white SecondaryColour provides progressive highlighting; preserve white during any pre-display interval. A translated line-wide wipe is not separately timed English singing.

Render text after scaling picture to the final output dimensions. Inspect encoded white, partially highlighted, and completed lines plus every year cue. Date location/background follows the brief; an unboxed date may still need a thin outline for legibility.

Verify the exact title, creator name, and event text on the cover. A successful cover does not prove film identity consistency. Adding an intro must move both music and burned subtitles correctly. Burning subtitles onto the complete film before prepending a cover naturally shifts them with the picture.

## Preserve the audio tail

Encode silent picture, then mux complete audio separately. Use `-frames:v` on the picture stage, not on the final mux alongside the soundtrack. Avoid unintended `-shortest`, `-t`, or timestamp cutoffs.

```bash
# Replace these example specifications with the actual project values.
ffmpeg -i clean-picture.mkv -vf "scale=6192:2580:flags=lanczos,ass=lyrics.ass,setsar=1" \
  -an -frames:v 5112 -r 24 -c:v libx264 -crf 18 -pix_fmt yuv420p silent.mp4

# Encode a PCM mix as AAC. A compatible unchanged AAC source can instead be copied.
ffmpeg -i silent.mp4 -i expected-mix.wav -map 0:v:0 -map 1:a:0 \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart final.mp4
```

For a three-second intro, concatenate complete cover picture and film, and build three seconds of silence followed by the complete expected mix. Check codec parameters/time bases before video stream concatenation; normalize incompatible sources first. Container duration alone does not prove the audio stream reaches the expected end.

When music and Foley are separate, move only relevant Foley to match changed source intervals, leaving the music continuous. Removing obsolete footsteps under replacement traffic is a mix change; final AAC can no longer be claimed byte-identical to the previous mix. PCM identity, decoded AAC correlation, and listening are different evidence.

## Verify and provide usable files

```bash
python3 scripts/verify_delivery.py final.mp4 --width 6192 --height 2580 \
  --fps 24 --frames 5112 --decode --output delivery-check.json
```

The helper checks actual picture/audio durations, dimensions, fps, frame count, and full decode. It does not compare song content, measure foot contact, or grant visual approval. Compare against the expected full mix, inspect starts/tails and sync, and use decoded audio alignment/correlation/gain checks where appropriate.

A remote absolute path is not automatically playable for the user. Use the authorized delivery route. For an existing Tailscale/file service, check file existence, MIME, Range support, and a full-download hash. Client playback remains a separate check. Do not automatically expose ComfyUI publicly or upload media to another service.

Deliver review media, specified master, cover, subtitles/shot sheet, workflows/source records, timestamped changes, and unresolved issues. Report “6K-dimension export” when appropriate; do not call SR from a smaller source native 6K acquisition. Disclose remaining blur, identity, prop, or motion defects.
