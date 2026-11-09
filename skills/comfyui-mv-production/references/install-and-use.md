# 安装与使用

## 1. 安装技能

在Codex里发送：

```text
Use $skill-installer to install this entire skill directory:
https://github.com/moonriver0922/AI-MV-Making-Skills/tree/master/skills/comfyui-mv-production
```

也可手动把**整个目录**放进项目的`.agents/skills/comfyui-mv-production/`，或个人的`~/.agents/skills/comfyui-mv-production/`。不要只复制SKILL.md，配套references/scripts/assets也需要。先检查同名技能，避免重复安装不同版本或覆盖已有自定义。

```bash
git clone --branch master https://github.com/moonriver0922/AI-MV-Making-Skills.git
mkdir -p .agents/skills
# 在你的项目目录执行；下面源路径按实际clone位置修改。
test ! -e .agents/skills/comfyui-mv-production && \
  cp -R /path/to/AI-MV-Making-Skills/skills/comfyui-mv-production .agents/skills/
```

以上为命令示例，不是自动安装脚本。Codex会检测技能；未出现时开启新会话或重启客户端。官方说明：[Build skills](https://learn.chatgpt.com/docs/build-skills)。其他支持Agent Skills的助手按各自目录安装；不假设其工具权限或API与Codex相同。

示例命令以Linux/macOS的`python3`为准；Windows可将它替换为已安装Python 3的`py -3`。

## 2. 准备运行环境

技能检查脚本需要Python 3.10+标准库；媒体探测与解码需要FFmpeg/ffprobe。先运行 `python3 --version`、`ffmpeg -version`、`ffprobe -version`。实际视频生成另外需要可用的ComfyUI、适配GPU环境及匹配模型。

ComfyUI核心需包含MiniMax H3节点。[核心仓库](https://github.com/Comfy-Org/ComfyUI)与[Director安装说明](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director#安装)说明其版本和依赖要求。按项目记录固定版本；不要在临近截止的生产服务上直接git pull或pip升级。

需要长段续作时，按[Continuum上游安装文档](https://github.com/ukr8b3g-cmyk/ComfyUI-H3-Continuum#install-or-update)安装到自己的custom_nodes目录。Director是可选路径，不是首尾帧模板的必装项。Spectrum、KJNodes、LoRA等只在所选workflow确实使用时安装/启用，兼容性由对应版本验证。

模型单独获取，不随技能分发：

| 类型 | 目录 | 来源 |
| --- | --- | --- |
| H3 diffusion模型 | `ComfyUI/models/diffusion_models/` | [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3) |
| Qwen3-VL H3文本编码器 | `ComfyUI/models/text_encoders/` | 同上，选择loader支持的变体 |
| H3 video/audio VAE | `ComfyUI/models/vae/` | 同上，按workflow需要 |
| 可选RealESRGAN_x2plus | `ComfyUI/models/upscale_models/` | [官方模型说明](https://github.com/xinntao/Real-ESRGAN#inference-general-images) |

模型精度、尺寸、步数和offload策略按实测能力选择；技能不设置固定显存门槛，也不保证所有显卡可运行所有模型。安装缺失依赖需要相应环境权限；技能本身不授予这些权限。

## 3. 第一次调用

```text
使用 $comfyui-mv-production。
这是我的歌曲、权威歌词和故事方向。先整理人物/场景/道具规则、
按音乐计时的镜头表和ComfyUI节点方案，暂不生成。
```

修改旧片：

```text
使用 $comfyui-mv-production 修正现有MV。
以我批准的版本为叙事底板，先逐镜回溯同Take的最高ComfyUI最终输出，
保持原始完整构图。不要把预览、裁切放大或后期贴脸/贴门的中间片当母版。
保留歌曲、字幕和封面。每个问题两次失败后报告并继续其他项。
```

交付检查：

```text
使用 $comfyui-mv-production 检查完整导出。
规格为24fps、6192×2580、5112帧，歌曲必须完整到213秒。
分别报告技术检查、实际画面检查和仍未人工视听验证的部分。
```

## 4. 使用API模板

把 `assets/project.example.json` 和 `shot-manifest.example.json` 复制到自己的项目，填写实际路径、模型名和批准状态。API模板见 `assets/workflows/`；将占位参数替换后另存prepared文件，运行只读检查，再按已授权的生成范围提交。

长视频Continuum请从上游对应版本示例开始，不把某个旧版本的Take元数据套到另一版本。二采模板要求已有兼容latent，整帧SR模板要求实际源视频；它们不是同一个处理方式。模板结构/节点检查通过不等于GPU生成或影片质量通过。

## 5. 升级与排错

升级前备份当前技能和项目记录，对比新版本后再替换技能目录。影片原片、模型和项目缓存不应随技能升级删除。缺少ffprobe时先装媒体工具；缺少节点时核对Comfy版本与对应扩展；提交状态不明时查history，避免重复生成。

源文件全链不清、没有对应latent、显卡资源未确认、人物参考冲突时，先报告明确缺口并继续不依赖它的任务。不要靠改文件名、换模型架构loader、降低检验要求或声称“自动续跑”掩盖缺口。
