#!/usr/bin/env python3
"""
修复飞书文档图片 - 从 list_blocks 提取图片并下载到本地
"""

import json
import requests
from pathlib import Path

OUTPUT_DIR = Path("/root/.openclaw/workspace/wechat-output")
IMAGES_DIR = OUTPUT_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# 从之前 list_blocks 结果中提取的图片信息
images = [
    {"block_id": "MAJLdoaiIozA3gxRA4zcahnKnad", "token": "W3Z7bTQ6nobAK4xuqZ5cY65dnrd", "width": 1686, "height": 912},
    {"block_id": "GUJRdfeemovb0GxM3AacP080n3d", "token": "TOv7b4z8RoeNVExe5xucNmddn5f", "width": 1732, "height": 492},
    {"block_id": "R0DSdyAeto5ea1x8Y6Fchdprnyo", "token": "NuUIbQJl3oakS2xT4e6c4dHhn8b", "width": 888, "height": 1450},
]

print(f"📸 共发现 {len(images)} 张图片")

# 说明：飞书图片需要通过 API 下载
# 这里生成占位说明，实际使用需要配置飞书 API

download_script = f'''#!/bin/bash
# 飞书图片下载脚本
# 需要配置飞书 app_id 和 app_secret

APP_ID="your_feishu_app_id"
APP_SECRET="your_feishu_app_secret"

# 获取 tenant access token
TOKEN=$(curl -s -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \\
  -H "Content-Type: application/json" \\
  -d '{{"app_id":"'$APP_ID'","app_secret":"'$APP_SECRET'"}}' | jq -r '.tenant_access_token')

# 下载图片
'''

for i, img in enumerate(images, 1):
    local_file = IMAGES_DIR / f"image_{i}.png"
    download_script += f'''
# 图片{i}: {img['token']} ({img['width']}x{img['height']})
curl -s -H "Authorization: Bearer $TOKEN" \\
  "https://open.feishu.cn/open-apis/drive/v1/media/{img['token']}/download" \\
  -o "{local_file}"
echo "✅ 下载图片{i}: {local_file}"
'''

script_file = OUTPUT_DIR / "download_images.sh"
script_file.write_text(download_script)

print(f"📝 下载脚本已生成：{script_file}")
print("\n💡 使用方法：")
print("1. 编辑 download_images.sh，填入飞书 app_id 和 app_secret")
print("2. 运行：bash download_images.sh")
print("3. 更新 article.md 中的图片路径")

# 生成带图片占位的 Markdown
md_content = """# 【论文深读】RoadRunner：面向高速越野自动驾驶的自监督可通行性学习框架-TFR2025

## 论文示例：

在自动驾驶研究逐渐从"城市道路"走向"复杂自然环境"的今天，一个核心问题变得愈发关键：

**👉 机器人如何在"没有道路"的地方安全行驶？**

相比结构化道路，越野环境带来了本质挑战：
- 无车道线、无规则边界
- 地形复杂（坡度、碎石、植被）
- 感知不完整（遮挡、远距离稀疏）

在这样的背景下，来自 NASA JPL 与 ETH Zurich 的最新研究提出了一种新的解决范式：

**👉 RoadRunner：直接学习"可通行性"的端到端感知模型**

![ RoadRunner 概览图](images/image_1.png)

---

## 🧭 一、问题重构：从"语义理解"到"行动可行性"

传统自动驾驶感知 pipeline 通常是：

**感知 → 语义理解 → 规则推理 → 可通行性判断**

但论文指出，这种方法存在结构性缺陷：
- ❌ 语义类别与可通行性并非一一对应
- ❌ 规则依赖人工设计，难以泛化
- ❌ 高速场景下 LiDAR 稀疏，语义信息不足

![ 传统方法 vs RoadRunner](images/image_2.png)

---

## ✅ RoadRunner 的核心思想

**👉 绕开语义中间层，直接预测 Traversability（可通行性）与 Elevation（地形高度）**

这本质上是一次**任务驱动的感知范式转变（Task-oriented Perception）**：

> 不再问"这是什么"，而是直接回答"能不能走"。

---

## 🧠 二、方法框架：多模态 + 自监督 + BEV 统一建模

### 2️⃣ 自监督学习：Hindsight Traversability Learning

论文最具创新性的部分在于监督信号的构建方式。

#### 🚩 核心机制：利用"未来信息"生成标签

具体流程：
1. 车辆在环境中真实行驶
2. 收集过去 + 未来 60s 内的传感器数据
3. 融合生成更完整的地形与风险评估
4. 作为"伪真值"用于训练

📌 本质：

**👉 用"未来观察"纠正"当前不确定性"**

![ Hindsight Learning 流程图](images/image_3.png)

---

## 📊 三、数据集与实验设计

### 性能对比：RoadRunner vs X-Racer

结果表明：

**👉 RoadRunner 在多个维度全面优于传统系统**

- Traversability 误差显著降低（MSE ↓）
- Elevation 误差降低约 36%
- 风险检测精度大幅提升

---

## 🎓 六、总结

**👉 RoadRunner 的真正贡献，不只是性能提升，而是范式转变。**

### 📌 一句话总结

**👉 从"识别世界"，到"理解可行动性"，RoadRunner 迈出了关键一步。**

---

**✨ 持续关注，我们将带来更多自动驾驶与机器人前沿论文解读**

**✨欢迎对越野机器人感兴趣的同行加微信交流：15711463195**

---

*作者：RobotQu*
"""

md_file = OUTPUT_DIR / "article_with_images.md"
md_file.write_text(md_content, encoding='utf-8')

print(f"\n✅ 带图片占位的 Markdown 已生成：{md_file}")
print(f"📁 图片目录：{IMAGES_DIR}")
