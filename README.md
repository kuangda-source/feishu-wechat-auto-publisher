# 飞书文档自动发布到微信公众号

🚀 自动将飞书文档转换为微信公众号文章，支持智能标题处理、图片自动上传、双版本配置。

## ✨ 核心功能

- **智能标题处理** - 自动清理表情符号，智能精简超过 64 字的标题
- **图片自动上传** - 下载飞书图片并上传到微信服务器
- **双版本配置** - 测试版/正式版一键切换
- **Webhook 通知** - 发布完成自动发送到飞书群
- **精美排版** - 使用 viral 模板，自动格式化列表、表格、引用

## 📦 安装步骤

### 1. 配置前置条件

#### 微信公众号
1. 注册微信公众号（订阅号或服务号）
2. 登录 [微信公众平台](https://mp.weixin.qq.com/)
3. 获取 `app_id` 和 `app_secret`（开发 → 基本配置）

#### 飞书开放平台
1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `app_id` 和 `app_secret`
4. 申请权限：`docx:document`、`wiki:wiki`、`drive:file`

#### 飞书群机器人
1. 在飞书群添加自定义机器人
2. 获取 webhook URL

### 2. 安装 Python 依赖

```bash
cd feishu-wechat-auto-publisher
pip3 install -r scripts/requirements.txt
```

### 3. 配置应用

```bash
# 复制配置模板
cp config.json.template config.json

# 编辑配置文件，填入你的 API 密钥
vim config.json
```

### 4. 测试运行

```bash
# 测试版发布
python3 scripts/feishu-wechat-auto.py <飞书文档链接>

# 预览模式（不实际发布）
python3 scripts/feishu-wechat-auto.py <飞书文档链接> --dry-run
```

## 🚀 使用方法

### 基本用法

```bash
python3 scripts/feishu-wechat-auto.py https://xxx.feishu.cn/wiki/xxx
```

### 自定义标题

```bash
python3 scripts/feishu-wechat-auto.py https://xxx.feishu.cn/wiki/xxx --title "自定义标题"
```

### 指定作者

```bash
python3 scripts/feishu-wechat-auto.py https://xxx.feishu.cn/wiki/xxx --author "作者名"
```

### 切换正式版本

编辑 `config.json`，修改 `_comment` 字段：

```json
{
  "_comment": "当前使用版本：production"
}
```

## 📁 文件结构

```
feishu-wechat-auto-publisher/
├── SKILL.md                          # 技能文档
├── README.md                         # 使用说明
├── config.json                       # 配置文件（自行填写）
├── config.json.template              # 配置模板
├── scripts/
│   ├── feishu-wechat-auto.py        # 主脚本
│   ├── upload_images_to_wechat.py   # 图片上传脚本
│   └── requirements.txt             # Python 依赖
└── outputs/                          # 输出目录（运行时生成）
```

## ⚠️ 注意事项

1. **标题长度** - 微信限制 64 字，会自动智能精简
2. **图片格式** - 自动转换为 JPG（微信不支持 PNG）
3. **发布流程** - 建议先用测试版，审核通过后再用正式版
4. **权限配置** - 确保飞书应用有文档读取权限

## 📝 版本历史

### v2.1.1（2026-04-14）
- ✅ 智能标题精简（移除冗余词而非截断）
- ✅ Markdown 格式规范化
- ✅ 列表渲染修复

### v2.1.0（2026-04-12）
- ✅ 排版问题全面修复

### v2.0.0（2026-04-10）
- ✅ 双版本配置
- ✅ 图片自动上传
- ✅ Webhook 通知

## 🆘 常见问题

**Q: 图片无法显示？**  
A: 检查是否已上传到微信服务器，查看日志中是否有"已上传"输出。

**Q: 标题包含表情？**  
A: 自动清理功能已启用，会移除微信不支持的 emoji。

**Q: 如何切换测试/正式版本？**  
A: 编辑 `config.json`，修改 `_comment` 字段。

**Q: Webhook 没收到通知？**  
A: 检查 webhook URL 是否正确，查看日志中是否有"发送成功"。

## 📄 License

MIT License

## 👤 Author

custom
