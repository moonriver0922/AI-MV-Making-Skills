# AI MV Making Skills

Reusable skills for planning, producing, and reviewing AI-assisted music videos. The workflow starts with the song and the director's intent, then turns those decisions into editable shots.

本仓库现包含独立的 **ComfyUI MV制作技能**：从歌曲/剧本、人物与场景锁定，到一采、二采、Continuum续作、原片回源、剪辑、双语变色歌词和完整交付。原有通用制作技能保留，两个技能按制作方式选用。

## Available skills

| Skill | Use it for |
| --- | --- |
| [ComfyUI MV Production](skills/comfyui-mv-production/SKILL.md) | 写实叙事MV、MiniMax H3/Continuum、参考帧、同Take最高输出、人物/场景/动作连续性与截止交付。 |
| [AI Music Video Production](skills/ai-music-video-production/SKILL.md) | A complete music video or a revision that must preserve lyric timing, character continuity, and the delivery specifications. |

## 安装ComfyUI技能

把下面内容发给Codex：

```text
Use $skill-installer to install this entire skill directory:
https://github.com/moonriver0922/AI-MV-Making-Skills/tree/master/skills/comfyui-mv-production
```

手动安装时，将整个 `skills/comfyui-mv-production` 目录复制到项目的 `.agents/skills/` 或个人的 `~/.agents/skills/`。保留同目录的references、scripts和assets；先检查同名版本。技能安装不会自动下载模型、安装ComfyUI或启动GPU生成。

完整步骤、模型与节点来源、运行检查和排错见[安装与使用](skills/comfyui-mv-production/references/install-and-use.md)。Codex技能发现位置以[官方说明](https://learn.chatgpt.com/docs/build-skills)为准。

## 开始制作或修改

```text
使用 $comfyui-mv-production。
根据我的歌曲、歌词和批准人物场景整理镜头表，再按约定开始生成。
使用同一批准镜头的最高ComfyUI输出，保留完整原始构图。
每个问题两次失败后报告并继续其他项，保留完整可回退底板。
```

已有影片可以这样调用：

```text
使用 $comfyui-mv-production 修正这个MV。
先查清原生输出、二采、预览和烘焙裁切/修补的来源关系。
保留原曲、歌词时钟和批准叙事；逐镜修复，交付完整观看版及规定母版。
明确列出仍未修复的问题，不把升分辨率说成恢复原生细节。
```

## 工作流、模板与检查工具

- [制作流程](skills/comfyui-mv-production/references/pipeline.md)：故事、人物、场景、道具、年代、音乐cue与镜头表。
- [ComfyUI工作流](skills/comfyui-mv-production/references/comfyui.md)：MiniMax H3一采/二采、整帧SR、Continuum与参考帧。
- [来源链与最高分辨率](skills/comfyui-mv-production/references/source-integrity.md)：同批准Take、父阶段、真实尺寸、完整构图。
- [检查与恢复](skills/comfyui-mv-production/references/review-and-recovery.md)：模糊、换脸、漂移、门轴、纸张、有限重试与断点接续。
- [字幕和交付](skills/comfyui-mv-production/references/delivery.md)：双语karaoke、年份、封面、完整歌曲、HD/规定母版与远程观看。
- [API模板](skills/comfyui-mv-production/assets/workflows/)：首尾帧生成、兼容latent二采、整帧2倍SR。它们是API格式参考，不是前端UI画布或即装即跑承诺。

从仓库根目录准备一个参数化API图：

```bash
cp skills/comfyui-mv-production/assets/project.example.json my-project.json
# 编辑自己的模型、参考图、帧数和输出参数后：
python3 skills/comfyui-mv-production/scripts/bind_workflow.py \
  skills/comfyui-mv-production/assets/workflows/minimax-h3-first-last.api.json \
  my-project.json --output shot001.prepared.api.json
python3 skills/comfyui-mv-production/scripts/inspect_comfy.py \
  shot001.prepared.api.json --server http://127.0.0.1:8188
```

以上两步不会提交生成。源文件审计与最终媒体检查：

```bash
python3 skills/comfyui-mv-production/scripts/audit_sources.py \
  my-shot-manifest.json --probe --output source-audit.json
python3 skills/comfyui-mv-production/scripts/verify_delivery.py \
  final.mp4 --width 6192 --height 2580 --fps 24 --frames 5112 \
  --decode --output delivery-check.json
```

6192×2580、24fps、5112帧是示例项目参数，按实际提交要求替换。技术检查不代替人物/动作/叙事和真人视听验收。模型权重、原曲、歌词、人物图与影片素材不在本仓库。

## 验证本技能包

需要Python 3.10+与FFmpeg/ffprobe：

```bash
python3 -m unittest discover -s tests -v
```

测试覆盖同Take最高完整输出、裁切祖先、父链循环、帧区间、参数类型、缺节点和音轨尾部丢失。[验证记录](VALIDATION.md)区分代码/结构检查、行为测试和GPU生成验收。

## Install and use the original general-production skill

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

