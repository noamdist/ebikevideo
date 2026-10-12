# 提示词模板

生成前填写角色档案，再替换下面的参数。方括号是待填参数，不应原样传给生成工具。每次保存最终实际调用的提示词。

## 输入角色与固定描述

- `IDENTITY`：姓名、准确年龄、用户提供的身份信息、脸型、五官、肤色、发际线及发型、身体比例、可辨认个人标记。
- `OUTFIT`：已确定的一整套衣服与配饰，包含佩戴侧、包的背法和破洞位置。
- `TARGET`：本次唯一需要改变的视角、表情、姿势或细节。
- `REFERENCES`：明确列出每张输入图用途：身份基准、全身/服装基准、局部物件、仅布局参考。不要把布局图的角色当作新角色身份。
- `DIMENSION_GOAL`：期望的合适原生尺寸或最高可用分辨率。实际尺寸在生成后检查，不由提示词决定。

共用摄影约束：
```text
Photorealistic studio photography, natural anatomy and body proportions,
soft even studio light, clean white seamless background, authentic skin
and fabric texture, sharp natural focus without oversharpening.
One subject per standalone image. No labels, typography, borders, logos
or watermark. No distorted anatomy, extra limbs or fingers, face drift,
plastic skin, harsh halos or unnecessary props.
```

## 1. 正面肖像基准

新角色采用 `photorealistic-natural`；从既有角色图片建立基准采用 `identity-preserve`，并传入真实身份来源图。

```text
Use case: [photorealistic-natural OR identity-preserve]
Asset type: canonical facial identity reference for video and recurring scenes.
Subject: [IDENTITY].
[For continuation: Input image 1 is the authoritative identity reference.
Preserve its facial structure, eye/nose/lip geometry, skin tone, hairline,
hair length and hairstyle. Other panels in a supplied sheet depict this
same person, not additional people.]
Create a single straight-on head-and-shoulders portrait, neutral relaxed
expression, eyes facing the camera, head upright, complete crown and chin,
readable eyebrows and facial contour. Keep the existing hairstyle while
making the face readable. Visible shoulder clothing: [OUTFIT].
Soft even studio lighting, white seamless backdrop, natural skin texture.
[DIMENSION_GOAL]. No collage, text, labels or border.
```

删去不适用的分支。新角色不要附内置 Zara 图作为身份输入。

## 2. 全身基准

```text
Use case: identity-preserve
Asset type: canonical full-body identity and outfit reference for video.
Input image 1: canonical portrait, authoritative face and hair identity.
[Input image 2, if available: existing full-body/outfit reference.]
Create the exact same person: [IDENTITY].
Single front-facing neutral standing pose, full body from crown to shoe
soles visible, slight margins above and below, arms naturally relaxed and
hands readable. Natural proportions and perspective.
Wear exactly [OUTFIT], including recorded wearer-relative accessory sides.
Preserve the portrait's face, skin tone, hair and age. A new framing must
not create a new face. White background and soft studio light.
[DIMENSION_GOAL]. No text, frame, extra person or missing feet.
```

## 3. 独立视角、表情或姿势

```text
Use case: identity-preserve
Asset type: standalone [turnaround / face / expression / pose] video reference.
Input image 1: canonical portrait, authoritative facial identity.
[Input image 2: canonical full-body, authoritative proportions and outfit.]
Generate ONE image of this same person: [IDENTITY].
Requested change only: [TARGET].
Preserve facial bone structure, facial features, skin tone and markings,
hairline and hairstyle, age, body proportions, clothing and accessory
design/placement from the canonical references. Outfit: [OUTFIT].
[FRAMING AND VIEW RULES].
Use the same soft lighting and clean white background.
[DIMENSION_GOAL]. Natural anatomy, no text, labels or panel borders.
```

按模块替换规则：
- 全身转圈：全身完整、统一尺度和镜头高度。3/4 约 45°，侧面约 90°，背面约 180°；身体和头部朝向一致，中性站姿，不回头看镜头。
- 面部：头肩或清晰面部构图，正面/3/4/真正侧面，完整下巴及发顶，中性表情。
- 表情：正面头肩图，只改变面部肌肉。快乐为自然笑，愤怒为眉心与嘴部收紧，悲伤为眼神与嘴角下垂，惊讶为自然睁眼张口，担忧为眉心收紧和不安眼神，自信为放松稳定，坚定为专注眼神和较紧嘴部。
- 姿势：全身构图，只改变动作。坐姿可用简单白色凳；准备行动采用合理重心转换，避免凭空增加武器、设备或故事道具。

## 4. 服装、配饰与材质

```text
Use case: identity-preserve
Asset type: actual-character wardrobe/material close-up reference.
Input references: [canonical outfit image / approved detailed item image].
Show a clean high-detail photographic close-up of [TARGET] as actually worn
by the same character. Preserve the source item's exact shape, color,
construction, knit/weave, seams and hardware. Do not substitute a generic
product. When skin or hair appears, preserve the canonical character.
Soft consistent studio light, natural material texture, no text or logo.
[DIMENSION_GOAL].
```

色块对应实际图片的代表颜色。除非实际测量，不把目测颜色称为准确 HEX 或校准色值；可标材质名称，不虚构品牌和材质成分。

## 5. 总览表合成

输入合格单图或分区图。工具不能容纳全部参考时分区合成，再汇总；保留原始独立图。只为布局需要使用内置模板图，并明确它不控制新角色的脸。

```text
Use case: compositing
Asset type: vertical photographic character reference overview.
Input images: [list each approved reference and its role].
[Optional layout reference: its panel hierarchy, white backdrop and quiet
typography are layout guidance only; do not copy its character identity.]
Arrange the SAME character, [NAME], age [AGE], using the supplied approved
reference images. Preserve their facial identity, hair, body proportions,
outfit, expressions, poses and view directions.
Large vertical white canvas, clean margins and subtle panel separators.
From top to bottom: four full-body turnaround views, three identity
portraits, eight expressions, seven poses, wardrobe/detail crops, then
representative color and material swatches.
Give turnaround and identity portraits the largest readable areas.
Only allowed text: [exact title, age and approved panel captions].
Keep all heads and feet visible; no random text or missing panels.
[DIMENSION_GOAL]. Natural photographic detail and consistent lighting.
```

布局拥挤时用分区表，不牺牲独立图。合成后的面容、动作和文字也需检查，不能假设输入正确就意味着输出正确。

## 6. 针对性修正与清晰度增强

```text
Use case: identity-preserve
Edit target: [one failed asset or existing image].
Canonical identity reference: [portrait]; outfit reference: [full-body].
Change only [SPECIFIC DEFECT OR CLARITY ISSUE].
Keep the exact facial structure, skin tone, hair, proportions, pose,
outfit, accessory placement, framing and background. For a sheet, preserve
every panel and exact approved caption. Do not redesign the character.
Improve natural readable detail without face reshaping, invented markings,
waxy smoothing, harsh sharpening or halos. [DIMENSION_GOAL].
```

增强是生成式编辑，不能承诺像素级不变。检查身份变化与实际尺寸；如果尺寸未提高，明确仅做了细节增强。
