# 原片、最高分辨率与来源链

## 选源规则

“最高”指同一批准镜头/Take中，已完成、通过内容检查、来源清楚的最高质量ComfyUI阶段。它可能是一采，也可能是二采或整帧超分。输出尺寸只是一项属性；更大的另一演员、失败二采、剪辑预览、放大后的局部，都不能替换批准原片。

按以下顺序查：实际输出文件→ComfyUI history/SaveVideo节点→sampler/decoder或refine阶段→参考图与源latent→所选帧区间→下游变换。对每个中间文件追溯父链，包含嵌套片头、片尾、selected、restored和processed目录。不要只看最外层crop字段为空。

保留：

- shot_id / take_id / 人物与场景版本；
- prompt_id、原请求及工作流哈希、ComfyUI/扩展/模型版本；
- native、second_pass、super_resolution、preview、editorial阶段标签；
- 实际width/height/fps/frames、父文件ID、源帧区间、变换与SHA；
- 内容批准状态、证据、未解决问题。

原生尺寸和交付尺寸分开记录。例如1152×480宽镜头裁出576×240，放大到6192×2580，局部有效信息仍来自576×240；并不等于原生6K近景。原始MP4已经糊，重编码或空间放大不会自动恢复丢失的五官。更高分辨率的静态参考图也不证明生成视频具有同等细节。

## 默认保持构图

整帧等比例缩放可用于尺寸标准化；比例不同优先按约定加边，避免静默裁边或拉伸人体。原片、整帧二采和交付编码分目录保存。需要特写时，复用批准的原生特写或在ComfyUI制作相应景别。

用户明确授权裁切时，把裁切版本单列：坐标、原片尺寸、有效像素、目的与回退文件；不覆盖原母版，不作为新的原生参考。贴门、贴纸、变换头身和演员重投影不是常规清晰度处理。即使用某个ComfyUI节点实现，也仍须服从用户的内容修改边界。

## 检查脚本

复制 `assets/shot-manifest.example.json`，替换成真实候选。`native_start` 表示该候选第0帧对应原生Take的哪一帧；已裁切后再超分的文件应把裁切父阶段写出来。禁止把缺失父链补写成“native”。

```bash
python3 scripts/audit_sources.py manifest.json --output metadata-audit.json
python3 scripts/audit_sources.py manifest.json --probe --output file-audit.json
```

脚本排除不同Take、未批准候选、preview/editorial、裁切祖先、未知父链和不覆盖区间的候选。它根据**声明的**来源链选候选；`--probe`核对实际尺寸，不会证明声明真实、人物正确或无烘焙修补。还须人工/代理对照真实工作流与图像。

照片缺少视频帧数，不能用虚构nb_frames伪装已生成的视频。照片作为照片记录并按用户允许的编辑方式处理；有演员的静帧不能充作已经完成的行走。帧区间变化要同时核对Foley的原始时钟，音乐则保持连续。
