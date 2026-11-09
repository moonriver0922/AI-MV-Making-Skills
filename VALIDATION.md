# Validation record · 2026-11-09

新增技能为`comfyui-mv-production`；原有`ai-music-video-production`及其配套文件保持在原路径。

## 已执行

- Skill Creator的`quick_validate.py`检查通过：名称、frontmatter及入口文件结构有效。
- 标准库unittest **9/9通过**：同Take最高完整候选、裁切祖先、父链循环/缺失、区间覆盖、JSON数值绑定、缺参数、缺节点、现代COMBO素材选项、音轨尾部丢失与完整解码。缺实现时测试先失败；现代COMBO校验也实际出现过错误放行，补充失败回归后修复通过。
- 三个API模板均能用示例项目进行本地参数绑定；数值类型保持，已有准备文件不会覆盖。
- 在已有ComfyUI上只读查询`/object_info`：三个图所需节点类均存在。示例图像、latent和视频文件未提供时，检查会拒绝素材就绪状态；没有POST、排队、取消或改变服务。
- 独立使用测试将整个技能复制到临时`.agents/skills/`目录，再运行模板准备、来源审计和FFmpeg夹具验证。0.5秒/12帧画面配0.25秒音轨正确失败，完整0.5秒音轨版本通过，完整解码保持12帧，`visual_acceptance`仍为false。
- 按独立反馈补充了`python3`/Windows解释器说明；SR缺素材校验已用现代COMBO选项失败用例验证并修复。二采的latent前提和Director界面upscale路径已写明。

简单的无技能基线判断场景本来就通过，没有虚构“基线失败、技能治愈”的行为结论。独立测试证明的是说明可使用、工具可运行、故障能被识别，不证明技能对所有模型或项目都能提高画质。

## 未声称完成

- 没有为验证这个发布包新增GPU生成或二采；模板是脱敏、参数化的API参考，结构来源于曾完成的本地工作流，参数化副本没有重新GPU验收。
- 技能不含模型权重、参考人物、音乐、歌词、视频或用户机器路径。真实素材、节点版本和模型兼容性须在目标项目里确认。
- `minimax-h3-refine.api.json`是已有目标尺寸兼容video latent与对应audio latent之后的采样尾段，不自动制作放大latent。可使用所安装版本的Director/Continuum原生upscale流程准备，不能直接把一采latent改名冒充目标尺寸。
- 核源脚本的父链/批准状态是项目声明，`--probe`不证明声明真实或无烘焙修补；必须对照真实ComfyUI收据和画面。
- 技术媒体检查不证明原曲内容一致、歌词已逐字听校、脚底接触精确、人物无漂移或完成真人连续视听验收。
- 临时目录复制已验证；客户端重新启动后的自动发现、其他机器安装、GPU性能和9点交付能力不由本技能包测试证明。

## 复验

```bash
python3 -m unittest discover -s tests -v
```

需要Python 3.10+及FFmpeg/ffprobe。没有媒体工具时，媒体用例会显示skip，不能把skip计为已验收。技能结构验证可另用Codex自带Skill Creator工具；它不是运行这些检查脚本的依赖。
