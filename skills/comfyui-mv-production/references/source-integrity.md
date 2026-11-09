# Original sources, resolution, and lineage

## Select the right master

“Highest resolution” means the highest approved, compatible, completed ComfyUI stage of the same shot and take. This may be first pass, second pass, or whole-frame SR. A larger alternate actor, failed refinement, editorial preview, or enlarged crop is not a replacement master.

Trace actual output to ComfyUI history/SaveVideo, sampler/decoder/refine stage, references and source latents, selected native interval, and downstream transforms. Follow nested opening/ending edits and selected/restored/processed intermediates. An empty outer crop field does not establish an uncropped source.

Record:

- Shot/take and cast/set version.
- Prompt ID, original request/workflow hash, application/extensions/model versions.
- Native, second_pass, super_resolution, preview, or editorial stage.
- Actual dimensions/fps/frame count, parent ID, native interval, transforms, and SHA.
- Content approval, inspection evidence, and unresolved issues.

Keep native and delivery dimensions separate. Cropping a 1152×480 wide shot to 576×240 and exporting at 6192×2580 still derives local detail from 576×240. A high-resolution reference image does not establish equal detail in the generated video. Missing facial information is not automatically restored by resizing or re-encoding.

## Preserve composition

Whole-frame proportional scaling can standardize delivery size. For differing aspect ratios, prefer agreed padding over silent edge cropping or stretched bodies. Store originals, approved refined outputs, working edits, and encoded deliveries separately. Obtain close-ups from approved native coverage or ComfyUI generation at the intended shot size.

Explicitly requested crops need coordinates, source size, effective pixels, purpose, authorization, and a rollback file. They must not replace the native master or silently seed later references. Face/door/paper pasting, actor reprojection, and head/body warps are content edits, even if implemented by a ComfyUI node; user boundaries still apply.

## Audit with the helper

Copy `assets/shot-manifest.example.json` and replace examples with real candidates. `native_start` is the native-take frame represented by candidate frame zero. Include a crop parent when an enlarged crop was subsequently upscaled. Do not relabel missing lineage as native.

```bash
python3 scripts/audit_sources.py manifest.json --output metadata-audit.json
python3 scripts/audit_sources.py manifest.json --probe --output file-audit.json
```

The helper rejects different takes, unapproved candidates, preview/editorial stages, cropped ancestors, missing/cyclic parents, and insufficient frame coverage. It trusts declared lineage. `--probe` checks actual dimensions; it does not establish truthful ancestry, correct identity, or absence of baked compositing. Verify against real workflow receipts and pictures.

Record still images as stills, without inventing generated-video frame counts. Do not use a frozen actor as evidence of completed walking. When selected intervals change, realign Foley to its original source clock while leaving the music continuous.
