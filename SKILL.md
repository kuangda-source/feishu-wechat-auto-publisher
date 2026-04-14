---
name: feishu-wechat-auto-publisher
version: 2.0.0
description: 飞书文档自动转公众号推文 - 智能标题识别、图片自动上传、双版本配置、Webhook 通知
author: custom
tools: [filesystem, http, shell, feishu_doc]
trigger: "飞书转公众号 | 论文推文 | 公众号发布 | feishu.cn/wiki | feishu.cn/docx"
priority: 100
---

# 飞书文档自动发布到微信公众号（v2.0）

## 🎯 核心功能

### 1️⃣ 智能标题处理
- **优先使用文档原标题** - 从飞书 docx API 获取
- **自动清理表情符号** - 移除微信不支持的 emoji（🚀📊💡等）
- **智能生成备选** - 如无标题，从内容提取关键词生成
- **智能精简** - 超过 64 字时移除冗余词（"前沿"、"团队"、"提出"等），而非直接截断
- **语义完整** - 优先在逗号/冒号处截断，确保语句通顺

### 2️⃣ 图片自动处理
- **从 blocks 重建内容** - 保留图片在原文中的正确位置
- **自动下载转换** - 下载飞书图片并转换为 JPG 格式（微信支持）
- **上传到微信服务器** - 自动上传所有图片，替换为微信 URL
- **智能封面选择** - 使用第一张图片作为封面

### 3️⃣ 双版本配置
- **测试版 (test)** - 测试公众号 + 测试 webhook
- **正式版 (production)** - 正式公众号 + 正式 webhook
- **一键切换** - 修改 config.json 的 `_comment` 字段即可

### 4️⃣ Webhook 通知
- **发布完成自动通知** - 发送到飞书群
- **包含关键信息** - 标题、草稿箱提示
- **支持自定义** - 可配置不同环境的 webhook

## 📋 工作流程

```
飞书链接
  ↓
📄 读取飞书文档（docx API）
  ├─ 获取文档标题
  └─ 获取所有 blocks（支持分页）
  ↓
📝 重建内容
  ├─ 按 block 顺序重建文本
  ├─ 在原始位置插入图片引用
  └─ 下载图片并转换为 JPG
  ↓
🧹 标题处理
  ├─ 清理表情符号
  ├─ 检查字数限制
  └─ 如无标题则从内容生成
  ↓
📸 上传图片
  ├─ 扫描所有本地图片路径
  ├─ 逐个上传到微信服务器
  └─ 替换为微信 URL（mmbiz.qpic.cn）
  ↓
📮 发布到公众号
  ├─ 创建草稿
  ├─ 设置封面
  └─ 使用 viral 模板排版
  ↓
📢 Webhook 通知
  └─ 发送到配置的飞书群
```

## 🚀 使用方式

### 方式一：AI 助手自动触发（推荐）

当用户发送飞书文档链接时，AI 助手自动处理：

```
用户：https://lcnssrlun9lz.feishu.cn/wiki/xxx

AI: 📦 当前版本：TEST
    📢 使用 test webhook
    📄 读取飞书文档：xxx
    📋 Docx API 获取标题：文章标题
    📊 共获取 130 个 blocks
    📝 从 blocks 重建内容...
      ✅ 下载并转换：image_1.jpg
      ✅ 下载图片 1: image_1.jpg
      ...
    ✅ 使用文档原标题（已清理表情）：文章标题
    🖼️  发现 4 张图片（已插入到原文位置）
    📮 发布到微信公众号...
    📸 上传图片到微信服务器...
      ✅ 已上传：image_1.jpg -> http://mmbiz.qpic.cn/...
    ✅ 发布成功！
    📤 发送 webhook 通知...
    ✅ Webhook 通知发送成功
```

### 方式二：命令行直接运行

```bash
cd /root/.openclaw/workspace/skills/feishu-wechat-auto-publisher

# 基本用法
python3 scripts/feishu-wechat-auto.py <飞书链接>

# 自定义标题
python3 scripts/feishu-wechat-auto.py <飞书链接> --title "自定义标题"

# 预览模式（不实际发布）
python3 scripts/feishu-wechat-auto.py <飞书链接> --dry-run

# 指定 webhook
python3 scripts/feishu-wechat-auto.py <飞书链接> --webhook "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 指定作者
python3 scripts/feishu-wechat-auto.py <飞书链接> --author "作者名"
```

## ⚙️ 配置说明

### 配置文件结构

```json
{
  "_comment": "当前使用版本：test",
  "test": {
    "wechat": {
      "app_id": "wx58d246b37dfabe8f",
      "app_secret": "xxx"
    },
    "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/测试 hook"
  },
  "production": {
    "wechat": {
      "app_id": "wx749b42767a868fca",
      "app_secret": "xxx"
    },
    "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/正式 hook"
  },
  "feishu": {
    "app_id": "cli_xxx",
    "app_secret": "xxx"
  },
  "author": "RobotQu",
  "original": true,
  "template": "viral"
}
```

### 切换版本

修改 `_comment` 字段：

```json
{
  "_comment": "当前使用版本：test"
}
```

改为：

```json
{
  "_comment": "当前使用版本：production"
}
```

### 配置项说明

| 字段 | 说明 | 示例 |
|------|------|------|
| `_comment` | 当前激活的版本 | `当前使用版本：test` |
| `test.wechat.app_id` | 测试公众号 AppID | `wx58d246b37dfabe8f` |
| `test.wechat.app_secret` | 测试公众号密钥 | `xxx` |
| `test.webhook` | 测试环境 webhook | `https://...` |
| `production.*` | 正式环境配置 | 同上 |
| `feishu.app_id` | 飞书应用 ID | `cli_xxx` |
| `feishu.app_secret` | 飞书应用密钥 | `xxx` |
| `author` | 默认作者名 | `RobotQu` |
| `template` | 排版模板 | `viral` 或 `standard` |

## 📁 文件结构

```
feishu-wechat-auto-publisher/
├── SKILL.md                          # 技能文档
├── config.json                       # 配置文件（双版本）
├── scripts/
│   ├── feishu-wechat-auto.py        # 主脚本
│   ├── upload_images_to_wechat.py   # 图片上传脚本
│   ├── test-webhook.py              # Webhook 测试
│   └── requirements.txt             # Python 依赖
└── outputs/                          # 输出目录（运行时生成）
    ├── article.md                    # 原始 Markdown
    ├── article_uploaded.md           # 上传后的 Markdown
    └── images/                       # 图片目录
```

## 📦 依赖安装

### Python 依赖

```bash
cd /root/.openclaw/workspace/skills/feishu-wechat-auto-publisher
pip3 install -r scripts/requirements.txt
```

### 系统依赖（可选）

如需 PDF 截图功能（当前版本已不需要）：

```bash
# Ubuntu/Debian
sudo apt-get install -y poppler-utils
```

## 📊 输出结果

### 标准输出

```
📦 当前版本：TEST
📢 使用 test webhook
📄 读取飞书文档：xxx
📋 Docx API 获取标题：文章标题
📊 共获取 130 个 blocks
📝 从 blocks 重建内容...
  ✅ 下载并转换：image_1.jpg
  ...
✅ 使用文档原标题（已清理表情）：文章标题
🖼️  发现 4 张图片（已插入到原文位置）
📮 发布到微信公众号...
📸 上传图片到微信服务器...
  ✅ 已上传：image_1.jpg -> http://mmbiz.qpic.cn/...
✅ 发布成功！
📋 draft_media_id: xxx
📤 发送 webhook 通知...
✅ Webhook 通知发送成功
```

### 输出文件

| 文件 | 说明 |
|------|------|
| `wechat-output/article.md` | 原始 Markdown（本地图片路径） |
| `wechat-output/article_uploaded.md` | 上传后的 Markdown（微信 URL） |
| `wechat-output/images/` | 下载的图片（JPG 格式） |
| `wechat-preview.html` | 预览 HTML |

### Webhook 消息

```
✅ 推文已发布成功

📝 标题：文章标题

🔗 请登录微信公众号后台查看草稿箱
```

## 🔧 高级功能

### 标题处理规则

1. **优先使用文档原标题** - 从 docx API 获取
2. **清理表情符号** - 移除 🚀📊💡🧠 等 emoji
3. **字数限制** - 超过 64 字自动截断
4. **备选生成** - 如无标题，从内容提取：
   - 优先搜索包含模型名称的行
   - 其次搜索包含机构名称的行
   - 最后使用第一行有意义的文本

### 图片处理规则

1. **从 blocks 重建** - 保留原始位置
2. **格式转换** - PNG → JPG（微信支持）
3. **自动上传** - 所有图片上传到微信服务器
4. **URL 替换** - 本地路径 → mmbiz.qpic.cn

### Webhook 发送时机

- ✅ 发布成功后自动发送
- ✅ 包含文章标题
- ✅ 支持自定义 webhook URL

## ⚠️ 注意事项

1. **公众号权限** - 确保 app_id/app_secret 配置正确且有发布权限
2. **图片格式** - 自动转换为 JPG，微信不支持 PNG
3. **飞书权限** - 确保有权限访问目标飞书文档
4. **标题长度** - 微信限制 64 字，自动截断
5. **版本切换** - 修改 `_comment` 后重启脚本生效
6. **表格列数** - 自动从飞书 API 获取，支持 3/4/5 列混合表格
7. **列表格式** - 支持 ordered/bullet 富文本列表（带粗体强调）

## 📝 版本历史

### v2.1.1（2026-04-14）- 标题精简 + Markdown 格式修复

**新增功能**：
1. **智能标题精简** - 超过 64 字时移除冗余词（"前沿"、"团队"、"提出"、"用"、"的"），而非直接截断
2. **语义完整截断** - 优先在逗号/冒号/竖线处截断，确保语句通顺
3. **Markdown 后处理** - 新增 `postprocess_markdown()` 函数，自动规范化格式

**修复问题**：
1. **列表渲染失败** - 列表项前后添加空行，确保 Markdown 正确解析为 `<ul>/<li>`
2. **图片分隔问题** - 图片前后添加空行，避免与相邻段落粘连
3. **标题截断生硬** - 原标题"提升 2.5 倍"被截断为"提升 2"，现改为智能精简

**技术细节**：
- 标题精简策略：
  - 移除冗余词：`前沿`、`团队`、`提出`、`用`、`的`、`难题，` → `，`
  - 优先在分隔符（，,:|）处截断
  - 确保最后 1-2 个字符是完整词汇
- Markdown 规范化：
  - 列表前后确保有空行
  - 标题前后确保有空行
  - 图片前后确保有空行
  - 清理连续多余空行

**测试验证**：
- ✅ 标题：73 字 → 58 字，语句通顺完整
- ✅ 列表：正确渲染为带样式的 `<ul>` 框
- ✅ 排版：viral 模板正确应用

---

### v2.1.0（2026-04-12）- 排版问题全面修复

**修复问题**：
1. **小标题不显示** - 修复 block_type=4 (heading2) 的文本提取逻辑，现在正确识别所有层级的标题
2. **列表内容丢失** - 修复 block_type=13 (ordered/bullet) 的内容提取，支持 ordered 字段中的富文本列表
3. **表格格式错误** - 修复表格列数识别，从 `table.property.column_size` 获取正确列数（支持 3/4/5 列混合）
4. **引用内容丢失** - 新增 block_type=15 (quote) 支持，用粗体显示重要引用
5. **Bullet 列表丢失** - 修复 block_type=12 的 bullet 字段提取

**技术细节**：
- 飞书文档 block 类型映射：
  - `block_type=4` → heading2 (##)
  - `block_type=5` → heading3 (###)
  - `block_type=13` → ordered/bullet 列表（可能包含富文本）
  - `block_type=15` → quote 引用块
  - `block_type=31` → 表格（从 `table.property.column_size` 获取列数）
  - `block_type=32` → 表格单元格

**测试验证**：
- ✅ 小标题：15 个标题正确显示（## 和 ### 混合）
- ✅ 列表：15+ 项列表正确显示
- ✅ 表格：5 个表格正确格式化（3/4/5 列混合）
- ✅ 图片：4 张图片正确插入到原文位置

### v2.0.0（2026-04-10）

- ✅ 新增双版本配置（test/production）
- ✅ 新增标题表情清理
- ✅ 新增图片自动上传到微信
- ✅ 新增 Webhook 发布通知
- ✅ 优化标题识别逻辑
- ✅ 优化图片位置保留

### v1.0.0

- 基础发布功能
- 智能标题识别
- PDF 截图（已废弃）

## 🆘 常见问题

### Q: 如何切换测试/正式版本？
A: 编辑 `config.json`，修改 `_comment` 字段为 `当前使用版本：test` 或 `当前使用版本：production`

### Q: 图片无法显示？
A: 检查是否已上传到微信服务器，查看日志中是否有 `✅ 已上传` 输出

### Q: 标题包含表情？
A: 自动清理功能已启用，如仍有表情，检查标题是否从内容生成（生成标题也会清理）

### Q: 小标题/列表/表格排版不正确？
A: v2.1.0 已全面修复排版问题。如仍有问题，检查：
- 小标题：确认飞书文档中使用 H2/H3 格式
- 列表：确认使用飞书的标准列表格式
- 表格：确认使用飞书的标准表格格式

### Q: 某些内容排版后丢失？
A: 可能是飞书 block 类型未支持。当前支持的 block 类型：
- 文本：`block_type=2`
- 标题：`block_type=4` (H2), `block_type=5` (H3)
- 列表：`block_type=12/13/14/16` (bullet/ordered)
- 引用：`block_type=15` (quote)
- 表格：`block_type=31/32` (table/cell)
- 图片：`block_type=27`

### Q: Webhook 没收到通知？
A: 检查 webhook URL 是否正确，查看日志中是否有 `✅ Webhook 通知发送成功`

---

**最后更新：** 2026-04-09  
**维护者：** custom
