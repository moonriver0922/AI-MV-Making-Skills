# Review, failure budgets, and recovery

## Locate the first failing stage

Compare the same native frame through original ComfyUI output, approved refinement/SR, selected interval, and actual export. Trace selected/restored files to parents. Different poses, timestamps, or scales cannot prove a repair.

| Symptom | Inspect first | Appropriate direction |
| --- | --- | --- |
| Faces alternate between clear and soft | Native consecutive frames, facial pixel coverage, crops, encoding chain | Recover full framing; replace soft sources or generate controlled native close-ups |
| Different person across cuts | Cast version, references, take, refinement drift | Reuse/generate the approved identity; aging does not excuse another actor |
| Door color/size/hinge changes | References, native frames, pasted/reprojected plates | Fix references/native action; preserve frame, hinge, and handle relations |
| Child glides | Body displacement versus stance/swing phases over continuous frames | Improve controls/action scope or use honest native editing; avoid loops or slow-motion camouflage |
| Drawing changes or moves | Input art, native motion, pasted layers/tracking | Stabilize references and physical prop behavior; exclude failed references |
| Eras are unclear | Furnishings, materials, domestic detail, aging, year cues | Make visual changes readable and add authorized concise dates |
| Slow, confusing sequence | Musical cue, visible action, emotional purpose | Remove unmotivated coverage and restructure native shots |
| Remote playback looks poor | Local file, server response, client behavior | Diagnose separately; local source defects are not explained by network assumptions |

Prompts constrain meaning, references constrain identity/space, motion controls constrain action, and sampling changes generation behavior. Choose the layer from observed failure. Changing every variable at once prevents a useful diagnosis.

## Keep acceptance evidence specific

Record whether each shot was inspected in real-time playback, start/middle/end samples, and dense critical-action sequences. Inspect feet, doors, paper, and hands as well as faces. Include preceding and following cut boundaries. Editing away part of an action is an omission, not proof that a full landing or transfer was visibly completed.

Inspect actual encoded captions in white/partial-yellow/full-yellow states, English reading length, dates, cover spelling, intro offsets, music tail, and final pose. Sampled stills, full decode, continuous screening, and listening have separate statuses; exit code zero does not grant visual approval.

## Stop after the agreed failure budget

Count attempts by stable problem_id across seeds, prompts, and workflow variants. Unless agreed otherwise, stop and report after two failed attempts. Record objective, changed variable, output, failure, time, and adoption. Keep rejected references out of subsequent jobs.

At the limit, preserve the baseline, disclose the defect, use suitable existing native coverage or authorized editing, and advance other tasks. Do not repeatedly consume the complete-film window or present retained failures as fully repaired.

## Queue, deadline, and handoff

Save project state, selected manifest, intents/receipts/history/outputs, completed steps, and next actions. On resumption, read records and inspect actual files instead of resubmitting because a user said “continue.” Other users' GPU jobs, services, or files are not cleanup targets.

Progress should include completed/total frames and measured throughput. Estimates also need assembly, mux, decode, transfer, and review. Keep a complete playable fallback and independent versions. Reduce scope before dropping essential verification.

A finite batch supervisor is not quota-recovery automation. Scheduling, session resumption, and quota restoration are distinct capabilities; claim them only when configured and tested. Plan production environment changes separately. Cancel only known owned jobs, never global interrupt; resolve uncertain submission state before further POSTs.
