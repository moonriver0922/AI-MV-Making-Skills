# ComfyUI, MiniMax H3, and Continuum

## Dependencies and installation boundaries

Installing this skill copies instructions, templates, and inspection tools. It does not install ComfyUI, models, or GPU access. See [installation](install-and-use.md). Record the existing environment before checking nodes; importing a template does not authorize a production upgrade or restart.

These examples use MiniMax H3, not HunyuanVideo:

| Purpose | Nodes/components |
| --- | --- |
| Model, encoder, VAE | UNETLoader, CLIPLoader with type=minimax, VAELoader |
| First/last-frame conditioning | MiniMaxH3ImageToVideo, MiniMaxH3SigmaShift |
| Sampling | BasicScheduler/ManualSigmas, BasicGuider, RandomNoise, KSamplerSelect, SamplerCustomAdvanced |
| AV latents | LTXVSeparateAVLatent, LTXVConcatAVLatent, SaveLatent, LoadLatent |
| Video | VAEDecode, CreateVideo, SaveVideo |
| Whole-frame SR | LoadVideo, GetVideoComponents, ImageFromBatch, UpscaleModelLoader, ImageUpscaleWithModel, ImageScaleBy, ImageBlend |
| Chunked continuation | [ComfyUI-H3-Continuum](https://github.com/ukr8b3g-cmyk/ComfyUI-H3-Continuum) |
| Optional director/reference UI | [MiniMax H3 Director](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director) |

Template filenames describe one BF16/FP16 configuration, not the only supported choice or a minimum VRAM requirement. Obtain compatible weights separately from [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3), following their license and loader support. FL2VA serves its corresponding first/last-frame path; Director reference-video modes may require REF2VA. Do not interchange architectures or loaders. Even silent MV output must retain the AV structure expected by the selected nodes.

## First pass, second pass, and SR

**First pass:** Establish action and composition. MiniMaxH3ImageToVideo supplies conditioning/latent, the H3 model uses its sigma shift, sampling produces AV latents, and the split outputs can be saved and decoded. Record seed, references, model, and frame count for reproduction; a fixed seed does not guarantee cross-shot identity.

**Second pass:** Resample compatible first-pass latents/images under appropriate controls. It may improve texture or change faces, props, and movement. Adopt only after actual comparison. `minimax-h3-refine.api.json` is a sampling tail requiring an existing target-size compatible video latent and matching audio latent; it does not prepare an enlarged latent automatically. Use the installed, compatible native refine/upscale route first. Do not force-load another architecture's upscaler.

For the Director UI route, connect `MiniMax H3 Director Refine` to the director's `refine` input. Select same-size `refine` or target-size `upscale` as appropriate. Compare actual processed `images` against first-pass `images_pre_refine`. `latent_upscale` alone does not mean second-pass sampling occurred. Use Continuum's version-matched examples for its refinement/Take controls, and preserve both stages before adopting a result.

**Whole-frame SR:** `whole-frame-sr.api.json` blends RealESRGAN x2 with whole-frame Lanczos. It is image SR, not diffusion refinement. Check temporal face, paper-line, and fabric shimmer. Obtain weights from [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN). The graph assumes a 2x model; changing scale requires adapting its matching branch. Do not upscale a cropped preview and claim recovered native detail.

Select precision, resolution, steps, and offloading from actual supported capabilities and small tests. Avoid arbitrary fixed VRAM gates. First inspect the highest completed stage of the approved take rather than substituting a larger different actor.

## Continuum and references

Use the upstream workflow matching the installed tag/commit. Short shots can use first/last frames; longer work can use Chunk/Take continuation, with each segment reviewed before continuing from a compatible approved Take. Successful execution does not mean content approval.

Identity references constrain face, wardrobe, and proportions; set references constrain geometry and props; first/last frames constrain pose/composition; motion/video/pose controls constrain action. Resolve conflicting references before generation. Changes to references, dimensions, model, sampling, or time ranges require compatibility checks. Respect upstream read-only/incompatible states; never delete metadata to force reuse.

Inspect the entire segment and adjoining cuts for cast, furniture, hinges, prop ownership, movement direction, lighting, and era. Connected endpoints do not prove correct intermediate feet, hands, or head/body relationships. Repeatedly failing long actions may be covered with authorized native short-shot editing and understandable causal omissions.

## Prepare and submit responsibly

`assets/workflows/*.api.json` are API graphs, not frontend canvas JSON. Copy/edit `assets/project.example.json`, stage your own references in ComfyUI input, and install compatible models. Prepare without queuing:

```bash
python3 scripts/bind_workflow.py template.api.json project.json --output prepared.api.json
python3 scripts/inspect_comfy.py prepared.api.json --server http://127.0.0.1:8188
```

The inspector reads `/object_info`; runtime memory, latent compatibility, and visual quality remain unproven. Install missing nodes from their upstream instructions or select a verified alternative; do not invent class names.

For an authorized submission, atomically save a unique intent/request hash, POST `/prompt`, and save prompt_id. Confirm completion through `/history/{prompt_id}` and actual outputs. After a timeout with missing receipt, resolve unique client ID/history/output state before resubmitting. Respect queue admission and shared jobs. Cancel only a confirmed owned ID through a supported per-job cancellation endpoint.
