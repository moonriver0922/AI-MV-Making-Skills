# ComfyUI / MiniMax H3 / Continuum

## 安装边界与依赖

技能安装只复制说明、模板和检查工具；不会替你安装ComfyUI、下载模型、连接GPU或改变运行中的服务。完整安装步骤见[安装使用](install-and-use.md)。先记录本机版本，再检查节点。已有生产环境不要为导入模板自动升级、重启或替换依赖。

本包API示例来自MiniMax H3实际使用路径，**不是HunyuanVideo工作流**：

| 用途 | 节点/组件 |
| --- | --- |
| 模型/编码器/VAE | UNETLoader、CLIPLoader（type=minimax）、VAELoader |
| 首尾帧生成 | MiniMaxH3ImageToVideo、MiniMaxH3SigmaShift |
| 采样 | BasicScheduler或ManualSigmas、BasicGuider、RandomNoise、KSamplerSelect、SamplerCustomAdvanced |
| AV latent | LTXVSeparateAVLatent、LTXVConcatAVLatent、SaveLatent、LoadLatent |
| 视频输出 | VAEDecode、CreateVideo、SaveVideo |
| 整帧SR | LoadVideo、GetVideoComponents、ImageFromBatch、UpscaleModelLoader、ImageUpscaleWithModel、ImageScaleBy、ImageBlend |
| 长段续作 | [ComfyUI-H3-Continuum](https://github.com/ukr8b3g-cmyk/ComfyUI-H3-Continuum) |
| 可选多组参考/导演台 | [MiniMax H3 Director](https://github.com/AIMixer/ComfyUI_MiniMaxH3_Director) |

模板列出的模型文件名是一个已用过的BF16/FP16配置，不是唯一选择，也不是显存最低要求。模型从[Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3)按任务和许可证另行获取；变体须被实际loader支持。FL2VA用于相应首尾帧路径，Director的参考视频模式可能需要REF2VA，不能混接。纯影片不需要生成音频时也应按节点要求保留兼容AV latent结构。

## 一采、二采与超分

**一采：** 生成动作与构图。`MiniMaxH3ImageToVideo`提供条件和latent，模型经过H3 sigma shift，采样后拆出video/audio latent，保存并解码。固定seed、参考、模型和帧数供复现；固定seed本身不保证跨镜头同脸。

**二采：** 在兼容的一采latent/图像与约束基础上再次采样。可能改善纹理，也可能改脸、道具和动作；只在小样实际通过后采用。`minimax-h3-refine.api.json`展示**已具备目标尺寸兼容video latent和对应audio latent时**的采样尾段，不包含自动latent放大。没有对应latent时先用本机支持的原生refine/upscale路径准备，不能把不兼容模型通过另一架构loader硬载。

界面路径可使用Director上游示例：把`MiniMax H3 Director Refine`接到导演台的`refine`输入，按目的选择同尺寸`refine`或目标尺寸`upscale`，检查实际`images`（处理后）与`images_pre_refine`（一采）输出；`latent_upscale`本身不代表已经二采。Continuum对应版本的二采/Take选项以该版本示例为准。先保存并比较两个阶段，不因为设置了upscale就自动采用高像素结果。

**整帧超分：** `whole-frame-sr.api.json`用RealESRGAN与整帧Lanczos结果混合，是图像超分，不冒称扩散二采。需检查脸、纸线、衣纹在相邻帧是否闪烁。使用模型来自[Real-ESRGAN官方仓库](https://github.com/xinntao/Real-ESRGAN)；权重独立安装。拒绝从已经裁切放大的预览继续“修复”后声称拿到了原生细节。

生成/二采尺寸由实际模型支持、质量与可用资源决定，不写死某个GB显存门槛。目标尺寸提高前先看同Take已有最高完成阶段；不得拿另一人物的高像素Take替代。

## Continuum与参考帧

按安装版本使用上游提供的官方工作流，记录具体tag/commit。短镜头可采用首尾帧；长段用上游Chunk/Take机制逐段生成、逐段检查并从兼容Take续作。只续当前已批准段，不把“成功执行”视为内容通过。

身份参考负责脸、服装与比例；场景参考负责空间和道具；首尾帧约束姿态/构图；视频/姿态控制用于动作。明确各参考的职责，冲突时先修参考。每次更改参考、分辨率、模型、采样配置或时间范围，都应检查Take兼容性。遵守上游只读/不兼容状态，不删元数据强行复用。尾帧衔接不能证明中间足底接触、门轴或头身关系正确。

至少检查整段及相邻切点：同一人、门与家具几何、道具持有者、进出方向、光线和年代。如果长动作反复失败，在用户允许的范围里拆成原生短镜头；剪辑省略中间动作要有可理解的因果。

## API模板准备与有限提交

`assets/workflows/*.api.json`为API格式，不是前端画布JSON。先复制并编辑`assets/project.example.json`，把素材放到自己的ComfyUI input目录，模型放到对应models目录。用`python3 scripts/bind_workflow.py 模板.api.json project.json --output prepared.api.json`填入参数，数值字段保持JSON数值类型；它不会排队。接着运行：

```bash
python3 scripts/inspect_comfy.py prepared.api.json --server http://127.0.0.1:8188
```

工具只读检查 `/object_info`，不验证显存、画面质量或所有运行期约束，不提交任务。缺节点时按其上游文档安装，或者明确换用已验证的等价图；不要凭空改class_type。

实际提交时每个作业有唯一ID：先原子保存请求/意图/哈希，再POST `/prompt`，保存返回的prompt_id。用 `/history/{prompt_id}`和真实输出确认完成，失败/超时分别处理。请求超时且收据缺失时，先用唯一client_id、历史和输出查明是否已接收；不盲目重发。按服务实际排队限制工作，不绕过拒绝，不中断他人的任务。只取消明确属于本任务且已确认支持单作业取消的ID。
